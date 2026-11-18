"""Estructura de carpetas de cada vídeo (archivos intermedios reutilizables)."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .config import load_config


@dataclass
class VideoPaths:
    slug: str

    @property
    def root(self) -> Path:
        return load_config().path("paths.output") / self.slug

    def _d(self, name: str) -> Path:
        p = self.root / name
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def script(self) -> Path: return self.root / "script.json"
    @property
    def timeline(self) -> Path: return self.root / "timeline.json"
    @property
    def audio(self) -> Path: return self._d("audio")
    @property
    def scenes(self) -> Path: return self._d("scenes")
    @property
    def images(self) -> Path: return self._d("images")
    @property
    def qa(self) -> Path: return self._d("qa")
    @property
    def final(self) -> Path: return self.root / "final.mp4"
    @property
    def captions(self) -> Path: return self.root / "captions.ass"
    @property
    def metadata(self) -> Path: return self.root / "metadata.json"
    @property
    def thumbnail(self) -> Path: return self.root / "thumbnail.png"
    @property
    def costs(self) -> Path: return self.root / "costs.json"
    @property
    def log(self) -> Path: return self.root / "build.log"
