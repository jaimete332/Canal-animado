"""Ampliación del catálogo visual: Marte detallado, mundo submarino, interior de ballena,
cohete, base marciana, cultivos, robot explorador, ballenas, calamar, ámbar gris, periódico...

Se registra automáticamente en BACKGROUNDS y PROPS al importar fabrica.visuals.world.
"""
from __future__ import annotations

import math

import cairo
import numpy as np

from .draw import (INK, OUT, PAL, blob, circle, clamp, col, darken, ellipse, fill_stroke, lerp, lighten,
                   limb, linear_grad, mix, noise1, radial_grad, rrect, saved, smooth_closed, star, text)
from .world import BACKGROUNDS, H, M, PROPS, W, _pebbles, _sky


# ============================================================================
# FONDOS
# ============================================================================
def bg_mars(ctx, t, p):
    """Marte: variantes normal | dust (tormenta) | blue_sunset (atardecer azul real)."""
    mode = p.get("mode", "normal")
    g = p.get("ground", 1250)
    if mode == "blue_sunset":
        _sky(ctx, (0.10, 0.10, 0.22), (0.45, 0.42, 0.42))
        sx, sy = 540, g - 520
        circle(ctx, sx, sy, 520)
        ctx.set_source(radial_grad(ctx, sx, sy, 20, 520, [(0, (0.75, 0.88, 1.0), 0.95), (0.35, (0.35, 0.6, 0.95), 0.55),
                                                         (1, (0.3, 0.4, 0.7), 0)]))
        ctx.fill()
        circle(ctx, sx, sy, 42)
        ctx.set_source_rgb(0.92, 0.97, 1)
        ctx.fill()
    else:
        _sky(ctx, "#D98A5F", "#F2C49B")
        circle(ctx, 830, 330, 62)
        fill_stroke(ctx, (1, 0.95, 0.85), OUT)
        # lunas Fobos y Deimos
        for x, y, r in ((200, 260, 22), (330, 420, 13)):
            blob(ctx, x, y, r, n=7, wobble=0.15, seed=int(x))
            fill_stroke(ctx, (0.75, 0.68, 0.62), OUT * 0.6)
    # Monte Olimpo al fondo
    ctx.move_to(-M, g - 160)
    ctx.curve_to(150, g - 230, 300, g - 420, 520, g - 430)
    ctx.curve_to(720, g - 420, 850, g - 240, W + M, g - 180)
    ctx.line_to(W + M, g)
    ctx.line_to(-M, g)
    ctx.close_path()
    fill_stroke(ctx, "#B9542A" if mode != "blue_sunset" else "#5C3A2E", OUT)
    # suelo
    ctx.move_to(-M, g - 40)
    for x in range(-M, W + M + 1, 80):
        ctx.line_to(x, g - 40 + 18 * math.sin(x * 0.01))
    ctx.line_to(W + M, H + M)
    ctx.line_to(-M, H + M)
    ctx.close_path()
    ground = "#C65A28" if mode != "blue_sunset" else "#6E3F2C"
    fill_stroke(ctx, ground, OUT)
    for cx, cy, r in ((160, g + 160, 90), (820, g + 330, 130), (420, g + 520, 70)):
        ellipse(ctx, cx, cy, r, r * 0.3)
        fill_stroke(ctx, darken(ground, 0.2), OUT * 0.7)
        ellipse(ctx, cx, cy - r * 0.05, r * 0.8, r * 0.18)
        ctx.set_source_rgba(*darken(ground, 0.35), 1)
        ctx.fill()
    _pebbles(ctx, g + 40, H + 200, seed=6, tint=col(darken(ground, 0.3)), density=0.7)
    if mode == "dust":
        ctx.rectangle(-M, -M, W + 2 * M, H + 2 * M)
        ctx.set_source_rgba(0.78, 0.45, 0.25, 0.55 + 0.1 * math.sin(t * 2))
        ctx.fill()
        rng = np.random.default_rng(12)
        for i in range(120):
            sp = rng.uniform(600, 1300)
            x = (rng.uniform(0, W + 800) + t * sp) % (W + 800) - 400
            y = rng.uniform(-200, H + 200) + 30 * math.sin(t * 3 + i)
            ln = rng.uniform(30, 110)
            ctx.move_to(x, y)
            ctx.line_to(x + ln, y + ln * 0.15)
            ctx.set_source_rgba(1, 0.8, 0.6, rng.uniform(0.3, 0.8))
            ctx.set_line_width(rng.uniform(3, 8))
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.stroke()
        for i in range(5):  # remolinos de polvo
            x = (i * 300 + t * 500) % (W + 600) - 300
            blob(ctx, x, 500 + i * 250, 260, n=9, wobble=0.3, seed=i, t=t)
            ctx.set_source_rgba(0.85, 0.55, 0.32, 0.35)
            ctx.fill()


