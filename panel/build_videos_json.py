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
    "caer-de-un-avion": "2026-11-26T18:30",
    "un-ano-sin-sol": "2026-11-27T18:30",
    "caer-hacia-jupiter": "2026-11-28T18:30",
    "naufrago-sin-agua": "2026-11-29T18:30",
    "ascensor-sin-comida-3-semanas": "2026-11-30T18:30",
    "caer-desde-la-iss": "2026-12-01T18:30",
    "diez-zanahorias-al-dia": "2026-12-02T18:30",
    "aguantar-un-estornudo": "2026-12-03T18:30",
}
REPO_RAW = "https://github.com/jaimete332/Canal-animado/raw/claude/youtube-shorts-automation-qkjrhy/"

def _is_wide(png: Path) -> bool:
    import struct
    b = png.read_bytes()[16:24]
    w, h = struct.unpack(">II", b)
    return w > h


assets = json.loads(Path(sys.argv[1]).read_text()) if len(sys.argv) > 1 else {}
old = {}
out_f = ROOT / "panel" / "videos.json"
if out_f.exists():
    old = {v["slug"]: v for v in json.loads(out_f.read_text())}
videos = []
for d in sorted((ROOT / "PARA_SUBIR").glob("*_*/")):
    if not d.name.split("_", 1)[0].isdigit() or not (d / "extra" / "metadata.json").exists():
        continue  # carpetas sueltas (p. ej. la versión con otra voz de un Short ya entregado)
    slug = d.name.split("_", 1)[1]
    m = json.loads((d / "extra" / "metadata.json").read_text(encoding="utf-8"))
    a = {**{k: old.get(slug, {}).get(k) for k in ("video", "miniatura", "video_mb", "enlace")}, **assets.get(slug, {})}
    w = (m.get("format") == "landscape") or ((d / "miniatura.png").exists() and _is_wide(d / "miniatura.png"))
    if w:  # los vídeos largos horizontales van en videos_largo.json (panel/build_videos_largo.py)
        continue
    videos.append({
        "slug": slug, "orden": int(d.name.split("_")[0]), "fecha": CALENDARIO.get(slug),
        "titulo": m["title"], "descripcion": m["description"], "etiquetas": ", ".join(m["tags"]),
        "comentario": m["pinned_comment"], "duracion": round(m["duration_s"], 1),
        "video": a.get("video"), "miniatura": a.get("miniatura"), "formato": "16:9" if w else "9:16",
        "enlace": a.get("enlace") or (REPO_RAW + f"PARA_SUBIR/{d.name}/{slug}.mp4" if w else None),
        "video_mb": a.get("video_mb") or round((d / f"{slug}.mp4").stat().st_size / 1048576, 1),
    })
seen = {v["slug"] for v in videos}
videos += [v for slug, v in old.items() if slug not in seen]  # archivados (ya publicados): se conservan
videos.sort(key=lambda v: (v.get("fecha") or "", v["orden"]))
out_f.write_text(json.dumps(videos, ensure_ascii=False, indent=1), encoding="utf-8")
print(out_f, len(videos), "vídeos")
