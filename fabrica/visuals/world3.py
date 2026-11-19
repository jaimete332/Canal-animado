"""Catálogo «historia y crimen»: ciudad de los años 20, despacho, cárcel, tribunal, campo siciliano,
personajes secundarios (NPC), dinero, máquina de escribir, notas, esposas, coche de policía...
"""
from __future__ import annotations

import math

import cairo
import numpy as np

from .draw import (INK, OUT, PAL, blob, circle, clamp, col, darken, ellipse, fill_stroke, lerp, lighten,
                   limb, linear_grad, mix, noise1, radial_grad, rrect, saved, star, text)
from .world import BACKGROUNDS, H, M, PROPS, W, _sky


# ============================================================================
# FONDOS
# ============================================================================
def bg_city_night(ctx, t, p):
    """Calle de Chicago años 20 de noche: edificios de ladrillo, ventanas, farolas, lluvia opcional."""
    _sky(ctx, (0.08, 0.07, 0.2), (0.25, 0.18, 0.38))
    circle(ctx, 860, 300, 80)
    fill_stroke(ctx, (1, 0.97, 0.85), OUT)
    rng = np.random.default_rng(31)
    # skyline lejano
    x = -M
    while x < W + M:
        w, h = rng.uniform(90, 180), rng.uniform(380, 820)
        ctx.rectangle(x, 1250 - h, w, h + 800)
        ctx.set_source_rgb(0.16, 0.13, 0.28)
        ctx.fill()
        for wy in range(int(1250 - h + 30), 1240, 60):
            for wx in range(int(x + 15), int(x + w - 20), 38):
                if rng.random() < 0.35:
                    ctx.rectangle(wx, wy, 16, 24)
                    ctx.set_source_rgba(1, 0.85, 0.45, 0.8)
                    ctx.fill()
        x += w + 8
    # edificios cercanos de ladrillo
    for bx, bw, bh, c in ((-120, 420, 1150, "#7A3B2E"), (760, 460, 1250, "#5E3A4A")):
        rrect(ctx, bx, 1480 - bh, bw, bh + 600, 6)
        fill_stroke(ctx, c, OUT)
        for k in range(int(bh / 70)):  # hiladas
            ctx.move_to(bx, 1480 - bh + k * 70)
            ctx.line_to(bx + bw, 1480 - bh + k * 70)
        ctx.set_source_rgba(0, 0, 0, 0.18)
        ctx.set_line_width(3)
        ctx.stroke()
        for wy in range(int(1480 - bh + 80), 1300, 210):
            for wx in range(int(bx + 50), int(bx + bw - 90), 150):
                on = noise1(wx * 0.1 + wy + t * 0.3, 2) > -0.2
                rrect(ctx, wx, wy, 90, 130, 8)
                fill_stroke(ctx, (1, 0.82, 0.4) if on else (0.15, 0.15, 0.25), OUT * 0.7)
    # rótulo luminoso
    if p.get("sign", True):
        with saved(ctx):
            ctx.translate(980, 760)
            rrect(ctx, -100, -40, 200, 80, 14)
            fill_stroke(ctx, (0.15, 0.1, 0.2), OUT * 0.8)
            on = (t * 1.5) % 1 < 0.8
            text(ctx, p.get("sign_text", "BAR"), 0, 0, 52, color=(1, 0.3, 0.5) if on else (0.4, 0.2, 0.3),
                 outline=0, shadow_off=0)
    # acera y calle
    ctx.rectangle(-M, 1480, W + 2 * M, H)
    ctx.set_source_rgb(0.25, 0.24, 0.3)
    ctx.fill()
    ctx.rectangle(-M, 1480, W + 2 * M, 40)
    fill_stroke(ctx, (0.45, 0.43, 0.5), OUT)
    # farolas
    for fx in (380, 700):
        limb(ctx, [(fx, 1480), (fx, 980)], 18, (0.15, 0.15, 0.2), out=OUT * 0.6)
        circle(ctx, fx, 960, 150)
        ctx.set_source(radial_grad(ctx, fx, 960, 10, 150, [(0, (1, 0.9, 0.5), 0.5), (1, (1, 0.9, 0.5), 0)]))
        ctx.fill()
        rrect(ctx, fx - 32, 930, 64, 60, 10)
        fill_stroke(ctx, (1, 0.9, 0.55), OUT * 0.7)
    if p.get("rain"):
        for i in range(160):
            x0 = rng.uniform(-200, W + 200)
            y0 = (rng.uniform(0, H) + t * 1600) % (H + 200) - 100
            ctx.move_to(x0, y0)
            ctx.line_to(x0 - 10, y0 + 40)
            ctx.set_source_rgba(0.7, 0.8, 1, 0.45)
            ctx.set_line_width(3)
            ctx.stroke()