def bg_underwater(ctx, t, p):
    deep = p.get("deep", 0.0)
    top = mix((0.25, 0.75, 0.95), (0.05, 0.15, 0.35), deep)
    bot = mix((0.05, 0.3, 0.6), (0.01, 0.03, 0.12), deep)
    _sky(ctx, top, bot)
    # rayos de luz
    if deep < 0.7:
        for i in range(7):
            x = 80 + i * 170 + 40 * math.sin(t * 0.5 + i)
            ctx.move_to(x - 30, -M)
            ctx.line_to(x + 30, -M)
            ctx.line_to(x + 160, H)
            ctx.line_to(x + 40, H)
            ctx.close_path()
            ctx.set_source_rgba(1, 1, 1, 0.07 * (1 - deep))
            ctx.fill()
    # superficie ondulada arriba
    if p.get("surface", True) and deep < 0.3:
        ctx.move_to(-M, -M)
        for x in range(-M, W + M + 1, 40):
            ctx.line_to(x, 90 + 14 * math.sin(x * 0.015 + t * 2))
        ctx.line_to(W + M, -M)
        ctx.close_path()
        ctx.set_source_rgba(0.7, 0.95, 1, 0.6)
        ctx.fill()
    # fondo marino
    g = p.get("floor", 1700)
    if g < H + 200:
        ctx.move_to(-M, g)
        for x in range(-M, W + M + 1, 90):
            ctx.line_to(x, g + 25 * math.sin(x * 0.008))
        ctx.line_to(W + M, H + M)
        ctx.line_to(-M, H + M)
        ctx.close_path()
        fill_stroke(ctx, mix("#E9C98B", "#2B3A55", deep), OUT)
        for i, x in enumerate((90, 230, 860, 990)):
            sw = 25 * math.sin(t * 1.5 + i)
            for w, c in ((26, INK), (16, mix((0.25, 0.7, 0.35), (0.1, 0.3, 0.3), deep))):
                ctx.move_to(x, g + 10)
                ctx.curve_to(x + sw, g - 120, x - sw, g - 220, x + sw * 1.5, g - 320 - 40 * (i % 2))
                ctx.set_source_rgb(*col(c))
                ctx.set_line_width(w)
                ctx.set_line_cap(cairo.LINE_CAP_ROUND)
                ctx.stroke()
    # peces
    if p.get("fish", True):
        rng = np.random.default_rng(21)
        for i in range(7):
            d = 1 if i % 2 else -1
            sp = rng.uniform(80, 160)
            x = (rng.uniform(0, W + 400) + d * t * sp) % (W + 400) - 200
            y = rng.uniform(300, 1500) + 20 * math.sin(t * 2 + i)
            _fish(ctx, x, y, rng.uniform(0.5, 1.0), d, ["#FFB347", "#FF6B6B", "#FFD23F", "#9D7BFF"][i % 4], t)
    # burbujas
    rng = np.random.default_rng(3)
    for i in range(25):
        ph = (t * rng.uniform(0.2, 0.5) + rng.random()) % 1
        x = rng.uniform(0, W) + 12 * math.sin(t * 3 + i)
        y = H + 40 - ph * (H + 80)
        circle(ctx, x, y, rng.uniform(5, 14))
        ctx.set_source_rgba(1, 1, 1, 0.5)
        ctx.set_line_width(3)
        ctx.stroke()


