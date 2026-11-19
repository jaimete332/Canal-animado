"""Catálogo «ciencia cotidiana e historia»: dormitorio, aldea medieval, playa con mareas,
cielo nocturno; Luna, eclipse, peonza, cerebro, café, móvil, coche, fantasmas, trofeo,
alimentos, rata, grúa, baños, corales, wifi...
"""
from __future__ import annotations

import math

import cairo
import numpy as np

from .draw import (INK, OUT, PAL, blob, circle, clamp, col, darken, ellipse, fill_stroke, lerp, lighten,
                   limb, linear_grad, mix, noise1, radial_grad, rrect, saved, star, text)
from .world import BACKGROUNDS, H, M, PROPS, W, _cloud, _sky


# ============================================================================ FONDOS
def bg_bedroom(ctx, t, p):
    """Dormitorio de noche: ventana con luna (opcional), cama, mesilla con lámpara."""
    night = p.get("night", True)
    wall = "#3B3F78" if night else "#AFC8F2"
    ctx.rectangle(-M, -M, W + 2 * M, H + 2 * M)
    ctx.set_source(linear_grad(ctx, 0, 0, 0, H, [(0, wall), (1, darken(wall, 0.25))]))
    ctx.fill()
    for k in range(-4, 12):  # papel pintado de rayas
        ctx.rectangle(k * 120, -M, 50, 1400 + M)
    ctx.set_source_rgba(1, 1, 1, 0.05)
    ctx.fill()
    # ventana
    rrect(ctx, 610, 260, 380, 460, 14)
    fill_stroke(ctx, "#101433" if night else "#8FD3FF", OUT)
    with saved(ctx):
        rrect(ctx, 610, 260, 380, 460, 14)
        ctx.clip()
        rng = np.random.default_rng(5)
        if night:
            for i in range(30):
                circle(ctx, rng.uniform(610, 990), rng.uniform(260, 720), rng.uniform(2, 5))
                ctx.set_source_rgba(1, 1, 0.9, 0.5 + 0.5 * math.sin(t * 3 + i))
                ctx.fill()
            if p.get("moon", True):
                circle(ctx, 880, 370, 60)
                fill_stroke(ctx, (1, 0.97, 0.85), OUT * 0.7)
        else:
            _cloud(ctx, 680 + (t * 20) % 300, 400, 0.6)
    limb(ctx, [(800, 260), (800, 720)], 14, "#E8D9B5", out=OUT * 0.5)
    limb(ctx, [(610, 490), (990, 490)], 14, "#E8D9B5", out=OUT * 0.5)
    # cortinas
    for sx_, d in ((590, -1), (1010, 1)):
        ctx.move_to(sx_, 240)
        ctx.curve_to(sx_ + d * 60, 450, sx_ - d * 20, 600, sx_ + d * 50, 760)
        ctx.line_to(sx_ + d * 110, 760)
        ctx.line_to(sx_ + d * 110, 240)
        ctx.close_path()
        fill_stroke(ctx, "#E85D75", OUT)
    # póster
    with saved(ctx):
        ctx.translate(250, 450)
        ctx.rotate(-0.05)
        rrect(ctx, -120, -150, 240, 300, 8)
        fill_stroke(ctx, PAL["yellow"], OUT)
        text(ctx, "?", 0, 0, 160, color=PAL["red"], outline=7, shadow_off=0)
    # suelo de madera
    ctx.rectangle(-M, 1400, W + 2 * M, H)
    fill_stroke(ctx, "#8A5A3B", OUT)
    for k in range(6):
        ctx.move_to(-M, 1470 + k * 90)
        ctx.line_to(W + M, 1470 + k * 90)
    ctx.set_source_rgba(0, 0, 0, 0.2)
    ctx.set_line_width(4)
    ctx.stroke()
    if p.get("bed", True):
        rrect(ctx, 520, 1140, 640, 260, 30)  # cama
        fill_stroke(ctx, "#F2F2F7", OUT)
        rrect(ctx, 520, 1230, 640, 200, 30)
        fill_stroke(ctx, "#5B8DEF", OUT)
        rrect(ctx, 560, 1150, 180, 90, 40)
        fill_stroke(ctx, "#FFFFFF", OUT)
        rrect(ctx, 1000, 1000, 60, 420, 20)
        fill_stroke(ctx, "#8A5A3B", OUT)
    # mesilla y lámpara
    rrect(ctx, 60, 1180, 220, 220, 14)
    fill_stroke(ctx, "#A06A44", OUT)
    if night:
        circle(ctx, 170, 1060, 200)
        ctx.set_source(radial_grad(ctx, 170, 1060, 10, 200, [(0, (1, 0.9, 0.6), 0.45), (1, (1, 0.9, 0.6), 0)]))
        ctx.fill()
    ctx.move_to(100, 1080)
    ctx.line_to(240, 1080)
    ctx.line_to(205, 990)
    ctx.line_to(135, 990)
    ctx.close_path()
    fill_stroke(ctx, "#FFD86B", OUT)
    limb(ctx, [(170, 1080), (170, 1180)], 12, (0.4, 0.3, 0.2), out=OUT * 0.5)