def bg_office(ctx, t, p):
    """Despacho del jefe: paneles de madera, ventana con la ciudad, escritorio en primer plano."""
    ctx.rectangle(-M, -M, W + 2 * M, H + 2 * M)
    ctx.set_source(linear_grad(ctx, 0, 0, 0, H, [(0, "#5A3522"), (1, "#3A2216")]))
    ctx.fill()
    for k in range(-3, 10):
        ctx.move_to(k * 160, -M)
        ctx.line_to(k * 160, 1300)
    ctx.set_source_rgba(0, 0, 0, 0.25)
    ctx.set_line_width(6)
    ctx.stroke()
    # ventana con persiana
    rrect(ctx, 300, 260, 480, 560, 10)
    fill_stroke(ctx, (0.12, 0.1, 0.25), OUT)
    with saved(ctx):
        rrect(ctx, 300, 260, 480, 560, 10)
        ctx.clip()
        rng = np.random.default_rng(4)
        for i in range(9):
            bx = 300 + i * 55
            bh = rng.uniform(150, 380)
            ctx.rectangle(bx, 820 - bh, 48, bh)
            ctx.set_source_rgb(0.2, 0.17, 0.35)
            ctx.fill()
            for wy in range(int(820 - bh + 15), 810, 40):
                if rng.random() < 0.4:
                    ctx.rectangle(bx + 14, wy, 12, 18)
                    ctx.set_source_rgba(1, 0.85, 0.4, 0.9)
                    ctx.fill()
        for k in range(10):  # lamas de la persiana
            ctx.rectangle(300, 270 + k * 56, 480, 14)
        ctx.set_source_rgba(0.85, 0.75, 0.55, 0.55)
        ctx.fill()
    limb(ctx, [(540, 260), (540, 820)], 14, "#4A2C1C", out=OUT * 0.6)
    # cuadro torcido con «?»
    with saved(ctx):
        ctx.translate(900, 420)
        ctx.rotate(0.06)
        rrect(ctx, -90, -110, 180, 220, 6)
        fill_stroke(ctx, "#C9A24A", OUT)
        rrect(ctx, -65, -85, 130, 170, 4)
        fill_stroke(ctx, "#2B4C7E", OUT * 0.6)
        text(ctx, "?", 0, 0, 100, color=PAL["yellow"], outline=5, shadow_off=0)
    # lámpara de pie verde
    circle(ctx, 140, 640, 220)
    ctx.set_source(radial_grad(ctx, 140, 640, 10, 220, [(0, (1, 0.9, 0.6), 0.35), (1, (1, 0.9, 0.6), 0)]))
    ctx.fill()
    ctx.move_to(60, 600)
    ctx.line_to(220, 600)
    ctx.line_to(180, 520)
    ctx.line_to(100, 520)
    ctx.close_path()
    fill_stroke(ctx, (0.2, 0.55, 0.35), OUT)
    limb(ctx, [(140, 600), (140, 1300)], 14, (0.6, 0.5, 0.25), out=OUT * 0.6)
    # suelo de moqueta
    ctx.rectangle(-M, 1300, W + 2 * M, H)
    ctx.set_source_rgb(0.45, 0.12, 0.14)
    ctx.fill()
    if p.get("desk", True):
        dy = p.get("desk_y", 1330)
        rrect(ctx, -60, dy, W + 120, 120, 20)
        fill_stroke(ctx, "#6B3D24", OUT)
        rrect(ctx, 40, dy + 120, W - 80, 700, 10)
        fill_stroke(ctx, "#57311D", OUT)
        for k in range(2):
            rrect(ctx, 120 + k * 560, dy + 190, 280, 150, 10)
            fill_stroke(ctx, "#6B3D24", OUT * 0.7)
            circle(ctx, 260 + k * 560, dy + 265, 14)
            fill_stroke(ctx, PAL["yellow"], 3)


