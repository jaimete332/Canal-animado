"""Aprendizaje del PROPIO canal: qué tienen en común los Shorts que mejor han funcionado.

Pesa más que la competencia (es nuestra audiencia, nuestro personaje y nuestro formato). Fuentes de «ganador»:
  1. Métricas reales del registro (`python -m fabrica metrics`): se ordenan por % de retención y vistas.
  2. Lo que declara el usuario (`python -m fabrica research --winner slug ...`) → data/research/own_winners.json.

Compara ganadores contra el resto de Shorts con rasgos MEDIBLES de la historia (título, gancho, casos reales con
nombre y año, contadores, estructura) y con «arquetipos de premisa».

Filtro de honestidad: un rasgo solo genera regla si TODOS los ganadores superan la mediana del resto («consistente»).
Con n pequeño casi nada lo cumple, y está bien: es preferible no tener regla a tener una falsa. Las lecciones
cualitativas (lo que se ve al leer los guiones ganadores) se guardan a mano en `own_winners.json` → `lecciones`
y entran en la guía marcadas «(propio, obs.)». Con métricas reales (--views/--retention o `fabrica metrics`) el
análisis gana fuerza; sin ellas, es una pista para decidir qué repetir y qué probar.

Salidas en data/research/: own_winners.json (entrada), own_channel_<fecha>.json y .md (análisis) y la clave
`own_channel` + reglas «(propio)» dentro de style_guide.json (las leen el guionista y el banco de ideas).
"""
from __future__ import annotations

import datetime as dt
import json
import re
import statistics
from pathlib import Path

from ..core.config import ROOT
from ..core.log import get_logger
from .niche import OUT, _norm

log = get_logger("research.own")
WINNERS_FILE = OUT / "own_winners.json"
STORIES = ROOT / "stories"
TAG = "(propio"

# --------------------------------------------------------------------------------------- rasgos de texto
YEAR = re.compile(r"\bmil (?:novecientos|ochocientos|setecientos|seiscientos|quinientos)\b|\bdos mil\b|\b1[5-9]\d\d\b|\b20[0-3]\d\b", re.I)
NAME = re.compile(r"\b[A-ZÁÉÍÓÚÑ]\w+(?: (?:de |del |la |el )?[A-ZÁÉÍÓÚÑ]\w+)+\b")
PLACE_TOKENS = {"polo", "sur", "norte", "gran", "mancha", "roja", "edad", "media", "estación", "espacial",
                "internacional", "fosa", "marianas", "nueva", "york", "tierra", "luna", "sol", "marte", "júpiter",
                "mar", "océano", "atlántico", "pacífico", "primera", "segunda", "día", "semana", "mes", "año"}
NUMBER_WORDS = r"(?:un|una|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|quince|veinte|treinta|cien|mil|diez mil)"
TITLE_NUM = re.compile(rf"\d|\b{NUMBER_WORDS}\b", re.I)
SECOND_PERSON = re.compile(r"\b(tu|tú|te|tus|eres|estás|estas|decides|imagina|vas|coges|miras|despiertas|despiertes|"
                           r"\w+(?:aras|ieras|eras|ases|ieses)|\w+(?:ás|és))\b", re.I)
DANGER = re.compile(r"sobreviv|morir|muert|peligr", re.I)
CTA = re.compile(r"comentarios|cu[ée]ntame|te leo", re.I)


def _overlays(s: dict) -> list[dict]:
    return ((s.get("visual") or s).get("overlays") or [])


def _named(text: str) -> list[str]:
    out = []
    for m in NAME.finditer(text):
        toks = [t for t in re.split(r"\s+", m.group(0)) if t[0].isupper()]
        if toks and not all(_norm(t) in PLACE_TOKENS for t in toks):
            out.append(m.group(0))
    return out