def bg_village(ctx, t, p):
    """Aldea medieval con castillo en la colina; mode = day | plague (noche, niebla, cruces)."""
    mode = p.get("mode", "day")
    plague = mode == "plague"
    if plague:
        _sky(ctx, (0.12, 0.12, 0.18), (0.35, 0.33, 0.35))
    else:
        _sky(ctx, (0.45, 0.72, 0.98), (0.85, 0.93, 1))
        circle(ctx, 860, 300, 85)
        fill_stroke(ctx, PAL["yellow"], OUT)
        _cloud(ctx, (120 + t * 15) % 1300 - 200, 260, 0.9)
    # colina con castillo
    ctx.move_to(-M, 1000)
    ctx.curve_to(150, 700, 500, 640, 760, 760)
    ctx.curve_to(900, 820, 1000, 900, W + M, 950)
    ctx.line_to(W + M, H + M)
    ctx.line_to(-M, H + M)
    ctx.close_path()
    fill_stroke(ctx, "#5F8F4A" if not plague else "#3C4A3A", OUT)
    cx, cy = 430, 690
    stone = "#B9B3A6" if not plague else "#6E6A66"
    for dx, h in ((-170, 260), (170, 260)):
        rrect(ctx, cx + dx - 55, cy - h, 110, h, 6)
        fill_stroke(ctx, stone, OUT)
        for k in range(3):
            rrect(ctx, cx + dx - 55 + k * 40, cy - h - 30, 30, 32, 4)
            fill_stroke(ctx, stone, OUT * 0.6)
        ctx.move_to(cx + dx - 65, cy - h - 28)
        ctx.line_to(cx + dx, cy - h - 130)
        ctx.line_to(cx + dx + 65, cy - h - 28)
        ctx.close_path()
        fill_stroke(ctx, "#B5532F" if not plague else "#4A2E2A", OUT)
    rrect(ctx, cx - 140, cy - 180, 280, 180, 6)
    fill_stroke(ctx, stone, OUT)
    for k in range(6):
        rrect(ctx, cx - 140 + k * 48, cy - 210, 34, 34, 4)
        fill_stroke(ctx, stone, OUT * 0.6)
    ctx.move_to(cx - 45, cy)
    ctx.line_to(cx - 45, cy - 80)
    ctx.arc(cx, cy - 80, 45, math.pi, 0)
    ctx.line_to(cx + 45, cy)
    ctx.close_path()
    fill_stroke(ctx, "#5A3A28", OUT * 0.8)
    if not plague:  # banderín
        ctx.move_to(cx + 170, cy - 390)
        ctx.line_to(cx + 170, cy - 470)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(5)
        ctx.stroke()
        ctx.move_to(cx + 170, cy - 470)
        ctx.line_to(cx + 250, cy - 450 + 8 * math.sin(t * 4))
        ctx.line_to(cx + 170, cy - 430)
        ctx.close_path()
        fill_stroke(ctx, PAL["red"], 3)
    # casas con tejado de paja
    for hx, hy, s in ((150, 1290, 1.0), (520, 1340, 0.9), (870, 1280, 1.05)):
        with saved(ctx):
            ctx.translate(hx, hy)
            ctx.scale(s, s)
            rrect(ctx, -130, -170, 260, 170, 6)
            fill_stroke(ctx, "#E3CFA4" if not plague else "#8D8470", OUT)
            for k in (-1, 1):  # entramado de madera
                ctx.move_to(k * 130, -170)
                ctx.line_to(-k * 20, 0)
            ctx.set_source_rgb(0.4, 0.28, 0.18)
            ctx.set_line_width(10)
            ctx.stroke()
            ctx.move_to(-165, -160)
            ctx.line_to(0, -300)
            ctx.line_to(165, -160)
            ctx.close_path()
            fill_stroke(ctx, "#D6A84E" if not plague else "#6B5A3A", OUT)
            rrect(ctx, -30, -100, 60, 100, 6)
            fill_stroke(ctx, "#6B3D24", OUT * 0.7)
    # camino de tierra
    ctx.move_to(380, H + M)
    ctx.curve_to(460, 1500, 520, 1420, 540, 1400)
    ctx.line_to(620, 1400)
    ctx.curve_to(640, 1500, 760, 1700, 820, H + M)
    ctx.close_path()
    fill_stroke(ctx, "#C9A86A" if not plague else "#6E5E46", OUT)
    if plague:
        ctx.rectangle(-M, 900, W + 2 * M, H)
        ctx.set_source(linear_grad(ctx, 0, 900, 0, H, [(0, (0.6, 0.65, 0.6), 0), (1, (0.6, 0.65, 0.6), 0.5)]))
        ctx.fill()
        for i in range(4):  # niebla que se desliza
            x = (i * 400 + t * 60) % (W + 800) - 400
            blob(ctx, x, 1250 + i * 120, 260, n=9, wobble=0.25, seed=i, t=t * 0.2)
            ctx.set_source_rgba(0.8, 0.85, 0.8, 0.25)
            ctx.fill()