def bg_prison(ctx, t, p):
    ctx.rectangle(-M, -M, W + 2 * M, H + 2 * M)
    ctx.set_source(linear_grad(ctx, 0, 0, 0, H, [(0, "#6E7180"), (1, "#4A4C57")]))
    ctx.fill()
    rng = np.random.default_rng(8)
    for row in range(-2, 30):  # bloques de piedra
        y = row * 90
        off = 90 if row % 2 else 0
        for k in range(-3, 10):
            rrect(ctx, k * 180 + off, y, 176, 86, 10)
            ctx.set_source_rgba(*mix("#7A7D8C", "#5C5F6C", rng.random()), 1)
            ctx.fill()
    # ventanuco con rayo de luz
    rrect(ctx, 400, 300, 280, 200, 10)
    fill_stroke(ctx, (0.55, 0.75, 1), OUT)
    for k in range(1, 5):
        limb(ctx, [(400 + k * 56, 300), (400 + k * 56, 500)], 12, (0.25, 0.25, 0.3), out=OUT * 0.5)
    ctx.move_to(400, 500)
    ctx.line_to(680, 500)
    ctx.line_to(900, 1500)
    ctx.line_to(300, 1500)
    ctx.close_path()
    ctx.set_source_rgba(1, 1, 0.9, 0.12)
    ctx.fill()
    ctx.rectangle(-M, 1450, W + 2 * M, H)
    fill_stroke(ctx, "#3A3C46", OUT)
    # catre
    if p.get("bed", True):
        rrect(ctx, 650, 1300, 380, 60, 12)
        fill_stroke(ctx, (0.85, 0.85, 0.8), OUT)
        limb(ctx, [(680, 1360), (680, 1450)], 14, (0.3, 0.3, 0.35), out=OUT * 0.5)
        limb(ctx, [(1000, 1360), (1000, 1450)], 14, (0.3, 0.3, 0.35), out=OUT * 0.5)
    # marcas de días en la pared
    if p.get("tally", True):
        ctx.set_source_rgba(1, 1, 1, 0.7)
        ctx.set_line_width(6)
        for g in range(5):
            for k in range(4):
                ctx.move_to(90 + g * 80 + k * 14, 760)
                ctx.line_to(90 + g * 80 + k * 14, 840)
            ctx.move_to(84 + g * 80, 820)
            ctx.line_to(144 + g * 80, 770)
        ctx.stroke()
    if p.get("bars", False):
        _bars(ctx, {}, t)


