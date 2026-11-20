"""Backgrounds and props for the stickman channel (1920×1080, flat colours + ink outlines).

Every function is a pure function of time `t`, so scenes render in parallel and frame-exact.
Backgrounds: draw_background(ctx, spec, t). Props: draw_prop(ctx, spec, t, age).
"""
from __future__ import annotations

import math

import cairo
import numpy as np

from ..visuals.draw import clamp, ease_back, ease_io, ease_out, lerp, noise1
from .style import (INK, OUTLINE, P, H, W, c, circ, ink_fill, line, poly, rrect, shade, stroke, tint, write,
                    write_block, MARKER, HAND)

GROUND = 0.84          # default ground line (fraction of height)
TAU = 2 * math.pi


def px(x, y):
    """Fractions (|v| <= 1.5) → pixels."""
    return (x * W if abs(x) <= 1.5 else x, y * H if abs(y) <= 1.5 else y)


def _rng(seed):
    return np.random.default_rng(seed)


# ---------------------------------------------------------------------------
# Sky, ground and shared scenery
# ---------------------------------------------------------------------------
SKY = {
    "day": [(0, (0.55, 0.78, 0.96)), (1, (0.86, 0.94, 0.99))],
    "dusk": [(0, (0.36, 0.33, 0.62)), (0.6, (0.96, 0.58, 0.45)), (1, (0.99, 0.82, 0.55))],
    "night": [(0, (0.06, 0.08, 0.2)), (1, (0.17, 0.2, 0.38))],
    "grey": [(0, (0.62, 0.66, 0.72)), (1, (0.84, 0.86, 0.88))],
}
SEASON_GRASS = {"spring": ("grass", "darkgrass"), "summer": ((0.6, 0.76, 0.32), (0.44, 0.6, 0.24)),
                "autumn": ((0.78, 0.66, 0.34), (0.62, 0.48, 0.24)), "winter": ("snow", (0.82, 0.86, 0.92))}
SEASON_TREE = {"spring": ((0.45, 0.74, 0.36),), "summer": ((0.33, 0.6, 0.27),), "autumn": ((0.9, 0.55, 0.2),),
               "winter": (None,)}


def sky(ctx, spec, t, horizon=None):
    tod = spec.get("time", "day")
    g = cairo.LinearGradient(0, 0, 0, horizon or H)
    for off, col_ in SKY.get(tod, SKY["day"]):
        g.add_color_stop_rgb(off, *col_)
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(g)
    ctx.fill()
    if tod == "night":
        r = _rng(4)
        for i in range(70):
            x, y = r.random() * W, r.random() * (horizon or H) * 0.8
            tw = 0.6 + 0.4 * math.sin(t * 2 + i)
            circ(ctx, x, y, 1.5 + r.random() * 2)
            ctx.set_source_rgba(1, 1, 0.9, tw)
            ctx.fill()
        circ(ctx, W * 0.8, H * 0.18, 55)
        ink_fill(ctx, (0.98, 0.96, 0.85), 0)
        circ(ctx, W * 0.8 + 22, H * 0.18 - 12, 46)
        ctx.set_source_rgb(*SKY["night"][0][1])
        ctx.fill()
    elif spec.get("sun", tod in ("day", "dusk")):
        sx, sy = px(*spec.get("sun_pos", (0.84, 0.17 if tod == "day" else 0.5)))
        for k in range(12):
            a = k * TAU / 12 + t * 0.15
            line(ctx, sx + math.cos(a) * 78, sy + math.sin(a) * 78, sx + math.cos(a) * 100, sy + math.sin(a) * 100,
                 6, "yellow")
        circ(ctx, sx, sy, 62)
        ink_fill(ctx, "yellow", OUTLINE)
    if spec.get("clouds", tod != "night"):
        for i in range(spec.get("n_clouds", 4)):
            x = ((i * 530 + 140 + t * (14 + 5 * i)) % (W + 500)) - 250
            cloud(ctx, x, 110 + (i * 97) % 200, 0.8 + 0.25 * (i % 3), alpha=0.95,
                  color="lightgrey" if tod == "grey" else "white")


def cloud(ctx, x, y, s=1.0, alpha=1.0, color="white"):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.move_to(-110, 30)
    ctx.curve_to(-140, 30, -140, -18, -100, -14)
    ctx.curve_to(-96, -60, -30, -66, -18, -30)
    ctx.curve_to(0, -78, 80, -70, 76, -20)
    ctx.curve_to(130, -26, 140, 30, 100, 30)
    ctx.close_path()
    ink_fill(ctx, color, OUTLINE / s, alpha)
    ctx.restore()


def hills(ctx, spec, horizon):
    season = spec.get("season", "spring")
    g1, g2 = SEASON_GRASS.get(season, SEASON_GRASS["spring"])
    far = tint(g2, 0.35) if season != "winter" else (0.88, 0.9, 0.95)
    ctx.move_to(0, horizon)
    for i in range(0, W + 1, 40):
        ctx.line_to(i, horizon - 70 - 50 * math.sin(i / 260 + 1) - 30 * math.sin(i / 120))
    ctx.line_to(W, horizon + 60)
    ctx.line_to(0, horizon + 60)
    ctx.close_path()
    ink_fill(ctx, far, OUTLINE * 0.7)


def ground(ctx, spec, gy):
    season = spec.get("season", "spring")
    kind = spec.get("ground", "grass")
    g1, g2 = SEASON_GRASS.get(season, SEASON_GRASS["spring"])
    fill = {"grass": g1, "dirt": "dirt", "stone": "stone", "sand": "tan", "snow": "snow", "floor": "wood",
            "mud": (0.5, 0.38, 0.26)}.get(kind, g1)
    if season == "winter" and kind == "grass":
        fill = "snow"
    ctx.move_to(-10, gy)
    for i in range(0, W + 21, 60):
        ctx.line_to(i, gy + 5 * math.sin(i / 90))
    ctx.line_to(W + 10, H + 10)
    ctx.line_to(-10, H + 10)
    ctx.close_path()
    ink_fill(ctx, fill, OUTLINE)
    if kind == "grass" and season != "winter":
        r = _rng(9)
        for _ in range(40):
            x, y = r.random() * W, gy + 30 + r.random() * (H - gy - 40)
            line(ctx, x, y, x - 6, y - 14, 3, g2)
            line(ctx, x + 7, y, x + 9, y - 16, 3, g2)


# ---------------------------------------------------------------------------
# Backgrounds
# ---------------------------------------------------------------------------
def bg_paper(ctx, spec, t):
    ctx.set_source_rgb(*c(spec.get("color", "paper")))
    ctx.paint()
    if spec.get("lines"):   # notebook lines
        for y in range(120, H, 72):
            line(ctx, 0, y, W, y, 2, (0.75, 0.84, 0.93), 0.6)
        line(ctx, 150, 0, 150, H, 2.5, (0.93, 0.6, 0.6), 0.6)
    if spec.get("floor", True):
        gy = H * spec.get("ground_y", GROUND)
        line(ctx, 0, gy, W, gy, 5, INK, 0.85)


def bg_solid(ctx, spec, t):
    ctx.set_source_rgb(*c(spec.get("color", "navy")))
    ctx.paint()
    g = cairo.RadialGradient(W / 2, H / 2, H * 0.3, W / 2, H / 2, H)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, spec.get("vignette", 0.35))
    ctx.set_source(g)
    ctx.paint()
    if spec.get("rays"):
        ctx.save()
        ctx.translate(W / 2, H / 2)
        ctx.rotate(t * 0.12)
        for k in range(16):
            a = k * TAU / 16
            ctx.move_to(0, 0)
            ctx.arc(0, 0, 1500, a, a + TAU / 32)
            ctx.close_path()
            ctx.set_source_rgba(1, 1, 1, 0.06)
            ctx.fill()
        ctx.restore()


def bg_field(ctx, spec, t):
    gy = H * spec.get("ground_y", GROUND)
    sky(ctx, spec, t, gy)
    hills(ctx, spec, gy - 40)
    if spec.get("village"):
        for i, x in enumerate((300, 520, 1450, 1640)):
            hut(ctx, x, gy - 70, 0.45, spec, t, seed=i)
        church(ctx, 1000, gy - 70, 0.5)
    if spec.get("castle"):
        castle(ctx, *px(*spec.get("castle_pos", (0.78, 0.0))) if False else (W * spec.get("castle_x", 0.78), gy - 90),
               spec.get("castle_scale", 0.6))
    ground(ctx, spec, gy)
    if spec.get("crops") is not None:
        crop_rows(ctx, spec, t, gy)
    if spec.get("fence"):
        for x in range(40, W, 140):
            line(ctx, x, gy + 10, x, gy - 60, 8, "wood")
        line(ctx, 0, gy - 45, W, gy - 45, 7, "wood")
        line(ctx, 0, gy - 18, W, gy - 18, 7, "wood")
    weather(ctx, spec, t)


