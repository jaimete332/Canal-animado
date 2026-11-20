"""Revisión de precisión del guion.

1. Reglas locales (siempre): cada escena con afirmaciones 'fact' debe tener fuente; las escenas de
   ficción deben llevar el overlay FICCIÓN o decirlo en la narración; cifras de la narración
   deben aparecer en alguna afirmación registrada.
2. Revisión por LLM (si hay API key): un 'editor científico' marca afirmaciones dudosas.
"""
from __future__ import annotations

import re

from ..core.log import get_logger
from ..llm.client import NoLLMAvailable, complete
from .schema import Story

log = get_logger("factcheck")

NUM_WORDS = r"\b(mil|millones|millón|cien|doscient|trescient|cuatrocient|quinient|seiscient|setecient|ochocient|novecient|\d+)"
FICTION_HINTS = ("imagina", "supón", "supongamos", "ficción", "en la vida real", "indestructible", "mágic")
NUM_WORDS_EN = (r"\b(hundred|thousand|million|billion|half|third|quarter|twice|percent|"
                r"twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|\d+)")
FICTION_HINTS_EN = ("imagine", "let's say", "pretend", "what if", "suppose", "our story", "meet stan")


def rule_review(story: Story) -> dict:
    from ..core.config import lang, load_config
    en = lang() == "en"
    num_words, hints = (NUM_WORDS_EN, FICTION_HINTS_EN) if en else (NUM_WORDS, FICTION_HINTS)
    warnings, blocking = [], []
    for sc in story.scenes:
        has_num = re.search(num_words, sc.narration.lower())
        facts = [c for c in sc.claims if c.kind == "fact"]
        if has_num and not sc.claims:
            warnings.append(f"{sc.id}: contiene cifras pero no tiene afirmaciones registradas")
        for c in facts:
            if not c.source:
                blocking.append(f"{sc.id}: dato sin fuente → '{c.text}'")
        fiction = [c for c in sc.claims if c.kind == "fiction"]
        if fiction:
            ov = {o.get("type") for o in sc.visual.overlays}
            if "fiction" not in ov and not any(h in sc.narration.lower() for h in hints):
                warnings.append(f"{sc.id}: ficción sin señalizar (añade overlay 'fiction' o 'imagina...')")
    max_words = load_config().get_path("script.max_words", 230)
    if story.word_count > max_words:
        warnings.append(f"Guion largo ({story.word_count} palabras > {max_words})")
    return {"warnings": warnings, "blocking": blocking}


SYSTEM = ("Eres un editor científico riguroso. Revisas guiones de divulgación en español. Distingues "
          "hechos verificables de licencias narrativas. Respondes solo JSON.")


def llm_review(story: Story) -> dict | None:
    claims = [{"scene": s.id, "narration": s.narration, "claims": [c.model_dump() for c in s.claims]}
              for s in story.scenes]
    prompt = ("Revisa cada escena. Para cada afirmación presentada como hecho, indica si es correcta, "
              "imprecisa o falsa, y propone corrección. Señala también hechos implícitos en la narración "
              "que no estén registrados. Formato: {\"issues\":[{\"scene\":\"s01\",\"severity\":"
              "\"high|medium|low\",\"problem\":\"...\",\"fix\":\"...\"}]}\n\n" + str(claims))
    try:
        return complete(SYSTEM, prompt, temperature=0.1)
    except NoLLMAvailable:
        return None
    except Exception as e:  # la revisión LLM no debe tumbar el pipeline
        log.warning("Revisión LLM no disponible: %s", e)
        return None


def review(story: Story) -> dict:
    rep = rule_review(story)
    llm = llm_review(story)
    rep["llm"] = llm
    if llm:
        for i in llm.get("issues", []):
            msg = f"{i.get('scene')}: {i.get('problem')} → {i.get('fix')}"
            (rep["blocking"] if i.get("severity") == "high" else rep["warnings"]).append(msg)
    for w in rep["warnings"]:
        log.warning("Revisión: %s", w)
    return rep