def bg_beach(ctx, t, p):
    """Playa: el nivel del mar sube y baja con la marea (`tide` 0..1 de amplitud)."""
    night = p.get("night", False)
    if night:
        _sky(ctx, (0.05, 0.05, 0.15), (0.15, 0.13, 0.3))
    else:
        _sky(ctx, (0.4, 0.75, 1), (0.85, 0.95, 1))
        circle(ctx, 850, 330, 80)
        fill_stroke(ctx, PAL["yellow"], OUT)
    amp = p.get("tide", 1.0) * 160
    lvl = 1150 - amp * math.sin(t * p.get("tide_speed", 1.2))
    # arena
    ctx.move_to(-M, 1050)
    ctx.curve_to(300, 1000, 700, 1060, W + M, 1020)
    ctx.line_to(W + M, H + M)
    ctx.line_to(-M, H + M)
    ctx.close_path()
    fill_stroke(ctx, "#F2D49B", OUT)
    # mar (diagonal: sube por la arena)
    for k in range(3):
        y0 = lvl + k * 70
        ctx.move_to(-M, H + M)
        ctx.line_to(-M, y0 + 300)
        for x in range(-M, W + M + 1, 40):
            ctx.line_to(x, y0 + 300 - x * 0.35 + 14 * math.sin(x * 0.02 + t * 3 + k))
        ctx.line_to(W + M, H + M)
        ctx.close_path()
        fill_stroke(ctx, mix((0.3, 0.7, 0.95), (0.1, 0.35, 0.7), k / 2), OUT * (0.9 if k == 0 else 0.5))
    # marca de la marea alta
    if p.get("mark", True):
        ctx.set_dash([24, 18])
        ctx.move_to(-M, 1150 - 160 + 300 + 350 * 0.35)
        for x in range(-M, W + M + 1, 40):
            ctx.line_to(x, 1150 - 160 + 300 - x * 0.35)
        ctx.set_source_rgba(1, 1, 1, 0.8)
        ctx.set_line_width(8)
        ctx.stroke()
        ctx.set_dash([])
    # sombrilla
    limb(ctx, [(220, 1200), (260, 900)], 12, (0.95, 0.95, 0.95), out=OUT * 0.6)
    ctx.move_to(80, 920)
    ctx.curve_to(150, 780, 380, 760, 440, 880)
    ctx.close_path()
    fill_stroke(ctx, PAL["red"], OUT)


