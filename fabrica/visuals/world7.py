"""Catálogo «épocas de la historia»: obra de las pirámides (Egipto), calle de Roma con ínsulas y acueducto,
Londres industrial, cubierta de un barco pirata y túnel del tiempo; bloque en trineo, ánfora, moneda, limón,
velero, bomba de agua y medidor de supervivencia.

Fondos diseñados en el lienzo vertical (world.W×world.H): en formato horizontal scene.py muestra una franja.
Suelo de referencia ~1350 para que la franja por defecto (window≈1150, zoom 0.75) enseñe cielo y suelo.
"""
from __future__ import annotations

import math

import cairo
import numpy as np

from .draw import (INK, OUT, PAL, blob, circle, clamp, col, darken, ellipse, fill_stroke, lerp, lighten,
                   limb, linear_grad, mix, noise1, radial_grad, rrect, saved, star, text)
from .world import BACKGROUNDS, H, M, PROPS, W, _cloud, _sky


# ============================================================================ FONDOS
def bg_egypt(ctx, t, p):
    """Meseta de Giza: pirámide en obra (`progress` 0..1), rampa, Nilo al fondo, sol abrasador."""
    g = p.get("ground", 1350)
    _sky(ctx, "#F6B45A", "#FCE3A8")
    sx, sy = 860, 520
    circle(ctx, sx, sy, 190)
    ctx.set_source(radial_grad(ctx, sx, sy, 60, 190, [(0, (1, 0.95, 0.6), 0.9), (1, (1, 0.8, 0.3), 0)]))
    ctx.fill()
    circle(ctx, sx, sy, 80)
    fill_stroke(ctx, "#FFE070", OUT)
    # Nilo y palmeras al fondo
    rrect(ctx, -M, g - 330, W + 2 * M, 40, 10)
    ctx.set_source_rgb(0.25, 0.55, 0.75)
    ctx.fill()
    for x in (-60, 60, 980, 1100):
        limb(ctx, [(x, g - 300), (x + 10, g - 420)], 16, "#8A5A30", out=OUT * 0.6)
        for a in range(5):
            ang = -math.pi / 2 + (a - 2) * 0.55
            ctx.move_to(x + 10, g - 420)
            ctx.curve_to(x + 10 + 60 * math.cos(ang), g - 450 + 30 * math.sin(ang),
                         x + 10 + 90 * math.cos(ang), g - 420 + 60 * math.sin(ang) + 40, x + 10 + 100 * math.cos(ang),
                         g - 400 + 50 * math.sin(ang) + 40)
            ctx.set_source_rgb(*col("#4E8A3A"))
            ctx.set_line_width(14)
            ctx.stroke()
    # pirámide (escalonada mientras se construye) + rampa
    prog = clamp(p.get("progress", 0.7))
    cx, base, half = p.get("cx", 520), g - 290, 430
    hmax = 520
    hcur = hmax * prog
    ctx.move_to(cx - half, base)
    ctx.line_to(cx - half * (1 - prog), base - hcur)
    ctx.line_to(cx + half * (1 - prog), base - hcur)
    ctx.line_to(cx + half, base)
    ctx.close_path()
    fill_stroke(ctx, "#E2C27A", OUT)
    for k in range(1, int(10 * prog) + 1):
        y = base - k * hmax / 10
        if y < base - hcur:
            break
        w = half * (1 - k / 10)
        ctx.move_to(cx - w, y)
        ctx.line_to(cx + w, y)
    ctx.set_source_rgba(*INK, 0.35)
    ctx.set_line_width(4)
    ctx.stroke()
    if prog < 0.99:  # rampa
        ctx.move_to(cx + half + 260, base)
        ctx.line_to(cx + half * (1 - prog) * 0.6, base - hcur)
        ctx.line_to(cx + half * (1 - prog) * 0.6 + 80, base - hcur)
        ctx.line_to(cx + half + 380, base)
        ctx.close_path()
        fill_stroke(ctx, "#C9A060", OUT * 0.8)
    # arena
    ctx.move_to(-M, g - 280)
    for x in range(-M, W + M + 1, 60):
        ctx.line_to(x, g - 280 + 18 * math.sin(x * 0.007 + 1))
    ctx.line_to(W + M, H + M)
    ctx.line_to(-M, H + M)
    ctx.close_path()
    fill_stroke(ctx, "#EFCB86", OUT)
    rng = np.random.default_rng(4)
    for i in range(40):
        x, y = rng.uniform(-M, W + M), rng.uniform(g - 200, H)
        ellipse(ctx, x, y, rng.uniform(8, 20), 3)
        ctx.set_source_rgba(0.7, 0.55, 0.3, 0.5)
        ctx.fill()
    if p.get("heat", True):  # calima
        for i in range(6):
            y = g - 360 + i * 30
            ctx.move_to(-M, y)
            for x in range(-M, W + M + 1, 40):
                ctx.line_to(x, y + 6 * math.sin(x * 0.03 + t * 4 + i))
            ctx.set_source_rgba(1, 1, 1, 0.12)
            ctx.set_line_width(3)
            ctx.stroke()


