"""Catálogo «cuerpo al límite»: volcán con lluvia de ceniza, mar helado de noche; pulmones,
mascarilla FFP2, lupa con granos de ceniza, iceberg, transatlántico, bote salvavidas,
cámara de vacío, corazón y lluvia de ceniza/nieve a pantalla completa.

Se registra automáticamente en BACKGROUNDS y PROPS al importar fabrica.visuals.world.
"""
from __future__ import annotations

import math

import cairo
import numpy as np

from .draw import (INK, OUT, PAL, blob, circle, clamp, col, darken, ellipse, fill_stroke, lerp, lighten,
                   limb, linear_grad, mix, noise1, radial_grad, rrect, saved, text)
from .world import BACKGROUNDS, H, M, PROPS, W, _sky


# ============================================================================ FONDOS
def bg_volcano(ctx, t, p):
    """Volcán en erupción. `ash` 0..1 oscurece el cielo y cubre el suelo; `town` dibuja casas al pie;
    `erupt` activa columna y bombas; `near` acerca el cono (más grande)."""
    ash = p.get("ash", 0.3)
    _sky(ctx, mix("#7FB8E8", "#4A4650", ash), mix("#F2C9A0", "#8A7F78", ash))
    g = p.get("ground", 1420)
    near = p.get("near", False)
    cx = p.get("cx", 560)
    top = g - (900 if near else 640)
    half = 620 if near else 430
    crater = 110 if near else 80
    # columna eruptiva (detrás del cono)
    if p.get("erupt", True):
        for i in range(9):
            ph = (t * 0.25 + i / 9) % 1
            r = 90 + ph * 330
            x = cx + 60 * math.sin(i * 1.7 + t * 0.4) + ph * 260
            y = top - 40 - ph * 900
            blob(ctx, x, y, r, n=9, wobble=0.22, seed=i, t=t * 0.5)
            ctx.set_source_rgba(*mix((0.35, 0.32, 0.33), (0.55, 0.52, 0.52), ph), 0.9 - 0.35 * ph)
            ctx.fill()
        glow = 0.6 + 0.4 * math.sin(t * 6)
        circle(ctx, cx, top, 140)
        ctx.set_source(radial_grad(ctx, cx, top, 10, 160, [(0, (1, 0.75, 0.2), 0.9 * glow), (1, (1, 0.3, 0.1), 0)]))
        ctx.fill()
    # cono
    ctx.move_to(cx - half - 380, g + 10)
    ctx.curve_to(cx - half, g - 120, cx - crater - 60, top + 60, cx - crater, top)
    ctx.line_to(cx + crater, top)
    ctx.curve_to(cx + crater + 60, top + 60, cx + half, g - 120, cx + half + 380, g + 10)
    ctx.close_path()
    fill_stroke(ctx, mix("#6B4A3A", "#4A4044", ash * 0.6), OUT)
    # coladas de lava
    if p.get("lava", True):
        for s, w in ((-1, 26), (1, 20), (-0.3, 16)):
            ctx.move_to(cx + s * crater * 0.6, top + 6)
            ctx.curve_to(cx + s * 140, top + 220, cx + s * 260, g - 300, cx + s * 340, g - 30)
            ctx.set_source_rgb(*INK)
            ctx.set_line_width(w + 12)
            ctx.stroke_preserve()
            ctx.set_source_rgb(1, 0.45 + 0.1 * math.sin(t * 4 + s), 0.12)
            ctx.set_line_width(w)
            ctx.stroke()
    # bombas volcánicas
    if p.get("erupt", True) and p.get("bombs", True):
        rng = np.random.default_rng(9)
        for i in range(6):
            ph = (t * 0.7 + rng.random()) % 1
            vx = rng.uniform(-420, 420)
            x = cx + vx * ph
            y = top - 700 * ph + 900 * ph * ph
            circle(ctx, x, y, 12)
            fill_stroke(ctx, (1, 0.5, 0.15), 4)
    # suelo
    ctx.rectangle(-M, g, W + 2 * M, H + M - g)
    fill_stroke(ctx, mix("#5E8C3A", "#6E6A6C", min(1, ash * 1.3)), OUT)
    # pueblo al pie
    if p.get("town", True):
        for i, (x, w, h, c) in enumerate(((90, 170, 150, "#F4E3C1"), (300, 150, 190, "#FFFFFF"),
                                         (740, 180, 160, "#F7D9A8"), (950, 140, 140, "#FFFFFF"))):
            y = g + 40
            rrect(ctx, x - w / 2, y - h, w, h, 8)
            fill_stroke(ctx, c, OUT * 0.8)
            ctx.move_to(x - w / 2 - 14, y - h)
            ctx.line_to(x + w / 2 + 14, y - h)
            ctx.line_to(x + w / 2, y - h - 26)
            ctx.line_to(x - w / 2, y - h - 26)
            ctx.close_path()
            fill_stroke(ctx, mix("#C9543A", "#77716F", ash), OUT * 0.8)
            rrect(ctx, x - 25, y - h + 35, 50, 50, 6)
            fill_stroke(ctx, (0.55, 0.8, 1), OUT * 0.6)
            if ash > 0.2:  # tejado cubierto de ceniza
                rrect(ctx, x - w / 2 - 12, y - h - 38, w + 24, 16 + 18 * ash, 8)
                ctx.set_source_rgba(0.25, 0.24, 0.26, 0.95)
                ctx.fill()
    # capa de ceniza en el suelo
    if ash > 0.05:
        ctx.move_to(-M, g + 6)
        for x in range(-M, W + M + 1, 60):
            ctx.line_to(x, g + 6 - 30 * ash * (0.6 + 0.4 * math.sin(x * 0.013)))
        ctx.line_to(W + M, H + M)
        ctx.line_to(-M, H + M)
        ctx.close_path()
        ctx.set_source_rgba(0.22, 0.21, 0.23, min(1, 0.5 + ash * 0.6))
        ctx.fill()
    if p.get("fall", True) and ash > 0.05:
        _particles(ctx, t, int(140 * ash), (0.28, 0.27, 0.3), seed=4, speed=180, size=(3, 8))


