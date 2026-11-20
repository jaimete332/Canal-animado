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

from ..core.config import ROOT, lang, load_config


def _pending() -> Path:
    """Carpeta de entrega del canal activo (PARA_SUBIR/ en el canal principal, TO_UPLOAD/ en el inglés)."""
    return ROOT / load_config().get_path("paths.deliver", "PARA_SUBIR")


def _archive() -> Path:
    return ROOT / load_config().get_path("paths.archive", "samples")


# nombres de archivo en la carpeta de entrega, por idioma
NAMES = {
    "es": {"thumb": "miniatura.png", "thumb169": "miniatura_16x9.png", "sheet": "PUBLICAR.md", "plain": "textos.txt",
           "report": "extra/informe_calidad.md", "contact": "extra/hoja_de_contactos.jpg"},
    "en": {"thumb": "thumbnail.png", "thumb169": "thumbnail_16x9.png", "sheet": "PUBLISH.md", "plain": "texts.txt",
           "report": "extra/qa_report.md", "contact": "extra/contact_sheet.jpg"},
}


def find(slug: str) -> Path | None:
    """Carpeta de entrega de `slug`: PARA_SUBIR/<NN>_<slug>/ o, si ya se archivó, samples/<slug>/."""
    for d in sorted(_pending().glob(f"*_{slug}")) + [_pending() / slug]:
        if d.is_dir():
            return d
    d = _archive() / slug
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
    for f in sorted(list(_pending().glob("*/extra/metadata.json")) + list(_archive().glob("*/metadata.json"))):
        try:
            out.append(json.loads(f.read_text(encoding="utf-8")).get("title", ""))
        except (OSError, ValueError):
            pass
    return [t for t in out if t]


def _next_number() -> int:
    nums = [int(m.group(1)) for d in _pending().glob("*_*") if (m := re.match(r"(\d+)_", d.name))]
    return max(nums, default=0) + 1


def sheet(m: dict) -> str:
    return f"""# Publicar: «{m['title']}»

**Vídeo:** `{m['_slug']}.mp4` ({m['duration_s']:.1f} s) · **Miniatura:** `miniatura.png` (1080×1920)

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


def sheet_en(m: dict) -> str:
    chapters = ""
    if m.get("chapters"):
        chapters = "\n## Chapters (already inside the description)\n" + "\n".join(
            f"* {c['time']} {c['title']}" for c in m["chapters"]) + "\n"
    mins = int(m["duration_s"] // 60)
    return f"""# Publish: "{m['title']}"

**Video:** `{m['_slug']}.mp4` ({mins} min {m['duration_s'] - mins * 60:.0f} s, 1920×1080) · **Thumbnail:** `thumbnail.png` (1280×720)
**Subtitles:** `captions.srt` (YouTube Studio → Subtitles → Add → Upload file → *With timing*)

## Title ({len(m['title'])} characters)
```
{m['title']}
```

## Description
```
{m['description']}
```
{chapters}
## Tags (YouTube Studio → Show more → Tags)
```
{', '.join(m['tags'])}
```

## Pinned comment
```
{m['pinned_comment']}
```

## Settings
* Category: Education · Video language: English (United States) · Not made for kids
* "Altered or synthetic content": **Yes** (synthetic voice)
* Upload `captions.srt` as English subtitles · Add an end screen (last 20 s) pointing to another video
* Thumbnail test: if `thumbnail_2.png` exists, use YouTube's *Test & compare* with both thumbnails
"""


def plain_en(m: dict) -> str:
    return (f"TITLE\n{m['title']}\n\nDESCRIPTION\n{m['description']}\n\nTAGS\n{', '.join(m['tags'])}\n\n"
            f"PINNED COMMENT\n{m['pinned_comment']}\n\nSETTINGS\nCategory: Education · Language: English · "
            "Not made for kids · Altered or synthetic content: Yes (synthetic voice) · Upload captions.srt\n")


def plain(m: dict) -> str:
    return (f"TÍTULO\n{m['title']}\n\nDESCRIPCIÓN\n{m['description']}\n\nETIQUETAS\n{', '.join(m['tags'])}\n\n"
            f"COMENTARIO FIJADO\n{m['pinned_comment']}\n\nAJUSTES\nCategoría: Educación · Idioma: español (España) · "
            "No es contenido para niños · Contenido alterado o sintético: Sí (voz sintética)\n")


def deliver(slug: str, src: Path | None = None) -> Path:
    """Copia el vídeo terminado (output/<slug>/ por defecto) a la carpeta de entrega del canal (<NN>_<slug>/)."""
    src = src or load_config().path("paths.output") / slug
    pending = _pending()
    d = find(slug)
    if d is None or d.parent != pending:
        d = pending / f"{_next_number():02d}_{slug}"
    (d / "extra").mkdir(parents=True, exist_ok=True)
    n = NAMES.get(lang(), NAMES["es"])
    copies = {"final.mp4": f"{slug}.mp4", "thumbnail.png": n["thumb"], "thumbnail_16x9.png": n["thumb169"],
              "captions.srt": "captions.srt", "metadata.json": "extra/metadata.json", "qa/report.md": n["report"],
              "qa/contact_sheet.jpg": n["contact"]}
    for f in sorted(src.glob("thumbnail_[0-9]*.png")):   # alternativas para «Probar y comparar» de YouTube
        copies[f.name] = f"{n['thumb'].split('.')[0]}_{f.stem.split('_')[-1]}.png"
    for a, b in copies.items():
        if (src / a).exists():
            shutil.copy(src / a, d / b)
    m = json.loads((d / "extra/metadata.json").read_text(encoding="utf-8"))
    m["_slug"] = slug
    en = lang() == "en"
    (d / n["sheet"]).write_text(sheet_en(m) if en else sheet(m), encoding="utf-8")
    (d / n["plain"]).write_text(plain_en(m) if en else plain(m), encoding="utf-8")
    return d


def archive(slug: str) -> Path:
    """Vídeo ya publicado: mueve <entrega>/<NN>_<slug>/ al archivo (<archivo>/<slug>/)."""
    d = find(slug)
    if d is None or d.parent != _pending():
        raise FileNotFoundError(f"'{slug}' no está en {_pending().name}/")
    dst = _archive() / slug
    if dst.exists():
        shutil.rmtree(dst)
    shutil.move(str(d), str(dst))
    return dst