def _fish(ctx, x, y, s, d, c, t):
    with saved(ctx):
        ctx.translate(x, y)
        ctx.scale(s * d, s)
        wag = 0.25 * math.sin(t * 10 + x)
        ctx.move_to(-45, 0)
        ctx.line_to(-80, -28 + wag * 20)
        ctx.line_to(-80, 28 + wag * 20)
        ctx.close_path()
        fill_stroke(ctx, c, OUT * 0.7)
        ellipse(ctx, 0, 0, 55, 32)
        fill_stroke(ctx, c, OUT * 0.7)
        circle(ctx, 28, -6, 8)
        fill_stroke(ctx, (1, 1, 1), 3)
        circle(ctx, 30, -6, 4)
        ctx.set_source_rgb(*INK)
        ctx.fill()


def bg_stomach(ctx, t, p):
    """Interior de una ballena: paredes carnosas que se contraen, jugos y burbujas."""
    squeeze = p.get("squeeze", 0.4)
    ctx.rectangle(-M, -M, W + 2 * M, H + 2 * M)
    ctx.set_source(radial_grad(ctx, 540, 900, 50, 1300, [(0, "#FF9BA8"), (0.6, "#C94A62"), (1, "#5E1626")]))
    ctx.fill()
    pulse = math.sin(t * 2.6)
    for k, (side, base) in enumerate(((1, 0), (-1, W))):   # side = dirección hacia dentro
        ctx.move_to(base - side * M, -M)
        for y in range(-M, H + M + 1, 60):
            xx = base + side * (90 + squeeze * 90 * (1 + pulse) * (0.6 + 0.4 * math.sin(y * 0.008 + k)) +
                                30 * math.sin(y * 0.012 + t * 1.5))
            ctx.line_to(xx, y)
        ctx.line_to(base - side * M, H + M)
        ctx.close_path()
        fill_stroke(ctx, "#A8324D", OUT)
        for j in range(6):  # pliegues
            yy = 150 + j * 320 + 20 * math.sin(t + j)
            xx = base + side * (60 + squeeze * 60 * (1 + pulse))
            ctx.move_to(xx - side * 70, yy)
            ctx.curve_to(xx + side * 10, yy - 40, xx + side * 10, yy + 40, xx - side * 70, yy + 80)
            ctx.set_source_rgba(*INK, 0.5)
            ctx.set_line_width(6)
            ctx.stroke()
    # charco de jugos gástricos
    lvl = p.get("liquid", 1500)
    ctx.move_to(-M, H + M)
    for x in range(-M, W + M + 1, 30):
        ctx.line_to(x, lvl + 16 * math.sin(x * 0.02 + t * 3))
    ctx.line_to(W + M, H + M)
    ctx.close_path()
    fill_stroke(ctx, (0.75, 0.85, 0.3), OUT)
    rng = np.random.default_rng(5)
    for i in range(14):
        ph = (t * 0.7 + rng.random()) % 1
        x = rng.uniform(100, W - 100)
        circle(ctx, x, lvl + 120 - ph * 200, rng.uniform(8, 18) * (1 - ph * 0.5))
        ctx.set_source_rgba(0.9, 1, 0.6, 1 - ph)
        ctx.fill()
    # restos de calamar flotando
    if p.get("debris", True):
        for i, (x, y) in enumerate(((260, lvl - 20), (780, lvl + 30))):
            with saved(ctx):
                ctx.translate(x, y + 8 * math.sin(t * 2 + i))
                ctx.rotate(0.4 * (1 if i else -1))
                for k in range(4):
                    ctx.move_to(0, 0)
                    ctx.curve_to(20, 40 + k * 10, -20, 70, 10 + k * 8, 110)
                ctx.set_source_rgb(0.95, 0.55, 0.6)
                ctx.set_line_width(12)
                ctx.stroke()