def bg_courtroom(ctx, t, p):
    ctx.rectangle(-M, -M, W + 2 * M, H + 2 * M)
    ctx.set_source(linear_grad(ctx, 0, 0, 0, H, [(0, "#E9DCC0"), (1, "#C9B48C")]))
    ctx.fill()
    for k in range(-2, 9):  # columnas
        rrect(ctx, k * 170 + 20, 120, 70, 1100, 12)
        ctx.set_source_rgba(1, 1, 1, 0.35)
        ctx.fill()
    # escudo / balanza
    with saved(ctx):
        ctx.translate(540, 330)
        circle(ctx, 0, 0, 120)
        fill_stroke(ctx, "#C9A24A", OUT)
        limb(ctx, [(0, -70), (0, 60)], 12, INK, out=0)
        limb(ctx, [(-70, -40), (70, -40)], 10, INK, out=0)
        for sd in (-1, 1):
            ctx.arc(sd * 70, 0, 30, 0, math.pi)
            ctx.set_source_rgb(*INK)
            ctx.set_line_width(8)
            ctx.stroke()
    if p.get("judge"):  # juez detrás del estrado
        from .world import draw_prop
        draw_prop(ctx, {"type": "npc", "outfit": "judge", "x": 540, "y": 1010, "abs": True, "enter": "none",
                        "size": 1.0, "hair": "#DDDDDD", **p["judge"]}, t)
    # estrado del juez
    rrect(ctx, 140, 860, 800, 520, 20)
    fill_stroke(ctx, "#6B3D24", OUT)
    rrect(ctx, 100, 820, 880, 70, 16)
    fill_stroke(ctx, "#7E4A2C", OUT)
    for k in range(3):
        rrect(ctx, 200 + k * 240, 960, 200, 330, 12)
        fill_stroke(ctx, "#5A321E", OUT * 0.6)
    if p.get("label"):
        rrect(ctx, 340, 1000, 400, 90, 12)
        fill_stroke(ctx, "#C9A24A", OUT * 0.8)
        text(ctx, p["label"], 540, 1045, 46, color=INK, outline=0, shadow_off=0, max_w=370)
    ctx.rectangle(-M, 1380, W + 2 * M, H)
    fill_stroke(ctx, "#5A3A28", OUT)
    if p.get("cages"):  # jaulas del aula búnker
        for cx in (-80, 840):
            rrect(ctx, cx, 1180, 320, 420, 10)
            ctx.set_source_rgba(0.2, 0.2, 0.25, 0.25)
            ctx.fill()
            for k in range(7):
                limb(ctx, [(cx + 20 + k * 46, 1180), (cx + 20 + k * 46, 1600)], 10, (0.4, 0.4, 0.45), out=OUT * 0.4)


def bg_countryside(ctx, t, p):
    """Campo siciliano: colinas secas, olivos y una granja de piedra."""
    _sky(ctx, (0.45, 0.72, 0.98), (0.98, 0.88, 0.7))
    circle(ctx, 820, 330, 90)
    fill_stroke(ctx, PAL["yellow"], OUT)
    for k, (yb, c) in enumerate(((1050, "#C9A86A"), (1200, "#B8924F"), (1350, "#A07A3E"))):
        ctx.move_to(-M, yb)
        for x in range(-M, W + M + 1, 60):
            ctx.line_to(x, yb - 120 * math.sin(x * 0.004 + k * 1.7) - 40)
        ctx.line_to(W + M, H + M)
        ctx.line_to(-M, H + M)
        ctx.close_path()
        fill_stroke(ctx, c, OUT)
    if p.get("farm", True):
        fx, fy = p.get("farm_x", 640), p.get("farm_y", 1180)
        rrect(ctx, fx - 200, fy - 220, 400, 230, 8)
        fill_stroke(ctx, "#D9C7A0", OUT)
        ctx.move_to(fx - 230, fy - 210)
        ctx.line_to(fx, fy - 330)
        ctx.line_to(fx + 230, fy - 210)
        ctx.close_path()
        fill_stroke(ctx, "#B5532F", OUT)
        rrect(ctx, fx - 40, fy - 120, 80, 130, 8)
        fill_stroke(ctx, "#6B3D24", OUT * 0.7)
        for wx in (fx - 140, fx + 90):
            rrect(ctx, wx, fy - 160, 60, 60, 6)
            fill_stroke(ctx, (0.25, 0.3, 0.4), OUT * 0.6)
    for ox, oy in ((150, 1300), (930, 1380), (360, 1500)):  # olivos
        limb(ctx, [(ox, oy + 120), (ox + 10, oy)], 24, "#6B4A2E", out=OUT * 0.6)
        for k in range(5):
            blob(ctx, ox + (k - 2) * 45, oy - 40 - (k % 2) * 40, 60, n=7, wobble=0.2, seed=k + ox)
            fill_stroke(ctx, "#7C8B4E", OUT * 0.6)


