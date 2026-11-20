"""Catálogo «alturas y abismos»: montaña nevada con altitud, campamento, fosa abisal; tiendas, bombona de
oxígeno, banderas de oración, batiscafo, pez abisal y pez caracol.

Se registra automáticamente en BACKGROUNDS y PROPS al importar fabrica.visuals.world.
"""
from __future__ import annotations

import math

import numpy as np

from .draw import INK, OUT, PAL, circle, clamp, col, darken, ellipse, fill_stroke, lighten, mix, rrect, saved
from .world import BACKGROUNDS, H, M, PROPS, W, _sky


# ============================================================================ FONDOS
def bg_mountain(ctx, t, p):
    """Ladera nevada del Everest. `alt` 0..1 (campo base → cima): el cielo se vuelve azul oscuro, aparecen
    picos por debajo y el viento arrastra nieve. `summit` dibuja la cumbre bajo el personaje."""
    alt = clamp(p.get("alt", 0.3))
    _sky(ctx, mix("#6FB2F0", "#14205A", alt), mix("#CFE8FF", "#5E7BC8", alt))
    if alt > 0.75:   # estrellas de día a gran altura (cielo muy oscuro)
        rs = np.random.default_rng(3)
        for _ in range(30):
            x, y = rs.random() * W, rs.random() * 700
            circle(ctx, x, y, 2.5)
            ctx.set_source_rgba(1, 1, 1, 0.5 * (alt - 0.75) * 4)
            ctx.fill()
    # sol intenso
    circle(ctx, 860, 260, 85)
    fill_stroke(ctx, "#FFF3B0", OUT)
    # cordillera lejana (más baja cuanto más alto estás)
    far_y = 1150 + 380 * alt
    ctx.move_to(-M, far_y)
    for i, x in enumerate(range(-M, W + M + 1, 140)):
        ctx.line_to(x, far_y - (160 if i % 2 else 40) - 60 * math.sin(i))
    ctx.line_to(W + M, H + M)
    ctx.line_to(-M, H + M)
    ctx.close_path()
    fill_stroke(ctx, mix("#B9C9E6", "#7F93C2", alt), OUT)
    # nubes por debajo a gran altura
    if alt > 0.4:
        for i in range(4):
            x = (i * 340 + t * 25) % (W + 400) - 200
            ellipse(ctx, x, far_y + 40, 220, 60)
            ctx.set_source_rgba(1, 1, 1, 0.85)
            ctx.fill()
    # ladera principal
    g = p.get("ground", 1430)
    if p.get("summit"):
        ctx.move_to(-M, H + M)
        ctx.line_to(-M, g + 380)
        ctx.line_to(W * 0.5, g - 60)
        ctx.line_to(W + M, g + 420)
        ctx.line_to(W + M, H + M)
    else:
        ctx.move_to(-M, g + 260)
        ctx.line_to(W + M, g - 200)
        ctx.line_to(W + M, H + M)
        ctx.line_to(-M, H + M)
    ctx.close_path()
    fill_stroke(ctx, "#F6FAFF", OUT)
    for i in range(6):   # sombras de la nieve
        x = 80 + i * 180
        ctx.move_to(x, H)
        ctx.line_to(x + 90, g + 200 - i * 20)
        ctx.set_source_rgba(0.6, 0.7, 0.9, 0.35)
        ctx.set_line_width(14)
        ctx.stroke()
    # cuerda fija
    if p.get("rope", True) and not p.get("summit"):
        ctx.move_to(-M, g + 330)
        ctx.curve_to(300, g + 150, 700, g, W + M, g - 140)
        ctx.set_source_rgb(*col("#E8392F"))
        ctx.set_line_width(7)
        ctx.stroke()
    # viento con nieve
    wind = p.get("wind", 0.3 + 0.6 * alt)
    rs = np.random.default_rng(7)
    for i in range(int(40 + 80 * wind)):
        x0, y0, sp = rs.random() * (W + 600), rs.random() * H, 600 + rs.random() * 900 * wind
        x = (x0 - t * sp) % (W + 600) - 300
        y = y0 + 30 * math.sin(t * 2 + i)
        ctx.move_to(x, y)
        ctx.line_to(x + 30 + 50 * wind, y - 6)
        ctx.set_source_rgba(1, 1, 1, 0.8)
        ctx.set_line_width(4)
        ctx.stroke()


