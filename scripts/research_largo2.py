"""Segunda ronda de nichos para vídeo largo en español (10-40 min), sin videojuegos.
Escribe data/research/largo2_<fecha>.json/.md. Uso: python3 scripts/research_largo2.py"""
import datetime as dt
import time
import json
import re
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fabrica.research.niche import fetch_api  # noqa: E402

NICHOS = {
    "sobrevivir solo en X (isla, selva, desierto)": ["cuánto podrías sobrevivir solo en", "sobrevivir solo en una isla desierta",
                                                     "sobrevivir en la selva"],
    "apocalipsis / colapso (primeros días)": ["primeros 7 días apocalipsis", "qué pasaría si se apagara internet para siempre",
                                              "qué pasaría si desaparecieran los humanos"],
    "qué pasaría si la Tierra / el planeta": ["qué pasaría si la tierra", "qué pasaría si la luna", "qué pasaría si el sol"],
    "cuerpo humano al límite": ["qué le pasa a tu cuerpo si", "qué pasaría si dejaras de dormir", "cuánto tiempo puede vivir un humano sin"],
    "escala del universo / viaje": ["viaje al borde del universo", "qué hay al final del universo", "viaje al centro de la tierra"],
    "animales vs / naturaleza extrema": ["animales más peligrosos del mundo", "qué pasaría si los dinosaurios", "qué pasaría si los insectos"],
    "historias reales de supervivencia": ["la increíble historia de supervivencia", "sobrevivió días en el mar", "atrapados en la montaña"],
    "futuro / dentro de X años": ["cómo será la tierra en 1000 años", "el futuro de la humanidad", "qué pasará en el año 3000"],
}
GAME = re.compile(r"minecraft|roblox|gta|fortnite|free fire|brookhaven|mod\b|gameplay", re.I)


def main():
    now = dt.datetime.now(dt.timezone.utc)
    rows, seen = [], set()
    for nicho, qs in NICHOS.items():
        for dur in ("medium", "long"):
            try:
                found = fetch_api(qs, per_query=50, months=18, video_duration=dur, min_duration=600, max_duration=2400)
            except Exception as e:  # límite de peticiones: se salta esa consulta y se sigue
                print(f"[aviso] {nicho} ({dur}): {str(e)[:120]}")
                found = []
            time.sleep(1.5)
            for v in found:
                if v.url in seen or GAME.search(v.title + " " + v.channel):
                    continue
                seen.add(v.url)
                days = max(1.0, (now - dt.datetime.fromisoformat(v.published.replace("Z", "+00:00"))).days)
                rows.append({"nicho": nicho, **v.__dict__, "vpd": round((v.views or 0) / days, 1)})
    stamp = dt.date.today().isoformat()
    out = Path(__file__).resolve().parents[1] / "data" / "research"
    (out / f"largo2_{stamp}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    md = [f"# Nichos de vídeo largo en español (2.ª ronda, sin videojuegos) — {stamp}", "",
          "| Nicho | Vídeos | Mediana vistas/día | P75 vistas/día | Mediana vistas | Mediana duración |", "|---|---|---|---|---|---|"]
    res = []
    for n in NICHOS:
        vs = [r for r in rows if r["nicho"] == n]
        if not vs:
            continue
        vpd = sorted(r["vpd"] for r in vs)
        res.append((st.median(vpd), n, vs, vpd[int(len(vpd) * 0.75)]))
    for med, n, vs, p75 in sorted(res, reverse=True):
        md.append(f"| {n} | {len(vs)} | {med:,.0f} | {p75:,.0f} | {st.median([v['views'] for v in vs]):,.0f} | "
                  f"{st.median([v['duration_s'] for v in vs]) / 60:.1f} min |")
    for med, n, vs, _ in sorted(res, reverse=True):
        md += ["", f"## {n}", "", "| Vistas/día | Vistas | Duración | Canal | Título |", "|---|---|---|---|---|"]
        for v in sorted(vs, key=lambda r: -r["vpd"])[:10]:
            md.append(f"| {v['vpd']:,.0f} | {v['views']:,} | {v['duration_s'] / 60:.0f} min | {v['channel']} | "
                      f"[{v['title'].replace('|', '/')}]({v['url']}) |")
    (out / f"largo2_{stamp}.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
