"""Visual identity of the stickman channel: palette, line weights and hand-drawn text."""
from __future__ import annotations

import math

import cairo

from ..visuals.draw import clamp, col, ease_back, ease_out, lerp, saved  # noqa: F401  (re-exported)

W, H = 1920, 1080

INK = (0.09, 0.09, 0.11)
PAPER = (0.973, 0.957, 0.918)       # warm off-white "notebook" background
P = {
    "ink": INK, "paper": PAPER, "white": (1, 1, 1),
    "red": (0.89, 0.24, 0.22), "orange": (0.96, 0.55, 0.18), "yellow": (0.99, 0.80, 0.25),
    "gold": (0.93, 0.71, 0.17), "green": (0.36, 0.69, 0.33), "lime": (0.62, 0.82, 0.30),
    "teal": (0.16, 0.66, 0.64), "blue": (0.24, 0.50, 0.86), "sky": (0.62, 0.82, 0.96),
    "navy": (0.15, 0.20, 0.38), "purple": (0.52, 0.34, 0.74), "pink": (0.95, 0.52, 0.64),
    "brown": (0.55, 0.37, 0.22), "tan": (0.85, 0.71, 0.49), "wheat": (0.93, 0.79, 0.42),
    "grey": (0.60, 0.61, 0.64), "lightgrey": (0.83, 0.83, 0.84), "darkgrey": (0.33, 0.34, 0.37),
    "stone": (0.70, 0.68, 0.63), "wood": (0.62, 0.43, 0.26), "darkwood": (0.40, 0.27, 0.17),
    "thatch": (0.85, 0.68, 0.36), "grass": (0.53, 0.76, 0.36), "darkgrass": (0.37, 0.60, 0.27),
    "dirt": (0.62, 0.47, 0.32), "snow": (0.96, 0.97, 1.0), "water": (0.38, 0.62, 0.86),
    "skin": (0.98, 0.98, 0.96), "sick": (0.80, 0.90, 0.62), "night": (0.10, 0.12, 0.24),
    "parchment": (0.93, 0.86, 0.68), "chalk": (0.17, 0.27, 0.22), "fire": (1.0, 0.62, 0.18),
}
LW = 9.0          # stickman line width (scale 1)
OUTLINE = 4.5     # outline of props and scenery

HAND = "Patrick Hand"      # body text / labels
MARKER = "Gochi Hand"      # titles, big numbers
BOLD = "Lilita One"        # thumbnails


def c(v) -> tuple:
    """Colour name / hex / tuple → rgb."""
    if isinstance(v, str) and v in P:
        return P[v]
    return col(v)


def shade(v, k=0.25):
    r, g, b = c(v)
    return (r * (1 - k), g * (1 - k), b * (1 - k))


def tint(v, k=0.3):
    r, g, b = c(v)
    return (r + (1 - r) * k, g + (1 - g) * k, b + (1 - b) * k)


def ink_fill(ctx, fill, lw=OUTLINE, alpha=1.0, ink=INK):
    """Fill the current path with `fill` and outline it in ink."""
    if fill is not None:
        ctx.set_source_rgba(*c(fill), alpha)
        ctx.fill_preserve()
    if lw:
        ctx.set_source_rgba(*c(ink), alpha)
        ctx.set_line_width(lw)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()
    else:
        ctx.new_path()


def stroke(ctx, lw=LW, color=INK, alpha=1.0):
    ctx.set_source_rgba(*c(color), alpha)
    ctx.set_line_width(lw)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.stroke()


def line(ctx, x0, y0, x1, y1, lw=LW, color=INK, alpha=1.0):
    ctx.move_to(x0, y0)
    ctx.line_to(x1, y1)
    stroke(ctx, lw, color, alpha)


def circ(ctx, x, y, r):
    ctx.new_sub_path()
    ctx.arc(x, y, max(r, 0.01), 0, 2 * math.pi)


def rrect(ctx, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    ctx.close_path()


def poly(ctx, pts, close=True):
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    if close:
        ctx.close_path()


def measure(ctx, s, size, font=HAND):
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    return ctx.text_extents(s)


def write(ctx, s, x, y, size, color=INK, font=HAND, align="center", alpha=1.0, outline=0.0,
          outline_color="white", max_w=None, valign="middle"):
    """Single line of text. Returns (width, size used)."""
    if not s:
        return 0.0, size
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    ext = ctx.text_extents(s)
    if max_w and ext.width > max_w:
        size *= max_w / ext.width
        ctx.set_font_size(size)
        ext = ctx.text_extents(s)
    fe = ctx.font_extents()
    tx = {"center": x - ext.width / 2 - ext.x_bearing, "right": x - ext.width - ext.x_bearing}.get(align, x - ext.x_bearing)
    # vertical centring on the cap height (stable across words, unlike the ink box)
    cap = fe[0] * 0.72
    ty = {"middle": y + cap / 2, "top": y + cap, "baseline": y}.get(valign, y + cap / 2)
    ctx.new_path()
    ctx.move_to(tx, ty)
    ctx.text_path(s)
    if outline:
        ctx.set_source_rgba(*c(outline_color), alpha)
        ctx.set_line_width(outline * 2)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.stroke_preserve()
    ctx.set_source_rgba(*c(color), alpha)
    ctx.fill()
    return ext.width, size


def wrap(ctx, s, size, max_w, font=HAND) -> list[str]:
    """Greedy word wrap; explicit \\n respected."""
    out = []
    for para in str(s).split("\n"):
        cur = ""
        for w in para.split():
            trial = (cur + " " + w).strip()
            if cur and measure(ctx, trial, size, font).x_advance > max_w:
                out.append(cur)
                cur = w
            else:
                cur = trial
        out.append(cur)
    return out


def write_block(ctx, s, x, y, size, max_w, color=INK, font=HAND, align="center", alpha=1.0, leading=1.15,
                outline=0.0, outline_color="white"):
    """Wrapped paragraph centred vertically on y. Returns block height."""
    lines = wrap(ctx, s, size, max_w, font)
    lh = size * leading
    top = y - lh * (len(lines) - 1) / 2
    for i, ln in enumerate(lines):
        write(ctx, ln, x, top + i * lh, size, color, font, align, alpha, outline, outline_color)
    return lh * len(lines)


def pop(age: float, d: float = 0.35) -> float:
    """0→1 entrance scale with overshoot."""
    return ease_back(clamp(age / d)) if age < d else 1.0


def fade(age: float, d: float = 0.25) -> float:
    return ease_out(clamp(age / d))