def bg_night_sky(ctx, t, p):
    """Cielo nocturno sobre un horizonte; con o sin Luna."""
    _sky(ctx, (0.04, 0.05, 0.16), (0.16, 0.15, 0.35))
    rng = np.random.default_rng(42)
    for i in range(160):
        x, y = rng.uniform(-M, W + M), rng.uniform(-M, 1300)
        tw = 0.5 + 0.5 * math.sin(t * rng.uniform(1, 4) + i)
        circle(ctx, x, y, rng.uniform(1.5, 4) * (0.6 + 0.4 * tw))
        ctx.set_source_rgba(1, 1, 0.9, 0.4 + 0.6 * tw)
        ctx.fill()
    if p.get("moon", True):
        _moon(ctx, {"x": 0, "y": 0, "r": 140, "abs": True}, t, 700, 420)
    ctx.move_to(-M, 1350)
    ctx.curve_to(300, 1250, 700, 1320, W + M, 1260)
    ctx.line_to(W + M, H + M)
    ctx.line_to(-M, H + M)
    ctx.close_path()
    fill_stroke(ctx, "#1C2A3A", OUT)


# ============================================================================ PROPS
def _moon(ctx, p, t, ox=0, oy=0):
    r = p.get("r", 140)
    circle(ctx, ox, oy, r * 1.6)
    ctx.set_source(radial_grad(ctx, ox, oy, r * 0.9, r * 1.6, [(0, (1, 1, 0.9), 0.35), (1, (1, 1, 0.9), 0)]))
    ctx.fill()
    circle(ctx, ox, oy, r)
    fill_stroke(ctx, (0.96, 0.95, 0.88), OUT)
    for cx, cy, cr in ((-0.3, -0.25, 0.22), (0.3, 0.1, 0.16), (-0.05, 0.4, 0.12), (0.35, -0.4, 0.09)):
        circle(ctx, ox + cx * r, oy + cy * r, cr * r)
        ctx.set_source_rgba(0.75, 0.74, 0.68, 0.9)
        ctx.fill()
    if p.get("face", True):
        for s in (-1, 1):
            circle(ctx, ox + s * r * 0.28, oy - r * 0.05, r * 0.07)
            ctx.set_source_rgb(*INK)
            ctx.fill()
        ctx.arc(ox, oy + r * 0.15, r * 0.25, 0.25, math.pi - 0.25)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(r * 0.05)
        ctx.stroke()


def _eclipse(ctx, p, t):
    """Eclipse total: corona del Sol tras un disco oscuro."""
    r = p.get("r", 160)
    for k in range(18):
        a = k * math.pi / 9 + t * 0.2
        ctx.move_to(0, 0)
        ctx.line_to(r * 2.1 * math.cos(a - 0.05), r * 2.1 * math.sin(a - 0.05))
        ctx.line_to(r * 2.1 * math.cos(a + 0.05), r * 2.1 * math.sin(a + 0.05))
        ctx.close_path()
    ctx.set_source_rgba(1, 0.9, 0.5, 0.35)
    ctx.fill()
    circle(ctx, 0, 0, r * 1.15)
    ctx.set_source(radial_grad(ctx, 0, 0, r, r * 1.4, [(0, (1, 1, 0.9), 1), (1, (1, 0.85, 0.4), 0)]))
    ctx.fill()
    circle(ctx, 0, 0, r)
    fill_stroke(ctx, (0.06, 0.06, 0.1), OUT)


def _top(ctx, p, t):
    """Peonza: estable (`wobble` 0) o tambaleándose."""
    wob = p.get("wobble", 0.0)
    with saved(ctx):
        ctx.rotate(wob * 0.5 * math.sin(t * 3))
        ctx.move_to(0, 160)
        ctx.curve_to(-40, 100, -170, 20, -160, -40)
        ctx.curve_to(-120, -110, 120, -110, 160, -40)
        ctx.curve_to(170, 20, 40, 100, 0, 160)
        ctx.close_path()
        fill_stroke(ctx, PAL["red"], OUT)
        with saved(ctx):  # franjas que giran
            ctx.move_to(0, 160)
            ctx.curve_to(-40, 100, -170, 20, -160, -40)
            ctx.curve_to(-120, -110, 120, -110, 160, -40)
            ctx.curve_to(170, 20, 40, 100, 0, 160)
            ctx.close_path()
            ctx.clip()
            for k in range(-4, 5):
                x = ((k * 60 + t * 400) % 480) - 240
                ctx.rectangle(x, -120, 26, 300)
            ctx.set_source_rgba(*PAL["yellow"], 0.9)
            ctx.fill()
        limb(ctx, [(0, -60), (0, -170)], 18, "#8B5A2B", out=OUT * 0.6)
    ellipse(ctx, 0, 175, 90, 14)
    ctx.set_source_rgba(0, 0, 0, 0.25)
    ctx.fill()


