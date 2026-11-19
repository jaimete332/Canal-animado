"""Generador de guiones con LLM.

El LLM escribe la narración Y la dirección visual usando el catálogo del motor de animación
(fondos, props, acciones, expresiones, overlays, efectos). El resultado se valida y se
corrige automáticamente antes de pasar al pipeline.
"""
from __future__ import annotations

import json

from ..core.config import ROOT, load_config
from ..core.log import get_logger
from ..llm.client import NoLLMAvailable, complete
from .schema import Story

log = get_logger("writer")


def catalog() -> dict:
    from ..audio.sfx import LIB
    from ..visuals.character import ACTIONS, EXPRESSIONS
    from ..visuals.overlays import OVERLAYS
    from ..visuals.world import BACKGROUNDS, PROPS
    return {"backgrounds": sorted(BACKGROUNDS), "props": sorted(PROPS), "actions": sorted(ACTIONS),
            "expressions": EXPRESSIONS, "overlays": sorted(OVERLAYS), "sfx": sorted(LIB),
            "transitions": ["cut", "whip", "zoom", "flash", "circle", "slide"],
            "camera_moves": ["push_in", "pull_out", "punch", "static", "pan_up", "pan_down", "pan_left",
                             "pan_right", "zoom_burst"]}


SYSTEM = """Eres el guionista y director de animación de un canal de YouTube Shorts en español de España
del tipo "¿Qué pasaría si...?". Protagonista: Leo (pelirrojo, sudadera turquesa con un "?").
Escribes en castellano peninsular, tuteando al espectador, frases cortas, ritmo muy rápido, humor
cuando encaje, curiosidad creciente y giros. NUNCA inventas datos: todo dato real va en "claims"
con su fuente; lo imaginario se marca como ficción (overlay "fiction" o "imagina..."). Respondes solo JSON."""

RULES = """ESTRUCTURA OBLIGATORIA (≈{seconds}s, {min_words}-{max_words} palabras en total):
- hook (0-3 s): una escena, frase que despierte curiosidad YA. Sin saludos ni presentación.
- setup (3-15 s): situación y primer problema.
- development (15-40 s): consecuencias progresivas, sorpresas, mitos desmontados.
- climax (40-55 s): el momento más sorprendente.
- ending (55-60 s): giro final + pregunta para comentarios.
Escenas de 2-4,5 s (8-14 palabras). Mínimo {min_scenes} escenas. Números escritos con palabras en
"narration" (las cifras con dígitos van en overlays). Cada escena debe tener movimiento: acción del
personaje, cámara y al menos un prop u overlay que ilustre lo que se dice. Sincroniza con "at_word"
(índice de palabra de la escena, desde 0).

CATÁLOGO DEL MOTOR (usa SOLO estos nombres): {catalog}

Coordenadas x,y en fracciones de pantalla (0-1). Personaje: y≈0.55-0.65 (pies), scale 1.0-1.4.
Overlays de texto arriba (y 230-420 px). Los subtítulos van solos a y≈0.66: no pongas texto ahí.

Devuelve un objeto con esta forma (ejemplo real de un vídeo publicado, recortado):
{example}"""


def _example() -> str:
    p = ROOT / "stories" / "centro-de-la-tierra.json"
    if not p.exists():
        return "{}"
    d = json.loads(p.read_text())
    d["scenes"] = [s for s in d["scenes"] if s["id"] in ("s01", "s02", "s04", "s11", "s14", "s21")]
    return json.dumps(d, ensure_ascii=False)


def sanitize(story: Story) -> Story:
    """Sustituye nombres fuera de catálogo por valores seguros (el LLM a veces inventa)."""
    cat = catalog()
    for sc in story.scenes:
        v = sc.visual
        if v.background.get("type") not in cat["backgrounds"]:
            log.warning("%s: fondo desconocido %s → color", sc.id, v.background.get("type"))
            v.background = {"type": "color", "color": v.background.get("color", "#2B2D6E")}
        if v.character:
            if v.character.get("action", "idle") not in cat["actions"]:
                v.character["action"] = "talk"
            if v.character.get("expression", "happy") not in cat["expressions"]:
                v.character["expression"] = "happy"
            v.character["actions"] = [a for a in v.character.get("actions", []) if a[1] in cat["actions"]]
            v.character["expressions"] = [e for e in v.character.get("expressions", []) if e[1] in cat["expressions"]]
        v.props = [p for p in v.props if p.get("type") in cat["props"]]
        v.overlays = [o for o in v.overlays if o.get("type") in cat["overlays"]]
        sc.sfx = [s for s in sc.sfx if s.name in cat["sfx"]]
        if v.camera.get("move") not in cat["camera_moves"]:
            v.camera["move"] = "push_in"
    return story


def write_story(idea: str, feedback: str | None = None) -> Story:
    cfg = load_config()
    sc = cfg["script"]
    if feedback is None:
        try:
            from ..analytics.metrics import insights
            feedback = json.dumps(insights().get("guidance", []), ensure_ascii=False)
        except Exception:
            feedback = ""
    rules = RULES.format(seconds=58, min_words=150, max_words=sc["max_words"], min_scenes=sc["min_scenes"],
                         catalog=json.dumps(catalog()), example=_example())
    from ..research.niche import style_guide
    guide = style_guide()
    niche = ("\n".join(f"- {r}" for r in guide["rules"]) + f"\nPRINCIPIO: {guide['principle']}") if guide else "sin datos aún"
    prompt = (f"IDEA: {idea}\n\n{rules}\n\nAPRENDIZAJES DE VÍDEOS ANTERIORES: {feedback or 'ninguno aún'}"
              f"\n\nGUÍA DE ESTILO DEL NICHO (investigación de los vídeos que mejor funcionan):\n{niche}")
    try:
        data = complete(SYSTEM, prompt, max_tokens=12000)
    except NoLLMAvailable as e:
        raise RuntimeError(
            "Para escribir guiones nuevos automáticamente hace falta una API key de LLM "
            "(ANTHROPIC_API_KEY, OPENAI_API_KEY o GEMINI_API_KEY; ver docs/API_KEYS.md). "
            "Mientras tanto puedes usar `python -m fabrica make stories/<guion>.json`.") from e
    data.setdefault("idea", idea)
    story = sanitize(Story.model_validate(data))
    if story.word_count > sc["max_words"] + 15:
        log.info("Guion largo (%d palabras), pidiendo recorte", story.word_count)
        data = complete(SYSTEM, "Recorta este guion a menos de "
                        f"{sc['max_words']} palabras manteniendo estructura, datos y JSON idéntico en forma:\n"
                        + story.model_dump_json(), max_tokens=12000, temperature=0.4)
        data.setdefault("idea", idea)
        story = sanitize(Story.model_validate(data))
    return story