# ============================================================================
# PROPS
# ============================================================================
def _bars(ctx, p, t):
    for k in range(-2, 12):
        x = k * 120 + 40
        rrect(ctx, x - 18, -M, 36, H + 2 * M, 18)
        ctx.set_source(linear_grad(ctx, x - 18, 0, x + 18, 0, [(0, (0.3, 0.3, 0.35)), (0.5, (0.7, 0.72, 0.78)),
                                                              (1, (0.3, 0.3, 0.35))]))
        ctx.fill_preserve()
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(OUT * 0.8)
        ctx.stroke()
    for y in (350, 1450):
        rrect(ctx, -M, y, W + 2 * M, 40, 10)
        fill_stroke(ctx, (0.45, 0.46, 0.52), OUT * 0.8)


def _npc(ctx, p, t):
    """Personaje secundario: reutiliza el rig de Leo con otra paleta, ropa y sombrero."""
    from .character import Character, Pose, act
    pal = {"hair": col(p.get("hair", "#3A2A20")), "skin": col(p.get("skin", "#E8B48A")),
           "hoodie": col(p.get("shirt", "#4A6FA5"))}
    pal["skin_sh"] = darken(pal["skin"], 0.12)
    ch = Character(pal)
    base = Pose(x=0, y=0, scale=p.get("size", 1.0), facing=p.get("facing", 1.0),
                expression=p.get("expression", "neutral"), outfit=p.get("outfit", "mobster"),
                helmet=p.get("hat"), extras={"mustache": p.get("mustache", False), "hair": pal["hair"],
                                             "hat_color": col(p.get("hat_color", "#2A2630"))})
    pose = act(p.get("action", "idle"), t + p.get("seed", 0) * 0.37, 3.0, base, {})
    if p.get("silhouette"):
        ctx.push_group()
        ch.draw(ctx, pose)
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(1)
        return
    ch.draw(ctx, pose)


def _money(ctx, p, t):
    n = p.get("stacks", 3)
    for k in range(n):
        with saved(ctx):
            ctx.translate((k - (n - 1) / 2) * 120, -k % 2 * 30)
            for j in range(4):
                rrect(ctx, -90, -j * 26, 180, 30, 6)
                fill_stroke(ctx, "#7CC46A", OUT * 0.6)
            rrect(ctx, -20, -90, 40, 34, 6)
            fill_stroke(ctx, (0.95, 0.95, 0.9), 3)
            text(ctx, "$", 0, -50, 50, color="#2E7D32", outline=0, shadow_off=0)
    if p.get("bag", True):
        ctx.move_to(-160 + 0, 90)
        ctx.curve_to(-220, 30, -150, -120, -110, -110)
        ctx.line_to(-130, -170)
        ctx.line_to(-50, -170)
        ctx.line_to(-70, -110)
        ctx.curve_to(-30, -120, 40, 30, -20, 90)
        ctx.close_path()
        fill_stroke(ctx, "#C9A86A", OUT)
        text(ctx, "$", -90, 10, 90, color="#2E7D32", outline=6, shadow_off=0)


