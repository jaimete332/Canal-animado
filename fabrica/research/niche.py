"""Investigación del nicho: qué vídeos funcionan y por qué → guía de estilo para la fábrica.

Fuentes de datos (de mejor a peor):
  1. YouTube Data API v3 (`YOUTUBE_API_KEY` o clave inyectada por el proxy en el header X-Goog-Api-Key):
     búsquedas por consultas del nicho, vídeos cortos, ordenados por visualizaciones; estadísticas reales.
  2. Archivo JSON recopilado a mano o por Claude con búsqueda web (`--from-file`), con el esquema de
     `Video` (title, channel, views, published, duration_s, url, hook, notes...).

Salidas en data/research/:
  videos_<fecha>.json   datos crudos normalizados
  report_<fecha>.md     informe legible (top vídeos, patrones, recomendaciones)
  style_guide.json      guía viva que consumen script/writer.py e ideas/bank.py

Principio: se copian PATRONES (estructura, ritmo, formato de título, tipo de tema), nunca guiones,
personajes, marcas, música ni miniaturas de otros creadores.
"""
from __future__ import annotations

import datetime as dt
import json
import math
import re
import statistics
import unicodedata
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path

import requests

from ..core.config import ROOT, env
from ..core.log import get_logger
from ..core.retry import PermanentError, retry

log = get_logger("research")
OUT = ROOT / "data" / "research"
API = "https://www.googleapis.com/youtube/v3"

DEFAULT_QUERIES = [
    "qué pasaría si", "que pasaria si animación", "y si", "qué pasaría si shorts", "cómo sería tu vida si",
    "qué pasaría si fueras", "sobrevivirías", "what if animated shorts", "what would happen if",
]

STOP = set("""a al algo como con de del el en es eso esta este fue ha la las le lo los mas más me mi muy no o
para pero por que qué se si sí su sus te tu tú un una uno y ya the a an of to in is you your if what would happen
shorts short""".split())


@dataclass
class Video:
    title: str
    channel: str = ""
    views: int | None = None
    likes: int | None = None
    comments: int | None = None
    published: str | None = None          # ISO
    duration_s: float | None = None
    url: str = ""
    lang: str = ""
    hook: str = ""                        # primera frase (si se conoce)
    thumbnail_text: str = ""
    notes: str = ""
    source: str = "api"
    metrics: dict = field(default_factory=dict)


# ------------------------------------------------------------------------------------------- datos
def _key() -> str:
    # con el proxy del entorno la clave puede inyectarse en el header; enviamos un marcador
    return env("YOUTUBE_API_KEY") or "proxy-injected"


@retry(tries=3)
def _get(path: str, **params) -> dict:
    params = {k: v for k, v in params.items() if v is not None}
    # la clave va solo en la cabecera: así nunca aparece en URLs de errores ni en registros
    r = requests.get(f"{API}/{path}", params=params, timeout=30, headers={"X-Goog-Api-Key": _key()})
    if r.status_code in (400, 401, 403):
        raise PermanentError(f"YouTube API {r.status_code}: {r.text[:300]}")
    if r.status_code >= 400:
        raise requests.HTTPError(f"YouTube API {r.status_code} en /{path}: {r.text[:200]}")
    return r.json()


def _iso_dur(s: str) -> float:
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", s or "")
    if not m:
        return 0.0
    h, mi, se = (int(x or 0) for x in m.groups())
    return h * 3600 + mi * 60 + se


