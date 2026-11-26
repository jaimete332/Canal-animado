"""Banco de ideas + evaluación de potencial + anti-duplicados.

Puntuación heurística (0-100) basada en patrones que suelen retener en Shorts:
  - protagonista en 2ª persona ("tú")         - peligro/supervivencia
  - escala extrema (centro, 100 días, todos)  - mezcla ciencia + fantasía
  - visual (fácil de dibujar = más dinámico)  - novedad respecto a lo ya publicado
Si hay LLM, se generan ideas nuevas y se puntúan también con el LLM.
Si hay métricas de YouTube, la categoría con mejor retención recibe un bonus.
Lo que funciona en el propio canal (data/research/own_winners.json → arquetipos de premisa) suma hasta +8.
"""
from __future__ import annotations

import random
import re

from ..core.log import get_logger
from ..core.registry import Registry, similarity
from ..llm.client import NoLLMAvailable, complete

log = get_logger("ideas")

# Banco v2 (2026-11-19), basado en data/research/style_guide.json (334 vídeos medidos con la API):
#  - temas por tirón medido: cuerpo humano > historia > tierra / catástrofes > espacio;
#    supervivencia está saturada (solo con giro concreto) y dinero / poder rinde poco.
#  - cifra concreta en la premisa (41-43 % de los top frente a 22-26 % del resto).
#  - situación cotidiana o reconocible llevada al extremo, en 2.ª persona, que permita escalada
#    por niveles (más tiempo, más profundo, más grande) con un número que avanza en pantalla.
#  - agrupadas en series de plantilla fija (los canales que dominan el top trabajan en serie).
#  - no repite los Shorts ya hechos en samples/ ni calca títulos ajenos del informe.
SEED_IDEAS = [
    # Serie «Tu cuerpo al límite» (cuerpo humano: el tema más estable en ambas pasadas)
    ("¿Qué le pasaría a tu cuerpo si respiraras ceniza de volcán 1 año?", "cuerpo"),
    ("¿Qué pasaría si no bebieras agua en 7 días?", "cuerpo"),
    ("¿Qué pasaría si aguantaras la respiración 10 minutos?", "cuerpo"),
    ("¿Qué pasaría si bebieras 6 litros de agua de golpe?", "cuerpo"),
    ("¿Qué pasaría si comieras solo comida rápida 30 días?", "cuerpo"),
    ("¿Qué pasaría si subieras al Everest sin oxígeno?", "cuerpo"),
    ("¿Qué pasaría si te cayera un rayo?", "cuerpo"),
    ("¿Qué pasaría si no te cortaras el pelo ni las uñas en 10 años?", "cuerpo"),
    ("¿Qué pasaría si estuvieras 1 hora en agua a 0 grados?", "cuerpo"),
    ("¿Qué pasa dentro de tu cuerpo si te pica una avispa?", "cuerpo"),
    ("¿Qué pasaría si no vieras la luz del sol en 1 año?", "cuerpo"),
    # Serie «Viaje a otra época» (historia: mediana más alta a 12 meses)
    ("¿Qué pasaría si vivieras en Pompeya el día de la erupción?", "historia"),
    ("¿Qué pasaría si estuvieras en el Titanic la noche del choque?", "historia"),
    ("¿Qué pasaría si te tocara construir una pirámide en Egipto?", "historia"),
    ("¿Qué pasaría si un médico de hoy viajara al año 1348?", "historia"),
    ("¿Qué pasaría si fueras un vikingo durante 1 año?", "historia"),
    ("¿Qué pasaría si vivieras 6 meses en un castillo asediado?", "historia"),
    ("¿Cómo sería tu vida si Roma nunca hubiera caído?", "historia"),
    ("¿Qué pasaría si fueras un gladiador en la antigua Roma?", "historia"),
    ("¿Qué pasaría si fueras pirata en el siglo XVII?", "historia"),
    # Serie «Planeta al revés» (tierra / catástrofes)
    ("¿Qué pasaría si entraras en el ojo de un huracán?", "ciencia"),
    ("¿Qué pasaría si dejara de llover en todo el mundo 1 año?", "ciencia"),
    ("¿Qué pasaría si el nivel del mar subiera 100 metros?", "ciencia"),
    ("¿Qué pasaría si la Tierra girara 2 veces más rápido?", "ciencia"),
    ("¿Qué pasaría si cayera un meteorito de 1 km en el mar?", "ciencia"),
    ("¿Qué pasaría si todos los volcanes entraran en erupción a la vez?", "ciencia"),
    ("¿Qué pasaría si bajaras 11.000 metros a la Fosa de las Marianas?", "ciencia"),
    ("¿Qué pasaría si vivieras dentro de un volcán?", "ciencia"),
    # Serie «Fuera de la Tierra» (espacio)
    ("¿Qué pasaría si te quitaras el casco en el espacio 15 segundos?", "espacio"),
    ("¿Qué pasaría si cayeras hacia Júpiter?", "espacio"),
    ("¿Qué pasaría si el Sol se apagara 24 horas?", "espacio"),
    ("¿Qué pasaría si vivieras 1 año en la Luna?", "espacio"),
    ("¿Qué pasaría si cayeras en un agujero negro?", "espacio"),
    ("¿Qué pasaría si un asteroide fuera a chocar en 7 días?", "espacio"),
    # Serie «Tu día a día, al extremo» (situaciones cotidianas llevadas al límite)
    ("¿Qué pasaría si cayeras de un avión a 10.000 metros?", "supervivencia"),
    ("¿Qué pasaría si te quedaras encerrado en un ascensor 3 días?", "supervivencia"),
    ("¿Qué pasaría si internet se apagara en todo el mundo 1 semana?", "vida"),
    ("¿Qué pasaría si todos los coches del mundo se pararan 1 día?", "vida"),
    ("¿Qué pasaría si te persiguiera un guepardo 1 minuto?", "supervivencia"),
    ("¿Qué pasaría si los dinosaurios volvieran 24 horas?", "fantasía"),
    ("¿Qué pasaría si te congelaran y despertaras dentro de 100 años?", "fantasía"),
    # Serie «Fórmula ganadora» (2026-11-26): premisa universal + un caso real con nombre y año contado a mitad del
    # vídeo, como en los Shorts que mejor han funcionado (avión, jefe de la mafia, un año sin sol).
    # Caso real orientativo (VERIFICAR con fuentes al escribir el guion):
    ("¿Qué pasaría si saltaras desde la Torre Eiffel?", "supervivencia"),                # Franz Reichelt, 1912
    ("¿Qué pasaría si vivieras 1 año sin dinero?", "vida"),                               # Mark Boyle, 2008
    ("¿Qué pasaría si te encerraran en Alcatraz?", "historia"),                           # fuga de 1962
    ("¿Qué pasaría si fueras espía en la Guerra Fría?", "historia"),                      # espías reales
    ("¿Qué pasaría si te tocara la lotería de 300 millones?", "vida"),                    # ganadores arruinados
    ("¿Qué pasaría si no usaras el móvil 1 año?", "vida"),                                # desintoxicación digital
    ("¿Qué pasaría si fueras presidente del Gobierno un solo día?", "vida"),
    # Series de los atípicos de canales pequeños (decisión 2026-11-26, ver estrategia en style_guide.json).
    # Formato A «comer X cada día» (cuerpo y comida cotidiana). VERIFICAR el efecto con fuentes al escribir el guion:
    ("¿Qué pasa si comes 3 zanahorias al día durante un mes?", "cuerpo"),               # carotenemia: piel anaranjada
    ("¿Qué pasa si bebes agua con limón todas las mañanas?", "cuerpo"),
    ("¿Qué pasa si comes un ajo crudo todos los días?", "cuerpo"),
    ("¿Qué pasa si comes 2 plátanos al día durante 30 días?", "cuerpo"),
    ("¿Qué pasa si comes nueces todos los días durante 1 mes?", "cuerpo"),
    ("¿Qué pasa si tomas 5 cafés al día durante una semana?", "cuerpo"),
    # Formato B «micro-accidentes del cuerpo» (le pasan a cualquiera):
    ("¿Qué pasa si aguantas un estornudo?", "cuerpo"),                                  # caso publicado: garganta desgarrada (BMJ 2018)
    ("¿Qué pasa si te tragas un chicle?", "cuerpo"),                                    # mito de los 7 años
    ("¿Qué pasa si te tragas una pila de botón?", "cuerpo"),
    ("¿Qué pasa si te pisas un clavo oxidado?", "cuerpo"),                              # tétanos
    ("¿Qué pasa si te quedas dormido con las lentillas puestas?", "cuerpo"),
    ("¿Qué pasa si te pega el hipo y no se te quita en años?", "cuerpo"),               # Charles Osborne, 1922-1990
]

