"""Fondos ilustrados y props animados. Todo es vectorial y función pura del tiempo.

Catálogo (lo que el guionista/LLM puede pedir) en BACKGROUNDS y PROPS.
Coordenadas de mundo = píxeles de un lienzo 1080x1920; se dibuja con margen para zooms.
"""
from __future__ import annotations

import math

import cairo
import numpy as np

from .draw import (INK, OUT, PAL, blob, circle, clamp, col, darken, ellipse, fill_stroke, lerp,
                   lighten, limb, linear_grad, mix, noise1, radial_grad, rrect, saved, smooth_closed,
                   star, text)

W, H = 1080, 1920
M = 500   # margen de dibujo fuera de cuadro


def _sky(ctx, top, bot):
    ctx.rectangle(-M, -M, W + 2 * M, H + 2 * M)
    ctx.set_source(linear_grad(ctx, 0, -M, 0, H, [(0, top), (1, bot)]))
    ctx.fill()


# ============================================================================
# FONDOS
# ============================================================================
def bg_backyard(ctx, t, p):
    g = p.get("ground", 1380)
    _sky(ctx, PAL["sky_top"], PAL["sky_bot"])
    # sol con rayos giratorios
    sx, sy = 850, 330
    with saved(ctx):
        ctx.translate(sx, sy)
        ctx.rotate(t * 0.25)
        for i in range(12):
            ctx.rotate(math.pi / 6)
            ctx.move_to(0, -110)
            ctx.line_to(-22, -175)
            ctx.line_to(22, -175)
            ctx.close_path()
        ctx.set_source_rgba(1, 0.9, 0.4, 0.75)
        ctx.fill()
    circle(ctx, sx, sy, 95)
    fill_stroke(ctx, PAL["yellow"], OUT)
    # nubes
    for i, (cx, cy, s) in enumerate(((150, 260, 1.0), (520, 170, 0.8), (980, 560, 0.9), (-200, 520, 1.1))):
        x = (cx + t * 18 * (1 + i * 0.3)) % (W + 600) - 300
        _cloud(ctx, x, cy, s)
    # colinas
    ctx.move_to(-M, g - 180)
    ctx.curve_to(150, g - 380, 380, g - 330, 560, g - 210)
    ctx.curve_to(760, g - 360, 1000, g - 380, W + M, g - 200)
    ctx.line_to(W + M, g)
    ctx.line_to(-M, g)
    ctx.close_path()
    fill_stroke(ctx, (0.55, 0.85, 0.45), OUT)
    # casa
    hx = p.get("house_x", 80)
    if hx is not None:
        _house(ctx, hx, g)
    # valla
    for i in range(-4, 16):
        x = i * 85 + 420
        rrect(ctx, x, g - 150, 46, 160, 10)
        fill_stroke(ctx, (0.98, 0.95, 0.88), OUT * 0.8)
    rrect(ctx, -M, g - 110, W + 2 * M, 22, 6)
    fill_stroke(ctx, (0.98, 0.95, 0.88), OUT * 0.8)
    # suelo: césped + tierra
    ctx.rectangle(-M, g, W + 2 * M, H + M - g)
    ctx.set_source(linear_grad(ctx, 0, g, 0, H + M, [(0, PAL["dirt"]), (1, darken(PAL["dirt"], 0.35))]))
    ctx.fill()
    _pebbles(ctx, g + 60, H + M, seed=3)
    ctx.move_to(-M, g + 30)
    for i in range(-10, 60):
        x = i * 30
        ctx.line_to(x + 15, g - 18 - 8 * math.sin(i * 1.7 + t * 2))
        ctx.line_to(x + 30, g + 10)
    ctx.line_to(W + M, g + 40)
    ctx.line_to(-M, g + 40)
    ctx.close_path()
    fill_stroke(ctx, PAL["grass"], OUT * 0.9)
    # flores
    for fx in (230, 330, 900, 980):
        _flower(ctx, fx, g - 10, t)
    # agujero
    hole = p.get("hole")
    if hole:
        hw = hole.get("w", 300)
        depth = hole.get("depth", 0) + hole.get("grow", 0) * t
        hxc = hole.get("x", 540)
        ellipse(ctx, hxc, g + 12, hw / 2, 30)
        fill_stroke(ctx, (0.18, 0.1, 0.06), OUT)
        if depth > 0:
            rrect(ctx, hxc - hw / 2 + 20, g + 12, hw - 40, depth, 20)
            ctx.set_source_rgb(0.16, 0.09, 0.05)
            ctx.fill()
        pile = hole.get("pile", 0) + hole.get("pile_grow", 0) * t
        if pile > 0:
            px = hxc + hw / 2 + 120
            ctx.move_to(px - 150 - pile * 0.4, g + 15)
            ctx.curve_to(px - 80, g - pile * 1.1, px + 80, g - pile * 1.1, px + 150 + pile * 0.4, g + 15)
            ctx.close_path()
            fill_stroke(ctx, lighten(PAL["dirt"], 0.1), OUT)


def _cloud(ctx, x, y, s):
    with saved(ctx):
        ctx.translate(x, y)
        ctx.scale(s, s)
        for cx, cy, r in ((0, 0, 60), (60, -30, 70), (130, 0, 55), (65, 15, 60)):
            circle(ctx, cx, cy, r)
        ctx.set_source_rgb(1, 1, 1)
        ctx.fill_preserve()
        ctx.set_source_rgba(0.75, 0.85, 1, 1)
        ctx.set_line_width(5)
        ctx.stroke()
        for cx, cy, r in ((0, 0, 60), (60, -30, 70), (130, 0, 55), (65, 15, 60)):
            circle(ctx, cx, cy, r - 2)
        ctx.set_source_rgb(1, 1, 1)
        ctx.fill()


def _house(ctx, x, g):
    rrect(ctx, x, g - 420, 300, 420, 12)
    fill_stroke(ctx, (1.0, 0.86, 0.62), OUT)
    ctx.move_to(x - 40, g - 400)
    ctx.line_to(x + 150, g - 600)
    ctx.line_to(x + 340, g - 400)
    ctx.close_path()
    fill_stroke(ctx, PAL["red"], OUT)
    rrect(ctx, x + 40, g - 330, 90, 90, 8)
    fill_stroke(ctx, (0.6, 0.85, 1), OUT * 0.8)
    rrect(ctx, x + 170, g - 220, 85, 220, 10)
    fill_stroke(ctx, (0.6, 0.38, 0.25), OUT * 0.8)