def bg_ice_sea(ctx, t, p):
    """Atlántico Norte de noche, mar en calma y helado; `stars`, `ice` (trozos de hielo flotando),
    `level` (altura del agua), `under` (vista bajo el agua)."""
    lvl = p.get("level", 1050)
    if p.get("under"):
        _sky(ctx, (0.04, 0.12, 0.25), (0.0, 0.02, 0.08))
        rng = np.random.default_rng(3)
        for i in range(22):
            ph = (t * rng.uniform(0.15, 0.35) + rng.random()) % 1
            circle(ctx, rng.uniform(0, W), H + 40 - ph * (H + 80), rng.uniform(4, 11))
            ctx.set_source_rgba(0.8, 0.95, 1, 0.45)
            ctx.set_line_width(3)
            ctx.stroke()
        return
    _sky(ctx, (0.02, 0.03, 0.1), (0.08, 0.1, 0.25))
    if p.get("stars", True):
        rng = np.random.default_rng(12)
        for i in range(120):
            x, y = rng.uniform(-M, W + M), rng.uniform(-M, lvl - 40)
            tw = 0.5 + 0.5 * math.sin(t * rng.uniform(1, 3) + i)
            circle(ctx, x, y, rng.uniform(1.5, 4) * (0.6 + 0.4 * tw))
            ctx.set_source_rgba(1, 1, 0.95, 0.35 + 0.6 * tw)
            ctx.fill()
    for k in range(4):
        y0 = lvl + k * 110
        ctx.move_to(-M, H + M)
        for x in range(-M, W + M + 1, 30):
            ctx.line_to(x, y0 + 6 * math.sin(x * 0.012 + t * (1.2 - k * 0.2) + k))
        ctx.line_to(W + M, H + M)
        ctx.close_path()
        fill_stroke(ctx, mix((0.08, 0.2, 0.38), (0.02, 0.06, 0.16), k / 3), OUT * 0.5)
    # reflejo de estrellas
    for i in range(14):
        x = (i * 97) % W
        rrect(ctx, x, lvl + 40 + (i * 53) % 500, 40 + (i % 3) * 20, 5, 2)
        ctx.set_source_rgba(0.8, 0.9, 1, 0.25 + 0.2 * math.sin(t * 2 + i))
        ctx.fill()
    if p.get("ice", True):
        rng = np.random.default_rng(8)
        for i in range(6):
            x = rng.uniform(40, W - 40) + 10 * math.sin(t * 0.6 + i)
            y = lvl + 60 + rng.uniform(0, 700)
            blob(ctx, x, y, rng.uniform(22, 48), n=6, wobble=0.25, seed=i)
            fill_stroke(ctx, (0.85, 0.95, 1), OUT * 0.5)