def _brain(ctx, p, t):
    """Cerebro; `dirt` 0..1 añade «basura» acumulada; `clean` muestra burbujas de limpieza."""
    pulse = 1 + 0.03 * math.sin(t * 4)
    with saved(ctx):
        ctx.scale(pulse, pulse)
        for k, (x, y, r) in enumerate(((-90, -40, 110), (60, -60, 120), (-20, 50, 120), (110, 40, 90), (-120, 60, 80))):
            blob(ctx, x, y, r, n=9, wobble=0.12, seed=k)
        fill_stroke(ctx, "#FF9EB5", OUT)
        ctx.set_source_rgba(*INK, 0.5)
        ctx.set_line_width(6)
        for k in range(6):
            ctx.move_to(-150 + k * 50, -110 + (k % 2) * 30)
            ctx.curve_to(-130 + k * 50, -40, -170 + k * 50, 20, -140 + k * 50, 90)
        ctx.stroke()
    dirt = p.get("dirt", 0.0)
    rng = np.random.default_rng(3)
    for i in range(int(16 * dirt)):
        blob(ctx, rng.uniform(-160, 160), rng.uniform(-110, 110), rng.uniform(10, 22), n=6, seed=i)
        ctx.set_source_rgba(0.45, 0.4, 0.2, 0.85)
        ctx.fill()
    if p.get("clean"):
        for i in range(12):
            ph = (t * 0.8 + i / 12) % 1
            circle(ctx, rng.uniform(-170, 170), 120 - ph * 300, 10 + 6 * (1 - ph))
            ctx.set_source_rgba(0.6, 0.9, 1, 0.8 * (1 - ph))
            ctx.set_line_width(5)
            ctx.stroke()


def _coffee(ctx, p, t):
    for i in range(3):
        ph = (t * 0.7 + i * 0.33) % 1
        x0 = -30 + i * 30
        ctx.move_to(x0, -110 - ph * 120)
        ctx.curve_to(x0 + 20, -140 - ph * 120, x0 - 20, -170 - ph * 120, x0, -200 - ph * 120)
        ctx.set_source_rgba(1, 1, 1, 0.7 * (1 - ph))
        ctx.set_line_width(8)
        ctx.stroke()
    ctx.move_to(-80, -90)
    ctx.line_to(80, -90)
    ctx.line_to(60, 80)
    ctx.line_to(-60, 80)
    ctx.close_path()
    fill_stroke(ctx, (1, 1, 1), OUT)
    ctx.arc(95, -10, 38, -math.pi / 2, math.pi / 2)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(22)
    ctx.stroke()
    ctx.arc(95, -10, 38, -math.pi / 2, math.pi / 2)
    ctx.set_source_rgb(1, 1, 1)
    ctx.set_line_width(10)
    ctx.stroke()
    ellipse(ctx, 0, -90, 80, 16)
    fill_stroke(ctx, (0.4, 0.25, 0.15), OUT * 0.6)
    n = p.get("count")
    if n:
        text(ctx, f"x{n}", 0, 10, 60, color=PAL["red"], outline=0, shadow_off=0)


