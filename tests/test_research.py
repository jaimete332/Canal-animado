import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fabrica.research.niche import Video, analyze, build_style_guide, report_md  # noqa: E402


def test_analyze_and_guide():
    vids = [Video(title=f"¿Qué pasaría si te tragaras {i} chicles? 🤔", channel="A", views=1_000_000 * (i + 1),
                  published="2025-06-01T00:00:00Z", duration_s=30 + i, url=f"u{i}", hook="Te tragas un chicle")
            for i in range(8)]
    vids += [Video(title=f"Datos aburridos número {i}", channel="B", views=1000, published="2025-06-01T00:00:00Z",
                   duration_s=90) for i in range(8)]
    a = analyze(vids)
    assert a["top_videos"][0]["channel"] == "A"
    assert a["title_patterns"]["pregunta «¿qué pasaría si…?»"]["top"] == 1.0
    g = build_style_guide(a)
    assert any("Duración" in r for r in g["rules"])
    assert "Investigación" in report_md(a, g, ["q"])
