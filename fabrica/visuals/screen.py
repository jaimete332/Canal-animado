"""Tamaño de la pantalla de salida (vertical 1080×1920 para Shorts, horizontal 1920×1080 para vídeos largos).

Los fondos se siguen diseñando en el lienzo vertical de world.W×world.H; en horizontal, scene.py muestra una
franja de ese lienzo ampliada (ver `bg_window`). Personaje, props, rótulos y subtítulos se dibujan en pantalla.
El formato se elige con FABRICA_FORMAT=landscape o con "format": "landscape" en los metadatos del guion.
"""
from ..core.config import load_config

_v = load_config()["video"]
SW, SH = int(_v["width"]), int(_v["height"])
LANDSCAPE = SW > SH