def _flower(ctx, x, y, t):
    sw = 4 * math.sin(t * 2 + x)
    ctx.move_to(x, y)
    ctx.line_to(x + sw, y - 50)
    ctx.set_source_rgb(*PAL["grass_dk"])
    ctx.set_line_width(6)
    ctx.stroke()
    for i in range(5):
        a = i * 2 * math.pi / 5 + t
        circle(ctx, x + sw + 16 * math.cos(a), y - 50 + 16 * math.sin(a), 11)
    fill_stroke(ctx, PAL["pink"], 3)
    circle(ctx, x + sw, y - 50, 9)
    fill_stroke(ctx, PAL["yellow"], 3)


def _pebbles(ctx, y0, y1, seed=1, scroll=0.0, tint=None, density=1.0):
    rng = np.random.default_rng(seed)
    n = int(40 * density)
    span = y1 - y0
    for i in range(n):
        x = rng.uniform(-200, W + 200)
        y = y0 + ((rng.uniform(0, span) - scroll) % span)
        r = rng.uniform(8, 26)
        c = mix(PAL["dirt"], (0.35, 0.3, 0.3), rng.uniform(0.1, 0.6)) if tint is None else tint
        ellipse(ctx, x, y, r, r * 0.7, rng.uniform(0, 3))
        ctx.set_source_rgba(*darken(c, 0.15), 0.9)
        ctx.fill()


# Capas de la Tierra (km, color) — profundidades aproximadas reales
LAYERS = [
    (0, "#8B5A2B"), (2, "#7A4A25"), (6, "#6B5B53"), (15, "#5D5A63"), (35, "#B5452B"),
    (400, "#C9502A"), (2900, "#F08A24"), (5150, "#FFE08A"), (6371, "#FFF6D6"),
]


def layer_color(depth_km):
    for i in range(len(LAYERS) - 1):
        d0, c0 = LAYERS[i]
        d1, c1 = LAYERS[i + 1]
        if depth_km <= d1:
            return mix(c0, c1, (depth_km - d0) / max(1e-6, d1 - d0))
    return col(LAYERS[-1][1])


