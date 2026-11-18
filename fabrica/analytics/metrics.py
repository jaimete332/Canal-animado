"""Métricas de YouTube → aprendizaje para los próximos guiones.

`fetch_all()` descarga (YouTube Analytics API) visualizaciones, retención media, likes, comentarios,
compartidos y suscriptores por vídeo y los guarda en el registro SQLite.
`insights()` resume qué funciona (categorías, longitud del gancho, duración) y genera pautas
que el generador de guiones recibe en su prompt.
"""
from __future__ import annotations

import datetime as dt
import statistics

from ..core.log import get_logger
from ..core.registry import Registry

log = get_logger("metrics")
METRICS = "views,likes,comments,shares,averageViewDuration,averageViewPercentage,subscribersGained"


def fetch_all() -> int:
    from googleapiclient.discovery import build

    from ..publish.youtube import credentials
    reg = Registry()
    yta = build("youtubeAnalytics", "v2", credentials=credentials())
    n = 0
    for v in reg.videos():
        if not v["youtube_id"]:
            continue
        start = dt.date.fromtimestamp(v["created_at"]).isoformat()
        r = yta.reports().query(ids="channel==MINE", startDate=start, endDate=dt.date.today().isoformat(),
                                metrics=METRICS, filters=f"video=={v['youtube_id']}").execute()
        if r.get("rows"):
            names = [h["name"] for h in r["columnHeaders"]]
            reg.add_metrics(v["youtube_id"], dict(zip(names, r["rows"][0])))
            n += 1
    log.info("Métricas actualizadas para %d vídeos", n)
    return n


def insights() -> dict:
    rows = Registry().latest_metrics()
    if len(rows) < 3:
        return {"videos_with_metrics": len(rows), "guidance": [],
                "note": "Se necesitan al menos 3 vídeos publicados con métricas para sacar conclusiones."}
    by_cat: dict[str, list] = {}
    for r in rows:
        by_cat.setdefault(r["category"] or "?", []).append(r)
    cats = {c: {"n": len(v), "avg_view_pct": statistics.mean(x["avg_view_pct"] or 0 for x in v),
                "avg_views": statistics.mean(x["views"] or 0 for x in v)} for c, v in by_cat.items()}
    best = sorted(rows, key=lambda r: (r["avg_view_pct"] or 0), reverse=True)
    top, bottom = best[: max(1, len(best) // 3)], best[-max(1, len(best) // 3):]
    hook_len = lambda rs: statistics.mean(len((r["hook"] or "").split()) for r in rs)  # noqa: E731
    dur = lambda rs: statistics.mean(r["duration_s"] or 0 for r in rs)  # noqa: E731
    guidance = [
        f"Categorías con mejor retención: {', '.join(sorted(cats, key=lambda c: -cats[c]['avg_view_pct'])[:2])}.",
        f"Ganchos de los mejores vídeos: ~{hook_len(top):.0f} palabras (peores: ~{hook_len(bottom):.0f}).",
        f"Duración media de los mejores: {dur(top):.0f}s (peores: {dur(bottom):.0f}s).",
        "Ganchos que mejor funcionaron: " + " | ".join(r["hook"] for r in top[:3]),
    ]
    return {"videos_with_metrics": len(rows), "categories": cats, "guidance": guidance}
