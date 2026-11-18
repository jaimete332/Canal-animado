"""Mezcla final: narración + música con ducking + efectos. Normaliza a -14 LUFS (YouTube)."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.ndimage import maximum_filter1d, uniform_filter1d

from . import sfx as sfxlib

SR = 48000


def db(x: float) -> float:
    return 10 ** (x / 20)


@dataclass
class Cue:
    name: str
    t: float
    gain_db: float = 0.0


def voice_activity(voice: np.ndarray, win: float = 0.05) -> np.ndarray:
    env = np.sqrt(uniform_filter1d(voice.astype(np.float64) ** 2, int(win * SR)))
    act = (env > 0.02).astype(np.float64)
    act = maximum_filter1d(act, int(0.25 * SR))           # mantiene el ducking en micro-pausas
    return uniform_filter1d(act, int(0.15 * SR))          # suaviza ataque/relajación


def mix(voice: np.ndarray, music: np.ndarray | None, cues: list[Cue], music_gain_db=-20.0,
        duck_db=-9.0, sfx_gain_db=-9.0, target_lufs=-14.0) -> tuple[np.ndarray, dict]:
    n = len(voice)
    out = voice.astype(np.float64).copy()
    stems = {"voice": voice.copy()}
    if music is not None:
        m = np.zeros(n)
        m[: min(n, len(music))] = music[:n]
        act = voice_activity(voice)
        gain = db(music_gain_db) * (1 - act * (1 - db(duck_db)))
        mus = m * gain
        out += mus
        stems["music"] = mus.astype(np.float32)
    fx = np.zeros(n)
    for c in cues:
        s = sfxlib.get(c.name)
        i = int(c.t * SR)
        if i >= n or i < 0:
            continue
        e = min(n, i + len(s))
        fx[i:e] += s[: e - i] * db(sfx_gain_db + c.gain_db)
    out += fx
    stems["sfx"] = fx.astype(np.float32)
    # loudness
    try:
        import pyloudnorm as pyln
        meter = pyln.Meter(SR)
        lufs = meter.integrated_loudness(out)
        out *= db(target_lufs - lufs)
        stems_gain = db(target_lufs - lufs)
    except Exception:
        lufs, stems_gain = None, 1.0
    # limitador simple (true-peak aprox -1 dBFS)
    peak_lim = db(-1.0)
    env = maximum_filter1d(np.abs(out), int(0.005 * SR))
    env = uniform_filter1d(env, int(0.01 * SR))
    g = np.minimum(1.0, peak_lim / (env + 1e-9))
    out *= g
    for k in stems:
        stems[k] = (stems[k] * stems_gain).astype(np.float32)
    return out.astype(np.float32), {"input_lufs": lufs, "stems": stems}
