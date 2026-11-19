"""Banco de ideas + evaluación de potencial + anti-duplicados.

Puntuación heurística (0-100) basada en patrones que suelen retener en Shorts:
  - protagonista en 2ª persona ("tú")         - peligro/supervivencia
  - escala extrema (centro, 100 días, todos)  - mezcla ciencia + fantasía
  - visual (fácil de dibujar = más dinámico)  - novedad respecto a lo ya publicado
Si hay LLM, se generan ideas nuevas y se puntúan también con el LLM.
Si hay métricas de YouTube, la categoría con mejor retención recibe un bonus.
"""
from __future__ import annotations

import random

from ..core.log import get_logger
from ..core.registry import Registry, similarity
from ..llm.client import NoLLMAvailable, complete

log = get_logger("ideas")

SEED_IDEAS = [
    ("¿Qué pasaría si cavaras un agujero hasta el centro de la Tierra?", "ciencia"),
    ("¿Qué pasaría si vivieras 100 días en Marte?", "espacio"),
    ("¿Qué pasaría si te quedaras atrapado en mitad del océano?", "supervivencia"),
    ("¿Qué pasaría si fueras inmortal?", "fantasía"),
    ("¿Qué pasaría si todos los humanos desaparecieran?", "ciencia"),
    ("¿Qué pasaría si te despertaras en la Edad Media?", "historia"),
    ("¿Qué pasaría si fueras millonario de la noche a la mañana?", "vida"),
    ("¿Qué pasaría si te convirtieras en el jefe de la mafia?", "vida"),
    ("¿Qué pasaría si cayeras en un agujero negro?", "espacio"),
    ("¿Qué pasaría si no durmieras durante una semana?", "cuerpo"),
    ("¿Qué pasaría si la Luna desapareciera?", "espacio"),
    ("¿Qué pasaría si vivieras en la Antártida un año?", "supervivencia"),
    ("¿Qué pasaría si encogieras al tamaño de una hormiga?", "fantasía"),
    ("¿Qué pasaría si sobrevivieras a la extinción de los dinosaurios?", "historia"),
    ("¿Qué pasaría si bebieras solo agua de mar?", "cuerpo"),
    ("¿Qué pasaría si te tragara una ballena?", "supervivencia"),
    ("¿Qué pasaría si viajaras a la velocidad de la luz?", "espacio"),
    ("¿Qué pasaría si la Tierra dejara de girar?", "ciencia"),
    ("¿Qué pasaría si vivieras en la Estación Espacial un año?", "espacio"),
    ("¿Qué pasaría si te perdieras en el desierto del Sáhara?", "supervivencia"),
    ("¿Qué pasaría si fueras el último humano en la Tierra?", "fantasía"),
    ("¿Qué pasaría si bajaras a la Fosa de las Marianas?", "ciencia"),
    ("¿Qué pasaría si te quedaras encerrado en un supermercado un mes?", "vida"),
    ("¿Qué pasaría si fueras un gladiador en la antigua Roma?", "historia"),
    ("¿Qué pasaría si caminaras alrededor del mundo?", "vida"),
    ("¿Qué pasaría si un asteroide fuera a chocar mañana?", "espacio"),
    ("¿Qué pasaría si dejaras de comer azúcar un mes?", "cuerpo"),
    ("¿Qué pasaría si vivieras dentro de un volcán?", "ciencia"),
    ("¿Qué pasaría si fueras pirata en el siglo XVII?", "historia"),
    ("¿Qué pasaría si pudieras leer la mente?", "fantasía"),
]

HOOK_WORDS = {
    "danger": ["sobreviv", "atrapado", "agujero negro", "tragara", "volcán", "asteroide", "perdieras", "cayeras", "gladiador", "pirata"],
    "scale": ["centro", "todos", "100 días", "año", "velocidad de la luz", "último", "mundo", "inmortal", "fosa"],
    "visual": ["marte", "océano", "luna", "dinosaurio", "ballena", "hormiga", "volcán", "edad media", "espacial", "desierto", "roma"],
    "science": ["tierra", "marte", "luz", "luna", "agujero", "fosa", "girar", "agua de mar", "dormir", "durmieras", "azúcar"],
}


def heuristic_score(idea: str, published: list[str], category_bonus: dict[str, float] | None = None,
                    category: str = "") -> float:
    i = idea.lower()
    s = 40.0
    s += 6 if " te " in f" {i} " or "fueras" in i or "vivieras" in i else 0
    for k, w in (("danger", 12), ("scale", 9), ("visual", 10), ("science", 8)):
        if any(x in i for x in HOOK_WORDS[k]):
            s += w
    s -= 4 if len(idea) > 70 else 0
    max_sim = max((similarity(idea, p) for p in published), default=0)
    s -= 60 * max_sim
    s += (category_bonus or {}).get(category, 0)
    return max(0.0, min(100.0, s))


def _category_bonus() -> dict[str, float]:
    """Usa métricas reales: categorías con mejor % visto reciben hasta +10."""
    try:
        rows = Registry().latest_metrics()
    except Exception:
        return {}
    by: dict[str, list[float]] = {}
    for r in rows:
        if r["avg_view_pct"] is not None:
            by.setdefault(r["category"], []).append(r["avg_view_pct"])
    if not by:
        return {}
    avg = {k: sum(v) / len(v) for k, v in by.items()}
    best = max(avg.values())
    return {k: 10 * v / best for k, v in avg.items()}


def llm_ideas(n: int, published: list[str]) -> list[tuple[str, str]]:
    try:
        r = complete(
            "Eres guionista jefe de un canal de YouTube Shorts animados en español de España del tipo "
            "'¿Qué pasaría si...?'. Respondes solo JSON.",
            f"Propón {n} ideas originales y muy visuales (mezcla ciencia, historia, supervivencia y humor). "
            f"Evita estas ya publicadas: {published[:50]}. Formato: {{\"ideas\":[{{\"idea\":\"¿Qué pasaría si...?\","
            "\"category\":\"ciencia|espacio|historia|supervivencia|cuerpo|vida|fantasía\"}]}", temperature=1.0)
        return [(x["idea"], x.get("category", "")) for x in r.get("ideas", [])]
    except NoLLMAvailable:
        return []
    except Exception as e:
        log.warning("Ideas por LLM fallaron: %s", e)
        return []


def _niche_bonus(idea: str) -> float:
    """+8 si la idea toca un tema que la investigación del nicho marca como de más tirón."""
    from ..research.niche import TOPICS, _norm, style_guide
    g = style_guide()
    if not g:
        return 0.0
    i = _norm(idea)
    for rank, topic in enumerate(g.get("preferred_topics", [])):
        if any(w in i for w in TOPICS.get(topic, "").split()):
            return 8.0 - rank * 1.5
    return 0.0


def ranked_ideas(n: int = 15) -> list[tuple[float, str]]:
    reg = Registry()
    published = [r["idea"] for r in reg.videos()]
    bonus = _category_bonus()
    pool = SEED_IDEAS + llm_ideas(12, published)
    scored = []
    for idea, cat in pool:
        if reg.is_duplicate(idea):
            continue
        scored.append((round(min(100, heuristic_score(idea, published, bonus, cat) + _niche_bonus(idea)), 1), idea))
    scored.sort(reverse=True)
    return scored[:n]


def pick_idea() -> str:
    top = ranked_ideas(5)
    if not top:
        raise RuntimeError("No quedan ideas nuevas: añade más a SEED_IDEAS o configura un LLM")
    # algo de variedad entre las 3 mejores
    return random.choice(top[:3])[1]