# Shorts ya producidos (PARA_SUBIR/ y samples/): cuentan como publicados para no repetirlos
# aunque el registro local esté vacío (p. ej. en una máquina nueva).
def _already_made() -> list[str]:
    from ..publish.delivery import all_titles
    return [t for t in all_titles() if t.startswith("¿")]


HOOK_WORDS = {
    "danger": ["atrapado", "encerrado", "agujero negro", "rayo", "volcán", "meteorito", "asteroide", "huracán",
               "cayeras", "casco", "gladiador", "pirata", "titanic", "pompeya", "guepardo", "asediado",
               "saltaras", "encerraran", "guerra fría", "cárcel", "alcatraz"],
    "scale": ["centro", "todos", "todo el mundo", "año", "siglo", "a la vez", "más rápido", "nunca", "fosa", "everest"],
    "visual": ["marte", "océano", "luna", "júpiter", "sol", "dinosaurio", "volcán", "pirámide", "castillo", "vikingo",
               "roma", "titanic", "pompeya", "huracán", "ascensor", "avión", "everest", "espacio", "mar",
               "torre", "eiffel", "alcatraz", "móvil", "lotería", "dinero", "presidente", "espía"],
    "science": ["tierra", "agua", "respiración", "oxígeno", "cuerpo", "dentro de", "comida", "luz", "girar",
                "grados", "nivel del mar", "lluvia", "llover", "internet", "médico"],
}
_NUMBER = re.compile(r"\d|\b(una|un|dos|tres|cien|mil)\s+(día|días|semana|semanas|mes|meses|año|años|hora|horas|minuto|minutos|segundos?)\b")


