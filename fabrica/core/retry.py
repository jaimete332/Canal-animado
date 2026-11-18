"""Reintentos con backoff exponencial para llamadas a APIs."""
from __future__ import annotations

import functools
import random
import time
from typing import Callable, TypeVar

from .log import get_logger

T = TypeVar("T")
log = get_logger("retry")


class PermanentError(Exception):
    """Error que no merece reintento (clave inválida, petición mal formada...)."""


def retry(tries: int = 4, base: float = 1.5, max_wait: float = 30.0,
          exceptions: tuple[type[BaseException], ...] = (Exception,)) -> Callable:
    def deco(fn: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(fn)
        def wrapper(*a, **kw) -> T:
            for i in range(1, tries + 1):
                try:
                    return fn(*a, **kw)
                except PermanentError:
                    raise
                except exceptions as e:  # noqa: PERF203
                    if i == tries:
                        log.error("%s falló tras %d intentos: %s", fn.__name__, tries, e)
                        raise
                    wait = min(max_wait, base ** i + random.random())
                    log.warning("%s falló (%s). Reintento %d/%d en %.1fs", fn.__name__, e, i, tries - 1, wait)
                    time.sleep(wait)
            raise RuntimeError("unreachable")
        return wrapper
    return deco
