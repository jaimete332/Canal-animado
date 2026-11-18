"""Generador de música de fondo procedural (original, libre de derechos).

Produce un loop alegre/aventurero con estructura: intro → groove → tensión → clímax → final,
alineado con los beats del guion. Alternativa: `audio.music: library` usa pistas con licencia
comercial que pongas en assets/music/ (con su licencia en assets/music/LICENSES.md).
"""
from __future__ import annotations

import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000
rng = np.random.default_rng(3)

MOODS = {
    # tonalidad base (Hz de la tónica), progresión en grados, bpm
    "adventure": {"root": 146.83, "prog": [0, 5, 3, 4], "bpm": 112, "scale": [0, 2, 4, 5, 7, 9, 11]},
    "mystery": {"root": 130.81, "prog": [0, 8, 5, 7], "bpm": 100, "scale": [0, 2, 3, 5, 7, 8, 10]},
    "epic": {"root": 110.0, "prog": [0, 8, 3, 10], "bpm": 120, "scale": [0, 2, 3, 5, 7, 8, 10]},
    "funny": {"root": 174.61, "prog": [0, 3, 4, 0], "bpm": 124, "scale": [0, 2, 4, 5, 7, 9, 11]},
}


def _lp(x, f):
    return sosfilt(butter(2, f, btype="low", fs=SR, output="sos"), x)


def _hp(x, f):
    return sosfilt(butter(2, f, btype="high", fs=SR, output="sos"), x)


def _adsr(n, a=0.005, d=0.1, s=0.6, r=0.1):
    t = np.arange(n) / SR
    dur = n / SR
    env = np.where(t < a, t / a, np.where(t < a + d, 1 - (1 - s) * (t - a) / d, s))
    rel = np.clip((dur - t) / r, 0, 1)
    return env * rel


def _chord_freqs(root, degree, scale):
    """Tríada sobre el grado (semitonos desde la tónica)."""
    base = root * 2 ** (degree / 12)
    third = 4 if degree in (0, 5, 7) else 3
    return [base, base * 2 ** (third / 12), base * 2 ** (7 / 12)]


def kick(n):
    t = np.arange(n) / SR
    f = 50 + 110 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)


def snare(n):
    t = np.arange(n) / SR
    noise = _hp(rng.standard_normal(n), 1200) * np.exp(-t * 22)
    tone = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30)
    return noise * 0.7 + tone * 0.4


def hat(n, open_=False):
    t = np.arange(n) / SR
    return _hp(rng.standard_normal(n), 7000) * np.exp(-t * (12 if open_ else 60))


def pluck(f, n):
    t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * k * t) / k ** 1.6 for k in range(1, 6))
    return x * np.exp(-t * 7)


def bass(f, n):
    t = np.arange(n) / SR
    saw = 2 * ((f * t) % 1) - 1
    return _lp(saw, 500) * _adsr(n, 0.004, 0.08, 0.7, 0.05)


def pad(freqs, n):
    t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * t + 0.3 * np.sin(2 * np.pi * 0.3 * t)) +
            0.5 * np.sin(2 * np.pi * f * 2.003 * t) for f in freqs)
    return x * _adsr(n, 0.25, 0.3, 0.8, 0.4) / len(freqs)


def compose(duration: float, mood: str = "adventure", sections: list[tuple[float, str]] | None = None) -> np.ndarray:
    """sections: [(t_inicio, 'intro'|'groove'|'tension'|'climax'|'outro')]"""
    m = MOODS.get(mood, MOODS["adventure"])
    bpm, root, prog, scale = m["bpm"], m["root"], m["prog"], m["scale"]
    beat = 60 / bpm
    bar = beat * 4
    total = int((duration + 2) * SR)
    drums = np.zeros(total)
    bassl = np.zeros(total)
    keys = np.zeros(total)
    pads = np.zeros(total)
    sections = sections or [(0, "groove")]

    def section_at(t):
        cur = sections[0][1]
        for s, name in sections:
            if t >= s:
                cur = name
        return cur

    nbars = int(duration / bar) + 2
    melody_seed = np.random.default_rng(11)
    for b in range(nbars):
        t0 = b * bar
        sec = section_at(t0)
        deg = prog[b % len(prog)]
        chord = _chord_freqs(root, deg, scale)
        i0 = int(t0 * SR)
        # pad
        n = int(bar * SR)
        if i0 + n <= total:
            pads[i0:i0 + n] += pad([c * 2 for c in chord], n) * (0.5 if sec in ("intro", "outro") else 0.35)
        for s in range(16):  # semicorcheas
            ts = t0 + s * beat / 4
            i = int(ts * SR)
            if i >= total - SR:
                break
            # batería
            if sec != "intro":
                if s in (0, 8) or (sec == "climax" and s in (0, 4, 8, 12)) or (s == 10 and b % 2):
                    k = kick(int(0.35 * SR)); drums[i:i + len(k)] += k * 0.9
                if s in (4, 12):
                    sn = snare(int(0.25 * SR)); drums[i:i + len(sn)] += sn * 0.45
                if s % 2 == 0 or sec == "climax":
                    h = hat(int(0.08 * SR), open_=(s == 14)); drums[i:i + len(h)] += h * (0.16 if s % 4 else 0.22)
            elif s in (0,):
                k = kick(int(0.35 * SR)); drums[i:i + len(k)] += k * 0.5
            # bajo: corcheas con octava
            if s % 2 == 0 and sec != "intro":
                f = chord[0] / 2 * (2 if s in (6, 14) else 1)
                bl = bass(f, int(beat / 2 * SR * 0.9)); bassl[i:i + len(bl)] += bl * 0.5
            # arpegio pluck
            if sec in ("groove", "climax", "tension") and s % 2 == 0:
                if melody_seed.random() < (0.8 if sec == "climax" else 0.55):
                    idx = melody_seed.integers(0, 3)
                    f = chord[idx] * (4 if sec == "climax" else 2)
                    if sec == "tension":
                        f *= 2 ** (melody_seed.choice([0, 1]) / 12)
                    p = pluck(f, int(0.4 * SR)); keys[i:i + len(p)] += p * 0.22
    mix = drums * 0.8 + bassl + keys + pads * 0.6
    mix = np.tanh(mix * 1.2)  # saturación suave / glue
    mix = mix[: int(duration * SR)]
    # fundido de salida
    fo = int(1.2 * SR)
    mix[-fo:] *= np.linspace(1, 0, fo) ** 2
    return (mix / (np.abs(mix).max() + 1e-9) * 0.8).astype(np.float32)