def _particles(ctx, t, n, color, seed=1, speed=200, size=(3, 7), drift=40, alpha=0.85):
    rng = np.random.default_rng(seed)
    for i in range(n):
        ph = (t * speed / (H + 200) * rng.uniform(0.6, 1.3) + rng.random()) % 1
        x = rng.uniform(-M, W + M) + drift * math.sin(t * 1.3 + i)
        y = -100 + ph * (H + 200)
        blob(ctx, x, y, rng.uniform(*size), n=5, wobble=0.3, seed=i)
        ctx.set_source_rgba(*col(color), alpha)
        ctx.fill()


# ============================================================================ PROPS
def _ashfall(ctx, p, t):
    """Lluvia de ceniza (o nieve con `color`) a pantalla completa; usar con abs/x=0/y=0 y layer front."""
    _particles(ctx, t, int(p.get("density", 120)), p.get("color", (0.3, 0.29, 0.32)), seed=p.get("seed", 2),
               speed=p.get("speed", 220), size=tuple(p.get("size", (3, 9))), alpha=p.get("alpha", 0.85))
    haze = p.get("haze", 0.0)
    if haze > 0:
        ctx.rectangle(-M, -M, W + 2 * M, H + 2 * M)
        ctx.set_source_rgba(0.35, 0.33, 0.33, haze)
        ctx.fill()


def _lungs(ctx, p, t):
    """Pulmones con bronquios. `breathe` anima la respiración; `dirt` 0..1 los ensucia de ceniza;
    `inflow` muestra partículas entrando por la tráquea; `hold` los hincha (aguantar el aire)."""
    br = 1 + (0.06 * math.sin(t * 2.6) if p.get("breathe", True) else 0) + 0.18 * p.get("hold", 0)
    dirt = p.get("dirt", 0.0)
    base = mix("#FF8FA8", "#7A6E72", dirt * 0.75)
    with saved(ctx):
        ctx.scale(br, br)
        for s in (-1, 1):
            ctx.new_path()
            ctx.move_to(s * 40, -170)
            ctx.curve_to(s * 220, -220, s * 260, 40, s * 230, 170)
            ctx.curve_to(s * 200, 230, s * 70, 220, s * 50, 150)
            ctx.curve_to(s * 30, 40, s * 30, -100, s * 40, -170)
            ctx.close_path()
            fill_stroke(ctx, base, OUT)
            # alvéolos
            for k in range(7):
                circle(ctx, s * (100 + (k % 3) * 40), -90 + k * 38, 16)
                ctx.set_source_rgba(*lighten(base, 0.25), 0.8)
                ctx.fill()
        # tráquea y bronquios
        limb(ctx, [(0, -320), (0, -150)], 44, "#F4C9D2", out=OUT)
        for s in (-1, 1):
            limb(ctx, [(0, -150), (s * 70, -90), (s * 110, -20)], 26, "#F4C9D2", out=OUT * 0.8)
        rng = np.random.default_rng(5)
        for i in range(int(40 * dirt)):
            s = 1 if i % 2 else -1
            circle(ctx, s * rng.uniform(70, 220), rng.uniform(-150, 170), rng.uniform(5, 12))
            ctx.set_source_rgba(0.2, 0.19, 0.22, 0.9)
            ctx.fill()
    if p.get("inflow"):
        for i in range(14):
            ph = (t * 0.9 + i / 14) % 1
            circle(ctx, 14 * math.sin(i * 2.3), -420 + ph * 300, 8)
            ctx.set_source_rgba(0.25, 0.24, 0.27, 1 - ph * 0.4)
            ctx.fill()


def _mask(ctx, p, t):
    """Mascarilla FFP2 de frente."""
    c = col(p.get("color", "#F4F6FA"))
    ctx.new_path()
    ctx.move_to(-170, -60)
    ctx.curve_to(-60, -120, 60, -120, 170, -60)
    ctx.curve_to(190, 30, 120, 120, 0, 140)
    ctx.curve_to(-120, 120, -190, 30, -170, -60)
    ctx.close_path()
    fill_stroke(ctx, c, OUT)
    ctx.move_to(0, -100)
    ctx.line_to(0, 138)
    ctx.set_source_rgba(*INK, 0.35)
    ctx.set_line_width(5)
    ctx.stroke()
    for s in (-1, 1):
        ctx.move_to(s * 170, -50)
        ctx.curve_to(s * 260, -80, s * 260, 60, s * 175, 40)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(8)
        ctx.stroke()
    text(ctx, p.get("label", "FFP2"), 0, 20, 52, color="#2B6BE8", outline=0, shadow_off=0)