def _smartphone(ctx, p, t):
    rrect(ctx, -90, -170, 180, 340, 28)
    fill_stroke(ctx, (0.12, 0.12, 0.15), OUT)
    rrect(ctx, -75, -150, 150, 290, 16)
    ctx.set_source(linear_grad(ctx, 0, -150, 0, 140, [(0, "#6C63FF"), (1, "#FF6B9A")]))
    ctx.fill()
    for k in range(3):
        rrect(ctx, -55, -120 + k * 80, 110, 60, 10)
        ctx.set_source_rgba(1, 1, 1, 0.35 + 0.2 * math.sin(t * 4 + k))
        ctx.fill()
    if p.get("glow", True):
        circle(ctx, 0, 0, 260)
        ctx.set_source(radial_grad(ctx, 0, 0, 40, 260, [(0, (0.6, 0.7, 1), 0.3), (1, (0.6, 0.7, 1), 0)]))
        ctx.fill()


def _car(ctx, p, t):
    c = col(p.get("color", "#2EC4B6"))
    rrect(ctx, -260, -40, 520, 110, 40)
    fill_stroke(ctx, c, OUT)
    ctx.move_to(-150, -40)
    ctx.curve_to(-120, -150, 120, -150, 160, -40)
    ctx.close_path()
    fill_stroke(ctx, c, OUT)
    rrect(ctx, -110, -120, 100, 70, 14)
    fill_stroke(ctx, (0.7, 0.9, 1), OUT * 0.6)
    rrect(ctx, 10, -120, 100, 70, 14)
    fill_stroke(ctx, (0.7, 0.9, 1), OUT * 0.6)
    for x in (-160, 160):
        circle(ctx, x, 70, 50)
        fill_stroke(ctx, (0.2, 0.2, 0.22), OUT)
        circle(ctx, x, 70, 20)
        fill_stroke(ctx, PAL["metal"], 4)
    circle(ctx, 250, 0, 20)
    fill_stroke(ctx, (1, 0.95, 0.6), OUT * 0.5)


def _zzz(ctx, p, t):
    for i in range(3):
        ph = (t * 0.6 + i * 0.33) % 1
        text(ctx, "Z", 40 * i + ph * 60, -ph * 200, 60 + i * 20, color="white", outline=6, alpha=1 - ph,
             shadow_off=0)


def _ghost(ctx, p, t):
    """Alucinación: criatura translúcida y ondulante."""
    c = col(p.get("color", "#B388FF"))
    a = p.get("alpha", 0.75) * (0.7 + 0.3 * math.sin(t * 3 + p.get("seed", 0)))
    with saved(ctx):
        ctx.translate(20 * math.sin(t * 1.5 + p.get("seed", 0)), 15 * math.sin(t * 2.1))
        ctx.move_to(-90, 80)
        ctx.curve_to(-110, -150, 110, -150, 90, 80)
        for k in range(4):
            x0 = 90 - k * 45
            ctx.curve_to(x0 - 10, 110 + 15 * math.sin(t * 5 + k), x0 - 30, 110, x0 - 45, 80)
        ctx.close_path()
        ctx.set_source_rgba(*c, a)
        ctx.fill_preserve()
        ctx.set_source_rgba(*INK, a)
        ctx.set_line_width(OUT)
        ctx.stroke()
        for s in (-1, 1):
            ellipse(ctx, s * 32, -30, 16, 24)
            ctx.set_source_rgba(*INK, a)
            ctx.fill()
        ellipse(ctx, 0, 25, 20, 14)
        ctx.fill()


def _trophy(ctx, p, t):
    ctx.move_to(-120, -160)
    ctx.line_to(120, -160)
    ctx.curve_to(120, 0, 60, 40, 0, 50)
    ctx.curve_to(-60, 40, -120, 0, -120, -160)
    ctx.close_path()
    fill_stroke(ctx, "#FFD23F", OUT)
    for s in (-1, 1):
        ctx.arc(s * 125, -100, 45, -math.pi / 2 if s > 0 else math.pi / 2, math.pi / 2 if s > 0 else 3 * math.pi / 2)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(26)
        ctx.stroke()
    rrect(ctx, -25, 50, 50, 70, 6)
    fill_stroke(ctx, "#E0A93A", OUT)
    rrect(ctx, -90, 120, 180, 50, 10)
    fill_stroke(ctx, "#6B3D24", OUT)
    text(ctx, p.get("text", "1"), 0, -70, 90, color=INK, outline=0, shadow_off=0)
    star(ctx, 80, -200, 18 * (0.6 + 0.4 * math.sin(t * 6)), n=4, inner=0.3)
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill()