def bg_rome(ctx, t, p):
    """Calle de Roma: ínsulas de varios pisos, acueducto al fondo, adoquines; `fire` 0..1 añade humo y llamas."""
    g = p.get("ground", 1350)
    _sky(ctx, (0.45, 0.72, 0.98), (0.88, 0.94, 1))
    _cloud(ctx, (200 + t * 12) % 1400 - 250, 330, 0.8)
    # acueducto
    ay = g - 470
    rrect(ctx, -M, ay, W + 2 * M, 40, 4)
    fill_stroke(ctx, "#D7C3A0", OUT)
    for k in range(-3, 10):
        x = k * 150
        ctx.rectangle(x, ay + 40, 150, 200)
        ctx.new_sub_path()
        ctx.arc_negative(x + 75, ay + 140, 52, 0, math.pi)
        ctx.line_to(x + 23, ay + 240)
        ctx.line_to(x + 127, ay + 240)
        ctx.close_path()
    ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    fill_stroke(ctx, "#D7C3A0", OUT * 0.8)
    ctx.set_fill_rule(cairo.FILL_RULE_WINDING)
    # ínsulas
    colors = ["#E9A96B", "#F2D3A2", "#D9825B", "#EBC38F", "#C96F4E"]
    for i, (x, w, floors) in enumerate(((-260, 300, 6), (60, 260, 5), (340, 300, 7), (660, 250, 5), (930, 320, 6))):
        h = floors * 110
        y = g - h
        rrect(ctx, x, y, w, h, 4)
        fill_stroke(ctx, colors[i % 5], OUT)
        for f in range(floors):
            for c in range(int(w // 90)):
                rrect(ctx, x + 30 + c * 90, y + 25 + f * 110, 46, 60, 6)
                fill_stroke(ctx, "#5A3A2A", OUT * 0.5)
        rrect(ctx, x - 12, y - 18, w + 24, 26, 4)
        fill_stroke(ctx, "#B5532F", OUT * 0.8)
        rrect(ctx, x + 20, g - 150, w - 40, 30, 4)  # toldo de la taberna
        fill_stroke(ctx, ["#E8392F", "#2B6BE8", "#22B573"][i % 3], OUT * 0.6)
    fire = p.get("fire", 0.0)
    if fire > 0:
        for i in range(7):
            ph = (t * 0.3 + i / 7) % 1
            blob(ctx, 420 + 60 * math.sin(i) + ph * 120, g - 700 - ph * 600, 90 + ph * 200, n=8, seed=i, t=t)
            ctx.set_source_rgba(0.3, 0.28, 0.3, 0.7 * fire * (1 - ph * 0.6))
            ctx.fill()
        for i in range(5):
            x = 380 + i * 40
            h = (90 + 40 * math.sin(t * 9 + i)) * fire
            ctx.move_to(x - 30, g - 770)
            ctx.curve_to(x - 20, g - 770 - h, x + 10, g - 770 - h * 1.3, x, g - 770 - h * 1.5)
            ctx.curve_to(x + 20, g - 770 - h, x + 30, g - 770 - h * 0.6, x + 30, g - 770)
            ctx.close_path()
            fill_stroke(ctx, (1, 0.55 + 0.1 * math.sin(t * 7 + i), 0.15), OUT * 0.5)
    # adoquines
    ctx.rectangle(-M, g, W + 2 * M, H + M - g)
    fill_stroke(ctx, "#A89C8A", OUT)
    rng = np.random.default_rng(2)
    for r in range(8):
        for c in range(-6, 20):
            x = c * 90 + (45 if r % 2 else 0) + rng.uniform(-6, 6)
            rrect(ctx, x, g + 15 + r * 70, 80, 58, 14)
            fill_stroke(ctx, "#BDB2A0", OUT * 0.35)


def bg_london(ctx, t, p):
    """Londres industrial (1850): fábricas, chimeneas humeantes, casas de ladrillo, farola de gas, barro.
    `smog` 0..1 cubre de neblina amarillenta."""
    g = p.get("ground", 1350)
    smog = p.get("smog", 0.5)
    _sky(ctx, mix("#9DB4C8", "#8C8466", smog), mix("#D9DEE0", "#B8AD82", smog))
    # fábricas al fondo
    for x, w, h in ((-200, 380, 360), (250, 300, 300), (620, 420, 400), (1080, 300, 330)):
        rrect(ctx, x, g - 330 - h, w, h, 2)
        fill_stroke(ctx, "#6E5F5A", OUT * 0.7)
        for k in range(int(w // 70)):
            rrect(ctx, x + 20 + k * 70, g - 330 - h + 40, 36, 50, 4)
            fill_stroke(ctx, (1, 0.85, 0.45), OUT * 0.4)
        cxh = x + w * 0.7
        rrect(ctx, cxh - 25, g - 330 - h - 260, 50, 260, 4)
        fill_stroke(ctx, "#7A4A3A", OUT * 0.7)
        for i in range(5):
            ph = (t * 0.25 + i / 5 + x * 0.001) % 1
            blob(ctx, cxh + 40 * ph + 60 * ph * ph, g - 330 - h - 280 - ph * 380, 40 + ph * 110, n=8, seed=i + int(x), t=t)
            ctx.set_source_rgba(0.25, 0.23, 0.22, 0.75 * (1 - ph))
            ctx.fill()
    # casas de ladrillo
    for i, x in enumerate(range(-300, W + 400, 260)):
        h = 430 + (i % 3) * 50
        rrect(ctx, x, g - h, 250, h, 2)
        fill_stroke(ctx, ["#9A4A35", "#8A4232", "#A65A40"][i % 3], OUT * 0.8)
        for f in range(3):
            for c in range(2):
                rrect(ctx, x + 40 + c * 110, g - h + 40 + f * 130, 60, 80, 4)
                fill_stroke(ctx, "#2A2A35", OUT * 0.5)
        rrect(ctx, x + 95, g - 130, 60, 130, 4)
        fill_stroke(ctx, "#3A2A20", OUT * 0.5)
    # farola de gas
    if p.get("lamp", True):
        lx = p.get("lamp_x", 860)
        limb(ctx, [(lx, g + 10), (lx, g - 330)], 16, "#2A2A30", out=OUT * 0.6)
        rrect(ctx, lx - 34, g - 400, 68, 74, 8)
        fill_stroke(ctx, (1, 0.9, 0.55), OUT * 0.6)
        circle(ctx, lx, g - 363, 110)
        ctx.set_source(radial_grad(ctx, lx, g - 363, 10, 110, [(0, (1, 0.9, 0.5), 0.45), (1, (1, 0.9, 0.5), 0)]))
        ctx.fill()
    # calle de barro
    ctx.rectangle(-M, g, W + 2 * M, H + M - g)
    fill_stroke(ctx, "#5C4E3E", OUT)
    rng = np.random.default_rng(6)
    for i in range(18):
        ellipse(ctx, rng.uniform(-M, W + M), rng.uniform(g + 40, H), rng.uniform(40, 110), rng.uniform(8, 18))
        ctx.set_source_rgba(0.28, 0.24, 0.18, 0.7)
        ctx.fill()
    if smog > 0:
        ctx.rectangle(-M, -M, W + 2 * M, H + 2 * M)
        ctx.set_source_rgba(0.62, 0.58, 0.38, 0.35 * smog + 0.05 * math.sin(t))
        ctx.fill()


def bg_ship_deck(ctx, t, p):
    """Cubierta de un barco de vela del siglo XVIII: mástil, jarcias, barandilla y mar balanceándose."""
    g = p.get("ground", 1350)
    roll = 0.03 * math.sin(t * 0.9)
    night = p.get("night", False)
    _sky(ctx, "#0E1630" if night else "#7EC3F0", "#2A3A66" if night else "#D6EEFF")
    with saved(ctx):
        ctx.translate(W / 2, g)
        ctx.rotate(roll)
        ctx.translate(-W / 2, -g)
        # mar al fondo
        ctx.rectangle(-M, g - 420, W + 2 * M, 300)
        ctx.set_source_rgb(*col("#1D3F7A" if night else "#2F78C4"))
        ctx.fill()
        for k in range(5):
            y = g - 400 + k * 50
            ctx.move_to(-M, y)
            for x in range(-M, W + M + 1, 40):
                ctx.line_to(x, y + 6 * math.sin(x * 0.02 + t * 2 + k))
            ctx.set_source_rgba(1, 1, 1, 0.25)
            ctx.set_line_width(3)
            ctx.stroke()
        # mástil, vela y jarcias
        mx = p.get("mast_x", 760)
        limb(ctx, [(mx, g - 140), (mx, -M)], 46, "#7A4A2A", out=OUT)
        ctx.move_to(mx - 20, 120)
        ctx.curve_to(mx - 420, 200 + 30 * math.sin(t), mx - 440, 600, mx - 20, 700)
        ctx.close_path()
        fill_stroke(ctx, "#F2EAD6", OUT)
        for k in range(6):
            ctx.move_to(mx, 200 + k * 90)
            ctx.line_to(W + M, g - 140)
        ctx.set_source_rgba(*INK, 0.6)
        ctx.set_line_width(4)
        ctx.stroke()
        # barandilla
        rrect(ctx, -M, g - 150, W + 2 * M, 30, 6)
        fill_stroke(ctx, "#6A3E22", OUT)
        for x in range(-M, W + M, 90):
            rrect(ctx, x, g - 120, 22, 120, 4)
            fill_stroke(ctx, "#7E4C2A", OUT * 0.6)
        # tablones de cubierta
        ctx.rectangle(-M, g, W + 2 * M, H + M - g)
        fill_stroke(ctx, "#A8703E", OUT)
        for k in range(12):
            y = g + 30 + k * 55
            ctx.move_to(-M, y)
            ctx.line_to(W + M, y)
        ctx.set_source_rgba(*INK, 0.35)
        ctx.set_line_width(4)
        ctx.stroke()
        for x in range(-M, W + M, 230):  # barriles
            pass


def bg_time_tunnel(ctx, t, p):
    """Túnel del tiempo: espiral de colores con números de años pasando."""
    _sky(ctx, "#1B1240", "#3A1E6E")
    cx, cy = W / 2, H / 2
    for i in range(26):
        r = ((i * 70 + t * 520) % 1900)
        ctx.new_path()
        ctx.arc(cx, cy, max(1, r), 0, 2 * math.pi)
        c = ["#5CE1E6", "#9D7BFF", "#FFD23F", "#FF6B9A"][i % 4]
        ctx.set_source_rgba(*col(c), clamp(r / 900) * 0.55)
        ctx.set_line_width(18 + r * 0.03)
        ctx.stroke()
    years = p.get("years", ["2026", "1854", "1720", "1348", "64", "-2560"])
    for i, y in enumerate(years):
        ph = (t * 0.6 + i / len(years)) % 1
        a = i * 2.1 + t * 0.4
        rr = 80 + ph * 900
        with saved(ctx):
            ctx.translate(cx + rr * math.cos(a), cy + rr * math.sin(a))
            s = 0.4 + ph * 1.6
            ctx.scale(s, s)
            text(ctx, y, 0, 0, 60, color="white", outline=6, shadow_off=0)
    circle(ctx, cx, cy, 120)
    ctx.set_source(radial_grad(ctx, cx, cy, 0, 120, [(0, (1, 1, 1), 1), (1, (1, 1, 1), 0)]))
    ctx.fill()


def bg_fjord(ctx, t, p):
    """Fiordo nórdico: montañas, agua quieta y casas largas con tejado de hierba."""
    g = p.get("ground", 1350)
    _sky(ctx, "#8FB8D8", "#E2EEF4")
    _cloud(ctx, (150 + t * 10) % 1400 - 250, 300, 0.9)
    for x0, h, c in ((-400, 620, "#5E7488"), (250, 760, "#6E8498"), (800, 640, "#5A6E82")):
        ctx.move_to(x0 - 300, g - 260)
        ctx.line_to(x0 + 250, g - 260 - h)
        ctx.line_to(x0 + 800, g - 260)
        ctx.close_path()
        fill_stroke(ctx, c, OUT)
        ctx.move_to(x0 + 170, g - 260 - h + 90)
        ctx.line_to(x0 + 250, g - 260 - h)
        ctx.line_to(x0 + 330, g - 260 - h + 90)
        ctx.close_path()
        fill_stroke(ctx, (0.95, 0.97, 1), OUT * 0.6)
    ctx.rectangle(-M, g - 270, W + 2 * M, 120)
    ctx.set_source_rgb(*col("#3F6E96"))
    ctx.fill()
    for k in range(3):
        y = g - 250 + k * 35
        ctx.move_to(-M, y)
        ctx.line_to(W + M, y + 4 * math.sin(t + k))
    ctx.set_source_rgba(1, 1, 1, 0.3)
    ctx.set_line_width(3)
    ctx.stroke()
    ctx.move_to(-M, g - 150)
    for x in range(-M, W + M + 1, 60):
        ctx.line_to(x, g - 150 + 14 * math.sin(x * 0.01))
    ctx.line_to(W + M, H + M)
    ctx.line_to(-M, H + M)
    ctx.close_path()
    fill_stroke(ctx, "#6E9A4A", OUT)
    for x, w in ((-180, 420), (420, 380), (900, 400)):  # casas largas
        y = g - 150
        ctx.move_to(x, y)
        ctx.curve_to(x + 40, y - 150, x + w - 40, y - 150, x + w, y)
        ctx.close_path()
        fill_stroke(ctx, "#5E8A3A", OUT)
        rrect(ctx, x + 20, y - 70, w - 40, 70, 6)
        fill_stroke(ctx, "#8A5A30", OUT * 0.8)
        rrect(ctx, x + w / 2 - 25, y - 60, 50, 60, 6)
        fill_stroke(ctx, "#3A2418", OUT * 0.6)
        if p.get("smoke", True):
            for i in range(3):
                ph = (t * 0.3 + i / 3) % 1
                blob(ctx, x + w / 2 + 30 * ph, y - 150 - ph * 220, 20 + 40 * ph, n=7, seed=i + int(x))
                ctx.set_source_rgba(0.85, 0.85, 0.88, 0.6 * (1 - ph))
                ctx.fill()


def bg_tenochtitlan(ctx, t, p):
    """Tenochtitlan (1519): ciudad sobre el lago de Texcoco, Templo Mayor doble, calzada, canoas y volcanes."""
    g = p.get("ground", 1350)
    _sky(ctx, (0.42, 0.7, 0.96), (0.86, 0.93, 1))
    for x0, h in ((-200, 520), (900, 600)):  # volcanes al fondo
        ctx.move_to(x0 - 380, g - 330)
        ctx.line_to(x0 - 60, g - 330 - h)
        ctx.line_to(x0 + 60, g - 330 - h)
        ctx.line_to(x0 + 380, g - 330)
        ctx.close_path()
        fill_stroke(ctx, "#8A9AB4", OUT * 0.8)
        ctx.move_to(x0 - 120, g - 330 - h + 120)
        ctx.line_to(x0 - 60, g - 330 - h)
        ctx.line_to(x0 + 60, g - 330 - h)
        ctx.line_to(x0 + 120, g - 330 - h + 120)
        ctx.close_path()
        fill_stroke(ctx, (0.96, 0.97, 1), OUT * 0.5)
    # lago
    ctx.rectangle(-M, g - 340, W + 2 * M, H + M)
    ctx.set_source(linear_grad(ctx, 0, g - 340, 0, H, [(0, "#4FA6C8"), (1, "#2C7CA8")]))
    ctx.fill()
    # Templo Mayor (pirámide escalonada con dos templos)
    cx, base = p.get("cx", 540), g - 230
    for k in range(5):
        w, h = 560 - k * 90, 70
        rrect(ctx, cx - w / 2, base - (k + 1) * h, w, h, 4)
        fill_stroke(ctx, "#E8DCC4", OUT * 0.8)
    rrect(ctx, cx - 40, base - 350, 80, 350, 2)
    fill_stroke(ctx, "#D8CBB0", OUT * 0.6)
    for s_, c in ((-1, "#2B6BE8"), (1, "#E8392F")):
        x = cx + s_ * 85
        rrect(ctx, x - 55, base - 450, 110, 100, 4)
        fill_stroke(ctx, "#F2ECE0", OUT * 0.7)
        ctx.move_to(x - 65, base - 450)
        ctx.line_to(x, base - 520)
        ctx.line_to(x + 65, base - 450)
        ctx.close_path()
        fill_stroke(ctx, c, OUT * 0.7)
    # casas blancas y chinampas
    for i, x in enumerate(range(-420, W + 420, 170)):
        if abs(x + 60 - cx) < 330:
            continue
        rrect(ctx, x, g - 330, 130, 100, 4)
        fill_stroke(ctx, "#F4EEE2", OUT * 0.7)
        rrect(ctx, x + 45, g - 290, 40, 60, 4)
        fill_stroke(ctx, "#7A5A3A", OUT * 0.5)
    for i, x in enumerate(range(-400, W + 400, 260)):
        rrect(ctx, x, g - 200 + (i % 2) * 40, 210, 40, 10)
        fill_stroke(ctx, "#6EA84A", OUT * 0.6)
    # calzada
    ctx.move_to(-M, g + 40)
    ctx.line_to(W + M, g - 60)
    ctx.line_to(W + M, g + 30)
    ctx.line_to(-M, g + 130)
    ctx.close_path()
    fill_stroke(ctx, "#CDBB98", OUT)
    # canoas
    for i in range(3):
        x = (i * 420 + t * 40) % (W + 600) - 300
        y = g + 260 + i * 90
        ctx.move_to(x - 120, y)
        ctx.curve_to(x - 80, y + 40, x + 80, y + 40, x + 120, y)
        ctx.close_path()
        fill_stroke(ctx, "#8A5A30", OUT * 0.7)


def bg_jungle_canal(ctx, t, p):
    """Obra del canal de Panamá (h. 1885): selva, zanja embarrada, vía de tren de obra y lluvia (`rain` 0..1)."""
    g = p.get("ground", 1350)
    rain = p.get("rain", 0.4)
    _sky(ctx, mix("#8EC6E8", "#6E7E8A", rain), mix("#D8EEF8", "#A8B4B8", rain))
    rng = np.random.default_rng(11)
    for i in range(16):  # selva de fondo
        x = -M + i * 140 + rng.uniform(-30, 30)
        blob(ctx, x, g - 520 + rng.uniform(-60, 60), rng.uniform(120, 190), n=9, wobble=0.25, seed=i)
        fill_stroke(ctx, ["#2E7A3A", "#3E8E44", "#256A32"][i % 3], OUT * 0.8)
    # ladera excavada (escalones de la zanja)
    for k, (y, c) in enumerate(((g - 380, "#B06A3A"), (g - 290, "#9A5A30"), (g - 200, "#8A4E2A"))):
        ctx.move_to(-M, y)
        for x in range(-M, W + M + 1, 60):
            ctx.line_to(x, y + 10 * math.sin(x * 0.01 + k))
        ctx.line_to(W + M, H + M)
        ctx.line_to(-M, H + M)
        ctx.close_path()
        fill_stroke(ctx, c, OUT * 0.8)
    # vía de tren de obra
    ctx.move_to(-M, g - 110)
    ctx.line_to(W + M, g - 110)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(10)
    ctx.stroke()
    for x in range(-M, W + M, 70):
        rrect(ctx, x, g - 118, 40, 16, 3)
        ctx.set_source_rgb(*col("#5A3A20"))
        ctx.fill()
    # charcos (criaderos de mosquitos)
    ctx.rectangle(-M, g - 40, W + 2 * M, H + M)
    fill_stroke(ctx, "#7A4A2A", OUT)
    for i in range(6):
        ellipse(ctx, rng.uniform(-200, W + 200), rng.uniform(g + 30, g + 400), rng.uniform(70, 150), rng.uniform(14, 26))
        fill_stroke(ctx, "#6A8A9A", OUT * 0.5)
    if rain > 0:
        for i in range(int(160 * rain)):
            ph = (t * rng.uniform(1.2, 1.8) + rng.random()) % 1
            x = rng.uniform(-M, W + M) - ph * 60
            y = -M + ph * (H + 2 * M)
            ctx.move_to(x, y)
            ctx.line_to(x - 12, y + 40)
            ctx.set_source_rgba(0.85, 0.92, 1, 0.55)
            ctx.set_line_width(3)
            ctx.stroke()


# ============================================================================ PROPS
def _mosquito(ctx, p, t):
    """Mosquito revoloteando (`swarm` dibuja varios)."""
    n = int(p.get("swarm", 1))
    rng = np.random.default_rng(5)
    for i in range(n):
        ox = 0 if n == 1 else rng.uniform(-260, 260)
        oy = 0 if n == 1 else rng.uniform(-160, 160)
        x = ox + 30 * math.sin(t * 3 + i * 1.7)
        y = oy + 20 * math.sin(t * 4.3 + i)
        sc = 1.0 if n == 1 else 0.45
        with saved(ctx):
            ctx.translate(x, y)
            ctx.scale(sc, sc)
            flap = 0.4 + 0.6 * abs(math.sin(t * 40 + i))
            for s_ in (-1, 1):
                ellipse(ctx, s_ * 40, -40, 45 * flap, 22)
                ctx.set_source_rgba(0.85, 0.95, 1, 0.7)
                ctx.fill_preserve()
                ctx.set_source_rgb(*INK)
                ctx.set_line_width(4)
                ctx.stroke()
            ellipse(ctx, 0, 0, 22, 55)
            fill_stroke(ctx, "#3A3A44", OUT * 0.6)
            circle(ctx, 0, -60, 18)
            fill_stroke(ctx, "#3A3A44", OUT * 0.6)
            limb(ctx, [(0, -70), (0, -120)], 5, "#3A3A44", out=0)
            for k in (-1, 0, 1):
                for s_ in (-1, 1):
                    ctx.move_to(s_ * 15, 10 * k)
                    ctx.line_to(s_ * 60, 40 + 12 * k)
            ctx.set_source_rgb(*INK)
            ctx.set_line_width(4)
            ctx.stroke()


def _mosquito_net(ctx, p, t):
    """Mosquitero sobre una cama."""
    rrect(ctx, -220, 40, 440, 60, 10)
    fill_stroke(ctx, "#F2EAD6", OUT)
    ctx.move_to(-230, 100)
    ctx.curve_to(-200, -150, -60, -280, 0, -300)
    ctx.curve_to(60, -280, 200, -150, 230, 100)
    ctx.close_path()
    ctx.set_source_rgba(1, 1, 1, 0.35)
    ctx.fill_preserve()
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(OUT * 0.6)
    ctx.stroke()
    for k in range(-4, 5):
        ctx.move_to(k * 45, 100)
        ctx.line_to(0, -300)
    ctx.set_source_rgba(*INK, 0.15)
    ctx.set_line_width(2)
    ctx.stroke()


def _longship(ctx, p, t):
    """Barco vikingo (drakkar) con vela a rayas, escudos y proa de dragón."""
    roll = 0.04 * math.sin(t * 1.3)
    with saved(ctx):
        ctx.rotate(roll)
        ctx.move_to(-380, -60)
        ctx.curve_to(-300, 60, 300, 60, 380, -60)
        ctx.line_to(330, -30)
        ctx.curve_to(200, 0, -200, 0, -330, -30)
        ctx.close_path()
        fill_stroke(ctx, "#7A4A2A", OUT)
        for s_ in (-1, 1):  # proa y popa
            ctx.move_to(s_ * 370, -60)
            ctx.curve_to(s_ * 420, -140, s_ * 380, -200, s_ * 330, -190)
            ctx.set_source_rgb(*INK)
            ctx.set_line_width(26)
            ctx.stroke_preserve()
            ctx.set_source_rgb(*col("#7A4A2A"))
            ctx.set_line_width(14)
            ctx.stroke()
        circle(ctx, 335, -192, 18)
        fill_stroke(ctx, "#E8392F", OUT * 0.6)
        for i in range(8):
            circle(ctx, -260 + i * 74, -20, 26)
            fill_stroke(ctx, ["#E8392F", "#FFD23F"][i % 2], OUT * 0.6)
        limb(ctx, [(0, -20), (0, -420)], 16, "#5A3A20", out=OUT * 0.6)
        rrect(ctx, -190, -400, 380, 260, 8)
        fill_stroke(ctx, "#F2EAD6", OUT * 0.8)
        for k in range(4):
            ctx.rectangle(-190 + k * 95, -400, 48, 260)
        ctx.set_source_rgba(0.85, 0.2, 0.2, 0.85)
        ctx.fill()


def _horned_helmet(ctx, p, t):
    """Casco con cuernos (el del mito)."""
    for s_ in (-1, 1):
        ctx.move_to(s_ * 110, -40)
        ctx.curve_to(s_ * 200, -60, s_ * 230, -160, s_ * 200, -230)
        ctx.curve_to(s_ * 170, -150, s_ * 140, -110, s_ * 90, -90)
        ctx.close_path()
        fill_stroke(ctx, "#F2EAD6", OUT)
    ctx.new_path()
    ctx.arc(0, 0, 130, math.pi, 2 * math.pi)
    ctx.close_path()
    fill_stroke(ctx, PAL["metal"], OUT)
    rrect(ctx, -140, -10, 280, 34, 10)
    fill_stroke(ctx, PAL["metal_dk"], OUT * 0.8)


def _comb(ctx, p, t):
    """Peine vikingo de hueso o asta."""
    rrect(ctx, -200, -70, 400, 70, 20)
    fill_stroke(ctx, "#E8DCC0", OUT)
    for i in range(6):
        circle(ctx, -150 + i * 60, -35, 8)
        ctx.set_source_rgba(*INK, 0.5)
        ctx.fill()
    for i in range(26):
        x = -190 + i * 15
        rrect(ctx, x, 0, 9, 90, 3)
        fill_stroke(ctx, "#E8DCC0", OUT * 0.35)


def _cacao(ctx, p, t):
    """Puñado de granos de cacao (se usaban como moneda)."""
    rng = np.random.default_rng(2)
    for i in range(9):
        x, y = rng.uniform(-120, 120), rng.uniform(-60, 60)
        with saved(ctx):
            ctx.translate(x, y)
            ctx.rotate(rng.uniform(0, math.pi))
            ellipse(ctx, 0, 0, 38, 24)
            fill_stroke(ctx, "#6A3A20", OUT * 0.6)
            ctx.move_to(-28, 0)
            ctx.line_to(28, 0)
            ctx.set_source_rgba(1, 1, 1, 0.25)
            ctx.set_line_width(4)
            ctx.stroke()



def _stone_block(ctx, p, t):
    """Bloque de piedra sobre un trineo de madera, con cuerda (`pull` desplaza la cuerda)."""
    rrect(ctx, -170, -150, 340, 150, 8)
    fill_stroke(ctx, "#D9C08A", OUT)
    ctx.move_to(-120, -110)
    ctx.line_to(-40, -60)
    ctx.set_source_rgba(*INK, 0.3)
    ctx.set_line_width(5)
    ctx.stroke()
    rrect(ctx, -200, 0, 400, 30, 12)
    fill_stroke(ctx, "#8A5A30", OUT * 0.8)
    for s in (-1, 1):
        ctx.move_to(s * 200, 15)
        ctx.curve_to(s * 230, 15, s * 240, -10, s * 225, -30)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(OUT)
        ctx.stroke()
    ctx.move_to(200, -20)
    ctx.curve_to(320, -40, 420, -10 + 8 * math.sin(t * 3), 520, -30)
    ctx.set_source_rgb(*col("#C9A060"))
    ctx.set_line_width(12)
    ctx.stroke()


def _amphora(ctx, p, t):
    """Ánfora o jarra de cerámica (`label` opcional, p. ej. «CERVEZA»)."""
    c = col(p.get("color", "#C8693F"))
    ctx.new_path()
    ctx.move_to(-40, -170)
    ctx.line_to(40, -170)
    ctx.curve_to(40, -140, 110, -120, 110, -20)
    ctx.curve_to(110, 80, 40, 140, 0, 170)
    ctx.curve_to(-40, 140, -110, 80, -110, -20)
    ctx.curve_to(-110, -120, -40, -140, -40, -170)
    ctx.close_path()
    fill_stroke(ctx, c, OUT)
    for s in (-1, 1):
        ctx.move_to(s * 40, -150)
        ctx.curve_to(s * 110, -160, s * 120, -110, s * 80, -80)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(OUT * 1.6)
        ctx.stroke_preserve()
        ctx.set_source_rgb(*c)
        ctx.set_line_width(OUT * 0.8)
        ctx.stroke()
    ctx.move_to(-100, -30)
    ctx.line_to(100, -30)
    ctx.set_source_rgba(*INK, 0.4)
    ctx.set_line_width(5)
    ctx.stroke()
    if p.get("label"):
        text(ctx, p["label"], 0, 20, 34, color="white", outline=5, shadow_off=0, max_w=200)


def _coin(ctx, p, t):
    """Moneda (pieza de a ocho) que gira; `text` en la cara."""
    sx = abs(math.cos(t * p.get("spin", 2.5))) if p.get("spinning", True) else 1
    with saved(ctx):
        ctx.scale(max(0.08, sx), 1)
        circle(ctx, 0, 0, 90)
        fill_stroke(ctx, "#E6B830", OUT)
        circle(ctx, 0, 0, 68)
        ctx.set_source_rgba(*INK, 0.3)
        ctx.set_line_width(5)
        ctx.stroke()
        if sx > 0.4:
            text(ctx, p.get("text", "8"), 0, 4, 70, color="#8A6410", outline=0, shadow_off=0)


def _lemon(ctx, p, t):
    ellipse(ctx, 0, 0, 95, 70)
    fill_stroke(ctx, "#FFE13A", OUT)
    for s in (-1, 1):
        ellipse(ctx, s * 95, 0, 14, 10)
        fill_stroke(ctx, "#FFE13A", OUT * 0.6)
    ellipse(ctx, -30, -25, 30, 12)
    ctx.set_source_rgba(1, 1, 1, 0.6)
    ctx.fill()
    ctx.move_to(10, -70)
    ctx.curve_to(40, -110, 90, -100, 100, -80)
    ctx.curve_to(70, -70, 40, -70, 10, -70)
    fill_stroke(ctx, "#4E9A3A", OUT * 0.6)


def _meat(ctx, p, t):
    """Muslo de carne asada."""
    with saved(ctx):
        ctx.rotate(-0.5)
        limb(ctx, [(60, 0), (150, 0)], 34, "#F2EAD6", out=OUT * 0.8)
        for s in (-1, 1):
            circle(ctx, 160, s * 18, 22)
            fill_stroke(ctx, "#F2EAD6", OUT * 0.8)
        ellipse(ctx, -20, 0, 110, 80)
        fill_stroke(ctx, "#B5532F", OUT)
        ellipse(ctx, -45, -25, 40, 18)
        ctx.set_source_rgba(1, 0.8, 0.6, 0.5)
        ctx.fill()


def _orange(ctx, p, t):
    circle(ctx, 0, 0, 90)
    fill_stroke(ctx, "#FF9A1F", OUT)
    rng = np.random.default_rng(3)
    for i in range(14):
        circle(ctx, rng.uniform(-60, 60), rng.uniform(-60, 60), 4)
        ctx.set_source_rgba(0.85, 0.45, 0.05, 0.6)
        ctx.fill()
    ellipse(ctx, -30, -35, 26, 12)
    ctx.set_source_rgba(1, 1, 1, 0.55)
    ctx.fill()
    ctx.move_to(0, -88)
    ctx.curve_to(20, -130, 70, -120, 80, -100)
    ctx.curve_to(50, -90, 30, -90, 0, -88)
    fill_stroke(ctx, "#4E9A3A", OUT * 0.6)


def _sailing_ship(ctx, p, t):
    """Velero de época (bandera opcional `flag`: pirate | none)."""
    roll = 0.05 * math.sin(t * 1.2)
    with saved(ctx):
        ctx.rotate(roll)
        ctx.move_to(-330, -20)
        ctx.line_to(330, -20)
        ctx.curve_to(300, 60, 220, 110, 0, 110)
        ctx.line_to(-240, 110)
        ctx.curve_to(-300, 80, -340, 40, -330, -20)
        ctx.close_path()
        fill_stroke(ctx, "#6A3E22", OUT)
        rrect(ctx, -310, 10, 620, 16, 4)
        ctx.set_source_rgb(*col("#E6B830"))
        ctx.fill()
        for x, h in ((-120, 380), (110, 440)):
            limb(ctx, [(x, -20), (x, -20 - h)], 18, "#5A3A20", out=OUT * 0.6)
            for k, (w, y) in enumerate(((210, -h + 40), (250, -h * 0.55))):
                ctx.move_to(x - w / 2, y - 20)
                ctx.curve_to(x - w / 2 + 20, y + 90, x + w / 2 - 20, y + 90, x + w / 2, y - 20)
                ctx.close_path()
                fill_stroke(ctx, "#F2EAD6", OUT * 0.8)
        if p.get("flag", "pirate") == "pirate":
            rrect(ctx, 110, -500, 110, 70, 4)
            fill_stroke(ctx, "#1A1A22", OUT * 0.6)
            circle(ctx, 165, -470, 16)
            ctx.set_source_rgb(1, 1, 1)
            ctx.fill()
            for s in (-1, 1):
                ctx.move_to(140, -450 + s * 10)
                ctx.line_to(190, -450 - s * 10)
            ctx.set_source_rgb(1, 1, 1)
            ctx.set_line_width(6)
            ctx.stroke()


def _water_pump(ctx, p, t):
    """Bomba de agua de calle; `handle` False la muestra sin manivela (la retiró John Snow)."""
    rrect(ctx, -55, -330, 110, 330, 14)
    fill_stroke(ctx, "#3A4A5A", OUT)
    ellipse(ctx, 0, -340, 70, 26)
    fill_stroke(ctx, "#4A5A6A", OUT)
    limb(ctx, [(50, -230), (130, -230), (150, -200)], 20, "#3A4A5A", out=OUT * 0.8)
    if p.get("handle", True):
        a = -0.4 + 0.25 * math.sin(t * 3) if p.get("pumping") else -0.4
        with saved(ctx):
            ctx.translate(-50, -290)
            ctx.rotate(a)
            limb(ctx, [(0, 0), (-210, 0)], 18, "#2A3A4A", out=OUT * 0.8)
    rrect(ctx, -90, -10, 180, 30, 8)
    fill_stroke(ctx, "#5A6A7A", OUT * 0.8)


def _survival_meter(ctx, p, t):
    """Medidor «¿cuánto durarías?»: barra de HORAS a TODA LA VIDA con aguja en `value` (0..1) y etiqueta."""
    v = clamp(p.get("value", 0.5)) * clamp(p.get("_age", 1) / 0.9) if p.get("animate", True) else clamp(p.get("value", 0.5))
    w = 700
    rrect(ctx, -w / 2 - 90, -175, w + 180, 290, 30)
    fill_stroke(ctx, (1, 1, 1), OUT)
    for i in range(40):
        x0 = -w / 2 + i * w / 40
        ctx.rectangle(x0, -55, w / 40 + 1, 55)
        ctx.set_source_rgb(*mix(PAL["red"], PAL["green"], i / 39))
        ctx.fill()
    rrect(ctx, -w / 2, -55, w, 55, 8)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(OUT * 0.8)
    ctx.stroke()
    for k, lab in enumerate(p.get("ticks", ["HORAS", "DÍAS", "MESES", "AÑOS", "TODA\nLA VIDA"])):
        x = -w / 2 + k * w / 4
        for j, ln in enumerate(lab.split("\n")):
            text(ctx, ln, x, 30 + j * 28, 28, color=INK, outline=0, shadow_off=0)
    x = -w / 2 + v * w
    ctx.move_to(x, -60)
    ctx.line_to(x - 26, -108)
    ctx.line_to(x + 26, -108)
    ctx.close_path()
    fill_stroke(ctx, PAL["yellow"], OUT * 0.8)
    if p.get("label"):
        text(ctx, p["label"], 0, -140, 42, color=INK, outline=0, shadow_off=0, max_w=w + 140)


BACKGROUNDS.update({"egypt": bg_egypt, "rome": bg_rome, "london": bg_london, "ship_deck": bg_ship_deck,
                    "time_tunnel": bg_time_tunnel, "fjord": bg_fjord, "tenochtitlan": bg_tenochtitlan,
                    "jungle_canal": bg_jungle_canal})
PROPS.update({"stone_block": _stone_block, "amphora": _amphora, "coin": _coin, "lemon": _lemon, "meat": _meat, "orange": _orange, "longship": _longship, "horned_helmet": _horned_helmet,
              "comb": _comb, "cacao": _cacao, "mosquito": _mosquito, "mosquito_net": _mosquito_net,
              "sailing_ship": _sailing_ship, "water_pump": _water_pump, "survival_meter": _survival_meter})