def _magnifier(ctx, p, t):
    """Lupa con lo que se ve dentro: `view` = ash (granos afilados de roca y vidrio) | ice | bubbles."""
    r = 230
    view = p.get("view", "ash")
    with saved(ctx):
        circle(ctx, 0, 0, r)
        ctx.clip()
        ctx.rectangle(-r, -r, 2 * r, 2 * r)
        ctx.set_source_rgb(*({"ash": (0.93, 0.9, 0.85), "ice": (0.75, 0.9, 1)}.get(view, (0.85, 0.95, 1))))
        ctx.fill()
        rng = np.random.default_rng(11)
        for i in range(16):
            x, y = rng.uniform(-190, 190), rng.uniform(-190, 190)
            rot = rng.uniform(0, math.pi) + 0.15 * math.sin(t + i)
            sz = rng.uniform(26, 60)
            with saved(ctx):
                ctx.translate(x, y)
                ctx.rotate(rot)
                ctx.move_to(-sz, 0)
                ctx.line_to(-sz * 0.2, -sz * 0.45)
                ctx.line_to(sz, -sz * 0.1)
                ctx.line_to(sz * 0.3, sz * 0.4)
                ctx.close_path()
                if view == "ash":
                    fill_stroke(ctx, (0.55, 0.85, 0.95) if i % 3 == 0 else (0.38, 0.35, 0.36), OUT * 0.5)
                else:
                    fill_stroke(ctx, (0.9, 0.97, 1), OUT * 0.5)
    circle(ctx, 0, 0, r)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(34)
    ctx.stroke_preserve()
    ctx.set_source_rgb(*PAL["metal"])
    ctx.set_line_width(20)
    ctx.stroke()
    limb(ctx, [(r * 0.72, r * 0.72), (r * 1.25, r * 1.25)], 46, "#5A3A20", out=OUT)


def _iceberg(ctx, p, t):
    """Iceberg: parte visible y, con `under`, la masa sumergida (≈ 90 %)."""
    bob = 6 * math.sin(t * 1.2)
    with saved(ctx):
        ctx.translate(0, bob)
        if p.get("under", True):
            ctx.new_path()
            ctx.move_to(-260, 0)
            ctx.line_to(-360, 260)
            ctx.line_to(-200, 620)
            ctx.line_to(120, 700)
            ctx.line_to(380, 420)
            ctx.line_to(300, 0)
            ctx.close_path()
            ctx.set_source_rgba(0.55, 0.8, 0.95, 0.55)
            ctx.fill_preserve()
            ctx.set_source_rgba(*INK, 0.5)
            ctx.set_line_width(OUT)
            ctx.stroke()
        ctx.new_path()
        ctx.move_to(-260, 0)
        ctx.line_to(-170, -150)
        ctx.line_to(-60, -130)
        ctx.line_to(20, -300)
        ctx.line_to(140, -180)
        ctx.line_to(230, -210)
        ctx.line_to(300, 0)
        ctx.close_path()
        fill_stroke(ctx, (0.92, 0.97, 1), OUT)
        ctx.move_to(20, -300)
        ctx.line_to(60, -120)
        ctx.line_to(0, 0)
        ctx.set_source_rgba(0.6, 0.8, 0.95, 0.9)
        ctx.set_line_width(10)
        ctx.stroke()


