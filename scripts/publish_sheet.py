"""Deja el vídeo terminado en PARA_SUBIR/<NN>_<slug>/ (vídeo, miniatura, PUBLICAR.md y textos.txt).
Uso: python3 scripts/publish_sheet.py <slug> [<slug> ...]   (equivale a `python -m fabrica deliver`)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fabrica.publish.delivery import deliver  # noqa: E402

for slug in sys.argv[1:]:
    print("✓", deliver(slug))