def fetch_api(queries: list[str], per_query: int = 25, months: int = 12, region: str = "ES",
              max_duration: int = 180, video_duration: str = "short", min_duration: int = 0) -> list[Video]:
    """`video_duration`: short (<4 min) | medium (4-20 min) | long (>20 min), filtro de la búsqueda de YouTube."""
    after = (dt.datetime.utcnow() - dt.timedelta(days=30 * months)).strftime("%Y-%m-%dT%H:%M:%SZ")
    ids: list[str] = []
    for q in queries:
        lang = "en" if re.search(r"\b(what|would|happen)\b", q) else "es"
        j = _get("search", part="id", q=q, type="video", videoDuration=video_duration, order="viewCount",
                 maxResults=min(50, per_query), publishedAfter=after, regionCode=region if lang == "es" else None,
                 relevanceLanguage=lang)
        ids += [it["id"]["videoId"] for it in j.get("items", [])]
        log.info("«%s»: %d vídeos", q, len(j.get("items", [])))
    ids = list(dict.fromkeys(ids))
    vids: list[Video] = []
    for i in range(0, len(ids), 50):
        j = _get("videos", part="snippet,statistics,contentDetails", id=",".join(ids[i:i + 50]))
        for it in j.get("items", []):
            sn, st, cd = it["snippet"], it.get("statistics", {}), it["contentDetails"]
            d = _iso_dur(cd.get("duration"))
            if d and (d > max_duration or d < min_duration):
                continue
            vids.append(Video(title=sn["title"], channel=sn["channelTitle"], views=int(st.get("viewCount", 0)),
                              likes=int(st["likeCount"]) if "likeCount" in st else None,
                              comments=int(st["commentCount"]) if "commentCount" in st else None,
                              published=sn["publishedAt"], duration_s=d, lang=sn.get("defaultAudioLanguage", ""),
                              url=(f"https://youtube.com/shorts/{it['id']}" if video_duration == "short"
                                   else f"https://youtube.com/watch?v={it['id']}"), source="youtube_api",
                              notes=(sn.get("description") or "")[:300]))
    return vids


def load_file(path: Path) -> list[Video]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    items = raw["videos"] if isinstance(raw, dict) else raw
    fields = set(Video.__dataclass_fields__)
    return [Video(**{k: v for k, v in it.items() if k in fields}) for it in items]


# ------------------------------------------------------------------------------------------- análisis
def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def topic_hit(text: str, words: list[str]) -> bool:
    """¿Contiene `text` (normalizado) alguna palabra clave? Coincidencia por palabra, no por subcadena
    («ia» no debe casar con «pasaría» ni «sol» con «solo»); las claves largas admiten sufijos
    («sobrevivir» → «sobrevivirías»), las cortas solo el plural."""
    for w in words:
        w = _norm(w)
        tail = r"\w*" if len(w) >= 5 else r"(?:s|es)?"
        if re.search(rf"\b{re.escape(w)}{tail}\b", text):
            return True
    return False


EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
TITLE_PATTERNS = {
    "pregunta «¿qué pasaría si…?»": r"qu[eé] pasar[ií]a si|what would happen|what if",
    "segunda persona (tú/te)": r"\b(tu|tú|te|you|your)\b",
    "número / cifra": r"\d",
    "superlativo / extremo": r"\b(m[aá]s|nunca|todo|todos|siempre|imposible|extrem|mayor|peor|mejor|most|never|every)\w*",
    "supervivencia / peligro": r"sobreviv|atrapad|muer|peligr|surviv|trapped|die|danger",
    "tiempo concreto (días/años)": r"\b(\d+\s*)?(d[ií]as?|a[nñ]os?|horas?|semanas?|minutos?|days?|years?|hours?)\b",
    "con emoji": None,
    "en MAYÚSCULAS (alguna palabra)": r"\b[A-ZÁÉÍÓÚÑ]{4,}\b",
}
TOPICS = {
    "espacio": "espacio marte luna sol planeta agujero negro galaxia space mars moon sun planet black hole",
    "cuerpo humano": "cuerpo dormir sueño comer comieras comida beber bebieras agua sangre cerebro respiracion oxigeno pelo piel hueso corazon body sleep brain eat breath heart",
    "supervivencia": "sobrevivir atrapado isla desierto oceano mar selva survive trapped island ocean desert",
    "historia": "medieval edad media roma egipto antiguo historia vikingo history ancient rome egypt",
    "dinero / poder": "millonario dinero rico mafia jefe presidente rey billonario money rich boss king",
    "fantasía / poderes": "inmortal invisible poderes volar superpoder tiempo viaje immortal invisible powers fly",
    "tierra / catástrofes": "tierra volcán terremoto asteroide tsunami humanos desaparecieran earth volcano asteroid",
    "animales": "ballena tiburón animal dinosaurio hormiga whale shark dinosaur ant animal",
    "tecnología": "internet móvil robot ia inteligencia artificial internet phone robot ai",
}


