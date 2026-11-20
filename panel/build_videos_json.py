"""Genera panel/videos.json (datos del panel «Cola de publicación») a partir de PARA_SUBIR/.

Uso: python3 panel/build_videos_json.py [assets.json]
  assets.json (opcional): {"<slug>": {"video": "<url>", "miniatura": "<url>", "video_mb": 17.9}}
  con las URL que devuelve la subida de assets del artefacto. Las fechas salen de CALENDARIO.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CALENDARIO = {  # slug -> fecha y hora de publicación (hora de España)
    "ceniza-de-volcan": "2026-11-20T18:30",
    "agua-helada-del-titanic": "2026-11-21T18:30",
    "sin-casco-en-el-espacio": "2026-11-22T18:30",
}

assets = json.loads(Path(sys.argv[1]).read_text()) if len(sys.argv) > 1 else {}
old = {}
out_f = ROOT / "panel" / "videos.json"
if out_f.exists():
    old = {v["slug"]: v for v in json.loads(out_f.read_text())}
videos = []
for d in sorted((ROOT / "PARA_SUBIR").glob("*_*/")):
    slug = d.name.split("_", 1)[1]
    m = json.loads((d / "extra" / "metadata.json").read_text(encoding="utf-8"))
    a = {**{k: old.get(slug, {}).get(k) for k in ("video", "miniatura", "video_mb")}, **assets.get(slug, {})}
    videos.append({
        "slug": slug, "orden": int(d.name.split("_")[0]), "fecha": CALENDARIO.get(slug),
        "titulo": m["title"], "descripcion": m["description"], "etiquetas": ", ".join(m["tags"]),
        "comentario": m["pinned_comment"], "duracion": round(m["duration_s"], 1),
        "video": a.get("video"), "miniatura": a.get("miniatura"),
        "video_mb": a.get("video_mb") or round((d / f"{slug}.mp4").stat().st_size / 1048576, 1),
    })
out_f.write_text(json.dumps(videos, ensure_ascii=False, indent=1), encoding="utf-8")
print(out_f, len(videos), "vídeos")