def _typewriter(ctx, p, t):
    rrect(ctx, -200, -60, 400, 170, 30)
    fill_stroke(ctx, (0.18, 0.18, 0.2), OUT)
    rrect(ctx, -230, -120, 460, 60, 20)
    fill_stroke(ctx, (0.25, 0.25, 0.28), OUT)
    # papel que sale
    h = 120 + 40 * ((t * 0.5) % 1)
    rrect(ctx, -110, -120 - h, 220, h + 10, 4)
    fill_stroke(ctx, (1, 0.98, 0.9), OUT * 0.7)
    for k in range(int(h / 30)):
        ctx.rectangle(-90, -100 - h + k * 30 + 20, 150 - (k * 37 % 60), 6)
    ctx.set_source_rgb(0.3, 0.3, 0.35)
    ctx.fill()
    for r in range(3):
        for k in range(8):
            circle(ctx, -150 + k * 43 + r * 10, -10 + r * 40, 15)
            fill_stroke(ctx, (0.9, 0.9, 0.85), 3)
    if (t * 8) % 1 < 0.5:
        circle(ctx, -150 + int(t * 8) % 8 * 43, -10, 15)
        ctx.set_source_rgb(*PAL["yellow"])
        ctx.fill()


def _note(ctx, p, t):
    """Pizzino: notita doblada escrita a máquina."""
    with saved(ctx):
        ctx.rotate(p.get("tilt", -0.1) + 0.03 * math.sin(t * 3))
        rrect(ctx, -110, -70, 220, 140, 6)
        fill_stroke(ctx, (1, 0.97, 0.85), OUT * 0.7)
        for k in range(4):
            ctx.rectangle(-85, -45 + k * 28, 170 - (k * 29 % 50), 7)
        ctx.set_source_rgb(0.35, 0.35, 0.4)
        ctx.fill()
        ctx.move_to(-110, 0)
        ctx.line_to(110, 0)
        ctx.set_source_rgba(0, 0, 0, 0.15)
        ctx.set_line_width(3)
        ctx.stroke()


def _handcuffs(ctx, p, t):
    for sd in (-1, 1):
        circle(ctx, sd * 80, 0, 60)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(34)
        ctx.stroke()
        circle(ctx, sd * 80, 0, 60)
        ctx.set_source_rgb(0.8, 0.82, 0.88)
        ctx.set_line_width(20)
        ctx.stroke()
    for k in range(3):
        ellipse(ctx, -24 + k * 24, -60, 16, 10)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(8)
        ctx.stroke()


def _police_car(ctx, p, t):
    """Coche patrulla de época con sirena."""
    on = (t * 4) % 1 < 0.5
    rrect(ctx, -300, -60, 600, 130, 40)
    fill_stroke(ctx, (0.1, 0.1, 0.14), OUT)
    ctx.move_to(-170, -60)
    ctx.curve_to(-150, -170, 150, -170, 180, -60)
    ctx.close_path()
    fill_stroke(ctx, (0.1, 0.1, 0.14), OUT)
    rrect(ctx, -130, -140, 120, 70, 12)
    fill_stroke(ctx, (0.6, 0.8, 1), OUT * 0.6)
    rrect(ctx, 10, -140, 120, 70, 12)
    fill_stroke(ctx, (0.6, 0.8, 1), OUT * 0.6)
    rrect(ctx, -300, 0, 600, 30, 8)
    fill_stroke(ctx, (0.95, 0.95, 0.95), OUT * 0.6)
    text(ctx, "POLICE", 0, 15, 30, color=INK, outline=0, shadow_off=0)
    for x in (-180, 180):
        circle(ctx, x, 75, 55)
        fill_stroke(ctx, (0.2, 0.2, 0.22), OUT)
        circle(ctx, x, 75, 22)
        fill_stroke(ctx, PAL["metal"], 4)
    circle(ctx, 0, -180, 26)
    fill_stroke(ctx, PAL["red"] if on else (0.5, 0.15, 0.15), OUT * 0.7)
    if on:
        circle(ctx, 0, -180, 120)
        ctx.set_source(radial_grad(ctx, 0, -180, 10, 120, [(0, (1, 0.2, 0.2), 0.5), (1, (1, 0.2, 0.2), 0)]))
        ctx.fill()


