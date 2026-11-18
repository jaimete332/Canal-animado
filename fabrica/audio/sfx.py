"""Efectos de sonido sintetizados por código.

Al generarse matemáticamente son 100 % originales: sin licencias ni reclamaciones de Content ID.
Si prefieres efectos grabados, coloca WAV/MP3 con licencia comercial en assets/sfx/<nombre>.wav
(p. ej. de Pixabay o de la Biblioteca de audio de YouTube) y tendrán prioridad sobre los sintéticos.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.signal import butter, sosfilt

from ..core.config import ROOT

SR = 48000
rng = np.random.default_rng(7)


def _t(d: float) -> np.ndarray:
    return np.arange(int(d * SR)) / SR


def _env(n: int, a: float = 0.005, r: float = 0.2, shape: float = 3.0) -> np.ndarray:
    t = np.arange(n) / SR
    att = np.clip(t / max(a, 1e-4), 0, 1)
    rel = np.exp(-shape * t / max(r, 1e-4))
    return att * rel


def _bp(x, lo, hi, order=2):
    sos = butter(order, [lo, hi], btype="band", fs=SR, output="sos")
    return sosfilt(sos, x)


def _lp(x, f, order=2):
    return sosfilt(butter(order, f, btype="low", fs=SR, output="sos"), x)


def _hp(x, f, order=2):
    return sosfilt(butter(order, f, btype="high", fs=SR, output="sos"), x)


def _norm(x, peak=0.9):
    return (x / (np.abs(x).max() + 1e-9) * peak).astype(np.float32)


def whoosh(d=0.45, up=True):
    n = int(d * SR)
    noise = rng.standard_normal(n)
    out = np.zeros(n)
    seg = 512
    for i in range(0, n, seg):
        p = i / n
        f = 300 + (2600 if up else 2600 * (1 - p)) * (p if up else 1)
        f = 400 + 3000 * np.sin(np.pi * p) ** 2
        out[i:i + seg] = _bp(noise[i:i + seg], max(80, f * 0.6), min(SR / 2 - 100, f * 1.4), 1)
    env = np.sin(np.pi * np.linspace(0, 1, n)) ** 1.5
    return _norm(out * env, 0.7)


def pop(d=0.12, f0=900):
    t = _t(d)
    f = f0 * np.exp(-t * 18) + 200
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(len(t), 0.001, 0.05)
    return _norm(x, 0.8)


def boing(d=0.5):
    t = _t(d)
    f = 220 + 160 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 4)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(len(t), 0.002, 0.3)
    return _norm(x, 0.7)


def dig(d=0.28):
    n = int(d * SR)
    noise = _bp(rng.standard_normal(n), 200, 2500)
    thunk = np.sin(2 * np.pi * 95 * _t(d)) * _env(n, 0.001, 0.06)
    grit = noise * _env(n, 0.002, 0.12) * (1 + 0.6 * (rng.random(n) > 0.97))
    return _norm(thunk * 1.2 + grit, 0.85)


def drill(d=1.6):
    t = _t(d)
    f = 110 + 25 * np.sin(2 * np.pi * 3 * t)
    saw = 2 * ((np.cumsum(f) / SR) % 1) - 1
    buzz = _lp(saw, 1800) + 0.35 * _bp(rng.standard_normal(len(t)), 1500, 6000)
    am = 0.75 + 0.25 * np.sin(2 * np.pi * 28 * t)
    env = np.clip(t / 0.08, 0, 1) * np.clip((d - t) / 0.15, 0, 1)
    return _norm(buzz * am * env, 0.6)


def boom(d=1.3):
    t = _t(d)
    f = 70 * np.exp(-t * 2.5) + 32
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(len(t), 0.003, 0.7, 2.5)
    crack = _lp(rng.standard_normal(len(t)), 900) * _env(len(t), 0.001, 0.25)
    return _norm(sub + 0.6 * crack, 0.95)


def rumble(d=2.0):
    t = _t(d)
    x = _lp(rng.standard_normal(len(t)), 120, 4) * (0.6 + 0.4 * np.sin(2 * np.pi * 5 * t))
    env = np.sin(np.pi * np.linspace(0, 1, len(t)))
    return _norm(x * env, 0.8)


def splash(d=0.9):
    n = int(d * SR)
    x = _bp(rng.standard_normal(n), 300, 7000) * _env(n, 0.004, 0.25, 4)
    bubbles = np.zeros(n)
    for _ in range(14):
        s = rng.integers(int(0.05 * SR), int(0.8 * SR))
        bd = int(0.05 * SR)
        if s + bd >= n:
            continue
        bt = np.arange(bd) / SR
        f = rng.uniform(500, 1400) * (1 + 3 * bt)
        bubbles[s:s + bd] += np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-bt * 60) * 0.3
    return _norm(x + bubbles, 0.85)


def crack(d=0.5):
    n = int(d * SR)
    x = np.zeros(n)
    for i in range(7):
        s = int(rng.uniform(0, 0.35) * SR)
        ln = int(0.02 * SR)
        x[s:s + ln] += _hp(rng.standard_normal(ln), 1500) * np.exp(-np.arange(ln) / SR * 150)
    return _norm(x, 0.8)


def ding(d=1.0, f=1318.5):
    t = _t(d)
    mod = np.sin(2 * np.pi * f * 1.41 * t) * 2.0 * np.exp(-t * 6)
    x = np.sin(2 * np.pi * f * t + mod) * _env(len(t), 0.001, 0.4)
    return _norm(x, 0.55)


def sparkle(d=0.8):
    out = np.zeros(int(d * SR))
    notes = [1568, 1976, 2349, 2637, 3136]
    for i, f in enumerate(notes):
        s = int(i * 0.07 * SR)
        x = ding(0.4, f)
        out[s:s + len(x)] += x[: len(out) - s] * 0.5
    return _norm(out, 0.5)


def tick(d=0.06):
    t = _t(d)
    x = _hp(rng.standard_normal(len(t)), 3000) * _env(len(t), 0.0005, 0.01)
    return _norm(x, 0.6)


def clock(d=1.5, rate=8):
    out = np.zeros(int(d * SR))
    for i in range(int(d * rate)):
        s = int(i / rate * SR)
        x = tick()
        out[s:s + len(x)] += x[: len(out) - s] * (1.0 if i % 2 else 0.6)
    return _norm(out, 0.6)


def sizzle(d=1.2):
    n = int(d * SR)
    x = _hp(rng.standard_normal(n), 2500) * (rng.random(n) > 0.6)
    env = np.clip(np.arange(n) / (0.1 * SR), 0, 1) * np.clip((n - np.arange(n)) / (0.3 * SR), 0, 1)
    return _norm(x * env, 0.4)


def fall(d=1.0):
    t = _t(d)
    f = 1200 * np.exp(-t * 2.2) + 150
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.clip((d - t) / 0.2, 0, 1) * np.clip(t / 0.05, 0, 1)
    return _norm(x, 0.45)


def riser(d=1.2):
    t = _t(d)
    f = 200 * np.exp(t * 2.2)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.4 + _bp(rng.standard_normal(len(t)), 1000, 8000) * 0.4
    return _norm(x * (t / d) ** 2, 0.6)


def hit(d=0.6):
    """Golpe de impacto para el gancho (bombo grave + crash)."""
    t = _t(d)
    kick = np.sin(2 * np.pi * np.cumsum(120 * np.exp(-t * 20) + 45) / SR) * _env(len(t), 0.001, 0.35)
    crash = _hp(rng.standard_normal(len(t)), 4000) * _env(len(t), 0.001, 0.4) * 0.4
    return _norm(kick + crash, 0.95)


def gulp(d=0.35):
    t = _t(d)
    f = 300 + 500 * np.sin(np.pi * t / d)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d)
    return _norm(x, 0.5)


def float_(d=1.6):
    t = _t(d)
    x = sum(np.sin(2 * np.pi * f * t + np.sin(2 * np.pi * 0.7 * t)) for f in (523, 659, 784)) / 3
    return _norm(x * np.sin(np.pi * t / d), 0.35)


LIB = {
    "whoosh": whoosh, "pop": pop, "boing": boing, "dig": dig, "drill": drill, "boom": boom,
    "rumble": rumble, "splash": splash, "crack": crack, "ding": ding, "sparkle": sparkle,
    "tick": tick, "clock": clock, "sizzle": sizzle, "fall": fall, "riser": riser, "hit": hit,
    "gulp": gulp, "float": float_,
}

_cache: dict[str, np.ndarray] = {}


def get(name: str) -> np.ndarray:
    if name in _cache:
        return _cache[name]
    for ext in ("wav", "mp3", "ogg"):
        f = ROOT / "assets" / "sfx" / f"{name}.{ext}"
        if f.exists():
            from ..tts.providers import _decode
            from ..tts.narrator import _resample
            a, sr = _decode(Path(f).read_bytes())
            _cache[name] = _resample(a, sr)
            return _cache[name]
    if name not in LIB:
        raise KeyError(f"SFX desconocido: {name}. Disponibles: {sorted(LIB)}")
    _cache[name] = LIB[name]()
    return _cache[name]
