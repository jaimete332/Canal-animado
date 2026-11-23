"""Genera la narración escena a escena con tiempos por palabra.

Estrategia para máxima sincronía y ritmo:
  * Se sintetiza cada *cláusula* (cortes en , . : ; ? !) por separado.
  * Se recortan los silencios de cada cláusula y se insertan pausas controladas
    (evita silencios innecesarios y da ritmo de Short).
  * Los tiempos por palabra se toman del proveedor si los da; si no, se reparten
    dentro de cada cláusula por sílabas (error típico < 80 ms).
  * Caché por hash: regenerar una escena no vuelve a sintetizar las demás.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

from ..core.config import load_config
from ..core.costs import ledger
from ..core.log import get_logger
from .base import TTSProvider, TTSResult, WordTiming
from .providers import get_provider

log = get_logger("narrator")
SR = 48000
PAUSES = {",": 0.06, ";": 0.12, ":": 0.12, ".": 0.16, "?": 0.2, "!": 0.16, "…": 0.28}
_VOWELS = re.compile(r"[aeiouáéíóúüy]+", re.I)


def normalize_numbers(text: str) -> str:
    """'6.371 km' -> 'seis mil trescientos setenta y uno kilómetros' para el TTS."""
    from .numbers_es import to_words

    def rep(m: re.Match) -> str:
        raw = m.group(0)
        if "," in raw:  # decimal: 3,6 -> tres coma seis
            a, b = raw.replace(".", "").split(",", 1)
            return f"{to_words(int(a))} coma {to_words(int(b))}"
        return to_words(int(raw.replace(".", "")))
    text = re.sub(r"\d+(?:[.,]\d+)*", rep, text)
    return text.replace("km", "kilómetros").replace("°C", "grados")


def syllables(word: str) -> int:
    return max(1, len(_VOWELS.findall(word)))


def split_clauses(text: str) -> list[tuple[str, str]]:
    """Devuelve [(texto_cláusula, puntuación_final)]."""
    parts = re.findall(r"[^,.;:?!…]+[,.;:?!…]*", text)
    out = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        m = re.search(r"[,.;:?!…]+$", p)
        punct = m.group(0)[-1] if m else ""
        out.append((p, punct))
    # une cláusulas muy cortas (1 palabra) con la siguiente para no romper prosodia
    merged: list[tuple[str, str]] = []
    for c, pn in out:
        if merged and len(merged[-1][0].split()) <= 1 and merged[-1][1] == ",":
            merged[-1] = (merged[-1][0] + " " + c, pn)
        else:
            merged.append((c, pn))
    return merged


def trim_silence(a: np.ndarray, sr: int, thr_db: float = -45, pad: float = 0.04) -> tuple[np.ndarray, float]:
    win = int(sr * 0.01)
    if len(a) < win * 3:
        return a, 0.0
    frames = a[: len(a) // win * win].reshape(-1, win)
    rms = 20 * np.log10(np.sqrt((frames ** 2).mean(axis=1)) + 1e-9)
    peak = rms.max()
    voiced = np.where(rms > max(thr_db, peak - 42))[0]
    if len(voiced) == 0:
        return a, 0.0
    s = max(0, voiced[0] * win - int(pad * sr))
    e = min(len(a), (voiced[-1] + 1) * win + int(pad * sr))
    return a[s:e], s / sr


def _resample(a: np.ndarray, sr: int) -> np.ndarray:
    if sr == SR:
        return a
    from math import gcd
    g = gcd(sr, SR)
    return resample_poly(a, SR // g, sr // g).astype(np.float32)


def _distribute(words: list[str], start: float, end: float) -> list[WordTiming]:
    w = np.array([syllables(x) + 0.35 for x in words], dtype=float)
    edges = start + np.concatenate([[0], np.cumsum(w)]) / w.sum() * (end - start)
    return [WordTiming(x, float(edges[i]), float(edges[i + 1])) for i, x in enumerate(words)]


_STRENGTH = {".": 3, "?": 3, "!": 3, "…": 3, ":": 2, ";": 2, ",": 1}


def _align_clip_words(words: list[str], a: np.ndarray, sr: int, start: float, end: float,
                      min_gap: float = 0.09) -> list[WordTiming]:
    """Tiempos por palabra para un clip de voz ya grabado: las pausas reales del audio marcan los signos de
    puntuación (la de mayor peso se empareja con la pausa más larga) y dentro de cada frase las palabras se
    reparten por sílabas. Sin pausas detectables equivale a _distribute."""
    win = int(sr * 0.01)
    i0, i1 = int(start * sr), int(end * sr)
    seg = a[i0:i1]
    n = len(seg) // win
    if n < 10 or len(words) < 2:
        return _distribute(words, start, end)
    db = 20 * np.log10(np.sqrt((seg[: n * win].reshape(n, win) ** 2).mean(axis=1)) + 1e-9)
    silent = db < db.max() - 32
    gaps, j = [], 0
    while j < n:
        if silent[j]:
            k = j
            while k < n and silent[k]:
                k += 1
            if j > 0 and k < n and (k - j) * 0.01 >= min_gap:
                gaps.append((start + j * 0.01, start + k * 0.01))
            j = k
        else:
            j += 1
    bounds = [i for i, w in enumerate(words[:-1]) if w and w[-1] in _STRENGTH]
    k = min(len(bounds), len(gaps))
    if k == 0:
        return _distribute(words, start, end)
    bounds = sorted(sorted(bounds, key=lambda i: (-_STRENGTH[words[i][-1]], i))[:k])
    gaps = sorted(sorted(gaps, key=lambda g: -(g[1] - g[0]))[:k])
    out: list[WordTiming] = []
    first, t_from = 0, start
    for b, (g0, g1) in zip(bounds + [len(words) - 1], gaps + [(end, end)]):
        out += _distribute(words[first: b + 1], t_from, g0)
        first, t_from = b + 1, g1
    return out


class Narrator:
    def __init__(self, cache_dir: Path, provider: str | None = None):
        cfg = load_config()
        self.tts_cfg = cfg["tts"]
        self.name = provider or self.tts_cfg["provider"]
        self.chain = [self.name] + [f for f in self.tts_cfg.get("fallback", []) if f != self.name]
        self.cache = cache_dir
        self.cache.mkdir(parents=True, exist_ok=True)
        self.lexicon: dict[str, str] = self.tts_cfg.get("lexicon", {}) or {}
        self._providers: dict[str, TTSProvider] = {}

    def _prov(self, name: str) -> TTSProvider:
        if name not in self._providers:
            self._providers[name] = get_provider(name, self.tts_cfg)
        return self._providers[name]

    def _spoken(self, text: str) -> str:
        t = normalize_numbers(text)
        for k, v in self.lexicon.items():
            t = re.sub(rf"\b{re.escape(k)}\b", v, t)
        return t

    def _synth(self, text: str, voice: dict | None = None) -> tuple[TTSResult, str]:
        last: Exception | None = None
        for name in self.chain:
            p = self._prov(name)
            vcfg = self.tts_cfg.get(name)
            if voice and name == self.name:
                from .providers import get_provider
                vcfg = {**(vcfg or {}), **voice}
                p = get_provider(name, {**self.tts_cfg, name: vcfg})
            key = hashlib.sha1(json.dumps([name, vcfg, text], sort_keys=True,
                                          ensure_ascii=False).encode()).hexdigest()[:16]
            wav, meta = self.cache / f"{key}.wav", self.cache / f"{key}.json"
            if wav.exists() and meta.exists():
                a, sr = sf.read(wav, dtype="float32")
                words = [WordTiming(**w) for w in json.loads(meta.read_text())["words"]]
                return TTSResult(a, sr, words, len(text)), name
            try:
                ledger().check(p.estimate_cost(text))
                r = p.synthesize(text)
                ledger().add(f"tts:{name}", "chars", p.estimate_cost(text), chars=len(text))
                sf.write(wav, r.audio, r.sr, subtype="FLOAT")
                meta.write_text(json.dumps({"text": text, "words": [asdict(w) for w in r.words]},
                                           ensure_ascii=False))
                return r, name
            except Exception as e:  # pasa al siguiente proveedor
                log.warning("TTS %s falló: %s", name, e)
                last = e
        raise RuntimeError(f"Ningún proveedor TTS funcionó: {last}")

    def narrate_clip(self, text: str, clip: Path, pause_after: float = 0.08) -> tuple[np.ndarray, list[WordTiming]]:
        """Usa la voz de un vídeo real; los subtítulos se reparten sobre la parte con voz."""
        import subprocess
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(clip), "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le",
                              "-"], capture_output=True, check=True).stdout
        a = np.frombuffer(raw, np.float32).copy()
        _, off = trim_silence(a, SR)
        voiced, _ = trim_silence(a[int(off * SR):], SR)
        start, end = off, off + len(voiced) / SR
        words = _align_clip_words(text.split(), a, SR, start + 0.03, end - 0.03)
        a = np.concatenate([a, np.zeros(int(pause_after * SR), np.float32)])
        return (a / (np.abs(a).max() + 1e-9) * 0.89).astype(np.float32), words

    def narrate_scene(self, text: str, pause_after: float = 0.08, voice: dict | None = None
                      ) -> tuple[np.ndarray, list[WordTiming]]:
        chunks: list[np.ndarray] = []
        timings: list[WordTiming] = []
        t = 0.0
        clauses = split_clauses(text)
        for i, (clause, punct) in enumerate(clauses):
            r, used = self._synth(self._spoken(clause), voice)
            a, offset = trim_silence(r.audio, r.sr)
            a = _resample(a, r.sr)
            dur = len(a) / SR
            display_words = clause.split()
            if r.words and len(r.words) == len(display_words):
                ws = [WordTiming(dw, t + max(0, w.start - offset), t + min(dur, w.end - offset))
                      for dw, w in zip(display_words, r.words)]
            else:
                ws = _distribute(display_words, t + 0.03, t + dur - 0.03)
            timings += ws
            chunks.append(a)
            t += dur
            if i < len(clauses) - 1:
                gap = PAUSES.get(punct, 0.05)
                chunks.append(np.zeros(int(gap * SR), np.float32))
                t += gap
        chunks.append(np.zeros(int(pause_after * SR), np.float32))
        audio = np.concatenate(chunks)
        # normaliza pico a -1 dBFS por escena
        audio = audio / (np.abs(audio).max() + 1e-9) * 0.89
        return audio.astype(np.float32), timings