def bg_trench_deep(ctx, t, p):
    """Fosa abisal: negro azulado, nieve marina que cae, paredes de roca, suelo de lodo. `glow` partículas."""
    _sky(ctx, "#020614", "#071533")
    rs = np.random.default_rng(11)
    for i in range(120):   # nieve marina
        x0, y0 = rs.random() * W, rs.random() * H
        y = (y0 + t * (20 + 30 * rs.random())) % H
        circle(ctx, x0 + 10 * math.sin(t + i), y, 2 + 2 * rs.random())
        ctx.set_source_rgba(0.75, 0.85, 1, 0.35)
        ctx.fill()
    for side in (-1, 1):   # paredes de la fosa
        ctx.move_to(W / 2 + side * (W / 2 + M), -M)
        for k in range(0, 11):
            y = -M + k * (H + 2 * M) / 10
            ctx.line_to(W / 2 + side * (360 + 70 * math.sin(k * 1.7) + 30 * k), y)
        ctx.line_to(W / 2 + side * (W / 2 + M), H + M)
        ctx.close_path()
        fill_stroke(ctx, "#0E1D3B", OUT)
    g = p.get("floor", 1650)
    if g < H + 100:
        ctx.move_to(-M, g)
        for x in range(-M, W + M + 1, 80):
            ctx.line_to(x, g + 18 * math.sin(x * 0.01))
        ctx.line_to(W + M, H + M)
        ctx.line_to(-M, H + M)
        ctx.close_path()
        fill_stroke(ctx, "#3A3F52", OUT)


# ============================================================================ PROPS
def _tent(ctx, p, t):
    c = col(p.get("color", "#FF8A00"))
    flap = 6 * math.sin(t * 9)
    ctx.move_to(-230, 0)
    ctx.curve_to(-200, -260, 200, -260, 230, 0)
    ctx.close_path()
    fill_stroke(ctx, c, OUT)
    ctx.move_to(-60, 0)
    ctx.curve_to(-40, -120 + flap, 40, -120 + flap, 60, 0)
    ctx.close_path()
    fill_stroke(ctx, darken(c, 0.35), OUT)
    for x in (-120, 120):
        ctx.move_to(x * 0.3, -195)
        ctx.line_to(x, 0)
        ctx.set_source_rgba(*INK, 0.4)
        ctx.set_line_width(5)
        ctx.stroke()


def _oxygen(ctx, p, t):
    """Bombona de oxígeno con manómetro. `level` 0..1."""
    rrect(ctx, -70, -360, 140, 360, 60)
    fill_stroke(ctx, "#FF8A00", OUT)
    rrect(ctx, -38, -430, 76, 80, 16)
    fill_stroke(ctx, "#B9C2CF", OUT)
    circle(ctx, 0, -470, 46)
    fill_stroke(ctx, "white", OUT)
    lv = clamp(p.get("level", 1.0))
    a = math.pi * (0.75 + 1.5 * lv)
    ctx.move_to(0, -470)
    ctx.line_to(36 * math.cos(a), -470 + 36 * math.sin(a))
    ctx.set_source_rgb(*col("#E8392F"))
    ctx.set_line_width(7)
    ctx.stroke()
    rrect(ctx, -52, -250, 104, 70, 12)
    fill_stroke(ctx, "white", 5)
    from .draw import text
    text(ctx, "O2", 0, -215, 52, color="#19162B", outline=0, shadow_off=0)


def _prayer_flags(ctx, p, t):
    cols = ["#2B6BE8", "white", "#E8392F", "#22B573", "#FFD23F"]
    n = p.get("n", 10)
    span = p.get("w", 900)
    ctx.move_to(-span / 2, 0)
    ctx.curve_to(-span / 4, 90, span / 4, 90, span / 2, 0)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(4)
    ctx.stroke()
    for i in range(n):
        u = (i + 0.5) / n
        x = -span / 2 + u * span
        y = 360 * u * (1 - u) * 0.45 + 2
        sw = 8 * math.sin(t * 7 + i)
        ctx.move_to(x - 30, y)
        ctx.line_to(x + 30, y)
        ctx.line_to(x + 30 + sw, y + 70)
        ctx.line_to(x - 30 + sw, y + 70)
        ctx.close_path()
        fill_stroke(ctx, cols[i % 5], 4)


