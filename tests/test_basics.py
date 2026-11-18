"""Tests rápidos (sin render completo): python -m pytest -q"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import cairo  # noqa: E402

from fabrica.core.registry import similarity  # noqa: E402
from fabrica.edit.subtitles import build_ass, group_words  # noqa: E402
from fabrica.pipeline import load_story  # noqa: E402
from fabrica.qa.checks import wer  # noqa: E402
from fabrica.script.factcheck import rule_review  # noqa: E402
from fabrica.script.writer import sanitize  # noqa: E402
from fabrica.tts.narrator import normalize_numbers, split_clauses  # noqa: E402
from fabrica.tts.numbers_es import to_words  # noqa: E402
from fabrica.visuals.character import ACTIONS, Character, Pose, act  # noqa: E402

STORY = Path(__file__).resolve().parents[1] / "stories" / "centro-de-la-tierra.json"


def test_numbers():
    assert to_words(6371) == "seis mil trescientos setenta y uno"
    assert to_words(2900) == "dos mil novecientos"
    assert "seis mil" in normalize_numbers("6.371 km")


def test_clauses():
    assert [c for c, _ in split_clauses("Hola, mundo. ¿Qué tal?")] == ["Hola, mundo.", "¿Qué tal?"]


def test_story_valid_and_reviewed():
    s = load_story(STORY)
    assert 150 <= s.word_count <= 210
    assert s.scenes[0].beat == "hook" and s.scenes[-1].beat == "ending"
    assert not rule_review(s)["blocking"]
    sanitize(s)


def test_subtitles():
    words = [{"word": w, "start": i * 0.3, "end": i * 0.3 + 0.25} for i, w in enumerate("Hola a todos, esto es una prueba.".split())]
    assert all(len(g) <= 3 for g in group_words(words))
    ass = build_ass(words)
    assert "Dialogue:" in ass and "PRUEBA" in ass


def test_wer_and_similarity():
    assert wer("a dos mil novecientos kilómetros", "A 2.900 kilómetros") == 0
    assert similarity("¿Qué pasaría si vivieras en Marte?", "¿Qué pasaría si vivieras 100 días en Marte?") >= 0.5


def test_character_all_actions_render():
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 400, 700)
    ctx = cairo.Context(surf)
    for name in ACTIONS:
        for t in (0.0, 0.5, 1.3):
            Character().draw(ctx, act(name, t, 2.0, Pose(x=200, y=650, scale=1.0)))
