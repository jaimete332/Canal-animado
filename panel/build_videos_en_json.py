"""Genera panel/videos_en.json (pestaña «Stickpothetical» del panel) a partir de TO_UPLOAD/.

Uso: python3 panel/build_videos_en_json.py panel/assets_en.json
  assets_en.json: {"<slug>": {"video_parts": [urls...], "preview": url, "miniatura": url, "miniatura2": url}}
  El vídeo completo (> 20 MiB) se sube troceado (`split -b 18M`); el panel junta los trozos al descargar
  y el archivo resultante es idéntico al original. `preview` es una versión ligera para verlo en el panel.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CALENDARIO = {  # slug -> fecha y hora de publicación (hora de España; 21:00 = 15:00 en Nueva York)
    "medieval-peasant-1348": "2026-11-21T21:00",
}

assets = json.loads(Path(sys.argv[1]).read_text()) if len(sys.argv) > 1 else {}
videos = []
for d in sorted((ROOT / "TO_UPLOAD").glob("*_*/")):
    slug = d.name.split("_", 1)[1]
    m = json.loads((d / "extra" / "metadata.json").read_text(encoding="utf-8"))
    a = assets.get(slug, {})
    srt = d / "captions.srt"
    videos.append({
        "slug": slug, "orden": int(d.name.split("_")[0]), "fecha": CALENDARIO.get(slug),
        "titulo": m["title"], "descripcion": m["description"], "etiquetas": ", ".join(m["tags"]),
        "comentario": m["pinned_comment"], "duracion": round(m["duration_s"], 1),
        "capitulos": [f"{c['time']} {c['title']}" for c in m.get("chapters", [])],
        "srt": srt.read_text(encoding="utf-8") if srt.exists() else "",
        "video_parts": a.get("video_parts", []), "preview": a.get("preview"),
        "miniatura": a.get("miniatura"), "miniatura2": a.get("miniatura2"),
        "video_mb": round((d / f"{slug}.mp4").stat().st_size / 1048576, 1),
    })
out_f = ROOT / "panel" / "videos_en.json"
out_f.write_text(json.dumps(videos, ensure_ascii=False, indent=1), encoding="utf-8")
print(out_f, len(videos), "vídeos")
