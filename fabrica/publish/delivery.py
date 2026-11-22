"""Carpeta de entrega: PARA_SUBIR/<NN>_<slug>/ con lo justo para subir un vídeo a mano.

  <slug>.mp4      vídeo final (nombre claro, no «final.mp4»)
  miniatura.png   miniatura vertical 1080×1920 (miniatura_16x9.png, horizontal)
  PUBLICAR.md     título, descripción, etiquetas, comentario fijado y ajustes, listos para copiar
  textos.txt      lo mismo en texto plano (se abre en cualquier móvil)
  extra/          metadata.json, informe de calidad y hoja de contactos

Cuando un vídeo ya esté publicado, `python -m fabrica published <slug>` lo archiva en samples/<slug>/.
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from ..core.config import ROOT

PENDING = ROOT / "PARA_SUBIR"
ARCHIVE = ROOT / "samples"


def find(slug: str) -> Path | None:
    """Carpeta de entrega de `slug`: PARA_SUBIR/<NN>_<slug>/ o, si ya se archivó, samples/<slug>/."""
    for d in sorted(PENDING.glob(f"*_{slug}")) + [PENDING / slug]:
        if d.is_dir():
            return d
    d = ARCHIVE / slug
    return d if d.is_dir() else None


def files(d: Path, slug: str) -> dict[str, Path]:
    """Rutas de vídeo, metadatos y miniatura en una carpeta de entrega (formato nuevo o samples/ antiguo)."""
    pick = lambda *c: next((d / x for x in c if (d / x).exists()), d / c[0])  # noqa: E731
    return {"root": d, "final": pick(f"{slug}.mp4", "final.mp4"),
            "metadata": pick("extra/metadata.json", "metadata.json"),
            "thumbnail": pick("miniatura.png", "thumbnail.png"),
            "approved": d / "APPROVED"}


def all_titles() -> list[str]:
    """Títulos de todo lo producido (pendiente o archivado), para no repetir ideas."""
    out = []
    for f in sorted(list(PENDING.glob("*/extra/metadata.json")) + list(ARCHIVE.glob("*/metadata.json"))):
        try:
            out.append(json.loads(f.read_text(encoding="utf-8")).get("title", ""))
        except (OSError, ValueError):
            pass
    return [t for t in out if t]


def _next_number() -> int:
    nums = [int(m.group(1)) for d in PENDING.glob("*_*") if (m := re.match(r"(\d+)_", d.name))]
    return max(nums, default=0) + 1


def _dur(sec: float) -> str:
    return f"{sec:.1f} s" if sec < 120 else f"{int(sec) // 60} min {int(sec) % 60:02d} s"


def sheet(m: dict) -> str:
    return f"""# Publicar: «{m['title']}»

**Vídeo:** `{m['_slug']}.mp4` ({_dur(m['duration_s'])}) · **Miniatura:** `miniatura.png` ({m.get('_thumb', '1080×1920')})

## Título ({len(m['title'])} caracteres)
```
{m['title']}
```

## Descripción
```
{m['description']}
```

## Etiquetas (YouTube Studio → Mostrar más → Etiquetas)
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
"""


def plain(m: dict) -> str:
    return (f"TÍTULO\n{m['title']}\n\nDESCRIPCIÓN\n{m['description']}\n\nETIQUETAS\n{', '.join(m['tags'])}\n\n"
            f"COMENTARIO FIJADO\n{m['pinned_comment']}\n\nAJUSTES\nCategoría: Educación · Idioma: español (España) · "
            "No es contenido para niños · Contenido alterado o sintético: Sí (voz sintética)\n")


def deliver(slug: str, src: Path | None = None) -> Path:
    """Copia el vídeo terminado (output/<slug>/ por defecto) a PARA_SUBIR/<NN>_<slug>/."""
    src = src or ROOT / "output" / slug
    d = find(slug)
    if d is None or d.parent != PENDING:
        d = PENDING / f"{_next_number():02d}_{slug}"
    (d / "extra").mkdir(parents=True, exist_ok=True)
    copies = {"final.mp4": f"{slug}.mp4", "thumbnail.png": "miniatura.png", "thumbnail_16x9.png": "miniatura_16x9.png",
              "metadata.json": "extra/metadata.json", "qa/report.md": "extra/informe_calidad.md",
              "qa/contact_sheet.jpg": "extra/hoja_de_contactos.jpg"}
    for a, b in copies.items():
        if (src / a).exists():
            shutil.copy(src / a, d / b)
    m = json.loads((d / "extra/metadata.json").read_text(encoding="utf-8"))
    m["_slug"] = slug
    if (d / "miniatura.png").exists():
        import cairo
        im = cairo.ImageSurface.create_from_png(str(d / "miniatura.png"))
        m["_thumb"] = f"{im.get_width()}×{im.get_height()}"
    (d / "PUBLICAR.md").write_text(sheet(m), encoding="utf-8")
    (d / "textos.txt").write_text(plain(m), encoding="utf-8")
    return d


def archive(slug: str) -> Path:
    """Vídeo ya publicado: mueve PARA_SUBIR/<NN>_<slug>/ a samples/<slug>/."""
    d = find(slug)
    if d is None or d.parent != PENDING:
        raise FileNotFoundError(f"'{slug}' no está en PARA_SUBIR/")
    dst = ARCHIVE / slug
    if dst.exists():
        shutil.rmtree(dst)
    shutil.move(str(d), str(dst))
    return dst
