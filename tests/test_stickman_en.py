"""Tests for the English stickman channel (profile merge, numbers, captions, engine smoke render)."""
import os

import pytest


@pytest.fixture
def english(monkeypatch):
    from fabrica.core.config import load_config
    monkeypatch.setenv("FABRICA_CHANNEL", "stickman_en")
    load_config.cache_clear()
    yield load_config()
    monkeypatch.delenv("FABRICA_CHANNEL")
    load_config.cache_clear()


def test_profile_overrides(english):
    assert english["channel"]["engine"] == "stick"
    assert (english["video"]["width"], english["video"]["height"]) == (1920, 1080)
    assert english["tts"]["lexicon"] == {}            # Spanish lexicon replaced, not merged
    assert english["tts"]["fallback"] == []           # never mix voices
    assert english["tts"]["piper"]["speaker"] == 0    # untouched keys are inherited


def test_main_channel_unchanged():
    from fabrica.core.config import load_config
    load_config.cache_clear()
    assert os.environ.get("FABRICA_CHANNEL", "") == ""
    assert load_config()["channel"]["engine"] == "leo"
    assert load_config()["video"]["height"] == 1920


def test_english_numbers():
    from fabrica.tts.numbers_en import normalize
    assert normalize("In 1348") == "In thirteen forty-eight"
    assert normalize("40% died") == "forty percent died"
    assert normalize("2,000,000") == "two million"
    assert normalize("1066") == "ten sixty-six"
    assert normalize("1905") == "nineteen oh five"


def test_srt_cues():
    from fabrica.edit.srt import build_srt
    words = [{"word": w, "start": i * 0.4, "end": i * 0.4 + 0.3} for i, w in enumerate("Meet Stan. He farms.".split())]
    srt = build_srt(words)
    assert "1\n00:00:00,000 -->" in srt and "Meet Stan." in srt and "He farms." in srt


def test_stick_scene_renders(tmp_path, english):
    from fabrica.stick.scene import render_still
    item = {"id": "x", "dur": 2.0, "frames": 60, "words": [], "trans_in": "cut", "trans_out": "cut", "mouth": [],
            "scene": {"visual": {"background": {"type": "village"},
                                 "cast": [{"id": "stan", "action": "walk", "expression": "happy"},
                                          {"id": "lord", "preset": "lord", "x": 0.7, "action": "talk"}],
                                 "props": [{"type": "pig", "x": 0.3, "y": 0.9}],
                                 "overlays": [{"type": "fact", "text": "Hello", "source": "Test"}]}}}
    out = render_still(item, 1.0, tmp_path / "f.png")
    assert out.exists() and out.stat().st_size > 10_000
