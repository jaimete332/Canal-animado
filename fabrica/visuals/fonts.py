"""Registra las fuentes del proyecto en fontconfig (Cairo y libass las usan por nombre)."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from ..core.config import ROOT

FONT_DIR = ROOT / "assets" / "fonts"


def ensure_fonts() -> None:
    dest = Path.home() / ".local" / "share" / "fonts"
    dest.mkdir(parents=True, exist_ok=True)
    changed = False
    for f in FONT_DIR.glob("*.ttf"):
        if not (dest / f.name).exists():
            shutil.copy(f, dest / f.name)
            changed = True
    if changed:
        subprocess.run(["fc-cache", "-f"], capture_output=True)