def _liner(ctx, p, t):
    """Transatlántico de cuatro chimeneas (genérico, de época). `tilt` (rad) inclina la proa hacia abajo;
    `sink` 0..1 lo hunde; `lights` ventanillas encendidas; `smoke`."""
    tilt = p.get("tilt", 0.0)
    sink = p.get("sink", 0.0)
    with saved(ctx):
        ctx.translate(0, sink * 420)
        ctx.rotate(tilt)
        # casco
        ctx.new_path()
        ctx.move_to(-520, -40)
        ctx.line_to(500, -40)
        ctx.curve_to(540, -40, 560, -10, 520, 60)
        ctx.line_to(-480, 60)
        ctx.curve_to(-520, 40, -540, -10, -520, -40)
        ctx.close_path()
        fill_stroke(ctx, "#1C1C24", OUT)
        rrect(ctx, -500, 40, 1010, 24, 6)
        ctx.set_source_rgb(0.7, 0.12, 0.12)
        ctx.fill()
        # superestructura
        rrect(ctx, -380, -100, 760, 62, 6)
        fill_stroke(ctx, (0.97, 0.96, 0.92), OUT * 0.8)
        # chimeneas
        nf = int(p.get("funnels", 4))
        for i in range(nf):
            x = -270 + i * 170 if nf == 4 else (i - (nf - 1) / 2) * 170
            ctx.new_path()
            ctx.move_to(x - 34, -100)
            ctx.line_to(x - 26, -260)
            ctx.line_to(x + 34, -260)
            ctx.line_to(x + 34, -100)
            ctx.close_path()
            fill_stroke(ctx, p.get("funnel_color", "#E8A33A"), OUT * 0.8)
            rrect(ctx, x - 27, -262, 62, 34, 4)
            ctx.set_source_rgb(*INK)
            ctx.fill()
            if p.get("smoke", False):
                for k in range(3):
                    ph = (t * 0.5 + k / 3) % 1
                    blob(ctx, x + 20 - ph * 160, -300 - ph * 160, 22 + ph * 40, n=7, seed=i * 3 + k)
                    ctx.set_source_rgba(0.5, 0.5, 0.55, 0.6 * (1 - ph))
                    ctx.fill()
        # ventanillas
        if p.get("lights", True):
            for row, y in enumerate((-80, -20, 18)):
                for k in range(26 if row else 18):
                    x = (-460 if row else -350) + k * 36
                    on = 0.75 + 0.25 * math.sin(t * 5 + k * 1.3 + row)
                    circle(ctx, x, y, 6)
                    ctx.set_source_rgba(1, 0.9, 0.5, on)
                    ctx.fill()


def _sea_front(ctx, p, t):
    """Franja de mar en primer plano (usar abs, x=0, y=<nivel>, layer front): tapa el casco de un barco
    que se hunde o el cuerpo de alguien que flota. `color` y `waves`."""
    c = col(p.get("color", (0.06, 0.16, 0.32)))
    amp = p.get("waves", 10)
    ctx.new_path()
    ctx.move_to(-M, 0)
    for x in range(-M, W + M + 1, 30):
        ctx.line_to(x, amp * math.sin(x * 0.013 + t * 1.6))
    ctx.line_to(W + M, H + M)
    ctx.line_to(-M, H + M)
    ctx.close_path()
    fill_stroke(ctx, c, OUT * 0.6)
    for i in range(10):
        x = (i * 131 + t * 20) % (W + 200) - 100
        rrect(ctx, x, 40 + (i * 61) % 300, 60, 6, 3)
        ctx.set_source_rgba(0.75, 0.9, 1, 0.25)
        ctx.fill()


def _lifeboat(ctx, p, t):
    """Bote salvavidas de madera; `people` cuántas cabezas asoman."""
    with saved(ctx):
        ctx.rotate(0.04 * math.sin(t * 1.5))
        ctx.new_path()
        ctx.move_to(-230, -30)
        ctx.line_to(230, -30)
        ctx.curve_to(220, 40, 120, 70, 0, 70)
        ctx.curve_to(-120, 70, -220, 40, -230, -30)
        ctx.close_path()
        fill_stroke(ctx, "#F2F0E6", OUT)
        rrect(ctx, -232, -40, 464, 18, 6)
        fill_stroke(ctx, "#A66A3A", OUT * 0.7)
        cols = ["#5A3A20", "#2B2B2B", "#D9A441", "#7A4A2A", "#3A2A1A", "#B05A3A"]
        for i in range(int(p.get("people", 5))):
            x = -170 + i * 70
            circle(ctx, x, -70, 28)
            fill_stroke(ctx, PAL["skin"], OUT * 0.6)
            ctx.new_path()
            ctx.arc(x, -76, 29, math.pi, 2 * math.pi)
            ctx.set_source_rgb(*col(cols[i % len(cols)]))
            ctx.fill()


