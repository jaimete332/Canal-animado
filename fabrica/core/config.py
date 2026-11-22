"""Carga de configuración (config.yaml + variables de entorno/.env)."""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]


def _load_dotenv(path: Path) -> None:
    """Carga .env sin dependencias externas. No sobrescribe variables existentes."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


class Config(dict):
    """dict con acceso por ruta: cfg.get_path('tts.kokoro.voice')."""

    def get_path(self, dotted: str, default: Any = None) -> Any:
        cur: Any = self
        for part in dotted.split("."):
            if not isinstance(cur, dict) or part not in cur:
                return default
            cur = cur[part]
        return cur

    def path(self, dotted: str) -> Path:
        p = Path(self.get_path(dotted))
        return p if p.is_absolute() else ROOT / p


@lru_cache(maxsize=1)
def load_config(path: str | None = None) -> Config:
    _load_dotenv(ROOT / ".env")
    cfg_path = Path(path) if path else ROOT / "config.yaml"
    with open(cfg_path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    fmt = os.environ.get("FABRICA_FORMAT")  # p. ej. "landscape" para vídeos largos 16:9
    if fmt and fmt in (data.get("formats") or {}):
        _merge(data, data["formats"][fmt])
    return Config(data)


def _merge(base: dict, over: dict) -> None:
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _merge(base[k], v)
        else:
            base[k] = v


def env(name: str, default: str | None = None) -> str | None:
    _load_dotenv(ROOT / ".env")
    v = os.environ.get(name, default)
    return v if v else default