def bg_strata(ctx, t, p):
    """Corte del subsuelo con túnel central; `scroll` simula el descenso."""
    d0, d1 = p.get("depth_from", 0.0), p.get("depth_to", 4.0)
    dur = p.get("_dur", 3.0)
    scroll = p.get("scroll", 900) * t
    heat = p.get("heat", 0.0)
    base = layer_color(lerp(d0, d1, clamp(t / dur)))
    ctx.rectangle(-M, -M, W + 2 * M, H + 2 * M)
    ctx.set_source_rgb(*base)
    ctx.fill()
    # bandas sedimentarias onduladas que suben
    band_h = 260
    k0 = int((scroll - M) // band_h) - 1
    for k in range(k0, k0 + int((H + 2 * M) / band_h) + 3):
        y = k * band_h - scroll
        c = darken(base, 0.08 if k % 2 else -0.0) if k % 3 else lighten(base, 0.07)
        ctx.move_to(-M, y)
        for x in range(-M, W + M + 1, 120):
            ctx.line_to(x, y + 25 * math.sin(x * 0.006 + k * 1.3))
        ctx.line_to(W + M, y + band_h + 40)
        ctx.line_to(-M, y + band_h + 40)
        ctx.close_path()
        ctx.set_source_rgb(*c)
        ctx.fill()
        rng = np.random.default_rng(1000 + k)
        # decoraciones por banda: piedras, fósiles, gemas, gusanos
        for j in range(5):
            x = rng.uniform(-100, W + 100)
            yy = y + rng.uniform(30, band_h - 30)
            if abs(x - 540) < 230:
                continue
            kind = rng.choice(["rock", "rock", "rock", "bone", "gem", "worm"] if d1 < 40 else ["rock", "rock", "gem"])
            draw_prop(ctx, {"type": kind, "x": x, "y": yy, "scale": rng.uniform(0.6, 1.1),
                            "rot": rng.uniform(-1, 1), "seed": int(k * 10 + j)}, t)
    if heat > 0:
        ctx.rectangle(-M, -M, W + 2 * M, H + 2 * M)
        ctx.set_source(linear_grad(ctx, 0, 0, 0, H, [(0, (1, 0.3, 0.1), 0.0), (1, (1, 0.25, 0.05), 0.55 * heat)]))
        ctx.fill()
    # túnel central
    sw = p.get("shaft", 400)
    rrect(ctx, 540 - sw / 2, -M, sw, H + 2 * M, 40)
    ctx.set_source(linear_grad(ctx, 540 - sw / 2, 0, 540 + sw / 2, 0,
                               [(0, darken(base, 0.75)), (0.5, darken(base, 0.55)), (1, darken(base, 0.75))]))
    ctx.fill()
    for s in (-1, 1):
        ctx.move_to(540 + s * sw / 2, -M)
        for y in range(-M, H + M, 60):
            ctx.line_to(540 + s * (sw / 2 + 10 * noise1((y + scroll) * 0.02, 5 + s)), y)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(OUT)
        ctx.stroke()


def bg_earth_section(ctx, t, p):
    """Planeta cortado por la mitad mostrando capas. Útil para escalas y 'dónde estamos'."""
    bg_space(ctx, t, {"stars": True})
    cx, cy = p.get("cx", 540), p.get("cy", 960)
    R = p.get("R", 430)
    rot = t * 0.05
    hl = p.get("highlight")
    layers = [("crust", 1.0, "#7A4A25"), ("mantle", 0.985, "#D9542B"), ("outer_core", 0.546, "#F7A531"),
              ("inner_core", 0.19, "#FFF0B0")]
    # superficie (océanos y continentes)
    circle(ctx, cx, cy, R + 14)
    fill_stroke(ctx, (0.25, 0.55, 0.95), OUT)
    with saved(ctx):
        circle(ctx, cx, cy, R + 14)
        ctx.clip()
        for i in range(6):
            a = rot + i * 1.05
            blob(ctx, cx + (R + 10) * math.cos(a), cy + (R + 10) * math.sin(a), 70 + 20 * (i % 3), seed=i)
            ctx.set_source_rgb(*PAL["grass"])
            ctx.fill()
    for name, frac, c in layers:
        r = R * frac
        circle(ctx, cx, cy, r)
        cc = col(c)
        if hl and name != hl:
            cc = mix(cc, (0.3, 0.3, 0.35), 0.45)
        if name == "inner_core":
            ctx.set_source(radial_grad(ctx, cx, cy, 0, r, [(0, (1, 1, 1)), (1, cc)]))
            ctx.fill_preserve()
            ctx.set_source_rgb(*INK)
            ctx.set_line_width(OUT * 0.8)
            ctx.stroke()
        else:
            fill_stroke(ctx, cc, OUT * 0.8)
    if hl:
        r = R * dict((n, f) for n, f, _ in layers)[hl]
        circle(ctx, cx, cy, r + 4)
        ctx.set_source_rgba(1, 1, 1, 0.5 + 0.5 * math.sin(t * 6))
        ctx.set_line_width(10)
        ctx.stroke()
    # perforación desde la superficie
    hole = p.get("hole")
    if hole is not None:
        frac = hole if isinstance(hole, (int, float)) else hole.get("frac", 0.0)
        ctx.move_to(cx, cy - R - 14)
        ctx.line_to(cx, cy - R + R * frac)
        ctx.set_source_rgb(0.1, 0.05, 0.03)
        ctx.set_line_width(14)
        ctx.stroke()
        circle(ctx, cx, cy - R + R * frac, 18 + 4 * math.sin(t * 10))
        fill_stroke(ctx, PAL["red"], OUT * 0.8)
    for lab in p.get("labels", []):
        ly = cy - R * lab.get("frac", 0.5)
        text(ctx, lab["text"], lab.get("x", cx + R + 10), ly, lab.get("size", 50),
             color=lab.get("color", "white"), align=lab.get("align", "left"), outline=8)


def bg_space(ctx, t, p):
    _sky(ctx, (0.05, 0.05, 0.18), (0.12, 0.08, 0.3))
    rng = np.random.default_rng(42)
    for i in range(140):
        x, y = rng.uniform(-M, W + M), rng.uniform(-M, H + M)
        tw = 0.5 + 0.5 * math.sin(t * rng.uniform(1, 4) + i)
        circle(ctx, x, y, rng.uniform(1.5, 4.5) * (0.6 + 0.4 * tw))
        ctx.set_source_rgba(1, 1, 0.9, 0.4 + 0.6 * tw)
        ctx.fill()
    if p.get("earth"):
        e = p["earth"]
        _earth_globe(ctx, e.get("x", 600), e.get("y", 1000), e.get("r", 230), t, e.get("field", False), e.get("wind", False))


def _earth_globe(ctx, x, y, r, t, field=False, wind=False):
    if wind:
        # viento solar: partículas desde la izquierda que se desvían
        rng = np.random.default_rng(5)
        for i in range(70):
            ph = (t * 0.6 + rng.random()) % 1
            yy = rng.uniform(y - 700, y + 700)
            xx = -200 + ph * (x + 200)
            dy = yy - y
            if abs(dy) < r * 2.2 and xx > x - r * 3:
                k = clamp((xx - (x - r * 3)) / (r * 2))
                yy = yy + math.copysign(1, dy or 1) * k * (r * 2.3 - abs(dy)) * 0.9
            circle(ctx, xx, yy, 7)
            ctx.set_source_rgba(1, 0.85, 0.3, 0.9)
            ctx.fill()
    if field:
        for i in range(1, 6):
            k = 1 + i * 0.55
            for s in (-1, 1):
                with saved(ctx):
                    ctx.translate(x, y)
                    ctx.scale(s, 1)
                    ctx.move_to(0, -r * 0.95)
                    ctx.curve_to(r * k * 1.6, -r * k * 1.4, r * k * 1.6, r * k * 1.4, 0, r * 0.95)
                    ctx.set_dash([28, 18], -t * 80 * s)
                    ctx.set_source_rgba(0.45, 0.85, 1, 0.85 - i * 0.12)
                    ctx.set_line_width(7)
                    ctx.stroke()
                    ctx.set_dash([])
    circle(ctx, x, y, r)
    fill_stroke(ctx, (0.25, 0.55, 0.95), OUT)
    with saved(ctx):
        circle(ctx, x, y, r)
        ctx.clip()
        for i in range(5):
            a = t * 0.3 + i * 1.3
            bx = x + math.cos(a) * r * 0.75
            blob(ctx, bx, y + (i - 2) * r * 0.35, r * 0.32, seed=i + 3)
            ctx.set_source_rgb(*PAL["grass"])
            ctx.fill()
        circle(ctx, x + r * 0.35, y + r * 0.3, r * 1.0)
        ctx.set_source_rgba(0, 0, 0.1, 0.25)
        ctx.fill()
    circle(ctx, x, y, r)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(OUT)
    ctx.stroke()


def bg_mantle(ctx, t, p):
    ctx.rectangle(-M, -M, W + 2 * M, H + 2 * M)
    ctx.set_source(linear_grad(ctx, 0, 0, 0, H, [(0, "#A8341F"), (1, "#E8692A")]))
    ctx.fill()
    # celdas de convección: manchas que se desplazan muy despacio
    rng = np.random.default_rng(9)
    for i in range(16):
        x0, y0 = rng.uniform(-200, W + 200), rng.uniform(-200, H + 200)
        x = x0 + 60 * math.sin(t * 0.4 + i)
        y = y0 + 80 * math.cos(t * 0.3 + i * 0.7) - t * 25 * (1 if i % 2 else -1)
        blob(ctx, x, y, rng.uniform(110, 230), n=10, wobble=0.22, seed=i, t=t * 0.3)
        c = darken("#B23A20", rng.uniform(0, 0.35)) if i % 3 else lighten("#E8692A", 0.15)
        ctx.set_source_rgba(*c, 0.9)
        ctx.fill_preserve()
        ctx.set_source_rgba(*INK, 0.5)
        ctx.set_line_width(OUT * 0.7)
        ctx.stroke()
    # grietas incandescentes
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(10):
        x = rng.uniform(0, W)
        y = rng.uniform(0, H)
        ctx.move_to(x, y)
        for k in range(5):
            x += rng.uniform(-90, 90)
            y += rng.uniform(40, 120)
            ctx.line_to(x, y)
        glow = 0.6 + 0.4 * math.sin(t * 3 + i)
        ctx.set_source_rgba(1, 0.85, 0.3, glow)
        ctx.set_line_width(9)
        ctx.stroke()
    # flechas de convección
    if p.get("flow_arrows", True):
        for i, (x, y, s) in enumerate(((180, 500, 1), (900, 1350, -1))):
            with saved(ctx):
                ctx.translate(x, y)
                ctx.rotate(t * 0.15 * s)
                ctx.arc(0, 0, 150, 0.3, 4.5)
                ctx.set_dash([40, 25], -t * 30)
                ctx.set_source_rgba(1, 0.95, 0.6, 0.7)
                ctx.set_line_width(14)
                ctx.stroke()
                ctx.set_dash([])


def bg_outer_core(ctx, t, p):
    ctx.rectangle(-M, -M, W + 2 * M, H + 2 * M)
    ctx.set_source(linear_grad(ctx, 0, 0, 0, H, [(0, "#5C1A10"), (0.35, "#C2461F"), (1, "#FF9A2E")]))
    ctx.fill()
    surf = p.get("surface", 1150)
    # techo del manto
    ctx.move_to(-M, -M)
    ctx.line_to(W + M, -M)
    ctx.line_to(W + M, 260)
    for x in range(W + M, -M - 1, -90):
        ctx.line_to(x, 240 + 50 * noise1(x * 0.01, 4))
    ctx.close_path()
    fill_stroke(ctx, "#7A2416", OUT)
    # océano de hierro líquido
    for layer in range(3):
        y0 = surf + layer * 120
        c = mix("#FFB347", "#FF7A1A", layer / 2)
        ctx.move_to(-M, H + M)
        for x in range(-M, W + M + 1, 30):
            ctx.line_to(x, y0 + 28 * math.sin(x * 0.012 + t * (2.5 - layer * 0.5) + layer) +
                        12 * math.sin(x * 0.03 - t * 3))
        ctx.line_to(W + M, H + M)
        ctx.close_path()
        fill_stroke(ctx, c, OUT * (1 if layer == 0 else 0.6))
    # remolinos (corrientes que generan el campo magnético)
    for i, (x, y) in enumerate(((250, surf + 330), (800, surf + 480), (520, surf + 650))):
        with saved(ctx):
            ctx.translate(x, y)
            ctx.rotate(t * (1.2 if i % 2 else -1.2))
            ctx.new_path()
            for k in range(60):
                a = k * 0.25
                r = 4 + k * 2.2
                (ctx.move_to if k == 0 else ctx.line_to)(r * math.cos(a), r * math.sin(a) * 0.6)
            ctx.set_source_rgba(1, 0.95, 0.7, 0.75)
            ctx.set_line_width(7)
            ctx.stroke()
    # burbujas
    rng = np.random.default_rng(2)
    for i in range(18):
        ph = (t * 0.5 + rng.random()) % 1
        x = rng.uniform(0, W) + 15 * math.sin(t * 3 + i)
        y = H + 50 - ph * (H + 50 - surf)
        circle(ctx, x, y, rng.uniform(8, 20) * (1 - ph * 0.5))
        ctx.set_source_rgba(1, 0.95, 0.75, 0.8 * (1 - ph))
        ctx.fill()


def bg_inner_core(ctx, t, p):
    ctx.rectangle(-M, -M, W + 2 * M, H + 2 * M)
    ctx.set_source(linear_grad(ctx, 0, 0, 0, H, [(0, "#B8461C"), (1, "#FF9A2E")]))
    ctx.fill()
    cx, cy = p.get("cx", 540), p.get("cy", 1500)
    r = p.get("r", 640) * (1 + 0.01 * math.sin(t * 5))
    for i in range(18):
        a = i * math.pi / 9 + t * 0.2
        ctx.move_to(cx, cy)
        ctx.line_to(cx + 2000 * math.cos(a - 0.06), cy + 2000 * math.sin(a - 0.06))
        ctx.line_to(cx + 2000 * math.cos(a + 0.06), cy + 2000 * math.sin(a + 0.06))
        ctx.close_path()
    ctx.set_source_rgba(1, 0.9, 0.5, 0.25)
    ctx.fill()
    circle(ctx, cx, cy, r * 1.25)
    ctx.set_source(radial_grad(ctx, cx, cy, r * 0.9, r * 1.25, [(0, (1, 0.95, 0.7), 0.8), (1, (1, 0.8, 0.4), 0.0)]))
    ctx.fill()
    circle(ctx, cx, cy, r)
    ctx.set_source(radial_grad(ctx, cx - r * 0.2, cy - r * 0.3, 0, r, [(0, (1, 1, 1)), (0.6, "#FFF2B0"), (1, "#FFC94A")]))
    ctx.fill_preserve()
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(OUT)
    ctx.stroke()
    # cristales de hierro en la superficie
    with saved(ctx):
        circle(ctx, cx, cy, r)
        ctx.clip()
        rng = np.random.default_rng(8)
        for i in range(26):
            a = rng.uniform(math.pi, 2 * math.pi)
            rr = rng.uniform(0.3, 0.95) * r
            x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
            ctx.move_to(x, y - 30)
            ctx.line_to(x + 18, y)
            ctx.line_to(x, y + 30)
            ctx.line_to(x - 18, y)
            ctx.close_path()
            ctx.set_source_rgba(1, 1, 1, 0.35 + 0.3 * math.sin(t * 4 + i))
            ctx.fill()


def bg_center(ctx, t, p):
    ctx.rectangle(-M, -M, W + 2 * M, H + 2 * M)
    ctx.set_source(radial_grad(ctx, 540, 900, 0, 1300, [(0, (1, 1, 0.95)), (0.4, "#FFE07A"), (1, "#FF8A2A")]))
    ctx.fill()
    for i in range(5):
        r = ((t * 220 + i * 260) % 1300)
        circle(ctx, 540, 900, r)
        ctx.set_source_rgba(1, 1, 1, 0.5 * (1 - r / 1300))
        ctx.set_line_width(14)
        ctx.stroke()
    rng = np.random.default_rng(4)
    for i in range(40):
        x = rng.uniform(0, W) + 30 * math.sin(t + i)
        y = rng.uniform(0, H) + 30 * math.cos(t * 0.8 + i)
        star(ctx, x, y, rng.uniform(6, 16) * (0.6 + 0.4 * math.sin(t * 4 + i)), n=4, inner=0.35)
        ctx.set_source_rgba(1, 1, 1, 0.85)
        ctx.fill()


def bg_burst(ctx, t, p):
    """Fondo de cómic con rayos radiales (énfasis / gancho)."""
    c1, c2 = col(p.get("c1", "#FFD23F")), col(p.get("c2", "#FF8A2A"))
    ctx.rectangle(-M, -M, W + 2 * M, H + 2 * M)
    ctx.set_source_rgb(*c1)
    ctx.fill()
    cx, cy = p.get("cx", 540), p.get("cy", 900)
    with saved(ctx):
        ctx.translate(cx, cy)
        ctx.rotate(t * 0.4)
        for i in range(16):
            a = i * math.pi / 8
            ctx.move_to(0, 0)
            ctx.arc(0, 0, 2500, a, a + math.pi / 16)
            ctx.close_path()
        ctx.set_source_rgb(*c2)
        ctx.fill()


def bg_ocean(ctx, t, p):
    _sky(ctx, (0.4, 0.75, 1), (0.75, 0.92, 1))
    lvl = p.get("level", 900)
    for k in range(4):
        y0 = lvl + k * 90
        ctx.move_to(-M, H + M)
        for x in range(-M, W + M + 1, 30):
            ctx.line_to(x, y0 + 22 * math.sin(x * 0.01 + t * (2 - k * 0.3) + k))
        ctx.line_to(W + M, H + M)
        ctx.close_path()
        fill_stroke(ctx, mix((0.2, 0.6, 0.95), (0.05, 0.2, 0.55), k / 3), OUT * 0.6)


def bg_mars(ctx, t, p):
    _sky(ctx, "#E8A27A", "#F5C9A0")
    g = p.get("ground", 1350)
    circle(ctx, 820, 380, 70)
    fill_stroke(ctx, (1, 0.95, 0.85), OUT)
    ctx.move_to(-M, g - 120)
    ctx.curve_to(200, g - 300, 500, g - 140, 700, g - 260)
    ctx.curve_to(900, g - 360, 1000, g - 200, W + M, g - 160)
    ctx.line_to(W + M, H + M)
    ctx.line_to(-M, H + M)
    ctx.close_path()
    fill_stroke(ctx, "#C1440E", OUT)
    _pebbles(ctx, g, H, seed=6, tint=col("#8E2C08"))


def bg_color(ctx, t, p):
    c = col(p.get("color", "#2B2D6E"))
    ctx.rectangle(-M, -M, W + 2 * M, H + 2 * M)
    ctx.set_source(radial_grad(ctx, 540, 900, 0, 1400, [(0, lighten(c, 0.25)), (1, darken(c, 0.25))]))
    ctx.fill()


_IMG_CACHE: dict = {}


def bg_image(ctx, t, p):
    """Fondo de imagen (IA o propia) con 'cover' y Ken Burns suave."""
    path = p["path"]
    if path not in _IMG_CACHE:
        from PIL import Image
        im = Image.open(path).convert("RGB")
        w, h = im.size
        sc = max((W + 2 * 200) / w, (H + 2 * 200) / h)
        im = im.resize((int(w * sc), int(h * sc)))
        im.putalpha(255)
        b = bytearray(im.tobytes("raw", "BGRA"))
        _IMG_CACHE[path] = cairo.ImageSurface.create_for_data(b, cairo.FORMAT_ARGB32, im.width, im.height)
    surf = _IMG_CACHE[path]
    k = p.get("kenburns", 0.06) * t / max(1e-3, p.get("_dur", 3))
    with saved(ctx):
        ctx.translate(W / 2, H / 2)
        ctx.scale(1 + k, 1 + k)
        ctx.translate(-surf.get_width() / 2, -surf.get_height() / 2)
        ctx.set_source_surface(surf, 0, 0)
        ctx.paint()


BACKGROUNDS = {
    "image": bg_image,
    "backyard": bg_backyard, "strata": bg_strata, "earth_section": bg_earth_section, "space": bg_space,
    "mantle": bg_mantle, "outer_core": bg_outer_core, "inner_core": bg_inner_core, "center": bg_center,
    "burst": bg_burst, "ocean": bg_ocean, "mars": bg_mars, "color": bg_color,
}


def draw_background(ctx, spec: dict, t: float, dur: float):
    p = dict(spec)
    p["_dur"] = dur
    BACKGROUNDS.get(spec.get("type", "color"), bg_color)(ctx, t, p)


# ============================================================================
# PROPS
# ============================================================================
def _rock(ctx, p, t):
    blob(ctx, 0, 0, 40, n=7, wobble=0.25, seed=p.get("seed", 0))
    fill_stroke(ctx, p.get("color", (0.55, 0.5, 0.5)), OUT * 0.8)


def _gem(ctx, p, t):
    c = col(p.get("color", ["#5CE1E6", "#B388FF", "#FF5CA8", "#7CFF6B"][p.get("seed", 0) % 4]))
    ctx.move_to(0, -38)
    ctx.line_to(30, -10)
    ctx.line_to(0, 40)
    ctx.line_to(-30, -10)
    ctx.close_path()
    fill_stroke(ctx, c, OUT * 0.8)
    ctx.move_to(-30, -10)
    ctx.line_to(30, -10)
    ctx.set_line_width(3)
    ctx.stroke()
    star(ctx, 12, -18, 8 * (0.5 + 0.5 * math.sin(t * 5 + p.get("seed", 0))), n=4, inner=0.3)
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill()


def _bone(ctx, p, t):
    with saved(ctx):
        limb(ctx, [(-45, 0), (45, 0)], 18, (0.98, 0.95, 0.85), out=OUT * 0.7)
        for x in (-48, 48):
            for y in (-10, 10):
                circle(ctx, x, y, 14)
                fill_stroke(ctx, (0.98, 0.95, 0.85), OUT * 0.7)
        limb(ctx, [(-45, 0), (45, 0)], 18, (0.98, 0.95, 0.85), out=0)


def _worm(ctx, p, t):
    pts = [(-60 + i * 20, 10 * math.sin(i * 1.1 + t * 6)) for i in range(7)]
    for w, c in ((30 + 2 * OUT * 0.7, INK), (30, (1, 0.6, 0.65))):
        ctx.set_line_width(w)
        ctx.set_source_rgb(*col(c))
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.move_to(*pts[0])
        for q in pts[1:]:
            ctx.line_to(*q)
        ctx.stroke()
    circle(ctx, 62, pts[-1][1] - 4, 4)
    ctx.set_source_rgb(*INK)
    ctx.fill()


def _sign(ctx, p, t):
    txt = p.get("text", "")
    lines = txt.split("\n")
    w = p.get("w", 520)
    h = 70 + 62 * len(lines)
    limb(ctx, [(0, 0), (0, 230)], 26, (0.6, 0.38, 0.22), out=OUT * 0.8)
    with saved(ctx):
        ctx.rotate(0.03 * math.sin(t * 2))
        rrect(ctx, -w / 2, -h, w, h, 18)
        fill_stroke(ctx, p.get("color", (0.85, 0.6, 0.35)), OUT)
        for i, ln in enumerate(lines):
            text(ctx, ln, 0, -h + 62 + i * 62, p.get("size", 54), color=p.get("text_color", "white"),
                 outline=7, max_w=w - 40, shadow_off=3)


def _thermometer(ctx, p, t):
    lvl = clamp(p.get("level", 0.5) * clamp(p.get("_age", 1) / 0.8))
    rrect(ctx, -32, -260, 64, 280, 32)
    fill_stroke(ctx, (1, 1, 1), OUT)
    circle(ctx, 0, 40, 55)
    fill_stroke(ctx, PAL["red"], OUT)
    rrect(ctx, -16, -240 + 240 * (1 - lvl), 32, 240 * lvl + 40, 16)
    ctx.set_source_rgb(*PAL["red"])
    ctx.fill()
    for i in range(5):
        ctx.move_to(32, -220 + i * 50)
        ctx.line_to(12, -220 + i * 50)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(4)
    ctx.stroke()
    if p.get("text"):
        text(ctx, p["text"], 0, -320, p.get("size", 72), color=p.get("text_color", "#FFD23F"), outline=9)


def _clock(ctx, p, t):
    spd = p.get("speed", 6.0)
    circle(ctx, 0, 0, 120)
    fill_stroke(ctx, (1, 1, 1), OUT)
    for i in range(12):
        a = i * math.pi / 6
        ctx.move_to(100 * math.cos(a), 100 * math.sin(a))
        ctx.line_to(85 * math.cos(a), 85 * math.sin(a))
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(6)
    ctx.stroke()
    for ln, sp, w in ((70, spd / 12, 12), (95, spd, 7)):
        a = t * sp * 2 * math.pi - math.pi / 2
        ctx.move_to(0, 0)
        ctx.line_to(ln * math.cos(a), ln * math.sin(a))
        ctx.set_line_width(w)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()
    circle(ctx, 0, 0, 12)
    fill_stroke(ctx, PAL["red"], 4)
    for s in (-1, 1):  # campanas
        circle(ctx, s * 80, -110, 34)
        fill_stroke(ctx, PAL["red"], OUT)


def _calendar(ctx, p, t):
    rrect(ctx, -110, -120, 220, 240, 18)
    fill_stroke(ctx, (1, 1, 1), OUT)
    rrect(ctx, -110, -120, 220, 70, 18)
    fill_stroke(ctx, PAL["red"], OUT)
    yrs = int(p.get("from", 2026) + (p.get("to", 2726) - p.get("from", 2026)) * clamp(p.get("_age", 0) / p.get("over", 2.5)))
    text(ctx, str(yrs), 0, 30, 76, color=INK, outline=0, shadow_off=0)
    text(ctx, p.get("label", "AÑO"), 0, -85, 34, outline=0, shadow_off=0)


def _pipe(ctx, p, t):
    """Tubería de perforación que baja desde arriba (pozo de Kola)."""
    y_end = p.get("end", 0)
    rrect(ctx, -26, -2200, 52, 2200 + y_end, 8)
    ctx.set_source(linear_grad(ctx, -26, 0, 26, 0, [(0, PAL["metal_dk"]), (0.5, (0.95, 0.95, 1)), (1, PAL["metal_dk"])]))
    ctx.fill_preserve()
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(OUT * 0.8)
    ctx.stroke()
    for k in range(-12, 0):
        rrect(ctx, -34, y_end + k * 180, 68, 22, 6)
        fill_stroke(ctx, PAL["metal_dk"], OUT * 0.6)
    ctx.move_to(-40, y_end)
    ctx.line_to(40, y_end)
    ctx.line_to(0, y_end + 70)
    ctx.close_path()
    fill_stroke(ctx, PAL["yellow"], OUT * 0.8)


def _magnet(ctx, p, t):
    ctx.arc(0, 0, 110, math.pi, 2 * math.pi)
    ctx.set_line_width(70 + 2 * OUT)
    ctx.set_source_rgb(*INK)
    ctx.stroke()
    ctx.arc(0, 0, 110, math.pi, 2 * math.pi)
    ctx.set_line_width(70)
    ctx.set_source_rgb(*PAL["red"])
    ctx.stroke()
    for s in (-1, 1):
        rrect(ctx, s * 110 - 35, 0, 70, 60, 6)
        fill_stroke(ctx, PAL["metal"], OUT)


def _sun(ctx, p, t):
    with saved(ctx):
        ctx.rotate(t * 0.5)
        for i in range(14):
            ctx.rotate(math.pi / 7)
            ctx.move_to(-25, -120)
            ctx.line_to(0, -190)
            ctx.line_to(25, -120)
            ctx.close_path()
        ctx.set_source_rgb(1, 0.75, 0.2)
        ctx.fill()
    circle(ctx, 0, 0, 125)
    ctx.set_source(radial_grad(ctx, -30, -30, 0, 125, [(0, (1, 1, 0.8)), (1, (1, 0.7, 0.15))]))
    ctx.fill_preserve()
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(OUT)
    ctx.stroke()
    if p.get("face", True):
        for s in (-1, 1):
            circle(ctx, s * 38, -15, 12)
            ctx.set_source_rgb(*INK)
            ctx.fill()
        ctx.arc(0, 20, 40, 0.2, math.pi - 0.2)
        ctx.set_line_width(8)
        ctx.stroke()


def _earth(ctx, p, t):
    axis = p.get("axis")
    if axis is not None:  # eje de rotación inclinado (grados); `wobble` lo hace bambolearse
        a = math.radians(axis + p.get("wobble", 0) * math.sin(t * 2.2))
        r = p.get("r", 120)
        with saved(ctx):
            ctx.rotate(a)
            limb(ctx, [(0, -r * 1.45), (0, r * 1.45)], 10, PAL["red"], out=OUT * 0.6)
    _earth_globe(ctx, 0, 0, p.get("r", 120), t, p.get("field", False))


def _lamp(ctx, p, t):
    fl = 0.85 + 0.15 * noise1(t * 12, p.get("seed", 1))
    ctx.move_to(0, -200)
    ctx.line_to(0, -40)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(5)
    ctx.stroke()
    circle(ctx, 0, 0, 160)
    ctx.set_source(radial_grad(ctx, 0, 0, 10, 160, [(0, (1, 0.95, 0.6), 0.55 * fl), (1, (1, 0.9, 0.5), 0)]))
    ctx.fill()
    ellipse(ctx, 0, 0, 28, 36)
    fill_stroke(ctx, (1, 0.95, 0.6), OUT * 0.7)


def _cart(ctx, p, t):
    rrect(ctx, -130, -110, 260, 110, 10)
    fill_stroke(ctx, PAL["metal_dk"], OUT)
    for x in (-80, 80):
        circle(ctx, x, 10, 32)
        fill_stroke(ctx, (0.3, 0.3, 0.35), OUT)
    for i in range(5):
        blob(ctx, -90 + i * 45, -120, 32, seed=i)
        fill_stroke(ctx, "#5D5A63", OUT * 0.6)


def _arrow(ctx, p, t):
    ln = p.get("length", 220)
    c = p.get("color", PAL["yellow"])
    pulse = 1 + 0.08 * math.sin(t * 10)
    with saved(ctx):
        ctx.scale(pulse, pulse)
        ctx.move_to(-ln / 2, -26)
        ctx.line_to(ln / 2 - 70, -26)
        ctx.line_to(ln / 2 - 70, -70)
        ctx.line_to(ln / 2, 0)
        ctx.line_to(ln / 2 - 70, 70)
        ctx.line_to(ln / 2 - 70, 26)
        ctx.line_to(-ln / 2, 26)
        ctx.close_path()
        fill_stroke(ctx, c, OUT)


def _gravity_arrows(ctx, p, t):
    """Flechas hacia fuera en todas direcciones: gravedad que tira por igual."""
    n = p.get("n", 8)
    r0 = p.get("r", 330)
    for i in range(n):
        a = i * 2 * math.pi / n + 0.2
        r = r0 + 25 * math.sin(t * 6 + i)
        with saved(ctx):
            ctx.translate(r * math.cos(a), r * math.sin(a))
            ctx.rotate(a)
            _arrow(ctx, {"length": 170, "color": PAL["blue"]}, t)


def _pressure(ctx, p, t):
    """Flechas hacia dentro (presión)."""
    n = p.get("n", 8)
    for i in range(n):
        a = i * 2 * math.pi / n
        r = p.get("r", 480) - 40 * abs(math.sin(t * 5))
        with saved(ctx):
            ctx.translate(r * math.cos(a), r * math.sin(a))
            ctx.rotate(a + math.pi)
            _arrow(ctx, {"length": 200, "color": PAL["red"]}, t)


def _skull(ctx, p, t):
    circle(ctx, 0, -10, 70)
    fill_stroke(ctx, (1, 1, 0.95), OUT)
    rrect(ctx, -40, 30, 80, 50, 12)
    fill_stroke(ctx, (1, 1, 0.95), OUT)
    for s in (-1, 1):
        ellipse(ctx, s * 28, -10, 20, 24)
        ctx.set_source_rgb(*INK)
        ctx.fill()


def _question(ctx, p, t):
    with saved(ctx):
        ctx.rotate(0.15 * math.sin(t * 3))
        text(ctx, p.get("char", "?"), 0, 0, p.get("size", 220), color=p.get("color", "#FFD23F"), outline=12)


def _speedlines(ctx, p, t):
    """Líneas de velocidad verticales (caída / descenso rápido)."""
    rng = np.random.default_rng(p.get("seed", 3))
    d = p.get("dir", -1)   # -1 = líneas suben (personaje baja)
    for i in range(26):
        x = rng.uniform(-500, 500)
        ln = rng.uniform(150, 420)
        ph = (t * rng.uniform(1.8, 3.2) + rng.random()) % 1
        y = (1000 - ph * 2400) * (-d)
        ctx.move_to(x, y)
        ctx.line_to(x, y + ln)
        ctx.set_source_rgba(1, 1, 1, 0.5)
        ctx.set_line_width(rng.uniform(4, 10))
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()


def _debris(ctx, p, t):
    """Piedrecitas saltando (excavación/taladro)."""
    rng = np.random.default_rng(p.get("seed", 1))
    c = col(p.get("color", PAL["dirt"]))
    spread = p.get("spread", 1.0)
    for i in range(p.get("n", 22)):
        period = rng.uniform(0.5, 0.9)
        ph = ((t + rng.random() * period) % period) / period
        vx = rng.uniform(-420, 420) * spread
        vy = rng.uniform(-900, -500)
        x = vx * ph * period
        y = vy * ph * period + 0.5 * 2600 * (ph * period) ** 2
        r = rng.uniform(7, 16) * (1 - ph * 0.4)
        circle(ctx, x, y, r)
        fill_stroke(ctx, lighten(c, rng.uniform(-0.1, 0.25)), 3)


def _sparks(ctx, p, t):
    rng = np.random.default_rng(p.get("seed", 2))
    for i in range(p.get("n", 30)):
        ph = (t * rng.uniform(0.6, 1.2) + rng.random()) % 1
        x = rng.uniform(-500, 500) + 40 * math.sin(t * 2 + i)
        y = 400 - ph * 1200
        circle(ctx, x, y, rng.uniform(3, 9) * (1 - ph))
        ctx.set_source_rgba(1, rng.uniform(0.7, 1), 0.4, 1 - ph)
        ctx.fill()


def _heatwaves(ctx, p, t):
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(5):
        x0 = -200 + i * 100
        ph = (t * 0.8 + i * 0.2) % 1
        ctx.move_to(x0, 100 - ph * 300)
        for k in range(8):
            ctx.line_to(x0 + 20 * math.sin(k + t * 6), 100 - ph * 300 - k * 22)
        ctx.set_source_rgba(1, 1, 1, 0.6 * (1 - ph))
        ctx.set_line_width(7)
        ctx.stroke()


def _splash(ctx, p, t):
    age = p.get("_age", 0)
    rng = np.random.default_rng(7)
    c = col(p.get("color", "#FFB347"))
    for i in range(20):
        a = rng.uniform(math.pi * 1.1, math.pi * 1.9)
        v = rng.uniform(500, 1100)
        x = math.cos(a) * v * age
        y = math.sin(a) * v * age + 0.5 * 2800 * age ** 2
        r = rng.uniform(12, 28) * max(0, 1 - age * 0.8)
        if r > 1:
            circle(ctx, x, y, r)
            fill_stroke(ctx, c, 4)
    if age < 0.6:
        ellipse(ctx, 0, 0, 160 + 400 * age, 30 + 40 * age)
        ctx.set_source_rgba(1, 0.95, 0.7, 0.8 * (1 - age / 0.6))
        ctx.set_line_width(10)
        ctx.stroke()


def _vs(ctx, p, t):
    """Comparativa: dos tarjetas lado a lado."""
    for s, item in ((-1, p.get("left", {})), (1, p.get("right", {}))):
        with saved(ctx):
            ctx.translate(s * 240, 0)
            rrect(ctx, -200, -160, 400, 320, 36)
            fill_stroke(ctx, item.get("color", (1, 1, 1)), OUT)
            text(ctx, item.get("title", ""), 0, -95, 56, color="white", outline=8, max_w=360)
            text(ctx, item.get("value", ""), 0, 40, 84, color="#FFD23F", outline=10, max_w=360)
            text(ctx, item.get("sub", ""), 0, 120, 40, color="white", outline=6, max_w=360)
    circle(ctx, 0, 0, 70)
    fill_stroke(ctx, PAL["red"], OUT)
    text(ctx, p.get("mid", "VS"), 0, 0, 64, outline=6, shadow_off=0)


def _drill_rig(ctx, p, t):
    """Torre de perforación (superficie)."""
    ctx.move_to(-160, 0)
    ctx.line_to(-40, -700)
    ctx.line_to(40, -700)
    ctx.line_to(160, 0)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(OUT * 2.4)
    ctx.stroke_preserve()
    ctx.set_source_rgb(*PAL["red"])
    ctx.set_line_width(OUT * 1.2)
    ctx.stroke()
    for k in range(1, 7):
        y = -k * 100
        w = 160 - k * 17
        ctx.move_to(-w, y)
        ctx.line_to(w, y - 100)
        ctx.move_to(w, y)
        ctx.line_to(-w, y - 100)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(6)
    ctx.stroke()


PROPS = {
    "rock": _rock, "gem": _gem, "bone": _bone, "worm": _worm, "sign": _sign, "thermometer": _thermometer,
    "clock": _clock, "calendar": _calendar, "pipe": _pipe, "magnet": _magnet, "sun": _sun, "earth": _earth,
    "lamp": _lamp, "cart": _cart, "arrow": _arrow, "gravity_arrows": _gravity_arrows, "pressure": _pressure,
    "skull": _skull, "question": _question, "speedlines": _speedlines, "debris": _debris, "sparks": _sparks,
    "heatwaves": _heatwaves, "splash": _splash, "vs": _vs, "drill_rig": _drill_rig,
}


def draw_prop(ctx, p: dict, t: float, age: float | None = None):
    """Dibuja un prop con animación de entrada y bucle."""
    f = PROPS.get(p.get("type", ""))
    if f is None:
        return
    age = t if age is None else age
    q = dict(p)
    q["_age"] = age
    x, y = p.get("x", 540), p.get("y", 960)
    if 0 <= x <= 1.5 and 0 <= y <= 1.5 and not p.get("abs"):
        from .screen import SH, SW
        x, y = x * SW, y * SH
    s = p.get("scale", 1.0)
    rot = p.get("rot", 0.0)
    alpha = 1.0
    enter = p.get("enter", "pop")
    ed = p.get("enter_dur", 0.35)
    k = clamp(age / ed) if ed > 0 else 1.0
    if enter == "pop":
        from .draw import ease_back
        s *= ease_back(k) if k < 1 else 1
    elif enter == "drop":
        from .draw import bounce01
        y = lerp(y - 1400, y, bounce01(clamp(age / 0.7)))
    elif enter == "slide_left":
        from .draw import ease_out
        x = lerp(x - 1200, x, ease_out(k))
    elif enter == "slide_right":
        from .draw import ease_out
        x = lerp(x + 1200, x, ease_out(k))
    elif enter == "rise":
        from .draw import ease_out
        y = lerp(y + 1400, y, ease_out(clamp(age / 0.6)))
    elif enter == "fade":
        alpha = k
    loop = p.get("loop")
    if loop == "bob":
        y += 14 * math.sin(t * 3 + x)
    elif loop == "spin":
        rot += t * p.get("spin", 1.5)
    elif loop == "shake":
        x += 6 * noise1(t * 30, 1)
        y += 6 * noise1(t * 30, 2)
    elif loop == "pulse":
        s *= 1 + 0.06 * math.sin(t * 8)
    elif loop == "wobble":
        rot += 0.12 * math.sin(t * 4)
    if s <= 0.001:
        return
    with saved(ctx):
        ctx.translate(x, y)
        ctx.rotate(rot)
        ctx.scale(max(s, 1e-3) * p.get("flip", 1), max(s, 1e-3))
        if alpha < 1:
            ctx.push_group()
            f(ctx, q, t)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(alpha)
        else:
            f(ctx, q, t)
        if p.get("crossed"):
            k = clamp((age - p.get("cross_at", 0.4)) / 0.2)
            if k > 0:
                r = p.get("cross_r", 150)
                ctx.set_line_cap(cairo.LINE_CAP_ROUND)
                for (x0, y0, x1, y1) in ((-r, -r, r, r), (r, -r, -r, r)):
                    ctx.move_to(x0, y0)
                    ctx.line_to(lerp(x0, x1, k), lerp(y0, y1, k))
                    ctx.set_source_rgb(*INK)
                    ctx.set_line_width(46)
                    ctx.stroke_preserve()
                    ctx.set_source_rgb(*PAL["red"])
                    ctx.set_line_width(30)
                    ctx.stroke()


# Catálogo ampliado (Marte, océano, ballenas...)
from . import world2  # noqa: E402,F401
from . import world3  # noqa: E402,F401
from . import world4  # noqa: E402,F401
from . import world5  # noqa: E402,F401
from . import world6  # noqa: E402,F401
from . import world7  # noqa: E402,F401
