"""Primitivas de dibujo cartoon sobre Cairo: paleta, contornos gruesos, easing, partículas, texto."""
from __future__ import annotations

import math
from contextlib import contextmanager

import cairo
import numpy as np

# ---------------------------------------------------------------------------
# Identidad visual del canal (paleta fija = reconocible entre vídeos)
# ---------------------------------------------------------------------------
INK = (0.098, 0.086, 0.157)          # contorno #19162 8
WHITE = (1, 1, 1)
PAL = {
    "ink": INK, "white": WHITE,
    "skin": (0.98, 0.78, 0.60), "skin_sh": (0.92, 0.64, 0.48), "cheek": (1.0, 0.52, 0.52),
    "hair": (1.0, 0.45, 0.16), "hair_sh": (0.86, 0.30, 0.10),
    "hoodie": (0.13, 0.72, 0.68), "hoodie_sh": (0.08, 0.55, 0.55),
    "pants": (0.20, 0.25, 0.55), "shoe": (0.93, 0.22, 0.27),
    "yellow": (1.0, 0.82, 0.25), "orange": (1.0, 0.55, 0.15), "red": (0.93, 0.22, 0.27),
    "green": (0.30, 0.80, 0.40), "blue": (0.25, 0.55, 0.95), "purple": (0.58, 0.36, 0.92),
    "pink": (1.0, 0.45, 0.65), "sky_top": (0.30, 0.65, 0.98), "sky_bot": (0.70, 0.90, 1.0),
    "grass": (0.40, 0.80, 0.30), "grass_dk": (0.27, 0.62, 0.22), "dirt": (0.55, 0.36, 0.22),
    "metal": (0.78, 0.82, 0.88), "metal_dk": (0.52, 0.56, 0.64), "suit": (0.92, 0.94, 0.98),
    "suit_acc": (1.0, 0.55, 0.15),
}
OUT = 7.0   # grosor de contorno base en px (escala 1)


def hexrgb(h: str) -> tuple[float, float, float]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))  # type: ignore[return-value]


def col(c) -> tuple:
    if isinstance(c, str):
        return PAL[c] if c in PAL else hexrgb(c)
    return c


def mix(a, b, t):
    a, b = col(a), col(b)
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def lighten(c, t=0.3):
    return mix(c, WHITE, t)


def darken(c, t=0.3):
    return mix(c, (0, 0, 0), t)


# ---------------------------------------------------------------------------
# Easing
# ---------------------------------------------------------------------------
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def lerp(a, b, t):
    return a + (b - a) * t


def ease_out(t):
    t = clamp(t)
    return 1 - (1 - t) ** 3


def ease_in(t):
    t = clamp(t)
    return t ** 3


def ease_io(t):
    t = clamp(t)
    return 4 * t ** 3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2


def ease_back(t, s=1.9):
    t = clamp(t) - 1
    return t * t * ((s + 1) * t + s) + 1


def ease_elastic(t):
    t = clamp(t)
    if t in (0, 1):
        return t
    return 2 ** (-10 * t) * math.sin((t * 10 - 0.75) * (2 * math.pi) / 3) + 1


def bounce01(t):
    """0→1 con rebote al final (para caídas)."""
    t = clamp(t)
    n, d = 7.5625, 2.75
    if t < 1 / d:
        return n * t * t
    if t < 2 / d:
        t -= 1.5 / d
        return n * t * t + 0.75
    if t < 2.5 / d:
        t -= 2.25 / d
        return n * t * t + 0.9375
    t -= 2.625 / d
    return n * t * t + 0.984375


def noise1(x: float, seed: int = 0) -> float:
    """Ruido suave 1D determinista (-1..1) para temblores y derivas."""
    i = math.floor(x)
    f = x - i

    def h(n):
        n = (n * 374761393 + seed * 668265263) & 0xFFFFFFFF
        n = (n ^ (n >> 13)) * 1274126177 & 0xFFFFFFFF
        return ((n ^ (n >> 16)) & 0xFFFF) / 32767.5 - 1
    u = f * f * (3 - 2 * f)
    return h(i) * (1 - u) + h(i + 1) * u


# ---------------------------------------------------------------------------
# Formas
# ---------------------------------------------------------------------------
@contextmanager
def saved(ctx: cairo.Context):
    ctx.save()
    try:
        yield ctx
    finally:
        ctx.restore()


def fill_stroke(ctx, fill, lw=OUT, ink=INK, alpha=1.0):
    if fill is not None:
        c = col(fill)
        ctx.set_source_rgba(*c, alpha)
        if lw:
            ctx.fill_preserve()
        else:
            ctx.fill()
    if lw:
        ctx.set_source_rgba(*col(ink), alpha)
        ctx.set_line_width(lw)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()


def ellipse(ctx, x, y, rx, ry, rot=0.0):
    with saved(ctx):
        ctx.translate(x, y)
        ctx.rotate(rot)
        ctx.scale(max(rx, 1e-3), max(ry, 1e-3))
        ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.close_path()


def circle(ctx, x, y, r):
    ctx.new_sub_path()
    ctx.arc(x, y, max(r, 1e-3), 0, 2 * math.pi)
    ctx.close_path()