def _gavel(ctx, p, t):
    hit = abs(math.sin(t * 3))
    with saved(ctx):
        ctx.rotate(-0.6 * hit)
        limb(ctx, [(0, 0), (190, -10)], 22, "#8B5A2B", out=OUT * 0.7)
        rrect(ctx, 170, -80, 90, 150, 20)
        fill_stroke(ctx, "#6B3D24", OUT)
    rrect(ctx, 120, 110, 220, 40, 12)
    fill_stroke(ctx, "#6B3D24", OUT)


def _phone(ctx, p, t):
    """Teléfono antiguo; con `bug` muestra un micrófono espía."""
    rrect(ctx, -110, -40, 220, 130, 30)
    fill_stroke(ctx, (0.12, 0.12, 0.14), OUT)
    circle(ctx, 0, 25, 48)
    fill_stroke(ctx, (0.9, 0.9, 0.85), OUT * 0.6)
    for k in range(10):
        a = k * 0.55 + 0.8
        circle(ctx, 30 * math.cos(a), 25 + 30 * math.sin(a), 7)
        ctx.set_source_rgb(*INK)
        ctx.fill()
    ctx.move_to(-130, -60)
    ctx.curve_to(-120, -120, 120, -120, 130, -60)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(46)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.stroke()
    if p.get("bug"):
        with saved(ctx):
            ctx.translate(150, 80)
            rrect(ctx, -20, -40, 40, 70, 16)
            fill_stroke(ctx, (0.5, 0.5, 0.55), OUT * 0.6)
            circle(ctx, 0, -55, 14)
            fill_stroke(ctx, PAL["red"] if (t * 3) % 1 < 0.5 else (0.4, 0.1, 0.1), 3)
            for r in (40, 70):
                ctx.arc(0, -55, r + 10 * ((t * 2) % 1), -2.3, -0.8)
                ctx.set_source_rgba(1, 0.3, 0.3, 0.7)
                ctx.set_line_width(6)
                ctx.stroke()


def _card(ctx, p, t):
    """Tarjeta de visita."""
    with saved(ctx):
        ctx.rotate(-0.08)
        rrect(ctx, -300, -170, 600, 340, 16)
        fill_stroke(ctx, (0.98, 0.96, 0.9), OUT)
        for i, ln in enumerate(p.get("lines", ["A. CAPONE", "Muebles usados"])):
            text(ctx, ln, 0, -70 + i * 90, 66 if i == 0 else 52, color=INK if i == 0 else "#7A3B2E", outline=0,
                 shadow_off=0, max_w=540)


def _wanted(ctx, p, t):
    """Cartel de «se busca» con silueta."""
    with saved(ctx):
        ctx.rotate(0.05)
        rrect(ctx, -230, -320, 460, 640, 10)
        fill_stroke(ctx, (0.93, 0.85, 0.65), OUT)
        text(ctx, p.get("title", "SE BUSCA"), 0, -250, 76, color="#7A3B2E", outline=0, shadow_off=0)
        circle(ctx, 0, -60, 90)
        ctx.set_source_rgb(0.25, 0.22, 0.2)
        ctx.fill()
        ctx.move_to(-150, 120)
        ctx.curve_to(-150, 20, 150, 20, 150, 120)
        ctx.close_path()
        ctx.fill()
        text(ctx, p.get("sub", "43 AÑOS"), 0, 200, 64, color=INK, outline=0, shadow_off=0, max_w=420)


def _bunker(ctx, p, t):
    """Edificio blindado (aula búnker)."""
    rrect(ctx, -380, -260, 760, 400, 20)
    fill_stroke(ctx, (0.75, 0.78, 0.72), OUT)
    for k in range(6):
        rrect(ctx, -330 + k * 115, -180, 70, 40, 6)
        fill_stroke(ctx, (0.3, 0.35, 0.4), OUT * 0.6)
    rrect(ctx, -70, 20, 140, 120, 10)
    fill_stroke(ctx, (0.4, 0.42, 0.45), OUT * 0.8)
    rrect(ctx, -420, -300, 840, 60, 14)
    fill_stroke(ctx, (0.6, 0.62, 0.58), OUT)
    for s in (-1, 1):
        star(ctx, s * 300, 0, 26, n=4, inner=0.3)
        ctx.set_source_rgba(1, 1, 1, 0.5 + 0.5 * math.sin(t * 4 + s))
        ctx.fill()


