"""Interfaz común de proveedores de voz. Cambiar de proveedor = cambiar `tts.provider` en config."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import numpy as np


@dataclass
class WordTiming:
    word: str
    start: float
    end: float


@dataclass
class TTSResult:
    audio: np.ndarray            # float32 mono
    sr: int
    words: list[WordTiming] = field(default_factory=list)   # vacío si el proveedor no da tiempos
    chars: int = 0

    @property
    def duration(self) -> float:
        return len(self.audio) / self.sr


class TTSProvider(ABC):
    name = "base"
    cost_key: str | None = None        # clave de budget.prices (USD por 1k caracteres)
    gives_word_timings = False

    def __init__(self, cfg: dict):
        self.cfg = cfg

    @abstractmethod
    def synthesize(self, text: str) -> TTSResult: ...

    def estimate_cost(self, text: str) -> float:
        from ..core.costs import price
        return price(self.cost_key) * len(text) / 1000 if self.cost_key else 0.0