def rrect(ctx, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    ctx.close_path()


def blob(ctx, x, y, r, n=9, wobble=0.18, seed=0, t=0.0):
    """Forma orgánica cerrada (rocas, nubes, manchas)."""
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = r * (1 + wobble * noise1(i * 1.7 + seed * 13.1 + t, seed))
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    smooth_closed(ctx, pts)


def smooth_closed(ctx, pts, tension=0.5):
    n = len(pts)
    ctx.new_sub_path()
    ctx.move_to(*pts[0])
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) * tension / 3, p1[1] + (p2[1] - p0[1]) * tension / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * tension / 3, p2[1] - (p3[1] - p1[1]) * tension / 3)
        ctx.curve_to(*c1, *c2, *p2)
    ctx.close_path()


def smooth_open(ctx, pts, tension=0.5):
    n = len(pts)
    ctx.move_to(*pts[0])
    for i in range(n - 1):
        p0 = pts[max(0, i - 1)]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[min(n - 1, i + 2)]
        c1 = (p1[0] + (p2[0] - p0[0]) * tension / 3, p1[1] + (p2[1] - p0[1]) * tension / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * tension / 3, p2[1] - (p3[1] - p1[1]) * tension / 3)
        ctx.curve_to(*c1, *c2, *p2)


def limb(ctx, pts, width, color, ink=INK, out=OUT):
    """Extremidad tipo 'manguera' con contorno."""
    for w, c in ((width + 2 * out, ink), (width, col(color))):
        ctx.set_source_rgb(*c)
        ctx.set_line_width(w)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.move_to(*pts[0])
        if len(pts) == 3:
            # curva suave por el codo
            ctx.curve_to(*pts[1], *pts[1], *pts[2])
        else:
            for p in pts[1:]:
                ctx.line_to(*p)
        ctx.stroke()


def star(ctx, x, y, r, n=5, inner=0.45, rot=-math.pi / 2):
    ctx.new_sub_path()
    for i in range(2 * n):
        rr = r if i % 2 == 0 else r * inner
        a = rot + i * math.pi / n
        (ctx.move_to if i == 0 else ctx.line_to)(x + rr * math.cos(a), y + rr * math.sin(a))
    ctx.close_path()


def linear_grad(ctx, x0, y0, x1, y1, stops):
    g = cairo.LinearGradient(x0, y0, x1, y1)
    for off, c, *a in stops:
        g.add_color_stop_rgba(off, *col(c), a[0] if a else 1.0)
    return g


def radial_grad(ctx, x, y, r0, r1, stops):
    g = cairo.RadialGradient(x, y, r0, x, y, r1)
    for off, c, *a in stops:
        g.add_color_stop_rgba(off, *col(c), a[0] if a else 1.0)
    return g


def shadow(ctx, x, y, rx, ry=None, alpha=0.25):
    ellipse(ctx, x, y, rx, ry or rx * 0.22)
    ctx.set_source_rgba(0, 0, 0, alpha)
    ctx.fill()


# ---------------------------------------------------------------------------
# Texto (fuentes OFL en assets/fonts, registradas por fabrica.visuals.fonts)
# ---------------------------------------------------------------------------
def text(ctx, s, x, y, size, color="white", font="Lilita One", align="center", outline=10.0,
         ink=INK, alpha=1.0, shadow_off=6.0, max_w=None):
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    ext = ctx.text_extents(s)
    if max_w and ext.width > max_w:
        size *= max_w / ext.width
        ctx.set_font_size(size)
        ext = ctx.text_extents(s)
    if align == "center":
        tx = x - ext.width / 2 - ext.x_bearing
    elif align == "right":
        tx = x - ext.width - ext.x_bearing
    else:
        tx = x - ext.x_bearing
    ty = y - ext.height / 2 - ext.y_bearing
    ctx.new_path()
    if shadow_off:
        ctx.move_to(tx + shadow_off * 0.4, ty + shadow_off)
        ctx.text_path(s)
        ctx.set_source_rgba(0, 0, 0, 0.35 * alpha)
        ctx.set_line_width(outline * 2)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.stroke_preserve()
        ctx.fill()
    ctx.move_to(tx, ty)
    ctx.text_path(s)
    if outline:
        ctx.set_source_rgba(*col(ink), alpha)
        ctx.set_line_width(outline * 2)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.stroke_preserve()
    ctx.set_source_rgba(*col(color), alpha)
    ctx.fill()
    return ext.width, size


# ---------------------------------------------------------------------------
# Partículas deterministas (función pura del tiempo → render paralelo sin estado)
# ---------------------------------------------------------------------------
def particles(seed: int, n: int, t: float, period: float, spawn, step):
    """Llama step(i, age01, rng_vals) para n partículas que renacen cada `period`."""
    rs = np.random.default_rng(seed).random((n, 6))
    for i in range(n):
        offset = rs[i, 0] * period
        age = ((t + offset) % period) / period
        cycle = int((t + offset) // period)
        vals = rs[i] if spawn is None else spawn(i, cycle, rs[i])
        step(i, age, vals)
