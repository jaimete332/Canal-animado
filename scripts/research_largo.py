"""Investigación de vídeos LARGOS (10-40 min) en español para elegir nicho y formato.
No toca la guía de Shorts: escribe data/research/largo_<fecha>.json y largo_<fecha>.md.
Uso: python3 scripts/research_largo.py [--months 12] [--per-query 50]"""
import argparse
import datetime as dt
import json
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fabrica.research.niche import fetch_api  # noqa: E402

# Familias de nicho candidatas (animación explicativa en español, compatibles con el personaje Leo)
NICHOS = {
    "qué pasaría si (largo)": ["qué pasaría si", "qué pasaría si animación", "y si la tierra"],
    "historia animada": ["historia animada", "la historia de", "historia de la humanidad animada"],
    "cómo vivían / vida cotidiana": ["cómo vivían en la edad media", "un día en la vida de", "cómo era la vida en"],
    "cuerpo humano": ["cuerpo humano explicado", "qué le pasa a tu cuerpo", "cómo funciona el cuerpo humano"],
    "espacio y universo": ["el universo explicado", "viaje por el universo", "qué hay dentro de un agujero negro"],
    "supervivencia / casos reales": ["sobrevivió", "la increíble historia de", "atrapados durante"],
    "misterios y curiosidades": ["misterios sin resolver", "curiosidades del mundo", "cosas que no sabías"],
    "escala y comparaciones": ["comparación de tamaño", "qué tan profundo es", "la escala del universo"],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--months", type=int, default=12)
    ap.add_argument("--per-query", type=int, default=50)
    a = ap.parse_args()
    rows = []
    for nicho, qs in NICHOS.items():
        for dur in ("medium", "long"):  # 4-20 min y >20 min; luego filtramos 10-40 min
            vids = fetch_api(qs, per_query=a.per_query, months=a.months, video_duration=dur,
                             min_duration=600, max_duration=2400)
            for v in vids:
                rows.append({"nicho": nicho, **v.__dict__})
    now = dt.datetime.now(dt.timezone.utc)
    seen = {}
    for r in rows:
        days = max(1.0, (now - dt.datetime.fromisoformat(r["published"].replace("Z", "+00:00"))).days)
        r["vpd"] = round((r["views"] or 0) / days, 1)
        seen.setdefault(r["url"], r)
    rows = list(seen.values())
    by = defaultdict(list)
    for r in rows:
        by[r["nicho"]].append(r)
    stamp = dt.date.today().isoformat()
    out = Path(__file__).resolve().parents[1] / "data" / "research"
    (out / f"largo_{stamp}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    md = [f"# Vídeos largos (10-40 min) en español — {stamp}", "",
          f"{len(rows)} vídeos únicos, publicados en los últimos {a.months} meses. Métrica principal: visualizaciones/día.", "",
          "| Nicho | Vídeos | Mediana vistas/día | Mediana vistas | Mediana duración | Canales distintos |",
          "|---|---|---|---|---|---|"]
    summary = []
    for n, vs in by.items():
        summary.append((st.median([v["vpd"] for v in vs]), n, vs))
    for med, n, vs in sorted(summary, reverse=True):
        md.append(f"| {n} | {len(vs)} | {med:,.0f} | {st.median([v['views'] for v in vs]):,.0f} | "
                  f"{st.median([v['duration_s'] for v in vs]) / 60:.1f} min | {len({v['channel'] for v in vs})} |")
    md += ["", "## Top 40 por visualizaciones/día", "", "| # | Título | Canal | Nicho | Vistas | Vistas/día | Duración |",
           "|---|---|---|---|---|---|---|"]
    for i, v in enumerate(sorted(rows, key=lambda r: -r["vpd"])[:40], 1):
        md.append(f"| {i} | [{v['title'].replace('|', '/')}]({v['url']}) | {v['channel']} | {v['nicho']} | "
                  f"{v['views']:,} | {v['vpd']:,.0f} | {v['duration_s'] / 60:.1f} min |")
    (out / f"largo_{stamp}.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md[:16]))


if __name__ == "__main__":
    main()
