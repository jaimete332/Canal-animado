"""Genera panel/videos_largo.json (pestaña «Largos · ES» del panel) a partir de la entrega en PARA_SUBIR/ o samples/.

Uso: python3 panel/build_videos_largo.py   (lee panel/assets_largo.json: {slug: {miniatura, video_parts, fecha}})
Los vídeos largos no caben en un solo asset (máx. 20 MiB): se suben troceados con `split -b 18M` y la página
une las partes al descargar (el archivo resultante es idéntico al original).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
assets = json.loads((ROOT / "panel" / "assets_largo.json").read_text(encoding="utf-8"))
out = []
for i, (slug, a) in enumerate(assets.items(), 1):
    d = next(iter(sorted((ROOT / "PARA_SUBIR").glob(f"*_{slug}"))), None) or ROOT / "samples" / slug
    m = json.loads((d / "extra" / "metadata.json").read_text(encoding="utf-8"))
    desc = m["description"]
    caps = []
    if "⏱️ CAPÍTULOS" in desc:
        caps = [ln for ln in desc.split("⏱️ CAPÍTULOS\n", 1)[1].split("\n\n", 1)[0].splitlines() if ln.strip()]
    mp4 = d / f"{slug}.mp4"
    out.append({"slug": slug, "orden": i, "fecha": a.get("fecha"), "titulo": m["title"], "descripcion": desc,
                "etiquetas": ", ".join(m["tags"]), "comentario": m["pinned_comment"],
                "duracion": round(m["duration_s"], 1), "miniatura": a.get("miniatura"),
                "video_parts": a.get("video_parts", []),
                "video_mb": round(mp4.stat().st_size / 1048576, 1) if mp4.exists() else a.get("video_mb"),
                "capitulos": caps})
(ROOT / "panel" / "videos_largo.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(out), "vídeos largos")
