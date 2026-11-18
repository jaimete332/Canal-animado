"""Implementaciones de proveedores de voz.

- kokoro  (local, gratis, neuronal; recomendado sin presupuesto)
- piper   (local, gratis, voz nativa es_ES; más plana)
- edge    (gratis vía Microsoft Edge; es-ES-AlvaroNeural; requiere red a speech.platform.bing.com)
- elevenlabs (de pago, la más natural; da tiempos por carácter)
- openai  (de pago, barato)
- google  (Cloud TTS, voces Chirp3-HD es-ES)
"""
from __future__ import annotations

import base64
import io
import os

import numpy as np
import requests
import soundfile as sf

from ..core.config import ROOT, env
from ..core.log import get_logger
from ..core.retry import PermanentError, retry
from .base import TTSProvider, TTSResult, WordTiming

log = get_logger("tts")


def _abs(p: str) -> str:
    return p if os.path.isabs(p) else str(ROOT / p)


def _decode(data: bytes) -> tuple[np.ndarray, int]:
    try:
        a, sr = sf.read(io.BytesIO(data), dtype="float32")
    except Exception:
        # mp3 -> wav con ffmpeg
        import subprocess
        p = subprocess.run(["ffmpeg", "-v", "error", "-i", "pipe:0", "-f", "wav", "pipe:1"],
                           input=data, capture_output=True, check=True)
        a, sr = sf.read(io.BytesIO(p.stdout), dtype="float32")
    if a.ndim > 1:
        a = a.mean(axis=1)
    return a.astype(np.float32), sr


class KokoroTTS(TTSProvider):
    name = "kokoro"
    _engine = None

    def _get(self):
        if KokoroTTS._engine is None:
            from kokoro_onnx import Kokoro
            KokoroTTS._engine = Kokoro(_abs(self.cfg["model"]), _abs(self.cfg["voices"]))
        return KokoroTTS._engine

    def synthesize(self, text: str) -> TTSResult:
        k = self._get()
        audio, sr = k.create(text, voice=self.cfg.get("voice", "em_alex"),
                             speed=float(self.cfg.get("speed", 1.1)), lang="es")
        return TTSResult(np.asarray(audio, dtype=np.float32), sr, chars=len(text))


class PiperTTS(TTSProvider):
    name = "piper"
    _engine = None

    def _get(self):
        if PiperTTS._engine is None:
            import glob

            import sherpa_onnx
            d = _abs(self.cfg["model_dir"])
            model = glob.glob(os.path.join(d, "*.onnx"))[0]
            conf = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
                vits=sherpa_onnx.OfflineTtsVitsModelConfig(
                    model=model, tokens=os.path.join(d, "tokens.txt"),
                    data_dir=os.path.join(d, "espeak-ng-data")), num_threads=4))
            PiperTTS._engine = sherpa_onnx.OfflineTts(conf)
        return PiperTTS._engine

    def synthesize(self, text: str) -> TTSResult:
        g = self._get().generate(text, sid=0, speed=float(self.cfg.get("speed", 1.0)))
        return TTSResult(np.asarray(g.samples, dtype=np.float32), g.sample_rate, chars=len(text))


class EdgeTTS(TTSProvider):
    name = "edge"
    gives_word_timings = True

    @retry(tries=3)
    def synthesize(self, text: str) -> TTSResult:
        import asyncio

        import edge_tts

        async def run():
            com = edge_tts.Communicate(text, self.cfg.get("voice", "es-ES-AlvaroNeural"),
                                       rate=self.cfg.get("rate", "+0%"), boundary="WordBoundary")
            buf, words = bytearray(), []
            async for ch in com.stream():
                if ch["type"] == "audio":
                    buf += ch["data"]
                elif ch["type"] == "WordBoundary":
                    s = ch["offset"] / 1e7
                    words.append(WordTiming(ch["text"], s, s + ch["duration"] / 1e7))
            return bytes(buf), words

        data, words = asyncio.run(run())
        a, sr = _decode(data)
        return TTSResult(a, sr, words, chars=len(text))