def crop_rows(ctx, spec, t, gy):
    grow = clamp(spec.get("crops", 1.0))
    kind = spec.get("crop_kind", "wheat")
    season = spec.get("season", "summer")
    r = _rng(3)
    for row in range(3):
        y = gy + 40 + row * 55
        for i in range(-1, 24):
            x = i * 88 + (row % 2) * 44 + 20
            h = (30 + 60 * grow) * (1 + 0.15 * r.random())
            sway = 4 * math.sin(t * 1.7 + i * 0.6 + row)
            colr = "wheat" if (kind == "wheat" and (season in ("summer", "autumn") or grow > 0.9)) else "green"
            if grow < 0.05:
                line(ctx, x - 20, y, x + 20, y, 4, "darkwood")
                continue
            for k in (-10, 0, 10):
                line(ctx, x + k, y, x + k + sway, y - h, 4, shade(colr, 0.2))
                if colr == "wheat" and grow > 0.6:
                    ctx.save()
                    ctx.translate(x + k + sway, y - h)
                    ctx.scale(0.45, 1)
                    circ(ctx, 0, -6, 12)
                    ctx.restore()
                    ink_fill(ctx, "wheat", 2.5)


def weather(ctx, spec, t):
    w = spec.get("weather") or ("snow" if spec.get("season") == "winter" and spec.get("snowfall", True) else None)
    if w == "snow":
        r = _rng(7)
        for i in range(90):
            x0, sp, ph = r.random() * W, 40 + r.random() * 50, r.random() * H
            y = (ph + t * sp) % H
            x = x0 + 18 * math.sin(t + i)
            circ(ctx, x, y, 3 + 3 * r.random())
            ctx.set_source_rgba(1, 1, 1, 0.9)
            ctx.fill()
    elif w == "rain":
        r = _rng(8)
        for i in range(140):
            x0, ph = r.random() * W, r.random() * H
            y = (ph + t * 900) % H
            line(ctx, x0 - 0.15 * y, y, x0 - 0.15 * y - 6, y + 28, 2.5, (0.55, 0.7, 0.9), 0.8)


def bg_village(ctx, spec, t):
    spec = {**spec, "village": True}
    bg_field(ctx, spec, t)


def bg_castle(ctx, spec, t):
    spec = {**spec, "castle": True}
    bg_field(ctx, spec, t)


def bg_interior(ctx, spec, t):
    """Peasant hut: plank walls, dirt floor with straw, a hearth with fire and smoke."""
    gy = H * spec.get("ground_y", GROUND)
    wall = c(spec.get("wall", (0.66, 0.5, 0.34)))
    dark = spec.get("dark", 0.0)
    ctx.rectangle(0, 0, W, gy)
    ctx.set_source_rgb(*wall)
    ctx.fill()
    for x in range(0, W, 120):
        line(ctx, x, 0, x, gy, 3, shade(wall, 0.25))
    # beams
    line(ctx, 0, 90, W, 90, 22, "darkwood")
    for x in (300, 960, 1620):
        line(ctx, x, 90, x, gy, 18, "darkwood")
    if spec.get("window", True):
        wx, wy = W * spec.get("window_x", 0.72), 250
        rrect(ctx, wx - 90, wy - 80, 180, 160, 6)
        light = SKY.get(spec.get("time", "day"), SKY["day"])[0][1]
        if spec.get("season") == "winter":
            light = (0.8, 0.85, 0.92)
        ink_fill(ctx, light, OUTLINE)
        line(ctx, wx, wy - 80, wx, wy + 80, 6, "darkwood")
        line(ctx, wx - 90, wy, wx + 90, wy, 6, "darkwood")
    ctx.rectangle(0, gy, W, H - gy)
    ctx.set_source_rgb(*c((0.48, 0.36, 0.25)))
    ctx.fill()
    line(ctx, 0, gy, W, gy, OUTLINE, INK)
    r = _rng(5)
    for _ in range(60):  # straw on the floor
        x, y = r.random() * W, gy + 15 + r.random() * (H - gy - 20)
        a = r.random() * math.pi
        line(ctx, x, y, x + 20 * math.cos(a), y + 6 * math.sin(a), 3, "thatch")
    if spec.get("hearth", True):
        hx = W * spec.get("hearth_x", 0.5)
        poly(ctx, [(hx - 110, gy + 8), (hx + 110, gy + 8), (hx + 90, gy - 22), (hx - 90, gy - 22)])
        ink_fill(ctx, "stone", OUTLINE)
        fire(ctx, hx, gy - 20, 1.1, t)
        smoke(ctx, hx, gy - 140, t, 1.0)
    if dark:
        ctx.rectangle(0, 0, W, H)
        ctx.set_source_rgba(0.05, 0.04, 0.1, dark)
        ctx.fill()