def story_features(d: dict) -> dict:
    sc = d["scenes"]
    title = d.get("title") or d.get("idea") or ""
    texts = [s["narration"] for s in sc]
    words = sum(len(t.split()) for t in texts)
    mention = [bool(YEAR.search(t)) and bool(_named(t)) for t in texts[1:]]   # año + nombre propio en la misma escena
    first = next((i + 1 for i, m in enumerate(mention) if m), None)           # índice de escena (0 = gancho)
    case_words = sum(len(t.split()) for t in texts[first:-1]) if first else 0   # de la 1.ª mención hasta antes del cierre
    ov = [o.get("type") for s in sc for o in _overlays(s)]
    short_sentences = sum(1 for t in texts for x in re.split(r"(?<=[.!?])\s+", t) if 0 < len(x.split()) <= 4)
    return {
        "titulo": title, "titulo_chars": len(title),
        "titulo_cifra": bool(TITLE_NUM.search(title)),
        "titulo_2a_persona": bool(SECOND_PERSON.search(_norm(title)) or SECOND_PERSON.search(title)),
        "titulo_peligro": bool(DANGER.search(title)),
        "gancho_palabras": len(texts[0].split()),
        "gancho_en_situacion": bool(SECOND_PERSON.match(texts[0])) or bool(SECOND_PERSON.search(texts[0])),
        "escenas": len(sc), "palabras": words,
        "personas_con_nombre": len({n for t in texts[1:] for n in _named(t)}),
        "anios_citados": sum(len(YEAR.findall(t)) for t in texts[1:]),
        "caso_real_pct": round(100 * case_words / max(1, words)),        # % de la narración dedicado al caso real
        "caso_real_aparece_en": round(first / len(sc), 2) if first else None,   # fracción del vídeo
        "datos_por_100_palabras": round(100 * sum(len(s.get("claims") or []) for s in sc) / max(1, words), 1),
        "contadores": ov.count("counter"), "datos_en_pantalla": ov.count("fact"),
        "frases_cortas": short_sentences,
        "cierra_a_comentarios": bool(CTA.search(texts[-1])),
    }


# --------------------------------------------------------------------------------------- arquetipos de premisa
# Moldes de premisa (no de palabras sueltas): qué tipo de situación plantea el título.
ARCHETYPES = {
    "caída / altura extrema": r"cay(?:er|eras|era|eses)|caes|saltar|saltaras|\d+\.?\d* ?(?:metros|km)\b",
    "ser alguien con poder o un rol ajeno": r"te convirtieras|fueras|ser (?:el|un)|jefe|rey|presidente|capo|mafia",
    "quitar algo universal de tu vida": r"\bsin\b.{0,30}\b(?:sol|luz|agua|sueno|dormir|internet|electricidad|aire|comida)|"
                                         r"(?:no|nunca).{0,25}(?:vieras|bebieras|durmieras|comieras)|desapareciera|se apagara",
    "situación cotidiana llevada al extremo": r"ascensor|avion|metro|movil|coche|tren|casa|cama|oficina|cocina",
    "cuerpo humano / salud": r"cuerpo|respir|dormir|sueno|vitamina|piel|hueso|cerebro|corazon",
}


def archetypes_of(title: str) -> list[str]:
    t = _norm(title)
    return [k for k, pat in ARCHETYPES.items() if re.search(pat, t)]


# --------------------------------------------------------------------------------------- ganadores
def load_winners() -> list[dict]:
    if WINNERS_FILE.exists():
        return json.loads(WINNERS_FILE.read_text(encoding="utf-8")).get("winners", [])
    return []


def _winners_doc() -> dict:
    return json.loads(WINNERS_FILE.read_text(encoding="utf-8")) if WINNERS_FILE.exists() else {"winners": [], "lecciones": []}


def add_winners(slugs: list[str], fuente: str = "usuario", nota: str = "", views: int | None = None,
                retention: float | None = None) -> list[dict]:
    """Registra Shorts ganadores (lo que declara el usuario o sus métricas). `views`/`retention` (% visto) son opcionales."""
    doc = _winners_doc()
    cur = {w["slug"]: w for w in doc.get("winners", [])}
    for s in slugs:
        if not (STORIES / f"{s}.json").exists():
            raise FileNotFoundError(f"No existe stories/{s}.json (usa el slug del Short)")
        w = {**cur.get(s, {}), "slug": s, "fuente": fuente, "nota": nota or cur.get(s, {}).get("nota", ""),
             "declarado": dt.date.today().isoformat()}
        if views is not None:
            w["vistas"] = views
        if retention is not None:
            w["retencion_pct"] = retention
        cur[s] = w
    doc["winners"] = list(cur.values())
    WINNERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    WINNERS_FILE.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    return doc["winners"]