class ElevenLabsTTS(TTSProvider):
    name = "elevenlabs"
    cost_key = "elevenlabs_per_1k_chars"
    gives_word_timings = True

    @retry(tries=3)
    def synthesize(self, text: str) -> TTSResult:
        key = env("ELEVENLABS_API_KEY")
        if not key:
            raise PermanentError("Falta ELEVENLABS_API_KEY")
        vid = self.cfg.get("voice_id") or env("ELEVENLABS_VOICE_ID")
        r = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{vid}/with-timestamps",
            headers={"xi-api-key": key},
            json={"text": text, "model_id": self.cfg.get("model", "eleven_multilingual_v2"),
                  "language_code": "es",
                  "voice_settings": {"stability": 0.4, "similarity_boost": 0.8, "style": 0.35}},
            timeout=120)
        if r.status_code in (401, 403, 422):
            raise PermanentError(r.text)
        r.raise_for_status()
        j = r.json()
        a, sr = _decode(base64.b64decode(j["audio_base64"]))
        al = j.get("alignment") or {}
        words = _chars_to_words(al.get("characters", []), al.get("character_start_times_seconds", []),
                                al.get("character_end_times_seconds", []))
        return TTSResult(a, sr, words, chars=len(text))


class OpenAITTS(TTSProvider):
    name = "openai"
    cost_key = "openai_tts_per_1k_chars"

    @retry(tries=3)
    def synthesize(self, text: str) -> TTSResult:
        key = env("OPENAI_API_KEY")
        if not key:
            raise PermanentError("Falta OPENAI_API_KEY")
        r = requests.post("https://api.openai.com/v1/audio/speech",
                          headers={"Authorization": f"Bearer {key}"},
                          json={"model": self.cfg.get("model", "gpt-4o-mini-tts"),
                                "voice": self.cfg.get("voice", "ash"), "input": text,
                                "instructions": "Narrador español de España, castellano peninsular, "
                                                "enérgico y divertido, ritmo rápido de YouTube Shorts.",
                                "response_format": "wav"}, timeout=120)
        if r.status_code in (401, 403):
            raise PermanentError(r.text)
        r.raise_for_status()
        a, sr = _decode(r.content)
        return TTSResult(a, sr, chars=len(text))


class GoogleTTS(TTSProvider):
    name = "google"
    cost_key = "google_tts_per_1k_chars"

    @retry(tries=3)
    def synthesize(self, text: str) -> TTSResult:
        key = env("GOOGLE_TTS_API_KEY")
        if not key:
            raise PermanentError("Falta GOOGLE_TTS_API_KEY")
        r = requests.post(f"https://texttospeech.googleapis.com/v1/text:synthesize?key={key}",
                          json={"input": {"text": text},
                                "voice": {"languageCode": "es-ES", "name": self.cfg.get("voice")},
                                "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": 24000}},
                          timeout=120)
        if r.status_code in (400, 401, 403):
            raise PermanentError(r.text)
        r.raise_for_status()
        a, sr = _decode(base64.b64decode(r.json()["audioContent"]))
        return TTSResult(a, sr, chars=len(text))


def _chars_to_words(chars, starts, ends) -> list[WordTiming]:
    words, cur, s = [], "", None
    for c, st, en in zip(chars, starts, ends):
        if c.isspace():
            if cur:
                words.append(WordTiming(cur, s, prev_end))
            cur, s = "", None
            continue
        if s is None:
            s = st
        cur += c
        prev_end = en
    if cur:
        words.append(WordTiming(cur, s, prev_end))
    return words


PROVIDERS = {c.name: c for c in (KokoroTTS, PiperTTS, EdgeTTS, ElevenLabsTTS, OpenAITTS, GoogleTTS)}


def get_provider(name: str, tts_cfg: dict) -> TTSProvider:
    if name not in PROVIDERS:
        raise ValueError(f"Proveedor TTS desconocido: {name}. Opciones: {list(PROVIDERS)}")
    return PROVIDERS[name](tts_cfg.get(name, {}))