def _vacuum_chamber(ctx, p, t):
    """Cámara de vacío de laboratorio: gran cilindro con cúpula, ventanilla, tuberías y manómetro (`gauge` 0..1)."""
    # tuberías
    for y in (-150, 120):
        limb(ctx, [(300, y), (420, y), (420, y + 260)], 34, PAL["metal_dk"], out=OUT)
    # cuerpo y cúpula
    ctx.new_path()
    ctx.move_to(-300, 420)
    ctx.line_to(-300, -260)
    ctx.curve_to(-300, -470, 300, -470, 300, -260)
    ctx.line_to(300, 420)
    ctx.close_path()
    fill_stroke(ctx, PAL["metal"], OUT)
    for x in (-210, 210):
        for y in range(-240, 420, 90):
            circle(ctx, x, y, 9)
            ctx.set_source_rgb(*PAL["metal_dk"])
            ctx.fill()
    rrect(ctx, -330, 400, 660, 50, 14)
    fill_stroke(ctx, PAL["metal_dk"], OUT)
    # ventanilla (dentro se adivina un traje)
    rrect(ctx, -120, -230, 240, 300, 110)
    fill_stroke(ctx, (0.12, 0.16, 0.28), OUT * 0.8)
    circle(ctx, 0, -120, 46)
    ctx.set_source_rgba(0.92, 0.94, 0.98, 0.7)
    ctx.fill()
    rrect(ctx, -50, -75, 100, 130, 30)
    ctx.set_source_rgba(0.92, 0.94, 0.98, 0.6)
    ctx.fill()
    ctx.new_path()
    ctx.arc(-40, -150, 60, math.pi * 1.1, math.pi * 1.5)
    ctx.set_source_rgba(1, 1, 1, 0.35)
    ctx.set_line_width(12)
    ctx.stroke()
    rrect(ctx, -150, 120, 300, 64, 10)
    fill_stroke(ctx, "#FFD23F", OUT * 0.6)
    text(ctx, "VACÍO", 0, 152, 46, color=INK, outline=0, shadow_off=0)
    # manómetro
    gx, gy = 190, 250
    circle(ctx, gx, gy, 70)
    fill_stroke(ctx, (1, 1, 1), OUT * 0.8)
    g = clamp(p.get("gauge", 1.0))
    a = math.pi * (0.8 + 1.4 * (1 - g))
    limb(ctx, [(gx, gy), (gx + 52 * math.cos(a), gy + 52 * math.sin(a))], 8, PAL["red"], out=0)
    circle(ctx, gx, gy, 10)
    ctx.set_source_rgb(*INK)
    ctx.fill()


def _helmet(ctx, p, t):
    """Casco espacial suelto (cúpula de cristal con aro), para dejarlo flotar."""
    circle(ctx, 0, 0, 150)
    ctx.set_source_rgba(0.75, 0.9, 1, 0.45)
    ctx.fill_preserve()
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(OUT)
    ctx.stroke()
    ctx.new_path()
    ctx.arc(-40, -50, 80, math.pi * 1.05, math.pi * 1.5)
    ctx.set_source_rgba(1, 1, 1, 0.7)
    ctx.set_line_width(16)
    ctx.stroke()
    rrect(ctx, -120, 110, 240, 56, 20)
    fill_stroke(ctx, PAL["suit"], OUT)
    rrect(ctx, -90, 124, 180, 18, 8)
    ctx.set_source_rgb(*PAL["suit_acc"])
    ctx.fill()


def _heart(ctx, p, t):
    """Corazón que late; `bpm` marca el ritmo; `cold` lo tiñe de azul."""
    bpm = p.get("bpm", 80)
    ph = (t * bpm / 60) % 1
    s = 1 + 0.12 * math.exp(-((ph - 0.1) ** 2) / 0.004) + 0.06 * math.exp(-((ph - 0.3) ** 2) / 0.004)
    c = mix("#E8392F", "#5C8FE6", p.get("cold", 0.0))
    with saved(ctx):
        ctx.scale(s, s)
        ctx.new_path()
        ctx.move_to(0, 150)
        ctx.curve_to(-260, -10, -170, -230, 0, -110)
        ctx.curve_to(170, -230, 260, -10, 0, 150)
        ctx.close_path()
        fill_stroke(ctx, c, OUT)
        ctx.new_path()
        ctx.arc(-70, -90, 45, math.pi * 1.1, math.pi * 1.6)
        ctx.set_source_rgba(1, 1, 1, 0.5)
        ctx.set_line_width(14)
        ctx.stroke()


BACKGROUNDS.update({"volcano": bg_volcano, "ice_sea": bg_ice_sea})
PROPS.update({"ashfall": _ashfall, "lungs": _lungs, "mask": _mask, "magnifier": _magnifier, "iceberg": _iceberg,
              "liner": _liner, "sea_front": _sea_front, "lifeboat": _lifeboat, "vacuum_chamber": _vacuum_chamber, "heart": _heart, "helmet": _helmet})