def _food(ctx, p, t):
    """Alimento: potato | tomato | chocolate | bread | beer | water."""
    k = p.get("kind", "potato")
    if k == "potato":
        blob(ctx, 0, 0, 90, n=8, wobble=0.18, seed=2)
        fill_stroke(ctx, "#C9965A", OUT)
        for x, y in ((-30, -20), (25, 15), (5, -45)):
            circle(ctx, x, y, 7)
            ctx.set_source_rgb(0.5, 0.35, 0.2)
            ctx.fill()
    elif k == "tomato":
        circle(ctx, 0, 10, 90)
        fill_stroke(ctx, "#E8392F", OUT)
        star(ctx, 0, -70, 40, n=5, inner=0.4)
        fill_stroke(ctx, "#3FA34D", OUT * 0.6)
        ellipse(ctx, -30, -20, 20, 12, -0.5)
        ctx.set_source_rgba(1, 1, 1, 0.6)
        ctx.fill()
    elif k == "chocolate":
        rrect(ctx, -90, -110, 180, 220, 12)
        fill_stroke(ctx, "#5C3317", OUT)
        for i in range(2):
            for j in range(3):
                rrect(ctx, -75 + i * 80, -95 + j * 70, 70, 60, 8)
                fill_stroke(ctx, "#7A4421", OUT * 0.4)
    elif k == "bread":
        ellipse(ctx, 0, 0, 120, 70)
        fill_stroke(ctx, "#D9A35B", OUT)
        for x in (-50, 0, 50):
            ctx.move_to(x - 20, -40)
            ctx.line_to(x + 20, 20)
        ctx.set_source_rgb(*darken("#D9A35B", 0.3))
        ctx.set_line_width(8)
        ctx.stroke()
    elif k == "beer":
        rrect(ctx, -70, -100, 140, 200, 16)
        fill_stroke(ctx, "#F2B33D", OUT)
        blob(ctx, 0, -100, 75, n=8, wobble=0.15, seed=1)
        fill_stroke(ctx, (1, 1, 0.95), OUT * 0.8)
        ctx.arc(80, 0, 40, -math.pi / 2, math.pi / 2)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(22)
        ctx.stroke()
    elif k == "water":
        ctx.move_to(0, -110)
        ctx.curve_to(80, 0, 80, 100, 0, 100)
        ctx.curve_to(-80, 100, -80, 0, 0, -110)
        ctx.close_path()
        fill_stroke(ctx, "#5CC8FF", OUT)


def _rat(ctx, p, t):
    run = math.sin(t * 14)
    ctx.move_to(-100, 10)
    ctx.curve_to(-180, 0, -220, -40, -260, -20 + 10 * run)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(12)
    ctx.stroke()
    ctx.move_to(-100, 10)
    ctx.curve_to(-180, 0, -220, -40, -260, -20 + 10 * run)
    ctx.set_source_rgb(1, 0.6, 0.65)
    ctx.set_line_width(5)
    ctx.stroke()
    ellipse(ctx, 0, 0, 120, 60)
    fill_stroke(ctx, "#8A8580", OUT)
    ctx.move_to(90, -30)
    ctx.line_to(170, 10)
    ctx.line_to(90, 40)
    ctx.close_path()
    fill_stroke(ctx, "#8A8580", OUT)
    circle(ctx, 172, 10, 10)
    ctx.set_source_rgb(1, 0.55, 0.6)
    ctx.fill()
    circle(ctx, 70, -50, 30)
    fill_stroke(ctx, "#B5AFA8", OUT)
    circle(ctx, 110, -10, 8)
    ctx.set_source_rgb(*INK)
    ctx.fill()
    for x in (-60, 40):
        limb(ctx, [(x, 50), (x + 15 * run, 80)], 12, "#8A8580", out=OUT * 0.5)
    if p.get("fleas"):
        rng = np.random.default_rng(4)
        for i in range(8):
            circle(ctx, rng.uniform(-100, 100) + 10 * math.sin(t * 9 + i), -70 - abs(40 * math.sin(t * 6 + i)), 6)
            ctx.set_source_rgb(*INK)
            ctx.fill()


