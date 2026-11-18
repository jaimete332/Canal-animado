"""Subtítulos dinámicos estilo Shorts (ASS/libass).

- Grupos de 1-3 palabras, cortados en la puntuación.
- La palabra que suena se resalta en amarillo y crece (karaoke).
- Pop-in al aparecer cada grupo.
- Palabras de énfasis (números, nombres clave) en otro color.
- Posición en la franja segura (por defecto 66 % de altura, lejos de botones y descripción).
"""
from __future__ import annotations

import re

from ..core.config import load_config


def _ts(t: float) -> str:
    t = max(0.0, t)
    h = int(t // 3600)
    m = int(t % 3600 // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def _bgr(hexc: str) -> str:
    h = hexc.lstrip("#")
    return f"&H00{h[4:6]}{h[2:4]}{h[0:2]}&".upper()


def _clean(w: str) -> str:
    return re.sub(r"^[¿¡\"'(]+|[\"')]+$", "", w)


def group_words(words: list[dict], max_words: int = 3) -> list[list[dict]]:
    groups, cur = [], []
    for w in words:
        cur.append(w)
        txt = w["word"]
        end_punct = bool(re.search(r"[.,;:!?…]$", txt))
        if len(cur) >= max_words or end_punct or len(" ".join(x["word"] for x in cur)) > 14:
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return groups


def build_ass(words: list[dict], emphasis: set[str] | None = None, total: float | None = None) -> str:
    cfg = load_config()["subtitles"]
    W, H = load_config()["video"]["width"], load_config()["video"]["height"]
    size = cfg.get("size", 92)
    y = int(H * cfg.get("y_position", 0.66))
    base, hl = _bgr(cfg.get("base_color", "#FFFFFF")), _bgr(cfg.get("highlight_color", "#FFD23F"))
    emph = _bgr("#5CE1E6")
    outline = cfg.get("outline", 9)
    emphasis = {e.lower() for e in (emphasis or set())}
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{cfg.get('font', 'Lilita One')},{size},{base},&H000000FF&,&H00281619&,&H80000000&,0,0,0,0,100,100,1,0,1,{outline},5,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    groups = group_words(words, cfg.get("max_words", 3))
    for gi, g in enumerate(groups):
        g_start = g[0]["start"]
        g_end = groups[gi + 1][0]["start"] if gi + 1 < len(groups) else (total or g[-1]["end"] + 0.4)
        g_end = min(g_end, g[-1]["end"] + 0.6)
        for wi, w in enumerate(g):
            s = w["start"] if wi else g_start
            e = g[wi + 1]["start"] if wi + 1 < len(g) else g_end
            if e - s < 0.02:
                continue
            parts = []
            for j, x in enumerate(g):
                token = _clean(x["word"]).upper()
                key = re.sub(r"[^\wáéíóúüñ]", "", x["word"].lower())
                if j == wi:
                    parts.append(f"{{\\c{hl}\\fscx112\\fscy112}}{token}{{\\c{base}\\fscx100\\fscy100}}")
                elif key in emphasis:
                    parts.append(f"{{\\c{emph}}}{token}{{\\c{base}}}")
                else:
                    parts.append(token)
            chars = sum(len(_clean(x["word"])) for x in g) + len(g) - 1
            fit = min(100, int(100 * 15 / max(15, chars)))  # encoge grupos largos para no salirse
            pop = f"{{\\fs{int(size * fit / 100)}}}" + ("{\\fscx70\\fscy70\\t(0,90,\\fscx108\\fscy108)\\t(90,160,\\fscx100\\fscy100)}" if wi == 0 else "")
            txt = f"{{\\an5\\pos({W // 2},{y})\\blur0.6}}{pop}" + " ".join(parts)
            lines.append(f"Dialogue: 0,{_ts(s)},{_ts(e)},Cap,,0,0,0,,{txt}")
    return head + "\n".join(lines) + "\n"