def bg_church(ctx, spec, t):
    gy = H * spec.get("ground_y", GROUND)
    ctx.set_source_rgb(*c("stone"))
    ctx.paint()
    for x in range(0, W, 160):
        for y in range(0, int(gy), 80):
            rrect(ctx, x + (40 if (y // 80) % 2 else 0) - 80, y, 158, 78, 4)
            ctx.set_source_rgb(*shade("stone", 0.06 * ((x + y) % 3)))
            ctx.fill_preserve()
            ctx.set_source_rgba(*INK, 0.25)
            ctx.set_line_width(2)
            ctx.stroke()
    for i, x in enumerate((400, 960, 1520)):
        ctx.move_to(x - 110, gy - 200)
        ctx.line_to(x - 110, 330)
        ctx.arc(x, 330, 110, math.pi, 2 * math.pi)
        ctx.line_to(x + 110, gy - 200)
        ctx.close_path()
        ink_fill(ctx, (0.3, 0.28, 0.4), OUTLINE)
        cols = ["red", "blue", "yellow", "green"]
        for k in range(4):
            ctx.move_to(x, 330)
            ctx.arc(x, 330, 100, math.pi + k * math.pi / 4, math.pi + (k + 1) * math.pi / 4)
            ctx.close_path()
            ink_fill(ctx, cols[(k + i) % 4], 3)
        for k in range(3):
            rrect(ctx, x - 100 + k * 67, 340, 66, gy - 550, 2)
            ink_fill(ctx, cols[(k + i + 1) % 4], 3)
    # light shafts
    ctx.move_to(860, 200)
    ctx.line_to(1060, 200)
    ctx.line_to(1300, gy)
    ctx.line_to(700, gy)
    ctx.close_path()
    ctx.set_source_rgba(1, 0.95, 0.7, 0.18 + 0.04 * math.sin(t))
    ctx.fill()
    ctx.rectangle(0, gy, W, H - gy)
    ctx.set_source_rgb(*shade("stone", 0.2))
    ctx.fill()
    line(ctx, 0, gy, W, gy, OUTLINE)


def bg_town(ctx, spec, t):
    gy = H * spec.get("ground_y", GROUND)
    sky(ctx, spec, t, gy)
    cols = ["tan", (0.93, 0.88, 0.76), (0.85, 0.76, 0.6), (0.95, 0.9, 0.8)]
    for i in range(7):
        x = i * 290 - 40
        hh = 380 + (i * 73) % 120
        rrect(ctx, x, gy - hh, 280, hh, 2)
        ink_fill(ctx, cols[i % 4], OUTLINE)
        for k in range(3):   # timber frame
            line(ctx, x + k * 140, gy - hh, x + k * 140, gy, 7, "darkwood")
        line(ctx, x, gy - hh / 2, x + 280, gy - hh / 2, 7, "darkwood")
        line(ctx, x, gy - hh / 2, x + 140, gy - hh, 6, "darkwood")
        poly(ctx, [(x - 20, gy - hh), (x + 140, gy - hh - 150), (x + 300, gy - hh)])
        ink_fill(ctx, (0.62, 0.3, 0.24) if i % 2 else "thatch", OUTLINE)
        rrect(ctx, x + 105, gy - 140, 70, 140, 30)
        ink_fill(ctx, "darkwood", OUTLINE)
    spec2 = {**spec, "ground": spec.get("ground", "mud")}
    ground(ctx, spec2, gy)
    if spec.get("stalls"):
        for i, x in enumerate((420, 1100, 1650)):
            market_stall(ctx, x, gy + 60, ["red", "blue", "green"][i % 3])
    weather(ctx, spec, t)


def bg_forest(ctx, spec, t):
    gy = H * spec.get("ground_y", GROUND)
    sky(ctx, {**spec, "sun": False}, t, gy)
    for layer, (k, sc) in enumerate(((0.45, 0.8), (0.0, 1.1))):
        for i in range(9):
            x = i * 240 + (120 if layer else 0) - 40
            tree(ctx, x, gy - (60 if not layer else 0), sc * (0.9 + 0.2 * ((i * 7) % 3) / 2), spec, t, i, fade=k)
    ground(ctx, spec, gy)
    weather(ctx, spec, t)


def bg_map(ctx, spec, t):
    ctx.set_source_rgb(*c("parchment"))
    ctx.paint()
    g = cairo.RadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, H * 1.05)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0.4, 0.25, 0.05, 0.45)
    ctx.set_source(g)
    ctx.paint()
    # sea texture
    for y in range(80, H, 90):
        for x in range(0, W, 180):
            ctx.move_to(x + (y % 180) * 0.5, y)
            ctx.curve_to(x + 30, y - 12, x + 60, y + 12, x + 90, y)
            stroke(ctx, 2.5, (0.55, 0.45, 0.3), 0.35)
    land = spec.get("land", "island")
    r = _rng(spec.get("seed", 12))
    cx, cy = W * 0.5, H * 0.52
    pts = []
    n = 26
    for k in range(n):
        a = k * TAU / n
        rad = (330 + 90 * r.random()) * (1.0 if land == "island" else 1.4)
        pts.append((cx + math.cos(a) * rad * 1.5, cy + math.sin(a) * rad))
    ctx.move_to(*pts[0])
    for i in range(n):
        p0, p1 = pts[i], pts[(i + 1) % n]
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        ctx.curve_to(p0[0], p0[1], p0[0], p0[1], mx, my)
    ctx.close_path()
    ink_fill(ctx, (0.84, 0.78, 0.55), OUTLINE)
    # compass
    x0, y0 = W - 160, H - 160
    for k in range(4):
        a = k * math.pi / 2 - math.pi / 2
        poly(ctx, [(x0 + math.cos(a) * 70, y0 + math.sin(a) * 70), (x0 + math.cos(a + 0.6) * 18, y0 + math.sin(a + 0.6) * 18),
                   (x0 + math.cos(a - 0.6) * 18, y0 + math.sin(a - 0.6) * 18)])
        ink_fill(ctx, "red" if k == 0 else "parchment", 3)
    write(ctx, "N", x0, y0 - 92, 40, INK, MARKER)


def bg_chalkboard(ctx, spec, t):
    ctx.set_source_rgb(*c("darkwood"))
    ctx.paint()
    rrect(ctx, 40, 40, W - 80, H - 80, 10)
    ink_fill(ctx, "chalk", OUTLINE)
    r = _rng(2)
    for _ in range(25):
        x, y = 60 + r.random() * (W - 120), 60 + r.random() * (H - 120)
        line(ctx, x, y, x + 80 * r.random(), y + 10 * r.random(), 18, (1, 1, 1), 0.025)


def bg_split(ctx, spec, t):
    """Two-panel comparison (left vs right)."""
    a, b = spec.get("left", "sky"), spec.get("right", (0.95, 0.85, 0.75))
    ctx.rectangle(0, 0, W / 2, H)
    ctx.set_source_rgb(*c(a))
    ctx.fill()
    ctx.rectangle(W / 2, 0, W / 2, H)
    ctx.set_source_rgb(*c(b))
    ctx.fill()
    gy = H * spec.get("ground_y", GROUND)
    line(ctx, 0, gy, W, gy, 5)
    line(ctx, W / 2, 0, W / 2, H, 8)
    for i, key in enumerate(("left_label", "right_label")):
        if spec.get(key):
            x = W * (0.25 + 0.5 * i)
            write(ctx, spec[key], x, 90, 68, INK, MARKER, outline=5, outline_color="white")


def bg_manor(ctx, spec, t):
    gy = H * spec.get("ground_y", GROUND)
    sky(ctx, spec, t, gy)
    hills(ctx, spec, gy - 40)
    x0 = W * spec.get("manor_x", 0.62)
    rrect(ctx, x0 - 330, gy - 380, 660, 380, 2)
    ink_fill(ctx, "stone", OUTLINE)
    poly(ctx, [(x0 - 370, gy - 380), (x0, gy - 560), (x0 + 370, gy - 380)])
    ink_fill(ctx, (0.55, 0.28, 0.22), OUTLINE)
    for k in range(4):
        wx = x0 - 250 + k * 165
        rrect(ctx, wx - 35, gy - 320, 70, 90, 30)
        ink_fill(ctx, "yellow" if spec.get("time") == "night" else "sky", OUTLINE)
    rrect(ctx, x0 - 55, gy - 170, 110, 170, 50)
    ink_fill(ctx, "darkwood", OUTLINE)
    flag_x = x0
    line(ctx, flag_x, gy - 560, flag_x, gy - 680, 6)
    w = math.sin(t * 3) * 8
    poly(ctx, [(flag_x, gy - 680), (flag_x + 90, gy - 660 + w), (flag_x, gy - 630)])
    ink_fill(ctx, "red", 3)
    ground(ctx, spec, gy)
    weather(ctx, spec, t)


BACKGROUNDS = {
    "paper": bg_paper, "solid": bg_solid, "field": bg_field, "village": bg_village, "castle": bg_castle,
    "interior": bg_interior, "hut": bg_interior, "church": bg_church, "town": bg_town, "forest": bg_forest,
    "map": bg_map, "chalkboard": bg_chalkboard, "split": bg_split, "manor": bg_manor,
}


def draw_background(ctx, spec, t):
    f = BACKGROUNDS.get(spec.get("type", "paper"), bg_paper)
    f(ctx, spec, t)


# ---------------------------------------------------------------------------
# Scenery pieces (also usable as props)
# ---------------------------------------------------------------------------
def hut(ctx, x, y, s, spec=None, t=0.0, seed=0, smoke_=True):
    """Thatched peasant cottage; (x, y) = bottom centre."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -170, -230, 340, 230, 4)
    ink_fill(ctx, (0.92, 0.86, 0.72), OUTLINE / s)
    for k in (-170, 0, 170):
        line(ctx, k, -230, k, 0, 9, "darkwood")
    line(ctx, -170, -120, 170, -120, 8, "darkwood")
    ctx.move_to(-215, -205)
    ctx.curve_to(-150, -400, 150, -400, 215, -205)
    ctx.close_path()
    ink_fill(ctx, "thatch", OUTLINE / s)
    for k in range(-3, 4):
        line(ctx, k * 45, -230, k * 30, -360, 3, shade("thatch", 0.25))
    rrect(ctx, -40, -140, 80, 140, 36)
    ink_fill(ctx, "darkwood", OUTLINE / s)
    rrect(ctx, 80, -190, 60, 55, 4)
    ink_fill(ctx, (0.25, 0.2, 0.15), OUTLINE / s)
    ctx.restore()
    if smoke_:
        smoke(ctx, x + 60 * s, y - 380 * s, t, s)


def church(ctx, x, y, s):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -200, -260, 400, 260, 2)
    ink_fill(ctx, "stone", OUTLINE / s)
    rrect(ctx, -70, -560, 140, 560, 2)
    ink_fill(ctx, "stone", OUTLINE / s)
    poly(ctx, [(-90, -560), (0, -760), (90, -560)])
    ink_fill(ctx, "darkgrey", OUTLINE / s)
    line(ctx, 0, -760, 0, -840, 10)
    line(ctx, -26, -810, 26, -810, 10)
    rrect(ctx, -40, -150, 80, 150, 40)
    ink_fill(ctx, "darkwood", OUTLINE / s)
    circ(ctx, 0, -440, 40)
    ink_fill(ctx, "yellow", OUTLINE / s)
    ctx.restore()


def castle(ctx, x, y, s):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    stone = (0.72, 0.7, 0.66)
    rrect(ctx, -300, -330, 600, 330, 2)
    ink_fill(ctx, stone, OUTLINE / s)
    for tx in (-340, 260):
        rrect(ctx, tx, -520, 80, 520, 2)
        ink_fill(ctx, stone, OUTLINE / s)
        for k in range(3):
            rrect(ctx, tx + k * 30 - 5, -560, 25, 42, 2)
            ink_fill(ctx, stone, OUTLINE / s)
    for k in range(9):
        rrect(ctx, -300 + k * 68, -370, 40, 42, 2)
        ink_fill(ctx, stone, OUTLINE / s)
    ctx.move_to(-80, 0)
    ctx.line_to(-80, -150)
    ctx.arc(0, -150, 80, math.pi, 2 * math.pi)
    ctx.line_to(80, 0)
    ctx.close_path()
    ink_fill(ctx, "darkwood", OUTLINE / s)
    for tx in (-300, 300):
        line(ctx, tx, -560, tx, -680, 7)
        poly(ctx, [(tx, -680), (tx + 80, -660), (tx, -635)])
        ink_fill(ctx, "red", 3)
    ctx.restore()


def tree(ctx, x, y, s, spec=None, t=0.0, seed=0, fade=0.0, kind=None):
    season = (spec or {}).get("season", "spring")
    leaf = SEASON_TREE.get(season, SEASON_TREE["spring"])[0]
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    sway = math.sin(t * 0.8 + seed) * 4
    poly(ctx, [(-22, 0), (22, 0), (14, -200), (-14, -200)])
    ink_fill(ctx, "wood", OUTLINE / s)
    if leaf is None:
        for a, l in ((-0.6, 110), (0.5, 120), (-0.1, 140)):
            line(ctx, 0, -180, math.sin(a) * l, -180 - math.cos(a) * l, 9, "wood")
    else:
        for (dx, dy, r) in ((-60, -230, 90), (60, -240, 95), (0, -320, 110), (-10, -220, 90)):
            circ(ctx, dx + sway, dy, r)
        ink_fill(ctx, leaf, OUTLINE / s)
    ctx.restore()
    if fade:
        pass


def fire(ctx, x, y, s, t):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for a in (-0.5, 0.5):
        ctx.save()
        ctx.rotate(a)
        rrect(ctx, -60, -10, 120, 20, 8)
        ink_fill(ctx, "darkwood", 3.5)
        ctx.restore()
    for k, (cc, sc) in enumerate((("red", 1.0), ("fire", 0.72), ("yellow", 0.42))):
        f = 1 + 0.12 * math.sin(t * 13 + k) + 0.08 * math.sin(t * 7.3 + k * 2)
        w = 50 * sc
        h = 130 * sc * f
        ctx.move_to(-w, -5)
        ctx.curve_to(-w * 1.1, -h * 0.5, -w * 0.3, -h * 0.7, 4 * math.sin(t * 9 + k), -h)
        ctx.curve_to(w * 0.3, -h * 0.7, w * 1.1, -h * 0.5, w, -5)
        ctx.close_path()
        ink_fill(ctx, cc, 3.5 if k == 0 else 0)
    ctx.restore()


def smoke(ctx, x, y, t, s=1.0, color=(0.6, 0.6, 0.62)):
    for i in range(5):
        k = ((t * 0.35) + i / 5) % 1.0
        r = (14 + 30 * k) * s
        circ(ctx, x + 40 * s * math.sin(k * 5 + i), y - 220 * s * k, r)
        ctx.set_source_rgba(*c(color), 0.55 * (1 - k))
        ctx.fill()


def market_stall(ctx, x, y, color):
    ctx.save()
    ctx.translate(x, y)
    rrect(ctx, -150, -110, 300, 110, 4)
    ink_fill(ctx, "wood", OUTLINE)
    for k in (-140, 130):
        line(ctx, k, -110, k, -300, 9, "darkwood")
    for k in range(6):
        poly(ctx, [(-160 + k * 54, -300), (-106 + k * 54, -300), (-106 + k * 54, -250), (-160 + k * 54, -250)])
        ink_fill(ctx, color if k % 2 == 0 else "white", 3.5)
    for k in range(5):
        circ(ctx, -110 + k * 55, -125, 22)
        ink_fill(ctx, ["red", "orange", "green", "yellow", "red"][k], 3)
    ctx.restore()


# ---------------------------------------------------------------------------
# Props
# ---------------------------------------------------------------------------
def _animal_body(ctx, colr, w, h, legs=True, t=0.0, walk=False):
    if legs:
        for k, lx in enumerate((-w * 0.6, -w * 0.3, w * 0.35, w * 0.6)):
            sw = 10 * math.sin(t * 6 + k * math.pi) if walk else 0
            line(ctx, lx, -h * 0.4, lx + sw, 0, 9)
    ctx.save()
    ctx.translate(0, -h)
    ctx.scale(w, h * 0.65)
    circ(ctx, 0, 0, 1)
    ctx.restore()
    ink_fill(ctx, colr, OUTLINE)


def p_pig(ctx, p, t):
    _animal_body(ctx, "pink", 85, 95, t=t, walk=p.get("walk"))
    circ(ctx, 85, -105, 42)
    ink_fill(ctx, "pink", OUTLINE)
    rrect(ctx, 108, -118, 28, 26, 10)
    ink_fill(ctx, tint("pink", -0.0), 3.5)
    circ(ctx, 98, -122, 4.5)
    ctx.set_source_rgb(*INK)
    ctx.fill()
    poly(ctx, [(70, -140), (60, -170), (90, -150)])
    ink_fill(ctx, "pink", 3.5)
    ctx.move_to(-85, -110)
    ctx.curve_to(-110, -130, -95, -90, -115, -100)
    stroke(ctx, 4)


def p_cow(ctx, p, t):
    _animal_body(ctx, "white", 120, 150, t=t, walk=p.get("walk"))
    for (dx, dy, r) in ((-40, -160, 26), (30, -140, 22)):
        circ(ctx, dx, dy, r)
        ink_fill(ctx, INK, 0)
    rrect(ctx, 100, -210, 80, 95, 30)
    ink_fill(ctx, "white", OUTLINE)
    rrect(ctx, 140, -150, 52, 40, 16)
    ink_fill(ctx, "pink", 3.5)
    circ(ctx, 130, -180, 5)
    ctx.set_source_rgb(*INK)
    ctx.fill()
    line(ctx, 110, -205, 95, -235, 6)
    line(ctx, 160, -208, 172, -238, 6)


def p_sheep(ctx, p, t):
    for k, lx in enumerate((-50, -25, 30, 55)):
        line(ctx, lx, -40, lx, 0, 9)
    for (dx, dy) in ((-50, -90), (-10, -110), (35, -95), (-25, -70), (20, -70), (55, -75)):
        circ(ctx, dx, dy, 38)
    ink_fill(ctx, "white", OUTLINE)
    ctx.save()
    ctx.translate(90, -105)
    ctx.scale(0.8, 1)
    circ(ctx, 0, 0, 30)
    ctx.restore()
    ink_fill(ctx, "darkgrey", OUTLINE)
    circ(ctx, 98, -112, 4)
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill()


def p_chicken(ctx, p, t):
    peck = max(0, math.sin(t * 3)) ** 4 if p.get("peck", True) else 0
    line(ctx, -8, -20, -10, 0, 5, "orange")
    line(ctx, 8, -20, 10, 0, 5, "orange")
    ctx.save()
    ctx.translate(0, -45)
    ctx.scale(1.2, 0.9)
    circ(ctx, 0, 0, 30)
    ctx.restore()
    ink_fill(ctx, "white", OUTLINE)
    hx, hy = 32 + 12 * peck, -78 + 40 * peck
    circ(ctx, hx, hy, 17)
    ink_fill(ctx, "white", OUTLINE)
    poly(ctx, [(hx + 14, hy - 4), (hx + 30, hy + 2), (hx + 14, hy + 8)])
    ink_fill(ctx, "orange", 3)
    circ(ctx, hx - 2, hy - 18, 8)
    ink_fill(ctx, "red", 3)
    circ(ctx, hx + 4, hy - 3, 3)
    ctx.set_source_rgb(*INK)
    ctx.fill()


def p_rat(ctx, p, t):
    sc = p.get("size", 1.0)
    ctx.save()
    ctx.scale(sc, sc)
    run = p.get("walk", False)
    ctx.save()
    ctx.translate(0, -26)
    ctx.scale(1.7, 1)
    circ(ctx, 0, 0, 24)
    ctx.restore()
    ink_fill(ctx, "grey", OUTLINE)
    circ(ctx, 42, -34, 16)
    ink_fill(ctx, "grey", OUTLINE)
    circ(ctx, 34, -50, 10)
    ink_fill(ctx, "pink", 3)
    circ(ctx, 50, -38, 3.5)
    ctx.set_source_rgb(*INK)
    ctx.fill()
    ctx.move_to(-40, -24)
    ctx.curve_to(-70, -30 + 8 * math.sin(t * 8), -80, 0, -110, -10)
    stroke(ctx, 4, "pink")
    for k, lx in enumerate((-20, 20)):
        sw = 8 * math.sin(t * 14 + k * 3) if run else 0
        line(ctx, lx, -8, lx + sw, 0, 5)
    ctx.restore()


def p_fleas(ctx, p, t):
    r = _rng(p.get("seed", 1))
    for i in range(p.get("n", 7)):
        k = (t * 1.6 + r.random()) % 1.0
        x = (r.random() - 0.5) * 160 + 20 * math.sin(t * 5 + i)
        y = -60 - 120 * math.sin(k * math.pi) - r.random() * 120
        circ(ctx, x, y, 5)
        ctx.set_source_rgb(*c("brown"))
        ctx.fill()


def p_hut(ctx, p, t):
    hut(ctx, 0, 0, 1.0, p, t, smoke_=p.get("smoke", True))


def p_church(ctx, p, t):
    church(ctx, 0, 0, 1.0)


def p_castle(ctx, p, t):
    castle(ctx, 0, 0, 1.0)


def p_tree(ctx, p, t):
    tree(ctx, 0, 0, 1.0, p, t, p.get("seed", 0))


def p_fire(ctx, p, t):
    fire(ctx, 0, 0, 1.0, t)


def p_cloud(ctx, p, t):
    cloud(ctx, 20 * math.sin(t * 0.4), 0, 1.0, color=p.get("color", "white"))
    if p.get("rain"):
        for i in range(10):
            y = (t * 500 + i * 37) % 200
            line(ctx, -90 + i * 20, 30 + y, -94 + i * 20, 52 + y, 3, (0.4, 0.6, 0.9))


def p_sign(ctx, p, t):
    txt = p.get("text", "")
    w = p.get("w", 360)
    h = p.get("h", 150)
    sw = math.sin(t * 2) * 0.02 if p.get("swing", False) else 0
    ctx.rotate(sw)
    if p.get("post", True):
        line(ctx, 0, 0, 0, -h - 60, 14, "wood")
    rrect(ctx, -w / 2, -h - 120, w, h, 10)
    ink_fill(ctx, p.get("color", "parchment"), OUTLINE)
    write_block(ctx, txt, 0, -h / 2 - 120, p.get("size", 50), w - 40, INK, MARKER)


def p_board(ctx, p, t):
    """Free-standing text card (no post), centred on (x, y)."""
    txt = p.get("text", "")
    w, h = p.get("w", 520), p.get("h", 200)
    rrect(ctx, -w / 2, -h / 2, w, h, 16)
    ink_fill(ctx, p.get("color", "white"), OUTLINE)
    write_block(ctx, txt, 0, 0, p.get("size", 56), w - 50, c(p.get("text_color", INK)), p.get("font", MARKER))


def p_arrow(ctx, p, t):
    """Arrow from (0,0) towards (dx, dy) (pixels), with a wiggle."""
    dx, dy = p.get("dx", 200), p.get("dy", 0)
    grow = clamp(p.get("_age", 1) / 0.35)
    ex, ey = dx * grow, dy * grow
    bend = p.get("bend", 0.25)
    mx, my = ex / 2 - ey * bend, ey / 2 + ex * bend
    ctx.move_to(0, 0)
    ctx.curve_to(mx, my, mx, my, ex, ey)
    stroke(ctx, p.get("width", 10), p.get("color", "red"))
    a = math.atan2(ey - my, ex - mx)
    L = 34
    poly(ctx, [(ex + math.cos(a) * 8, ey + math.sin(a) * 8), (ex - math.cos(a - 0.5) * L, ey - math.sin(a - 0.5) * L),
               (ex - math.cos(a + 0.5) * L, ey - math.sin(a + 0.5) * L)])
    ink_fill(ctx, p.get("color", "red"), 0)


def p_coins(ctx, p, t):
    n = p.get("n", 6)
    for i in range(n):
        row = 0
        k = i
        while k > row:
            k -= row + 1
            row += 1
    pile = p.get("pile", n)
    for i in range(pile):
        x = (i % 5) * 30 - 60 + (i // 5) * 15
        y = -(i // 5) * 18
        ctx.save()
        ctx.translate(x, y - 10)
        ctx.scale(1, 0.4)
        circ(ctx, 0, 0, 24)
        ctx.restore()
        ink_fill(ctx, "gold", 3.5)


def p_coin(ctx, p, t):
    sp = math.cos(t * 4) if p.get("spin", True) else 1
    ctx.save()
    ctx.translate(0, -40)
    ctx.scale(max(0.1, abs(sp)), 1)
    circ(ctx, 0, 0, 40)
    ink_fill(ctx, "gold", OUTLINE)
    if abs(sp) > 0.4:
        write(ctx, p.get("text", "$"), 0, 2, 44, shade("gold", 0.4), MARKER)
    ctx.restore()


def p_sack(ctx, p, t):
    ctx.move_to(-20, -150)
    ctx.curve_to(-90, -110, -90, 0, 0, 0)
    ctx.curve_to(90, 0, 90, -110, 20, -150)
    ctx.close_path()
    ink_fill(ctx, p.get("color", "tan"), OUTLINE)
    line(ctx, -26, -142, 26, -142, 7, "brown")
    if p.get("label"):
        write(ctx, p["label"], 0, -65, 40, INK, MARKER)


def p_barrel(ctx, p, t):
    ctx.move_to(-50, 0)
    ctx.curve_to(-70, -60, -70, -100, -50, -150)
    ctx.line_to(50, -150)
    ctx.curve_to(70, -100, 70, -60, 50, 0)
    ctx.close_path()
    ink_fill(ctx, "wood", OUTLINE)
    for y in (-35, -115):
        line(ctx, -62, y, 62, y, 6, "darkgrey")


def p_table(ctx, p, t):
    w = p.get("w", 360)
    rrect(ctx, -w / 2, -110, w, 22, 5)
    ink_fill(ctx, "wood", OUTLINE)
    for x in (-w / 2 + 25, w / 2 - 25):
        line(ctx, x, -90, x, 0, 12, "darkwood")
    for i, it in enumerate(p.get("items", [])):
        ctx.save()
        n = len(p.get("items", []))
        ctx.translate((i - (n - 1) / 2) * (w / max(n, 1)) * 0.8, -112)
        draw_prop(ctx, {"type": it, "x": 0, "y": 0, "scale": p.get("item_scale", 0.6)}, t, 10.0, absolute=False)
        ctx.restore()


def p_stool(ctx, p, t):
    rrect(ctx, -45, -72, 90, 16, 5)
    ink_fill(ctx, "wood", OUTLINE)
    line(ctx, -32, -60, -40, 0, 9, "darkwood")
    line(ctx, 32, -60, 40, 0, 9, "darkwood")


def p_bed(ctx, p, t):
    rrect(ctx, -170, -60, 340, 50, 18)
    ink_fill(ctx, "thatch", OUTLINE)
    for k in range(-4, 5):
        line(ctx, k * 36, -56, k * 36 + 12, -16, 3, shade("thatch", 0.3))


def p_pot(ctx, p, t):
    ctx.move_to(-70, -110)
    ctx.curve_to(-80, 10, 80, 10, 70, -110)
    ctx.close_path()
    ink_fill(ctx, "darkgrey", OUTLINE)
    ctx.save()
    ctx.translate(0, -110)
    ctx.scale(1, 0.25)
    circ(ctx, 0, 0, 72)
    ctx.restore()
    ink_fill(ctx, p.get("soup", (0.62, 0.55, 0.35)), OUTLINE)
    if p.get("steam", True):
        smoke(ctx, 0, -130, t, 0.6, (0.85, 0.85, 0.88))


def p_well(ctx, p, t):
    rrect(ctx, -90, -110, 180, 110, 8)
    ink_fill(ctx, "stone", OUTLINE)
    for x in (-80, 80):
        line(ctx, x, -110, x, -260, 10, "wood")
    poly(ctx, [(-120, -250), (0, -320), (120, -250)])
    ink_fill(ctx, "thatch", OUTLINE)
    line(ctx, 0, -250, 0, -160, 3)
    p_bucket(ctx, {}, t, dy=-120)


def p_bucket(ctx, p, t, dy=0):
    poly(ctx, [(-28, dy - 50), (28, dy - 50), (22, dy), (-22, dy)])
    ink_fill(ctx, "wood", 4)


def p_cart(ctx, p, t):
    rrect(ctx, -170, -150, 340, 80, 6)
    ink_fill(ctx, "wood", OUTLINE)
    spin = t * (2.5 if p.get("moving") else 0)
    for x in (-100, 100):
        circ(ctx, x, -50, 50)
        ink_fill(ctx, "darkwood", OUTLINE)
        for k in range(4):
            a = spin + k * math.pi / 4
            line(ctx, x - math.cos(a) * 42, -50 - math.sin(a) * 42, x + math.cos(a) * 42, -50 + math.sin(a) * 42, 4)
    line(ctx, 170, -110, 290, -90, 9, "wood")
    for i, it in enumerate(p.get("load", [])):
        ctx.save()
        ctx.translate(-110 + i * 80, -150)
        draw_prop(ctx, {"type": it, "x": 0, "y": 0, "scale": 0.5}, t, 10.0, absolute=False)
        ctx.restore()


def p_grave(ctx, p, t):
    ctx.move_to(-60, 0)
    ctx.line_to(-60, -130)
    ctx.arc(0, -130, 60, math.pi, 2 * math.pi)
    ctx.line_to(60, 0)
    ctx.close_path()
    ink_fill(ctx, "stone", OUTLINE)
    write(ctx, p.get("text", "RIP"), 0, -120, 40, INK, MARKER)
    ctx.save()
    ctx.translate(0, 4)
    ctx.scale(1, 0.25)
    circ(ctx, 0, 0, 120)
    ctx.restore()
    ink_fill(ctx, "dirt", 3)


def p_cross(ctx, p, t):
    line(ctx, 0, 0, 0, -160, 16, "wood")
    line(ctx, -50, -115, 50, -115, 16, "wood")


def p_skull(ctx, p, t):
    circ(ctx, 0, -60, 46)
    ink_fill(ctx, "white", OUTLINE)
    rrect(ctx, -26, -30, 52, 32, 8)
    ink_fill(ctx, "white", OUTLINE)
    for x in (-17, 17):
        circ(ctx, x, -62, 12)
        ctx.set_source_rgb(*INK)
        ctx.fill()


def p_bubble(ctx, p, t):
    """Speech / thought / shout bubble; (x, y) = tail tip. text grows in."""
    kind = p.get("kind", "speech")
    txt = p.get("text", "")
    size = p.get("size", 54)
    w = p.get("w", 520)
    from .style import wrap
    lines = wrap(ctx, txt, size, w - 60, HAND)
    h = max(110, len(lines) * size * 1.12 + 50)
    side = p.get("side", 1)          # bubble to the right (1) or left (-1) of the tail
    bx, by = side * (w / 2 - 60), -h / 2 - 70
    age = p.get("_age", 10)
    k = ease_back(clamp(age / 0.3))
    ctx.save()
    ctx.scale(k, k)
    if kind == "thought":
        for i, r in enumerate((10, 16, 22)):
            circ(ctx, side * (10 + i * 22), -15 - i * 22, r)
            ink_fill(ctx, "white", OUTLINE)
        ctx.save()
        ctx.translate(bx, by)
        n = 12
        for i in range(n):
            a = i * TAU / n
            circ(ctx, math.cos(a) * w / 2 * 0.92, math.sin(a) * h / 2 * 0.92, 48)
        ink_fill(ctx, "white", OUTLINE)
        ctx.scale(w / 2, h / 2)
        circ(ctx, 0, 0, 1)
        ctx.restore()
        ctx.set_source_rgb(1, 1, 1)
        ctx.fill()
    else:
        rrect(ctx, bx - w / 2, by - h / 2, w, h, 40 if kind != "shout" else 6)
        if kind == "shout":
            ink_fill(ctx, "yellow", OUTLINE * 1.2)
        else:
            ink_fill(ctx, "white", OUTLINE)
        poly(ctx, [(0, 0), (side * 30, by + h / 2 - 4), (side * 90, by + h / 2 - 4)])
        ink_fill(ctx, "yellow" if kind == "shout" else "white", 0)
        ctx.move_to(side * 30, by + h / 2)
        ctx.line_to(0, 0)
        ctx.line_to(side * 90, by + h / 2)
        stroke(ctx, OUTLINE)
    for i, ln in enumerate(lines):
        write(ctx, ln, bx, by - (len(lines) - 1) * size * 0.56 + i * size * 1.12, size, INK, HAND)
    ctx.restore()


def p_icon(ctx, p, t):
    """Small pictograms: ! ? z heart check cross stink sparkle money sweat."""
    kind = p.get("icon", "!")
    if kind in ("!", "?"):
        bob = 6 * math.sin(t * 5)
        write(ctx, kind, 0, -40 + bob, p.get("size", 120), p.get("color", "red"), MARKER, outline=6)
    elif kind == "z":
        for i in range(3):
            k = (t * 0.6 + i / 3) % 1.0
            write(ctx, "z", 30 * k + i * 6, -60 - 140 * k, 40 + 30 * k, INK, MARKER, alpha=1 - k)
    elif kind == "heart":
        s = 1 + 0.1 * math.sin(t * 6)
        ctx.save()
        ctx.scale(s, s)
        ctx.move_to(0, -10)
        ctx.curve_to(-60, -70, -20, -110, 0, -70)
        ctx.curve_to(20, -110, 60, -70, 0, -10)
        ctx.restore()
        ink_fill(ctx, "red", OUTLINE)
    elif kind == "check":
        circ(ctx, 0, -60, 60)
        ink_fill(ctx, "green", OUTLINE)
        poly(ctx, [(-28, -60), (-8, -38), (30, -84)], close=False)
        stroke(ctx, 12, "white")
    elif kind == "x":
        circ(ctx, 0, -60, 60)
        ink_fill(ctx, "red", OUTLINE)
        line(ctx, -25, -85, 25, -35, 12, "white")
        line(ctx, -25, -35, 25, -85, 12, "white")
    elif kind == "stink":
        for i in range(3):
            ctx.move_to(-40 + i * 40, 0)
            for k in range(6):
                ctx.line_to(-40 + i * 40 + 12 * math.sin(t * 4 + k + i), -k * 25)
            stroke(ctx, 6, (0.5, 0.7, 0.3), 0.85)
    elif kind == "sparkle":
        for i in range(4):
            a = i * TAU / 4 + t
            sx, sy = math.cos(a) * 60, -60 + math.sin(a) * 60
            s = 0.6 + 0.4 * math.sin(t * 6 + i)
            poly(ctx, [(sx, sy - 22 * s), (sx + 6 * s, sy), (sx, sy + 22 * s), (sx - 6 * s, sy)])
            ink_fill(ctx, "yellow", 3)
    elif kind == "anger":
        for i in range(4):
            a = i * math.pi / 2 + math.pi / 4
            ctx.move_to(math.cos(a) * 10, -40 + math.sin(a) * 10)
            ctx.line_to(math.cos(a) * 30, -40 + math.sin(a) * 30)
        stroke(ctx, 7, "red")


def p_crowd(ctx, p, t):
    """Rows of tiny background stickmen (population, armies, congregations)."""
    from .rig import ACTIONS, Look, Placement, Stickman
    n, cols_ = p.get("n", 12), p.get("cols", 6)
    gap, row_gap = p.get("gap", 90), p.get("row_gap", 70)
    action = p.get("action", "idle")
    hl = set(p.get("highlight", []))
    for i in range(n):
        r_, c_ = divmod(i, cols_)
        x = (c_ - (cols_ - 1) / 2) * gap + (r_ % 2) * gap * 0.3
        y = -r_ * row_gap
        col_ = c(p.get("color", (0.45, 0.45, 0.48))) if i not in hl else c(p.get("highlight_color", "red"))
        look = Look(color=col_, seed=i, hat=p.get("hat"), outfit=p.get("outfit"),
                    outfit_color=p.get("outfit_color", "brown"))
        pose = ACTIONS.get(action, ACTIONS["idle"])(t + i * 0.37, 5, {})
        Stickman(look).draw(ctx, pose, Placement(x, y, p.get("fig_scale", 0.35), 1 if (i % 3) else -1, "neutral"), t + i)


def p_window_light(ctx, p, t):
    pass


def p_scroll(ctx, p, t):
    w, h = p.get("w", 520), p.get("h", 620)
    unroll = ease_out(clamp(p.get("_age", 10) / 0.5))
    hh = h * unroll
    rrect(ctx, -w / 2, -hh, w, hh, 6)
    ink_fill(ctx, "parchment", OUTLINE)
    for y in (-hh, 0):
        rrect(ctx, -w / 2 - 25, y - 18, w + 50, 36, 18)
        ink_fill(ctx, (0.85, 0.75, 0.55), OUTLINE)
    if unroll > 0.9:
        items = p.get("lines", [])
        for i, ln in enumerate(items):
            write(ctx, ln, -w / 2 + 40, -hh + 70 + i * p.get("size", 50) * 1.25, p.get("size", 50), INK, HAND,
                  align="left", max_w=w - 70)


def p_calendar(ctx, p, t):
    w, h = 300, 320
    rrect(ctx, -w / 2, -h, w, h, 14)
    ink_fill(ctx, "white", OUTLINE)
    rrect(ctx, -w / 2, -h, w, 90, 14)
    ink_fill(ctx, "red", OUTLINE)
    write(ctx, p.get("month", "MARCH"), 0, -h + 46, 52, "white", MARKER, max_w=w - 30)
    write(ctx, str(p.get("day", "")), 0, -h / 2 + 30, 120, INK, MARKER)


def p_hourglass(ctx, p, t):
    k = (t / p.get("period", 6)) % 1.0
    rrect(ctx, -70, -250, 140, 20, 6)
    ink_fill(ctx, "wood", OUTLINE)
    rrect(ctx, -70, -20, 140, 20, 6)
    ink_fill(ctx, "wood", OUTLINE)
    poly(ctx, [(-55, -230), (55, -230), (6, -125), (55, -20), (-55, -20), (-6, -125)])
    ink_fill(ctx, (0.85, 0.93, 0.98), OUTLINE)
    top = 1 - k
    poly(ctx, [(-45 * top, -125 - 95 * top), (45 * top, -125 - 95 * top), (4, -128), (-4, -128)])
    ink_fill(ctx, "wheat", 0)
    poly(ctx, [(-50, -24), (50, -24), (10 + 30 * (1 - k), -24 - 90 * k), (-10 - 30 * (1 - k), -24 - 90 * k)])
    ink_fill(ctx, "wheat", 0)


def p_bell(ctx, p, t):
    sw = 0.35 * math.sin(t * 6) if p.get("ring", True) else 0
    ctx.rotate(sw)
    ctx.move_to(-70, 0)
    ctx.curve_to(-60, -40, -50, -140, 0, -140)
    ctx.curve_to(50, -140, 60, -40, 70, 0)
    ctx.close_path()
    ink_fill(ctx, "gold", OUTLINE)
    circ(ctx, 0, 6, 14)
    ink_fill(ctx, "darkgrey", 3)


def p_scale(ctx, p, t):
    tilt = p.get("tilt", 0.2) * (0.8 + 0.2 * math.sin(t * 2))
    line(ctx, 0, 0, 0, -260, 10, "darkwood")
    line(ctx, -60, 0, 60, 0, 12, "darkwood")
    ctx.save()
    ctx.translate(0, -260)
    ctx.rotate(tilt)
    line(ctx, -180, 0, 180, 0, 8, "gold")
    for x, lab in ((-180, p.get("left", "")), (180, p.get("right", ""))):
        ctx.save()
        ctx.translate(x, 0)
        ctx.rotate(-tilt)
        line(ctx, 0, 0, -50, 100, 3)
        line(ctx, 0, 0, 50, 100, 3)
        ctx.arc(0, 100, 60, 0, math.pi)
        ctx.close_path()
        ink_fill(ctx, "gold", 4)
        if lab:
            write(ctx, lab, 0, 150, 40, INK, MARKER, outline=4)
        ctx.restore()
    ctx.restore()


def p_stocks(ctx, p, t):
    """The pillory/stocks (medieval public punishment)."""
    for x in (-110, 110):
        line(ctx, x, 0, x, -200, 16, "darkwood")
    rrect(ctx, -160, -200, 320, 60, 6)
    ink_fill(ctx, "wood", OUTLINE)
    for x in (-60, 60):
        circ(ctx, x, -170, 14)
        ink_fill(ctx, INK, 0)


def p_plate(ctx, p, t):
    ctx.save()
    ctx.scale(1, 0.35)
    circ(ctx, 0, -20, 80)
    ctx.restore()
    ink_fill(ctx, "white", OUTLINE)
    food = p.get("food", "porridge")
    if food == "porridge":
        ctx.save()
        ctx.translate(0, -18)
        ctx.scale(1, 0.4)
        circ(ctx, 0, 0, 55)
        ctx.restore()
        ink_fill(ctx, (0.85, 0.8, 0.62), 3)
    elif food == "meat":
        ctx.save()
        ctx.translate(0, -30)
        ctx.scale(1.3, 0.8)
        circ(ctx, 0, 0, 38)
        ctx.restore()
        ink_fill(ctx, (0.7, 0.35, 0.25), 3.5)
        line(ctx, 40, -35, 75, -50, 10, "white")


def p_small(ctx, p, t):
    """Any held item drawn on its own (mug, bread, coin, bag, book, scroll, apple, egg, letter...)."""
    from .rig import draw_item
    draw_item(ctx, p.get("item", "bread"), (0, 0), 0.0, t)


def p_privy(ctx, p, t):
    rrect(ctx, -70, -240, 140, 240, 4)
    ink_fill(ctx, "wood", OUTLINE)
    poly(ctx, [(-85, -240), (0, -300), (85, -240)])
    ink_fill(ctx, "darkwood", OUTLINE)
    ctx.save()
    ctx.translate(0, -190)
    ctx.scale(0.6, 1)
    ctx.arc(0, 0, 18, 0, TAU)
    ctx.restore()
    ink_fill(ctx, INK, 0)


def p_river(ctx, p, t):
    w = p.get("w", 900)
    ctx.save()
    ctx.scale(1, 0.22)
    rrect(ctx, -w / 2, -160, w, 260, 130)
    ctx.restore()
    ink_fill(ctx, "water", OUTLINE)
    for i in range(6):
        x = -w / 2 + 80 + ((i * 140 + t * 40) % (w - 160))
        line(ctx, x, -10, x + 50, -10, 4, "white", 0.8)


def p_mill(ctx, p, t):
    """Windmill (the lord's mill)."""
    poly(ctx, [(-90, 0), (90, 0), (60, -300), (-60, -300)])
    ink_fill(ctx, (0.92, 0.86, 0.72), OUTLINE)
    poly(ctx, [(-75, -300), (0, -380), (75, -300)])
    ink_fill(ctx, "thatch", OUTLINE)
    ctx.save()
    ctx.translate(0, -300)
    ctx.rotate(t * 0.8)
    for k in range(4):
        ctx.save()
        ctx.rotate(k * math.pi / 2)
        rrect(ctx, -18, -230, 36, 210, 4)
        ink_fill(ctx, "white", OUTLINE)
        ctx.restore()
    circ(ctx, 0, 0, 18)
    ink_fill(ctx, "darkwood", OUTLINE)
    ctx.restore()


def p_dog(ctx, p, t):
    wag = math.sin(t * 12) * 0.5
    _animal_body(ctx, "tan", 70, 80, t=t, walk=p.get("walk"))
    circ(ctx, 75, -100, 30)
    ink_fill(ctx, "tan", OUTLINE)
    ctx.save()
    ctx.translate(55, -120)
    ctx.scale(0.5, 1)
    circ(ctx, 0, 0, 20)
    ctx.restore()
    ink_fill(ctx, "brown", 3.5)
    circ(ctx, 86, -106, 4)
    ctx.set_source_rgb(*INK)
    ctx.fill()
    ctx.save()
    ctx.translate(-70, -85)
    ctx.rotate(-0.8 + wag)
    line(ctx, 0, 0, 0, -45, 8)
    ctx.restore()


def p_horse(ctx, p, t):
    _animal_body(ctx, p.get("color", "brown"), 130, 175, t=t, walk=p.get("walk"))
    poly(ctx, [(95, -190), (150, -300), (195, -280), (140, -170)])
    ink_fill(ctx, p.get("color", "brown"), OUTLINE)
    circ(ctx, 168, -278, 5)
    ctx.set_source_rgb(*INK)
    ctx.fill()


def p_germ(ctx, p, t):
    r = 40
    ctx.save()
    ctx.rotate(t * 0.8)
    for k in range(10):
        a = k * TAU / 10
        line(ctx, math.cos(a) * r, -r + math.sin(a) * r, math.cos(a) * (r + 22), -r + math.sin(a) * (r + 22), 6,
             p.get("color", "lime"))
    ctx.restore()
    circ(ctx, 0, -r, r)
    ink_fill(ctx, p.get("color", "lime"), OUTLINE)
    for x in (-12, 12):
        circ(ctx, x, -r - 6, 6)
        ctx.set_source_rgb(*INK)
        ctx.fill()
    ctx.move_to(-14, -r + 14)
    ctx.curve_to(-6, -r + 6, 6, -r + 22, 14, -r + 12)
    stroke(ctx, 4)


def p_plough(ctx, p, t):
    """Heavy plough pulled by two oxen (the team was often shared by several families)."""
    k = math.sin(t * 2.2)
    for dx in (0, 70):
        ctx.save()
        ctx.translate(260 + dx, 0)
        _animal_body(ctx, (0.62, 0.45, 0.3) if dx else (0.72, 0.55, 0.38), 110, 140, t=t + dx, walk=True)
        rrect(ctx, 90, -190, 70, 80, 26)
        ink_fill(ctx, (0.62, 0.45, 0.3) if dx else (0.72, 0.55, 0.38), OUTLINE)
        line(ctx, 100, -185, 85, -215, 6, "white")
        line(ctx, 150, -185, 165, -215, 6, "white")
        ctx.restore()
    line(ctx, 0, -40, 300, -150, 9, "wood")
    poly(ctx, [(-40, 0), (40, 0), (20, -50), (-20, -50)])
    ink_fill(ctx, "darkgrey", OUTLINE)
    line(ctx, -10, -40, -90, -150 + 4 * k, 9, "wood")
    r = _rng(3)
    for i in range(8):   # clods of earth
        x = -60 - i * 45 + 10 * r.random()
        circ(ctx, x, -6 - 6 * r.random(), 10 + 6 * r.random())
        ink_fill(ctx, "dirt", 3)


def p_ship(ctx, p, t):
    bob = 6 * math.sin(t * 1.5)
    ctx.translate(0, bob)
    ctx.rotate(0.03 * math.sin(t * 1.2))
    ctx.move_to(-260, -120)
    ctx.line_to(260, -120)
    ctx.line_to(200, 0)
    ctx.line_to(-200, 0)
    ctx.close_path()
    ink_fill(ctx, "wood", OUTLINE)
    line(ctx, -230, -80, 230, -80, 4, "darkwood")
    line(ctx, 0, -120, 0, -520, 12, "darkwood")
    ctx.move_to(-150, -480)
    ctx.curve_to(-60, -440 + 10 * math.sin(t), 60, -440 + 10 * math.sin(t), 150, -480)
    ctx.line_to(150, -190)
    ctx.curve_to(60, -160, -60, -160, -150, -190)
    ctx.close_path()
    ink_fill(ctx, p.get("sail", (0.95, 0.92, 0.85)), OUTLINE)
    if p.get("cross", True):
        line(ctx, 0, -420, 0, -250, 14, "red")
        line(ctx, -70, -335, 70, -335, 14, "red")
    poly(ctx, [(0, -520), (70, -505), (0, -490)])
    ink_fill(ctx, "red", 3)


def p_sea(ctx, p, t):
    w = p.get("w", 2200)
    ctx.rectangle(-w / 2, -40, w, 400)
    ctx.set_source_rgb(*c("water"))
    ctx.fill()
    for row in range(4):
        y = -40 + row * 60
        ctx.move_to(-w / 2, y)
        for x in range(int(-w / 2), int(w / 2) + 1, 80):
            ctx.curve_to(x + 20, y - 14 + 4 * math.sin(t * 2 + row), x + 60, y + 14, x + 80, y)
        stroke(ctx, 4, "white", 0.7)


def p_tub(ctx, p, t):
    ctx.move_to(-140, -150)
    ctx.line_to(140, -150)
    ctx.line_to(115, 0)
    ctx.line_to(-115, 0)
    ctx.close_path()
    ink_fill(ctx, "wood", OUTLINE)
    for x in (-60, 0, 60):
        line(ctx, x, -150, x * 0.85, 0, 3, "darkwood")
    for y in (-110, -35):
        line(ctx, -132, y, 132, y, 6, "darkgrey")
    ctx.save()
    ctx.translate(0, -150)
    ctx.scale(1, 0.22)
    circ(ctx, 0, 0, 138)
    ctx.restore()
    ink_fill(ctx, "water", 3)
    if p.get("steam", True):
        smoke(ctx, -30, -180, t, 0.6, (0.9, 0.9, 0.95))


def p_strips(ctx, p, t):
    """Bird's-eye open field divided into long strips (one highlighted = yours)."""
    w, h, n = p.get("w", 1300), p.get("h", 560), p.get("n", 12)
    mine = set(p.get("mine", [3, 8]))
    cols = [(0.6, 0.76, 0.32), (0.82, 0.72, 0.38), (0.5, 0.66, 0.3), (0.72, 0.6, 0.36)]
    sw = w / n
    for i in range(n):
        x = -w / 2 + i * sw
        rrect(ctx, x, -h, sw, h, 4)
        hl = i in mine and p.get("_age", 9) > p.get("reveal", 0.5)
        ink_fill(ctx, "yellow" if hl else cols[i % 4], 3)
        for k in range(1, 8):
            line(ctx, x + 10, -h + k * h / 8, x + sw - 10, -h + k * h / 8, 2, (0.3, 0.3, 0.2), 0.25)
    rrect(ctx, -w / 2, -h, w, h, 6)
    ink_fill(ctx, None, OUTLINE)


PROPS = {
    "pig": p_pig, "cow": p_cow, "sheep": p_sheep, "chicken": p_chicken, "rat": p_rat, "fleas": p_fleas,
    "dog": p_dog, "horse": p_horse, "hut": p_hut, "church": p_church, "castle": p_castle, "tree": p_tree,
    "fire": p_fire, "cloud": p_cloud, "sign": p_sign, "board": p_board, "arrow": p_arrow, "coins": p_coins,
    "coin": p_coin, "sack": p_sack, "barrel": p_barrel, "table": p_table, "stool": p_stool, "bed": p_bed,
    "pot": p_pot, "well": p_well, "bucket": p_bucket, "cart": p_cart, "grave": p_grave, "cross": p_cross,
    "skull": p_skull, "bubble": p_bubble, "icon": p_icon, "crowd": p_crowd, "scroll": p_scroll,
    "calendar": p_calendar, "hourglass": p_hourglass, "bell": p_bell, "scale": p_scale, "stocks": p_stocks,
    "plate": p_plate, "item": p_small, "plough": p_plough, "ship": p_ship, "sea": p_sea, "tub": p_tub,
    "strips": p_strips, "privy": p_privy, "river": p_river, "mill": p_mill, "germ": p_germ,
}


def draw_prop(ctx, p, t, age, absolute=True):
    """Draws a prop at (x, y) with its entrance and loop animations."""
    f = PROPS.get(p.get("type"))
    if f is None:
        return
    x, y = px(p.get("x", 0.5), p.get("y", GROUND)) if absolute else (p.get("x", 0), p.get("y", 0))
    s = p.get("scale", 1.0)
    alpha = p.get("alpha", 1.0)
    en = p.get("enter", "pop")
    d = 0.35
    if en == "pop":
        s *= ease_back(clamp(age / d)) if age < d else 1.0
    elif en == "drop":
        y -= (1 - ease_out(clamp(age / 0.45))) * 700 if age < 0.45 else 0
    elif en == "rise":
        y += (1 - ease_out(clamp(age / 0.45))) * 500 if age < 0.45 else 0
    elif en == "fade":
        alpha *= clamp(age / 0.4)
    elif en == "slide_left":
        x += (1 - ease_out(clamp(age / 0.5))) * 1200
    elif en == "slide_right":
        x -= (1 - ease_out(clamp(age / 0.5))) * 1200
    elif en == "grow":
        s *= ease_io(clamp(age / 0.6))
    # movement along a path [[t, x, y], ...]
    if p.get("move"):
        pts = [(float(a), *px(b, cc)) for a, b, cc in p["move"]]
        if age <= pts[0][0]:
            x, y = pts[0][1], pts[0][2]
        else:
            x, y = pts[-1][1], pts[-1][2]
            for (t0, x0, y0), (t1, x1, y1) in zip(pts, pts[1:]):
                if t0 <= age <= t1:
                    e = ease_io((age - t0) / max(1e-3, t1 - t0))
                    x, y = lerp(x0, x1, e), lerp(y0, y1, e)
                    break
    loop = p.get("loop")
    rot = p.get("rot", 0.0)
    if loop == "bob":
        y += 8 * math.sin(t * 3 + x)
    elif loop == "sway":
        rot += 0.06 * math.sin(t * 2.5)
    elif loop == "pulse":
        s *= 1 + 0.06 * math.sin(t * 6)
    elif loop == "shake":
        x += 4 * noise1(t * 30, 3)
    if s <= 0.01 or alpha <= 0.01:
        return
    ctx.save()
    ctx.translate(x, y)
    if rot:
        ctx.rotate(rot)
    ctx.scale(s * p.get("flip", 1), s)
    if alpha < 1:
        ctx.push_group()
    q = dict(p)
    q["_age"] = age
    f(ctx, q, t)
    if alpha < 1:
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(alpha)
    ctx.restore()