# ============================================================================
# PROPS
# ============================================================================
def _rocket(ctx, p, t):
    flame = 0.8 + 0.2 * math.sin(t * 30)
    if p.get("flame", True):
        for s, c in ((1.0, (1, 0.6, 0.15)), (0.6, (1, 0.92, 0.4))):
            ctx.move_to(-45 * s, 200)
            ctx.curve_to(-50 * s, 280, 0, 330 * flame * s + 60, 0, 380 * flame * s + 40)
            ctx.curve_to(0, 330 * flame * s + 60, 50 * s, 280, 45 * s, 200)
            ctx.close_path()
            ctx.set_source_rgb(*c)
            ctx.fill()
    for s in (-1, 1):  # aletas
        ctx.move_to(s * 60, 80)
        ctx.line_to(s * 140, 220)
        ctx.line_to(s * 60, 200)
        ctx.close_path()
        fill_stroke(ctx, PAL["red"], OUT)
    ctx.move_to(0, -260)
    ctx.curve_to(110, -150, 90, 120, 70, 200)
    ctx.line_to(-70, 200)
    ctx.curve_to(-90, 120, -110, -150, 0, -260)
    ctx.close_path()
    fill_stroke(ctx, (0.96, 0.96, 1), OUT)
    ctx.move_to(0, -260)
    ctx.curve_to(60, -200, 75, -150, 80, -120)
    ctx.line_to(-80, -120)
    ctx.curve_to(-75, -150, -60, -200, 0, -260)
    ctx.close_path()
    fill_stroke(ctx, PAL["red"], OUT)
    circle(ctx, 0, -30, 42)
    fill_stroke(ctx, (0.55, 0.85, 1), OUT)
    circle(ctx, -12, -42, 12)
    ctx.set_source_rgba(1, 1, 1, 0.8)
    ctx.fill()


def _habitat(ctx, p, t):
    """Base marciana: cúpula + módulo + paneles solares."""
    for s in (-1, 1):
        with saved(ctx):
            ctx.translate(s * 330, -20)
            ctx.rotate(-0.25 * s)
            rrect(ctx, -90, -60, 180, 110, 8)
            fill_stroke(ctx, (0.2, 0.3, 0.7), OUT)
            ctx.set_source_rgba(1, 1, 1, 0.5)
            ctx.set_line_width(3)
            for k in range(1, 4):
                ctx.move_to(-90 + k * 45, -60)
                ctx.line_to(-90 + k * 45, 50)
            ctx.stroke()
            limb(ctx, [(0, 50), (0, 110)], 10, PAL["metal_dk"], out=OUT * 0.6)
    rrect(ctx, -250, -40, 500, 140, 40)
    fill_stroke(ctx, (0.92, 0.92, 0.95), OUT)
    ctx.move_to(-200, -30)
    ctx.arc(0, -30, 200, math.pi, 2 * math.pi)
    ctx.close_path()
    ctx.set_source_rgba(0.7, 0.9, 1, 0.55)
    ctx.fill_preserve()
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(OUT)
    ctx.stroke()
    ctx.arc(0, -30, 170, math.pi * 1.15, math.pi * 1.4)
    ctx.set_source_rgba(1, 1, 1, 0.8)
    ctx.set_line_width(12)
    ctx.stroke()
    for x in (-150, 150):
        circle(ctx, x, 30, 28)
        fill_stroke(ctx, (1, 0.85, 0.4) if math.sin(t * 3 + x) > -0.3 else (0.6, 0.5, 0.3), OUT * 0.7)
    rrect(ctx, -45, 10, 90, 90, 16)
    fill_stroke(ctx, PAL["metal_dk"], OUT * 0.8)
    # bandera del canal
    ctx.move_to(120, -210)
    ctx.line_to(120, -60)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(6)
    ctx.stroke()
    ctx.move_to(120, -210)
    ctx.curve_to(170, -220 + 8 * math.sin(t * 4), 200, -190, 230, -200 + 8 * math.sin(t * 4 + 1))
    ctx.line_to(230, -140)
    ctx.curve_to(190, -130, 170, -160, 120, -150)
    ctx.close_path()
    fill_stroke(ctx, PAL["yellow"], 4)
    text(ctx, "?", 175, -175, 46, color=PAL["red"], outline=3, shadow_off=0)