def analyze(vids: list[Video]) -> dict:
    now = dt.datetime.now(dt.timezone.utc)
    for v in vids:
        if v.published:
            try:
                p = dt.datetime.fromisoformat(v.published.replace("Z", "+00:00"))
                if p.tzinfo is None:
                    p = p.replace(tzinfo=dt.timezone.utc)
                days = max(1.0, (now - p).total_seconds() / 86400)
            except ValueError:
                days = None
        else:
            days = None
        v.metrics = {
            "views_per_day": round(v.views / days, 1) if v.views and days else None,
            "like_rate": round(v.likes / v.views, 4) if v.likes and v.views else None,
            "comment_rate": round(v.comments / v.views, 5) if v.comments and v.views else None,
            "title_len": len(v.title), "title_words": len(v.title.split()),
        }
    ranked = sorted(vids, key=lambda v: (v.metrics.get("views_per_day") or 0, v.views or 0), reverse=True)
    top = ranked[: max(5, len(ranked) // 4)]
    rest = ranked[len(top):] or ranked

    def share(group, pat):
        if not group:
            return 0.0
        if pat is None:
            return sum(bool(EMOJI.search(v.title)) for v in group) / len(group)
        return sum(bool(re.search(pat, v.title if "A-Z" in pat else _norm(v.title))) for v in group) / len(group)

    patterns = {name: {"top": round(share(top, pat), 2), "resto": round(share(rest, pat), 2)}
                for name, pat in TITLE_PATTERNS.items()}
    topic_scores = {}
    for name, kw in TOPICS.items():
        words = kw.split()
        hits = [v for v in ranked if topic_hit(_norm(v.title), words)]
        if hits:
            topic_scores[name] = {
                "videos": len(hits),
                "mediana_vistas": int(statistics.median(v.views or 0 for v in hits)),
                "en_top": sum(v in top for v in hits),
            }
    words = Counter(w for v in top for w in re.findall(r"[a-záéíóúñü]{4,}", _norm(v.title)) if w not in STOP)
    durs = [v.duration_s for v in top if v.duration_s]
    tlen = [v.metrics["title_len"] for v in top]
    channels = Counter(v.channel for v in top if v.channel)
    return {
        "n_videos": len(vids), "n_top": len(top),
        "top_videos": [{"title": v.title, "channel": v.channel, "views": v.views,
                        "views_per_day": v.metrics.get("views_per_day"), "duration_s": v.duration_s,
                        "like_rate": v.metrics.get("like_rate"), "url": v.url, "hook": v.hook,
                        "thumbnail_text": v.thumbnail_text, "notes": v.notes[:200]} for v in top[:20]],
        "title_patterns": patterns,
        "topics": dict(sorted(topic_scores.items(), key=lambda kv: -kv[1]["mediana_vistas"])),
        "top_words": words.most_common(25),
        "duration_top": {"mediana_s": statistics.median(durs) if durs else None,
                         "min_s": min(durs) if durs else None, "max_s": max(durs) if durs else None},
        "title_len_top": {"mediana": statistics.median(tlen) if tlen else None},
        "top_channels": channels.most_common(10),
        "hooks": [v.hook for v in top if v.hook][:15],
    }


def build_style_guide(a: dict) -> dict:
    """Convierte el análisis en reglas accionables para el guionista y el banco de ideas."""
    pat = a["title_patterns"]
    rules = []
    for name, d in pat.items():
        if d["top"] >= 0.5 and d["top"] >= d["resto"]:
            rules.append(f"Título: usar {name} (aparece en el {int(d['top'] * 100)} % de los vídeos top).")
        elif d["top"] + 0.15 < d["resto"]:
            rules.append(f"Título: evitar abusar de {name} (menos frecuente en los top).")
    dur = a["duration_top"].get("mediana_s")
    if dur:
        lo, hi = max(20, dur * 0.8), min(90, dur * 1.2)
        rules.append(f"Duración: apuntar a {lo:.0f}-{hi:.0f} s (mediana de los top: {dur:.0f} s).")
    tl = a["title_len_top"].get("mediana")
    if tl:
        rules.append(f"Título de unos {tl:.0f} caracteres (mediana de los top).")
    topics = list(a["topics"])[:4]
    if topics:
        rules.append("Temas con más tirón ahora: " + ", ".join(topics) + ".")
    if a["hooks"]:
        rules.append("Ganchos de referencia (estructura, no copiar literal): " + " | ".join(a["hooks"][:5]))
    return {
        "updated": dt.date.today().isoformat(),
        "n_videos": a["n_videos"],
        "rules": rules,
        "preferred_topics": topics,
        "title_examples": [v["title"] for v in a["top_videos"][:10]],
        "target_seconds": a["duration_top"],
        "principle": "Replicar patrones (estructura, ritmo, formato), nunca guiones, personajes, marcas ni miniaturas ajenas.",
    }


def report_md(a: dict, guide: dict, queries: list[str]) -> str:
    L = [f"# Investigación del nicho «¿qué pasaría si…?» — {dt.date.today().isoformat()}", "",
         f"Vídeos analizados: **{a['n_videos']}** · Top: **{a['n_top']}** · Consultas: {', '.join(queries)}", "",
         "## Vídeos que mejor funcionan (por visualizaciones/día)", "",
         "| # | Título | Canal | Vistas | Vistas/día | Duración |", "|---|---|---|---|---|---|"]
    for i, v in enumerate(a["top_videos"], 1):
        vpd = f"{v['views_per_day']:,.0f}".replace(",", ".") if v["views_per_day"] else "—"
        views = f"{v['views']:,}".replace(",", ".") if v["views"] else "—"
        dur = f"{v['duration_s']:.0f} s" if v["duration_s"] else "—"
        L.append(f"| {i} | [{v['title']}]({v['url']}) | {v['channel']} | {views} | {vpd} | {dur} |")
    L += ["", "## Patrones en los títulos (top vs. resto)", "", "| Patrón | Top | Resto |", "|---|---|---|"]
    for k, d in a["title_patterns"].items():
        L.append(f"| {k} | {d['top']:.0%} | {d['resto']:.0%} |")
    L += ["", "## Temas", "", "| Tema | Vídeos | Mediana de vistas | En el top |", "|---|---|---|---|"]
    for k, d in a["topics"].items():
        L.append(f"| {k} | {d['videos']} | {d['mediana_vistas']:,} | {d['en_top']} |".replace(",", "."))
    L += ["", "## Palabras más frecuentes en títulos top", "", ", ".join(f"{w} ({n})" for w, n in a["top_words"]),
          "", "## Canales con más vídeos en el top", "", ", ".join(f"{c} ({n})" for c, n in a["top_channels"]),
          "", "## Guía de estilo resultante (la usa la fábrica)", ""]
    L += [f"- {r}" for r in guide["rules"]]
    L += ["", f"> {guide['principle']}"]
    return "\n".join(L)


def run(queries: list[str] | None = None, from_file: Path | None = None, **kw) -> dict:
    queries = queries or DEFAULT_QUERIES
    OUT.mkdir(parents=True, exist_ok=True)
    if from_file:
        vids = load_file(from_file)
        queries = [f"archivo {Path(from_file).name}"]
    else:
        vids = fetch_api(queries, **kw)
    if not vids:
        raise RuntimeError("No se obtuvo ningún vídeo para analizar")
    a = analyze(vids)
    guide = build_style_guide(a)
    stamp = dt.date.today().isoformat()
    (OUT / f"videos_{stamp}.json").write_text(json.dumps([asdict(v) for v in vids], indent=1, ensure_ascii=False))
    (OUT / f"analysis_{stamp}.json").write_text(json.dumps(a, indent=1, ensure_ascii=False))
    (OUT / f"report_{stamp}.md").write_text(report_md(a, guide, queries), encoding="utf-8")
    (OUT / "style_guide.json").write_text(json.dumps(guide, indent=1, ensure_ascii=False))
    log.info("Informe: %s", OUT / f"report_{stamp}.md")
    return guide


def style_guide() -> dict | None:
    f = OUT / "style_guide.json"
    return json.loads(f.read_text()) if f.exists() else None