def _plane(ctx, p, t):
    with saved(ctx):
        ctx.rotate(-0.15)
        ellipse(ctx, 0, 0, 260, 50)
        fill_stroke(ctx, (0.95, 0.95, 0.98), OUT)
        ctx.move_to(-40, 0)
        ctx.line_to(-140, 170)
        ctx.line_to(-60, 170)
        ctx.line_to(60, 10)
        ctx.close_path()
        fill_stroke(ctx, (0.85, 0.88, 0.95), OUT)
        ctx.move_to(-200, -20)
        ctx.line_to(-260, -120)
        ctx.line_to(-210, -120)
        ctx.line_to(-150, -30)
        ctx.close_path()
        fill_stroke(ctx, PAL["blue"], OUT)
        for k in range(6):
            circle(ctx, -100 + k * 50, -10, 12)
            fill_stroke(ctx, (0.55, 0.8, 1), 3)


def _flowers(ctx, p, t):
    """Ramo de flores (homenaje)."""
    for k in range(7):
        a = -math.pi / 2 + (k - 3) * 0.22
        ex, ey = 150 * math.cos(a), 150 * math.sin(a)
        ctx.move_to(0, 120)
        ctx.line_to(ex, ey)
        ctx.set_source_rgb(0.25, 0.55, 0.3)
        ctx.set_line_width(8)
        ctx.stroke()
        c = ["#FF5C8A", "#FFD23F", "#FFFFFF", "#FF8A3D"][k % 4]
        for j in range(5):
            b = j * 2 * math.pi / 5 + t
            circle(ctx, ex + 18 * math.cos(b), ey + 18 * math.sin(b), 13)
        fill_stroke(ctx, c, 3)
        circle(ctx, ex, ey, 9)
        ctx.set_source_rgb(*PAL["yellow"])
        ctx.fill()
    ctx.move_to(-60, 60)
    ctx.line_to(60, 60)
    ctx.line_to(20, 170)
    ctx.line_to(-20, 170)
    ctx.close_path()
    fill_stroke(ctx, "#C9A24A", OUT * 0.7)


def _speech(ctx, p, t):
    """Bocadillo de diálogo."""
    txt = p.get("text", "...")
    size = p.get("size", 54)
    ctx.select_font_face("Lilita One")
    ctx.set_font_size(size)
    w = min(760, ctx.text_extents(txt).width) + 70
    h = size * 1.7
    rrect(ctx, -w / 2, -h / 2, w, h, h / 2.2)
    fill_stroke(ctx, (1, 1, 1), OUT)
    tail = p.get("tail", -1)
    ctx.move_to(tail * w * 0.2 - 20, h / 2 - 4)
    ctx.line_to(tail * w * 0.3, h / 2 + 50)
    ctx.line_to(tail * w * 0.2 + 25, h / 2 - 4)
    ctx.close_path()
    fill_stroke(ctx, (1, 1, 1), OUT)
    rrect(ctx, tail * w * 0.2 - 22, h / 2 - 14, 50, 14, 4)
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill()
    text(ctx, txt, 0, 0, size, color=INK, outline=0, shadow_off=0, max_w=740)


BACKGROUNDS.update({"city_night": bg_city_night, "office": bg_office, "prison": bg_prison,
                    "courtroom": bg_courtroom, "countryside": bg_countryside})
PROPS.update({"bars": _bars, "npc": _npc, "money": _money, "typewriter": _typewriter, "note": _note,
              "handcuffs": _handcuffs, "police_car": _police_car, "gavel": _gavel, "phone": _phone, "card": _card,
              "wanted": _wanted, "bunker": _bunker, "plane": _plane, "flowers": _flowers, "speech": _speech})