def _plant(ctx, p, t):
    """Planta de patata; `health` 0..1 (marchita → sana)."""
    hlt = p.get("health", 1.0)
    c = mix((0.55, 0.45, 0.25), (0.3, 0.75, 0.3), hlt)
    rrect(ctx, -70, 0, 140, 70, 14)
    fill_stroke(ctx, (0.6, 0.38, 0.22), OUT * 0.8)
    for k in range(5):
        a = -math.pi / 2 + (k - 2) * 0.45 + 0.05 * math.sin(t * 2 + k)
        droop = (1 - hlt) * 1.2
        ln = 110 * (0.6 + 0.4 * hlt)
        ex, ey = ln * math.cos(a), ln * math.sin(a) + droop * 60
        ctx.move_to(0, 0)
        ctx.curve_to(0, -40, ex * 0.6, ey * 0.6 - 20, ex, ey)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(12)
        ctx.stroke()
        ctx.move_to(0, 0)
        ctx.curve_to(0, -40, ex * 0.6, ey * 0.6 - 20, ex, ey)
        ctx.set_source_rgb(*c)
        ctx.set_line_width(6)
        ctx.stroke()
        ellipse(ctx, ex, ey, 26, 14, a)
        fill_stroke(ctx, c, OUT * 0.6)
    if p.get("warning"):
        text(ctx, "⚠", 0, -180, 80, color=PAL["yellow"], outline=6)


def _rover(ctx, p, t):
    """Robot explorador con paneles solares (estilo Opportunity)."""
    dust = p.get("dust", 0.0)
    rrect(ctx, -170, -150, 340, 26, 6)
    fill_stroke(ctx, mix((0.2, 0.3, 0.7), (0.7, 0.45, 0.3), dust), OUT)
    for s in (-1, 1):
        ctx.move_to(s * 170, -137)
        ctx.line_to(s * 280, -150)
        ctx.line_to(s * 280, -124)
        ctx.close_path()
        fill_stroke(ctx, mix((0.2, 0.3, 0.7), (0.7, 0.45, 0.3), dust), OUT * 0.8)
    rrect(ctx, -120, -124, 240, 90, 14)
    fill_stroke(ctx, (0.85, 0.82, 0.75), OUT)
    limb(ctx, [(60, -150), (60, -260)], 14, PAL["metal_dk"], out=OUT * 0.6)
    rrect(ctx, 30, -300, 70, 44, 10)
    fill_stroke(ctx, (0.85, 0.82, 0.75), OUT * 0.8)
    for x in (48, 82):
        circle(ctx, x, -278, 10)
        ctx.set_source_rgb(*INK)
        ctx.fill()
    for x in (-110, 0, 110):
        circle(ctx, x, -10, 38)
        fill_stroke(ctx, (0.3, 0.3, 0.33), OUT)
        circle(ctx, x, -10, 14)
        fill_stroke(ctx, PAL["metal"], 3)
    if p.get("sleeping"):
        for i in range(3):
            ph = (t * 0.8 + i * 0.33) % 1
            text(ctx, "z", 120 + ph * 60, -320 - ph * 120, 40 + i * 10, color="white", outline=4,
                 alpha=1 - ph, shadow_off=0)


def _message(ctx, p, t):
    """Sobre volando con estela (mensaje a la Tierra)."""
    with saved(ctx):
        ctx.rotate(-0.15 + 0.05 * math.sin(t * 4))
        for i in range(4):
            ctx.move_to(-130 - i * 40, -10 + i * 10)
            ctx.line_to(-200 - i * 60, -10 + i * 10)
        ctx.set_source_rgba(1, 1, 1, 0.7)
        ctx.set_line_width(8)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()
        rrect(ctx, -110, -70, 220, 140, 14)
        fill_stroke(ctx, (1, 1, 1), OUT)
        ctx.move_to(-110, -66)
        ctx.line_to(0, 10)
        ctx.line_to(110, -66)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(OUT)
        ctx.stroke()
        circle(ctx, 0, 10, 22)
        fill_stroke(ctx, PAL["red"], 4)


