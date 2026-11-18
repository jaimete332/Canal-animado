"""Control de costes por vídeo. Cada proveedor registra aquí su gasto."""
from __future__ import annotations

import json
import threading
from dataclasses import dataclass, field
from pathlib import Path

from .config import load_config
from .log import get_logger

log = get_logger("costs")


class BudgetExceeded(RuntimeError):
    pass


@dataclass
class CostLedger:
    limit_usd: float
    entries: list[dict] = field(default_factory=list)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    @property
    def total(self) -> float:
        return round(sum(e["usd"] for e in self.entries), 5)

    def add(self, provider: str, item: str, usd: float, **meta) -> None:
        with self._lock:
            self.entries.append({"provider": provider, "item": item, "usd": round(usd, 5), **meta})
            if usd:
                log.info("Coste +%.4f USD (%s/%s) — total %.4f", usd, provider, item, self.total)
            if self.total > self.limit_usd:
                raise BudgetExceeded(f"Presupuesto superado: {self.total:.3f} > {self.limit_usd} USD")

    def check(self, upcoming_usd: float) -> None:
        if self.total + upcoming_usd > self.limit_usd:
            raise BudgetExceeded(f"La operación ({upcoming_usd:.3f} USD) superaría el presupuesto")

    def save(self, path: Path) -> None:
        path.write_text(json.dumps({"total_usd": self.total, "limit_usd": self.limit_usd,
                                    "entries": self.entries}, indent=2, ensure_ascii=False))


_current: CostLedger | None = None


def ledger() -> CostLedger:
    global _current
    if _current is None:
        _current = CostLedger(float(load_config().get_path("budget.max_usd_per_video", 1.5)))
    return _current


def reset_ledger() -> CostLedger:
    global _current
    _current = None
    return ledger()


def price(key: str) -> float:
    return float(load_config().get_path(f"budget.prices.{key}", 0.0))