def load_lessons() -> list[str]:
    return _winners_doc().get("lecciones", [])


def metric_winners(top: int = 3) -> list[dict]:
    """Ganadores por métricas reales del registro (si ya se han descargado)."""
    try:
        from ..core.registry import Registry
        rows = Registry().latest_metrics()
    except Exception:
        return []
    rows = [r for r in rows if r["views"] is not None]
    rows.sort(key=lambda r: ((r["avg_view_pct"] or 0), r["views"]), reverse=True)
    return [{"slug": r["slug"], "fuente": "métricas", "nota": f"{r['views']} vistas, {r['avg_view_pct']} % visto"}
            for r in rows[:top]]


def _shorts() -> dict[str, dict]:
    out = {}
    for f in sorted(STORIES.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        if d.get("category") == "anuncio" or len(d.get("scenes", [])) > 40:
            continue
        out[f.stem] = d
    return out


# --------------------------------------------------------------------------------------- análisis
def _med(xs):
    xs = [x for x in xs if x is not None]
    return round(statistics.median(xs), 2) if xs else None


def _share(group, key):
    return round(sum(bool(g[key]) for g in group) / len(group), 2) if group else None


def analyze_own(winners: list[dict] | None = None) -> dict:
    winners = winners if winners is not None else (metric_winners() or load_winners())
    shorts = _shorts()
    wset = [w["slug"] for w in winners if w["slug"] in shorts]
    if not wset:
        raise RuntimeError("No hay ganadores: usa `python -m fabrica research --own --winner slug ...`")
    feats = {s: story_features(d) for s, d in shorts.items()}
    for s, d in shorts.items():
        feats[s]["arquetipos"] = archetypes_of(feats[s]["titulo"])
    win = [feats[s] for s in wset]
    rest = [f for s, f in feats.items() if s not in wset]
    num = ["titulo_chars", "gancho_palabras", "escenas", "palabras", "personas_con_nombre", "anios_citados",
           "caso_real_pct", "caso_real_aparece_en", "datos_por_100_palabras", "contadores", "datos_en_pantalla",
           "frases_cortas"]
    boo = ["titulo_cifra", "titulo_2a_persona", "titulo_peligro", "gancho_en_situacion", "cierra_a_comentarios"]
    comp = {}
    for k in num:
        rm = _med([f[k] for f in rest])
        vals = [f[k] for f in win]
        comp[k] = {"ganadores": _med(vals), "resto": rm,
                   "consistente": bool(rm is not None and all((v or 0) > rm for v in vals))}   # TODOS los ganadores > mediana del resto
    for k in boo:
        gs, rs = _share(win, k), _share(rest, k)
        comp[k] = {"ganadores": gs, "resto": rs, "consistente": bool(gs == 1.0 and (rs or 0) <= 0.6)}
    arch = {}
    for name in ARCHETYPES:
        w_rate = round(sum(name in f["arquetipos"] for f in win) / len(win), 2)
        r_rate = round(sum(name in f["arquetipos"] for f in rest) / max(1, len(rest)), 2)
        arch[name] = {"ganadores": w_rate, "resto": r_rate, "bonus": round(max(0.0, min(8.0, 10 * (w_rate - r_rate))), 1)}
    return {"updated": dt.date.today().isoformat(), "n_ganadores": len(win), "n_resto": len(rest),
            "ganadores": winners, "rasgos": comp, "arquetipos": arch,
            "por_short": {s: feats[s] for s in feats}}


def own_rules(a: dict) -> list[str]:
    """Reglas accionables a partir de las diferencias medidas. Siempre con la n usada y marcadas como indicativas."""
    n = a["n_ganadores"]
    r = a["rasgos"]
    tag = f"(propio, n={n}, indicativo)" if n < 5 else f"(propio, n={n})"
    rules = []
    c = r["caso_real_pct"]
    if c["consistente"]:
        rules.append(f"Dedicar ~{int(c['ganadores'])} % de la narración a UN caso real con nombre y año contado como historia, no solo citado "
                     f"(ganadores: mediana {c['ganadores']} %; resto: {c['resto']} %) {tag}.")
    pc = r["personas_con_nombre"]
    if pc["consistente"]:
        rules.append(f"Al menos {int(pc['ganadores'])} personas o lugares con nombre propio por Short (ganadores: mediana {pc['ganadores']}; "
                     f"resto: {pc['resto']}) {tag}.")
    fc = r["datos_en_pantalla"]
    if fc["consistente"]:
        rules.append(f"Poner el dato clave también en una tarjeta «DATO REAL» en pantalla: {int(fc['ganadores'])}+ por Short "
                     f"(ganadores: mediana {fc['ganadores']}; resto: {fc['resto']}) {tag}.")
    best = [k for k, d in a["arquetipos"].items() if d["bonus"] >= 3]
    if best:
        rules.append("Premisas ganadoras (arquetipos): " + "; ".join(
            f"{k} ({int(a['arquetipos'][k]['ganadores'] * 100)} % de los ganadores frente a {int(a['arquetipos'][k]['resto'] * 100)} % del resto)"
            for k in best) + f" {tag}.")
    return rules + [f"{x} (propio, obs.)" if "(propio" not in x else x for x in load_lessons()]


def report_own_md(a: dict) -> str:
    L = [f"# Qué funciona en NUESTRO canal — {a['updated']}", "",
         f"Ganadores ({a['n_ganadores']}): " + ", ".join(f"`{w['slug']}` ({w['fuente']})" for w in a["ganadores"]) +
         f" · Resto de Shorts: {a['n_resto']}", "",
         "> Con n pequeño esto es una pista, no una prueba: sirve para decidir qué repetir y qué probar, "
         "y se valida con las métricas de los próximos Shorts.", "",
         "## Rasgos medidos (mediana o % de Shorts)", "", "| Rasgo | Ganadores | Resto | ¿Los 3 por encima? |", "|---|---|---|---|"]
    for k, d in a["rasgos"].items():
        L.append(f"| {k} | {d['ganadores']} | {d['resto']} | {'**sí**' if d['consistente'] else 'no'} |")
    L += ["", "## Arquetipos de premisa", "", "| Arquetipo | Ganadores | Resto | Bonus en el banco de ideas |", "|---|---|---|---|"]
    for k, d in a["arquetipos"].items():
        L.append(f"| {k} | {d['ganadores']:.0%} | {d['resto']:.0%} | +{d['bonus']} |")
    L += ["", "## Reglas resultantes", ""] + [f"- {x}" for x in own_rules(a)]
    return "\n".join(L)


# --------------------------------------------------------------------------------------- integración con la guía
def run_own(winners: list[dict] | None = None) -> dict:
    """Analiza, escribe el informe y fusiona el resultado en style_guide.json sin pisar el resto de la guía."""
    a = analyze_own(winners)
    stamp = dt.date.today().isoformat()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"own_channel_{stamp}.json").write_text(json.dumps(a, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / f"own_channel_{stamp}.md").write_text(report_own_md(a), encoding="utf-8")
    f = OUT / "style_guide.json"
    g = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {"rules": []}
    g["rules"] = [r for r in g.get("rules", []) if TAG not in r] + own_rules(a)
    g["own_channel"] = {"updated": stamp, "n_ganadores": a["n_ganadores"], "ganadores": [w["slug"] for w in a["ganadores"]],
                        "arquetipos": {k: v["bonus"] for k, v in a["arquetipos"].items()},
                        "rasgos": {k: v for k, v in a["rasgos"].items()}}
    f.write_text(json.dumps(g, ensure_ascii=False, indent=1), encoding="utf-8")
    log.info("Análisis del canal propio: %s", OUT / f"own_channel_{stamp}.md")
    return a


def archetype_bonus(idea: str) -> float:
    """Bonus (0-8) del banco de ideas para una idea cuyo molde de premisa coincide con el de los ganadores."""
    f = OUT / "style_guide.json"
    if not f.exists():
        return 0.0
    bonus = (json.loads(f.read_text(encoding="utf-8")).get("own_channel") or {}).get("arquetipos") or {}
    hits = [bonus.get(k, 0.0) for k in archetypes_of(idea)]
    return float(min(8.0, max(hits))) if hits else 0.0