def _scale(ctx, p, t):
    """Báscula con número que baja de `from` a `to`."""
    k = clamp(p.get("_age", 0) / p.get("over", 1.0))
    k = 1 - (1 - k) ** 3
    v = p.get("from", 60) + (p.get("to", 23) - p.get("from", 60)) * k
    rrect(ctx, -170, -40, 340, 80, 30)
    fill_stroke(ctx, (0.95, 0.95, 1), OUT)
    rrect(ctx, -90, -30, 180, 56, 12)
    fill_stroke(ctx, (0.15, 0.2, 0.25), OUT * 0.6)
    text(ctx, f"{v:.0f} kg", 0, -2, 46, color=(0.4, 1, 0.6), outline=0, shadow_off=0)


def _whale(ctx, p, t):
    """Ballena (jorobada/azul) de perfil; `mouth` 0..1 abre la boca."""
    mo = p.get("mouth", 0.0)
    if p.get("mouth_anim"):
        mo = 0.5 + 0.5 * math.sin(t * 2.2)
    c = col(p.get("color", "#3A5A8C"))
    tail = 18 * math.sin(t * 2)
    with saved(ctx):
        # cola
        ctx.move_to(-420, -20)
        ctx.curve_to(-520, -40, -560, -120 + tail, -640, -140 + tail)
        ctx.curve_to(-600, -60 + tail, -600, 40 + tail, -640, 110 + tail)
        ctx.curve_to(-560, 80 + tail, -520, 20, -420, 20)
        ctx.close_path()
        fill_stroke(ctx, c, OUT)
        # mandíbula inferior (rota al abrir)
        with saved(ctx):
            ctx.translate(300, 40)
            ctx.rotate(mo * 0.45)
            ctx.move_to(-720, 10)
            ctx.curve_to(-400, 160, 0, 120, 160, 0)
            ctx.line_to(-40, -10)
            ctx.close_path()
            fill_stroke(ctx, lighten(c, 0.35), OUT)
            for k in range(8):  # pliegues ventrales
                x = -600 + k * 80
                ctx.move_to(x, 40)
                ctx.line_to(x + 140, 30)
            ctx.set_source_rgba(*INK, 0.5)
            ctx.set_line_width(4)
            ctx.stroke()
        if mo > 0.05:
            ctx.move_to(460, 40)
            ctx.curve_to(300, 60, 200, 80 + 120 * mo, 80, 60)
            ctx.line_to(460, 40)
            ctx.close_path()
            ctx.set_source_rgb(0.35, 0.05, 0.12)
            ctx.fill()
        # cuerpo superior
        ctx.move_to(-430, -20)
        ctx.curve_to(-300, -200, 200, -230, 420, -80)
        ctx.curve_to(470, -40, 470, 30, 440, 40)
        ctx.curve_to(200, 40, -200, 40, -430, 20)
        ctx.close_path()
        fill_stroke(ctx, c, OUT)
        # aleta pectoral
        ctx.move_to(60, 20)
        ctx.curve_to(0, 160, -60, 220, -120, 240)
        ctx.curve_to(-60, 150, -20, 80, 0, 20)
        ctx.close_path()
        fill_stroke(ctx, darken(c, 0.1), OUT)
        circle(ctx, 300, -50, 16)
        fill_stroke(ctx, (1, 1, 1), 4)
        circle(ctx, 304, -50, 8)
        ctx.set_source_rgb(*INK)
        ctx.fill()
        for k in range(6):  # tubérculos (jorobada)
            circle(ctx, 360 + k * 14, -60 + (k % 2) * 16, 7)
            ctx.set_source_rgba(*darken(c, 0.3), 1)
            ctx.fill()


