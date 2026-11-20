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


def _deep_merge(base: dict, over: dict) -> dict:
    """Fusiona `over` sobre `base`. Un dict con `_replace: true` sustituye al original en vez de fusionarse."""
    out = dict(base)
    for k, v in over.items():
        if isinstance(v, dict) and v.get("_replace"):
            out[k] = {kk: vv for kk, vv in v.items() if kk != "_replace"}
        elif isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def active_channel() -> str:
    """Perfil de canal activo: FABRICA_CHANNEL (o `--channel` en la CLI). Vacío = canal principal (config.yaml)."""
    return os.environ.get("FABRICA_CHANNEL", "").strip()


def channel_file(name: str) -> Path:
    return ROOT / "channels" / f"{name}.yaml"


@lru_cache(maxsize=4)
def _load(path: str | None, channel: str) -> Config:
    _load_dotenv(ROOT / ".env")
    cfg_path = Path(path) if path else ROOT / "config.yaml"
    with open(cfg_path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if channel:
        cf = channel_file(channel)
        if not cf.exists():
            raise FileNotFoundError(f"No existe el perfil de canal {cf}")
        over = yaml.safe_load(cf.read_text(encoding="utf-8")) or {}
        data = _deep_merge(data, over)
    data.setdefault("channel", {}).setdefault("engine", "leo")
    data["channel"]["profile"] = channel or "main"
    return Config(data)


def load_config(path: str | None = None) -> Config:
    """config.yaml fusionado con channels/<FABRICA_CHANNEL>.yaml si hay un perfil activo."""
    return _load(path, active_channel())


load_config.cache_clear = _load.cache_clear  # type: ignore[attr-defined]


def lang() -> str:
    """Idioma corto del canal activo: 'es' o 'en'."""
    return str(load_config()["channel"].get("language", "es-ES")).split("-")[0].lower()


def env(name: str, default: str | None = None) -> str | None:
    _load_dotenv(ROOT / ".env")
    v = os.environ.get(name, default)
    return v if v else default