def _bathyscaphe(ctx, p, t):
    """Batiscafo tipo Trieste: flotador grande y esfera de observación con foco."""
    bob = 8 * math.sin(t * 1.4)
    ctx.translate(0, bob)
    rrect(ctx, -330, -260, 660, 200, 100)
    fill_stroke(ctx, p.get("color", "#FFD23F"), OUT)
    rrect(ctx, -60, -330, 120, 80, 16)
    fill_stroke(ctx, "#E8392F", OUT)
    circle(ctx, 0, 30, 120)
    fill_stroke(ctx, "#B9C2CF", OUT)
    circle(ctx, 40, 30, 50)
    fill_stroke(ctx, "#5CE1E6", OUT)
    if p.get("light", True):   # haz del foco
        ctx.move_to(150, 30)
        ctx.line_to(900, -140)
        ctx.line_to(900, 260)
        ctx.close_path()
        ctx.set_source_rgba(1, 0.95, 0.7, 0.18)
        ctx.fill()
        circle(ctx, 140, 30, 18)
        fill_stroke(ctx, "#FFF3B0", 5)


def _anglerfish(ctx, p, t):
    """Rape abisal con señuelo luminoso."""
    glow = 0.6 + 0.4 * math.sin(t * 4)
    from .draw import radial_grad
    ctx.set_source(radial_grad(ctx, 210, -230, 5, 120, [(0, (1, 0.95, 0.6), 0.8 * glow), (1, (1, 0.95, 0.6), 0)]))
    ctx.paint()
    ctx.move_to(20, -120)
    ctx.curve_to(60, -260, 160, -280, 210, -230)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(6)
    ctx.stroke()
    circle(ctx, 210, -230, 18)
    fill_stroke(ctx, "#FFF3B0", 5)
    ellipse(ctx, 0, 0, 200, 140)
    fill_stroke(ctx, "#3A3550", OUT)
    ctx.move_to(-190, 0)
    ctx.line_to(-300, -90)
    ctx.line_to(-300, 90)
    ctx.close_path()
    fill_stroke(ctx, "#3A3550", OUT)
    ctx.move_to(60, 40)
    ctx.curve_to(120, 120, 180, 60, 200, 20)
    ctx.close_path()
    fill_stroke(ctx, "#19162B", 5)
    for k in range(5):   # dientes
        x = 90 + k * 22
        ctx.move_to(x, 50 + k * 4)
        ctx.line_to(x + 8, 30 + k * 4)
        ctx.line_to(x + 16, 52 + k * 4)
        ctx.close_path()
        fill_stroke(ctx, "white", 2.5)
    circle(ctx, 70, -40, 22)
    fill_stroke(ctx, "white", 5)
    circle(ctx, 76, -40, 9)
    ctx.set_source_rgb(*INK)
    ctx.fill()


def _snailfish(ctx, p, t):
    """Pez caracol de las fosas: rosado, translúcido, cabeza grande."""
    sw = 0.08 * math.sin(t * 3)
    ctx.rotate(sw)
    ctx.move_to(-60, -80)
    ctx.curve_to(80, -110, 130, 40, 40, 70)
    ctx.curve_to(-120, 90, -260, 30, -330, 0)
    ctx.curve_to(-260, -30, -160, -70, -60, -80)
    ctx.close_path()
    fill_stroke(ctx, (1.0, 0.82, 0.86), OUT)
    circle(ctx, 40, -30, 16)
    ctx.set_source_rgb(*INK)
    ctx.fill()


BACKGROUNDS.update({"mountain": bg_mountain, "trench_deep": bg_trench_deep})
PROPS.update({"tent": _tent, "oxygen": _oxygen, "prayer_flags": _prayer_flags, "bathyscaphe": _bathyscaphe,
              "anglerfish": _anglerfish, "snailfish": _snailfish})