def _sperm_whale(ctx, p, t):
    """Cachalote: cabeza enorme y cuadrada."""
    mo = p.get("mouth", 0.0)
    c = col(p.get("color", "#5A5F6E"))
    tail = 18 * math.sin(t * 2)
    ctx.move_to(-380, 0)
    ctx.curve_to(-480, -20, -520, -110 + tail, -600, -130 + tail)
    ctx.curve_to(-560, -40 + tail, -560, 50 + tail, -600, 120 + tail)
    ctx.curve_to(-520, 90 + tail, -480, 30, -380, 30)
    ctx.close_path()
    fill_stroke(ctx, c, OUT)
    with saved(ctx):
        ctx.translate(380, 110)
        ctx.rotate(mo * 0.5)
        rrect(ctx, -420, -14, 420, 34, 16)
        fill_stroke(ctx, lighten(c, 0.3), OUT)
        for k in range(9):
            ctx.move_to(-400 + k * 44, -14)
            ctx.line_to(-390 + k * 44, -36)
            ctx.line_to(-380 + k * 44, -14)
            ctx.close_path()
            fill_stroke(ctx, (1, 1, 0.95), 3)
    ctx.move_to(-400, 0)
    ctx.curve_to(-250, -170, 0, -200, 150, -200)
    ctx.line_to(470, -200)
    ctx.curve_to(510, -200, 520, -170, 520, -130)
    ctx.line_to(520, 60)
    ctx.curve_to(520, 100, 490, 110, 450, 110)
    ctx.line_to(-50, 110)
    ctx.curve_to(-200, 100, -330, 60, -400, 30)
    ctx.close_path()
    fill_stroke(ctx, c, OUT)
    for k in range(4):
        ctx.move_to(-300 + k * 90, -40)
        ctx.curve_to(-280 + k * 90, -60, -260 + k * 90, -20, -240 + k * 90, -40)
    ctx.set_source_rgba(*INK, 0.4)
    ctx.set_line_width(5)
    ctx.stroke()
    circle(ctx, 130, 20, 14)
    fill_stroke(ctx, (1, 1, 1), 4)
    circle(ctx, 133, 20, 7)
    ctx.set_source_rgb(*INK)
    ctx.fill()


def _squid(ctx, p, t):
    c = col(p.get("color", "#FF7A8A"))
    for k in range(8):
        sw = 25 * math.sin(t * 4 + k)
        ctx.move_to(-40 + k * 11, 80)
        ctx.curve_to(-60 + k * 15 + sw, 180, -40 + k * 12 - sw, 260, -50 + k * 14 + sw, 340)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(22)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke_preserve()
        ctx.set_source_rgb(*c)
        ctx.set_line_width(12)
        ctx.stroke()
    ctx.move_to(0, -220)
    ctx.curve_to(80, -120, 70, 40, 50, 90)
    ctx.line_to(-50, 90)
    ctx.curve_to(-70, 40, -80, -120, 0, -220)
    ctx.close_path()
    fill_stroke(ctx, c, OUT)
    for s in (-1, 1):
        circle(ctx, s * 25, 50, 14)
        fill_stroke(ctx, (1, 1, 1), 3)
        circle(ctx, s * 25, 52, 7)
        ctx.set_source_rgb(*INK)
        ctx.fill()


def _ambergris(ctx, p, t):
    blob(ctx, 0, 0, 70, n=9, wobble=0.25, seed=3)
    fill_stroke(ctx, (0.72, 0.66, 0.55), OUT)
    blob(ctx, -15, -10, 30, n=7, wobble=0.3, seed=5)
    ctx.set_source_rgba(1, 1, 1, 0.3)
    ctx.fill()
    for i, (x, y) in enumerate(((-80, -60), (75, -50), (60, 70))):
        star(ctx, x, y, 14 * (0.6 + 0.4 * math.sin(t * 5 + i)), n=4, inner=0.3)
        ctx.set_source_rgb(1, 1, 0.8)
        ctx.fill()


def _perfume(ctx, p, t):
    rrect(ctx, -70, -60, 140, 160, 30)
    fill_stroke(ctx, (0.85, 0.65, 1), OUT)
    rrect(ctx, -25, -110, 50, 50, 8)
    fill_stroke(ctx, PAL["yellow"], OUT * 0.8)
    rrect(ctx, -40, -10, 80, 60, 10)
    fill_stroke(ctx, (1, 1, 1), 4)
    text(ctx, "€€€", 0, 20, 30, color=INK, outline=0, shadow_off=0)


