"""Copia el vídeo terminado a samples/<slug>/ y genera PUBLICAR.md (título, descripción, etiquetas...).
Uso: python3 scripts/publish_sheet.py <slug> [<slug> ...]"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

for slug in sys.argv[1:]:
    o, d = ROOT / "output" / slug, ROOT / "samples" / slug
    d.mkdir(parents=True, exist_ok=True)
    for f in ("final.mp4", "thumbnail.png", "thumbnail_16x9.png", "metadata.json", "qa/report.md", "qa/contact_sheet.jpg"):
        if (o / f).exists():
            shutil.copy(o / f, d / Path(f).name)
    m = json.loads((o / "metadata.json").read_text())
    (d / "PUBLICAR.md").write_text(f"""# Publicar: «{m['title']}»

**Vídeo:** `final.mp4` ({m['duration_s']:.1f} s) · **Miniatura Shorts:** `thumbnail.png` (1080×1920) · **Miniatura 16:9:** `thumbnail_16x9.png`

## Título ({len(m['title'])} caracteres)
```
{m['title']}
```

## Descripción
```
{m['description']}
```

## Etiquetas (YouTube Studio → Más opciones → Etiquetas)
```
{', '.join(m['tags'])}
```

## Comentario fijado
```
{m['pinned_comment']}
```

## Ajustes
* Categoría: Educación · Idioma: español (España) · No es contenido para niños
* «Contenido alterado o sintético»: **Sí** (voz sintética)
""", encoding="utf-8")
    print("✓", d)