def _crane(ctx, p, t):
    """Grúa de obra (para el mito del caballero)."""
    limb(ctx, [(0, 300), (0, -300)], 30, PAL["yellow"], out=OUT)
    limb(ctx, [(-120, -300), (360, -300)], 26, PAL["yellow"], out=OUT)
    for k in range(6):
        ctx.move_to(-15, 300 - k * 100)
        ctx.line_to(15, 250 - k * 100)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(5)
    ctx.stroke()
    sw = 15 * math.sin(t * 2)
    ctx.move_to(320, -300)
    ctx.line_to(320 + sw, 0)
    ctx.set_line_width(5)
    ctx.stroke()
    ctx.arc(320 + sw, 20, 20, 0, math.pi)
    ctx.set_line_width(8)
    ctx.stroke()


def _bathhouse(ctx, p, t):
    rrect(ctx, -330, -200, 660, 260, 10)
    fill_stroke(ctx, "#E3CFA4", OUT)
    ctx.move_to(-360, -190)
    ctx.line_to(0, -330)
    ctx.line_to(360, -190)
    ctx.close_path()
    fill_stroke(ctx, "#B5532F", OUT)
    rrect(ctx, -280, 40, 560, 120, 30)
    fill_stroke(ctx, "#6B3D24", OUT)
    rrect(ctx, -250, 60, 500, 70, 24)
    ctx.set_source_rgb(0.45, 0.78, 0.95)
    ctx.fill()
    for i in range(4):
        ph = (t * 0.6 + i * 0.25) % 1
        x0 = -180 + i * 120
        ctx.move_to(x0, 30 - ph * 140)
        ctx.curve_to(x0 + 25, -10 - ph * 140, x0 - 25, -40 - ph * 140, x0, -80 - ph * 140)
        ctx.set_source_rgba(1, 1, 1, 0.75 * (1 - ph))
        ctx.set_line_width(10)
        ctx.stroke()
    text(ctx, p.get("label", "BAÑOS"), 0, -130, 64, color=INK, outline=0, shadow_off=0)


def _wifi(ctx, p, t):
    for k, r in enumerate((60, 110, 160)):
        ctx.arc(0, 60, r, -math.pi * 0.78, -math.pi * 0.22)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(38)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()
        ctx.arc(0, 60, r, -math.pi * 0.78, -math.pi * 0.22)
        ctx.set_source_rgb(*PAL["blue"])
        ctx.set_line_width(22)
        ctx.stroke()
    circle(ctx, 0, 60, 22)
    fill_stroke(ctx, PAL["blue"], OUT)


def _coral(ctx, p, t):
    """Corales; con `spawn` sueltan nubes de huevos hacia arriba."""
    cols = ["#FF6B9A", "#FF9F1C", "#B388FF", "#2EC4B6"]
    for i in range(5):
        x = -320 + i * 160
        c = cols[i % 4]
        for b in range(3):
            a = -math.pi / 2 + (b - 1) * 0.5
            ln = 160 + 30 * b
            ex, ey = x + ln * math.cos(a), ln * math.sin(a)
            limb(ctx, [(x, 60), ((x + ex) / 2, ey / 2 + 20), (ex, ey)], 28, c, out=OUT * 0.7)
            circle(ctx, ex, ey, 22)
            fill_stroke(ctx, lighten(c, 0.3), OUT * 0.6)
    if p.get("spawn"):
        rng = np.random.default_rng(6)
        for i in range(60):
            ph = (t * 0.35 + rng.random()) % 1
            circle(ctx, rng.uniform(-360, 360) + 20 * math.sin(t + i), 40 - ph * 900, rng.uniform(5, 11))
            ctx.set_source_rgba(1, 0.75, 0.85, 1 - ph)
            ctx.fill()


BACKGROUNDS.update({"bedroom": bg_bedroom, "village": bg_village, "beach": bg_beach, "night_sky": bg_night_sky})
PROPS.update({"moon": _moon, "eclipse": _eclipse, "top": _top, "brain": _brain, "coffee": _coffee,
              "smartphone": _smartphone, "car": _car, "zzz": _zzz, "ghost": _ghost, "trophy": _trophy,
              "food": _food, "rat": _rat, "crane": _crane, "bathhouse": _bathhouse, "wifi": _wifi, "coral": _coral})