def _newspaper(ctx, p, t):
    with saved(ctx):
        ctx.rotate(-0.06 + 0.02 * math.sin(t * 2))
        rrect(ctx, -260, -330, 520, 660, 10)
        fill_stroke(ctx, (0.96, 0.92, 0.8), OUT)
        text(ctx, p.get("paper", "THE NEWS"), 0, -280, 52, color=INK, outline=0, shadow_off=0, font="Lilita One")
        ctx.move_to(-230, -240)
        ctx.line_to(230, -240)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(4)
        ctx.stroke()
        for i, ln in enumerate(p.get("headline", "HOMBRE TRAGADO\nPOR UNA BALLENA").split("\n")):
            text(ctx, ln, 0, -180 + i * 64, 54, color=INK, outline=0, shadow_off=0, max_w=480)
        text(ctx, p.get("year", "1891"), 0, -40, 44, color=PAL["red"], outline=0, shadow_off=0)
        rrect(ctx, -220, 0, 200, 150, 6)
        ctx.set_source_rgb(0.75, 0.72, 0.62)
        ctx.fill()
        for k in range(7):
            ctx.rectangle(10, 10 + k * 22, 210, 8)
            ctx.rectangle(-220, 170 + k * 22, 440, 8)
        ctx.set_source_rgb(0.7, 0.67, 0.58)
        ctx.fill()


def _diver_bubbles(ctx, p, t):
    rng = np.random.default_rng(9)
    for i in range(10):
        ph = (t * 1.2 + rng.random()) % 1
        circle(ctx, 20 * math.sin(t * 5 + i), -ph * 400, 6 + 8 * rng.random())
        ctx.set_source_rgba(1, 1, 1, 0.8 * (1 - ph))
        ctx.set_line_width(4)
        ctx.stroke()


def _planet(ctx, p, t):
    """Planeta genérico (Marte por defecto)."""
    r = p.get("r", 120)
    c = col(p.get("color", "#C1440E"))
    circle(ctx, 0, 0, r)
    fill_stroke(ctx, c, OUT)
    with saved(ctx):
        circle(ctx, 0, 0, r)
        ctx.clip()
        for i, (x, y, rr) in enumerate(((-0.3, -0.2, 0.22), (0.35, 0.3, 0.16), (0.1, -0.5, 0.1), (-0.2, 0.5, 0.14))):
            circle(ctx, x * r + t * 6 % 20, y * r, rr * r)
            ctx.set_source_rgba(*darken(c, 0.25), 0.8)
            ctx.fill()
        circle(ctx, r * 0.35, r * 0.3, r)
        ctx.set_source_rgba(0, 0, 0.1, 0.25)
        ctx.fill()


def _dotted_path(ctx, p, t):
    """Trayectoria punteada animada de A a B (viaje del cohete)."""
    x1, y1 = p.get("dx", 600), p.get("dy", -500)
    ctx.move_to(0, 0)
    ctx.curve_to(x1 * 0.2, y1 * 0.9, x1 * 0.8, y1 * 1.1, x1, y1)
    ctx.set_dash([18, 22], -t * 60)
    ctx.set_source_rgba(1, 1, 1, 0.85)
    ctx.set_line_width(8)
    ctx.stroke()
    ctx.set_dash([])


BACKGROUNDS.update({"mars": bg_mars, "underwater": bg_underwater, "stomach": bg_stomach})
PROPS.update({"rocket": _rocket, "habitat": _habitat, "plant": _plant, "rover": _rover, "message": _message,
              "scale": _scale, "whale": _whale, "sperm_whale": _sperm_whale, "squid": _squid,
              "ambergris": _ambergris, "perfume": _perfume, "newspaper": _newspaper,
              "bubbles": _diver_bubbles, "planet": _planet, "dotted_path": _dotted_path})