def heuristic_score(idea: str, published: list[str], category_bonus: dict[str, float] | None = None,
                    category: str = "") -> float:
    """Pesos ajustados a la investigación del nicho: la cifra concreta y la situación reconocible pesan
    más; el peligro sigue sumando pero menos (en títulos, la palabra «peligro/sobrevivir» rinde peor)."""
    i = idea.lower()
    s = 40.0
    s += 6 if " te " in f" {i} " or re.search(r"\b\w+(aras|ieras|eras)\b", i) or " tu " in f" {i} " else 0
    for k, w in (("danger", 8), ("scale", 7), ("visual", 10), ("science", 8)):
        if any(x in i for x in HOOK_WORDS[k]):
            s += w
    s += 8 if _NUMBER.search(i) else 0                       # cifra concreta (medido)
    s -= 6 if re.search(r"sobreviv|morir|muert|peligr", i) else 0  # peligro dicho, no mostrado (medido)
    s -= 4 if len(idea) > 65 else 0                           # títulos top: 55-66 caracteres
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
            f"Propón {n} ideas originales y muy visuales. Prioriza cuerpo humano, historia, catástrofes naturales "
            "y espacio; situaciones concretas y reconocibles llevadas al extremo, en segunda persona, con una cifra "
            "concreta (días, metros, años) cuando encaje; 45-65 caracteres; sin las palabras sobrevivir/morir. "
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
    from ..research.niche import TOPICS, _norm, style_guide, topic_hit
    g = style_guide()
    if not g:
        return 0.0
    i = _norm(idea)
    for rank, topic in enumerate(g.get("preferred_topics", [])):
        if topic_hit(i, TOPICS.get(topic, "").split()):
            return 8.0 - rank * 1.5
    return 0.0


# Formatos prioritarios decididos el 2026-11-26 (style_guide.json → estrategia): presente + acción cotidiana del cuerpo.
_FORMAT_A = re.compile(r"qu[eé] pasa si (?:comes|bebes|tomas|comieras|bebieras)\b.*(?:todos los d[ií]as|al d[ií]a|cada d[ií]a|todas las|durante|\d)|"
                       r"qu[eé] pasa si (?:comes|bebes|tomas) un", re.I)
_FORMAT_B = re.compile(r"qu[eé] pasa si (?:te|aguantas|tu)\b.*(?:traga|estornud|chicle|pila|clavo|lentill|hipo|ojos|diente|cana|pica|"
                       r"muerde|pisas|dormido)|qu[eé] pasa si aguantas", re.I)


def _strategy_bonus(idea: str) -> float:
    """+22 si la idea es del formato A («comer X cada día») o B (micro-accidente del cuerpo), los priorizados para el viral."""
    try:
        from ..research.niche import style_guide
        if not (style_guide() or {}).get("estrategia"):
            return 0.0
    except Exception:
        return 0.0
    return 22.0 if (_FORMAT_A.search(idea) or _FORMAT_B.search(idea)) else 0.0


def _own_bonus(idea: str) -> float:
    """+0 a +8 si el molde de la premisa coincide con el de los Shorts que mejor han funcionado en NUESTRO canal."""
    try:
        from ..research.own import archetype_bonus
        return archetype_bonus(idea)
    except Exception:
        return 0.0


def ranked_ideas(n: int = 15) -> list[tuple[float, str]]:
    reg = Registry()
    published = [r["idea"] for r in reg.videos()] + _already_made()
    bonus = _category_bonus()
    pool = SEED_IDEAS + llm_ideas(12, published)
    scored = []
    for idea, cat in pool:
        if reg.is_duplicate(idea) or any(similarity(idea, p) >= 0.6 for p in published):
            continue
        scored.append((round(min(100, heuristic_score(idea, published, bonus, cat) + _niche_bonus(idea) + _own_bonus(idea) + _strategy_bonus(idea)), 1), idea))
    scored.sort(reverse=True)
    return scored[:n]


def pick_idea() -> str:
    top = ranked_ideas(5)
    if not top:
        raise RuntimeError("No quedan ideas nuevas: añade más a SEED_IDEAS o configura un LLM")
    # algo de variedad entre las 3 mejores
    return random.choice(top[:3])[1]
