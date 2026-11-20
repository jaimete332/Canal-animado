"""Era sets for the stickman channel: Rome, baths, arena, Ice Age, Egypt, ship deck, trench, factory.

Registered into world.BACKGROUNDS / world.PROPS on import (world.py imports this module at the end).
"""
from __future__ import annotations

import math

import cairo

from ..visuals.draw import clamp, ease_out
from .style import INK, OUTLINE, P, H, W, c, circ, ink_fill, line, poly, rrect, shade, stroke, tint, write, MARKER
from . import world as wd

STONE = (0.88, 0.84, 0.74)
MARBLE = (0.95, 0.93, 0.88)
TERRA = (0.80, 0.45, 0.30)


# ---------------------------------------------------------------------------------------------- pieces
def column(ctx, x, y, h, w=46, color=MARBLE):
    rrect(ctx, x - w / 2 - 10, y - 18, w + 20, 18, 3)
    ink_fill(ctx, color, OUTLINE)
    rrect(ctx, x - w / 2, y - h + 18, w, h - 36, 2)
    ink_fill(ctx, color, OUTLINE)
    for k in (-0.25, 0, 0.25):
        line(ctx, x + k * w, y - h + 26, x + k * w, y - 26, 2.5, shade(color, 0.15))
    rrect(ctx, x - w / 2 - 12, y - h, w + 24, 20, 3)
    ink_fill(ctx, color, OUTLINE)


def temple(ctx, x, y, s=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -330, -40, 660, 40, 2)
    ink_fill(ctx, MARBLE, OUTLINE / s)
    for k in range(6):
        column(ctx, -250 + k * 100, -40, 330)
    rrect(ctx, -320, -400, 640, 40, 2)
    ink_fill(ctx, MARBLE, OUTLINE / s)
    poly(ctx, [(-340, -400), (0, -540), (340, -400)])
    ink_fill(ctx, MARBLE, OUTLINE / s)
    poly(ctx, [(-260, -415), (0, -515), (260, -415)])
    ink_fill(ctx, shade(MARBLE, 0.08), 3)
    ctx.restore()


def insula(ctx, x, y, w, floors, color, roof=TERRA):
    """Roman apartment block: shops at street level, flats above."""
    fh = 120
    h = floors * fh
    rrect(ctx, x, y - h, w, h, 2)
    ink_fill(ctx, color, OUTLINE)
    for f in range(floors):
        yy = y - (f + 1) * fh
        if f == 0:
            for k in range(int(w // 120)):
                rrect(ctx, x + 20 + k * 120, y - 100, 90, 100, 4)
                ink_fill(ctx, (0.35, 0.25, 0.18), OUTLINE)
        else:
            for k in range(int(w // 90)):
                rrect(ctx, x + 22 + k * 90, yy + 30, 46, 56, 3)
                ink_fill(ctx, (0.3, 0.24, 0.2), 3.5)
        line(ctx, x, yy, x + w, yy, 3, shade(color, 0.2))
    poly(ctx, [(x - 20, y - h), (x + w / 2, y - h - 60), (x + w + 20, y - h)])
    ink_fill(ctx, roof, OUTLINE)


def pyramid(ctx, x, y, s=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    poly(ctx, [(-420, 0), (0, -360), (420, 0)])
    ink_fill(ctx, (0.93, 0.8, 0.5), OUTLINE / s)
    poly(ctx, [(0, -360), (420, 0), (120, 0)])
    ink_fill(ctx, (0.85, 0.7, 0.42), 0)
    for k in range(1, 7):
        yy = -k * 50
        hw = 420 * (1 - k * 50 / 360)
        line(ctx, -hw, yy, hw, yy, 2.5, (0.7, 0.55, 0.3), 0.7)
    poly(ctx, [(-420, 0), (0, -360), (420, 0)])
    ink_fill(ctx, None, OUTLINE / s)
    ctx.restore()


def palm(ctx, x, y, s=1.0, t=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.move_to(-12, 0)
    ctx.curve_to(-10, -120, 20, -220, 30, -300)
    ctx.line_to(48, -298)
    ctx.curve_to(38, -220, 12, -120, 14, 0)
    ctx.close_path()
    ink_fill(ctx, "wood", OUTLINE / s)
    sw = math.sin(t * 1.5) * 0.05
    for a in (-2.6, -2.0, -1.2, -0.5, 0.2):
        ctx.save()
        ctx.translate(38, -300)
        ctx.rotate(a + sw)
        ctx.move_to(0, 0)
        ctx.curve_to(60, -30, 120, -10, 160, 30)
        ctx.curve_to(110, 10, 60, 10, 0, 0)
        ctx.restore()
        ink_fill(ctx, "green", 3)
    ctx.restore()


def mountains(ctx, gy, color=(0.8, 0.85, 0.92), snow=True):
    pts = [(-50, gy), (150, gy - 330), (380, gy - 120), (620, gy - 420), (900, gy - 150), (1150, gy - 380),
           (1420, gy - 140), (1700, gy - 360), (1980, gy - 100), (1980, gy)]
    poly(ctx, pts)
    ink_fill(ctx, color, OUTLINE)
    if snow:
        for (px_, py_) in pts[1:-1]:
            if py_ < gy - 300:
                poly(ctx, [(px_ - 60, py_ + 70), (px_, py_), (px_ + 60, py_ + 70), (px_ + 20, py_ + 55), (px_ - 15, py_ + 75)])
                ink_fill(ctx, "white", 3)


def gear(ctx, x, y, r, t, speed=1.0, color="grey"):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(t * speed)
    n = max(8, int(r / 12))
    for k in range(n):
        ctx.save()
        ctx.rotate(k * 2 * math.pi / n)
        rrect(ctx, -r * 0.14, -r - 16, r * 0.28, 30, 4)
        ctx.restore()
    ink_fill(ctx, color, OUTLINE)
    circ(ctx, 0, 0, r)
    ink_fill(ctx, color, OUTLINE)
    circ(ctx, 0, 0, r * 0.3)
    ink_fill(ctx, shade(color, 0.3), 3)
    ctx.restore()


# ---------------------------------------------------------------------------------------------- backgrounds
def bg_rome(ctx, spec, t):
    """Busy Roman street: insulae, a temple, the forum."""
    gy = H * spec.get("ground_y", wd.GROUND)
    wd.sky(ctx, spec, t, gy)
    if spec.get("temple", True):
        temple(ctx, W * spec.get("temple_x", 0.78), gy - 20, spec.get("temple_scale", 0.95))
    cols = [(0.95, 0.86, 0.68), (0.92, 0.78, 0.6), (0.97, 0.9, 0.78), (0.9, 0.72, 0.55)]
    xs = spec.get("insulae", [(-40, 3), (300, 4), (640, 3)])
    for i, (x, fl) in enumerate(xs):
        insula(ctx, x, gy, 320, fl, cols[i % 4])
    ctx.rectangle(0, gy, W, H - gy)
    ctx.set_source_rgb(*c("stone"))
    ctx.fill()
    for x in range(0, W, 90):
        for y in range(int(gy) + 8, H, 45):
            rrect(ctx, x + (45 if (y // 45) % 2 else 0), y, 86, 40, 6)
            ctx.set_source_rgba(*INK, 0.18)
            ctx.set_line_width(2)
            ctx.stroke()
    line(ctx, 0, gy, W, gy, OUTLINE)
    wd.weather(ctx, spec, t)


def bg_baths(ctx, spec, t):
    gy = H * spec.get("ground_y", wd.GROUND)
    ctx.set_source_rgb(*tint("sky", 0.3))
    ctx.paint()
    for x in range(0, W + 1, 160):        # coffered vault
        for y in range(0, int(gy - 360), 120):
            rrect(ctx, x + 10, y + 10, 140, 100, 8)
            ink_fill(ctx, (0.86, 0.82, 0.72), 2.5)
    for x in (160, 560, 1360, 1760):
        column(ctx, x, gy, gy - 40, 60)
    # pool
    pool_y = gy + 40
    rrect(ctx, 0, gy, W, H - gy, 0)
    ink_fill(ctx, (0.92, 0.88, 0.8), 0)
    line(ctx, 0, gy, W, gy, OUTLINE)
    ctx.move_to(W * 0.22, pool_y)
    ctx.line_to(W * 0.78, pool_y)
    ctx.line_to(W * 0.74, H + 10)
    ctx.line_to(W * 0.26, H + 10)
    ctx.close_path()
    ink_fill(ctx, "water", OUTLINE)
    for i in range(7):
        x = W * 0.28 + ((i * 130 + t * 30) % (W * 0.44))
        line(ctx, x, pool_y + 40 + (i % 3) * 30, x + 60, pool_y + 40 + (i % 3) * 30, 4, "white", 0.8)
    wd.smoke(ctx, W * 0.4, pool_y - 10, t, 1.2, (0.95, 0.95, 0.97))
    wd.smoke(ctx, W * 0.62, pool_y - 10, t + 1.3, 1.2, (0.95, 0.95, 0.97))


def bg_arena(ctx, spec, t):
    """Inside a Roman arena / circus: tiers of spectators and a sand floor."""
    gy = H * spec.get("ground_y", wd.GROUND)
    wd.sky(ctx, {**spec, "sun": spec.get("sun", True)}, t, gy)
    for row in range(5):
        y0 = 150 + row * 85
        rrect(ctx, -20, y0, W + 40, 85, 0)
        ink_fill(ctx, shade(STONE, 0.05 * row), 3.5)
        for k in range(int(W / 46) + 1):    # tiny crowd heads
            x = k * 46 + (row % 2) * 23
            bob = 4 * math.sin(t * (3 + row) + k)
            circ(ctx, x, y0 + 30 + bob, 11)
            ink_fill(ctx, [(0.95, 0.82, 0.7), (0.85, 0.65, 0.5), "white"][(k + row) % 3], 2.5)
    rrect(ctx, -10, 575, W + 20, 70, 0)
    ink_fill(ctx, (0.75, 0.3, 0.25), OUTLINE)
    ctx.rectangle(0, 645, W, H - 645)
    ctx.set_source_rgb(0.93, 0.82, 0.58)
    ctx.fill()
    line(ctx, 0, 645, W, 645, OUTLINE)
    wd.weather(ctx, spec, t)


def bg_ice_age(ctx, spec, t):
    gy = H * spec.get("ground_y", wd.GROUND)
    wd.sky(ctx, {**spec, "time": spec.get("time", "grey")}, t, gy)
    mountains(ctx, gy - 20)
    ctx.move_to(-10, gy)
    for i in range(0, W + 61, 60):
        ctx.line_to(i, gy + 6 * math.sin(i / 70))
    ctx.line_to(W + 10, H + 10)
    ctx.line_to(-10, H + 10)
    ctx.close_path()
    ink_fill(ctx, "snow", OUTLINE)
    if spec.get("cave"):
        cx = W * spec.get("cave_x", 0.15)
        ctx.move_to(cx - 260, gy + 4)
        ctx.curve_to(cx - 250, gy - 420, cx + 250, gy - 420, cx + 260, gy + 4)
        ctx.close_path()
        ink_fill(ctx, (0.55, 0.52, 0.5), OUTLINE)
        ctx.move_to(cx - 120, gy + 4)
        ctx.curve_to(cx - 110, gy - 230, cx + 110, gy - 230, cx + 120, gy + 4)
        ctx.close_path()
        ink_fill(ctx, (0.15, 0.13, 0.12), 3)
    wd.weather(ctx, {**spec, "weather": spec.get("weather", "snow")}, t)


def bg_desert(ctx, spec, t):
    gy = H * spec.get("ground_y", wd.GROUND)
    wd.sky(ctx, {**spec, "sun_pos": spec.get("sun_pos", (0.15, 0.17))}, t, gy)
    if spec.get("pyramids", True):
        pyramid(ctx, W * 0.62, gy - 10, 0.9)
        pyramid(ctx, W * 0.86, gy - 20, 0.55)
    ctx.move_to(-10, gy)
    for i in range(0, W + 61, 60):
        ctx.line_to(i, gy + 10 * math.sin(i / 160))
    ctx.line_to(W + 10, H + 10)
    ctx.line_to(-10, H + 10)
    ctx.close_path()
    ink_fill(ctx, (0.95, 0.84, 0.58), OUTLINE)
    if spec.get("nile"):
        ctx.save()
        ctx.translate(W * 0.25, gy + 70)
        wd.p_river(ctx, {"w": 900}, t)
        ctx.restore()
    if spec.get("palms", True):
        palm(ctx, W * 0.08, gy + 10, 0.9, t)
        palm(ctx, W * 0.36, gy + 6, 0.7, t + 1)


def bg_deck(ctx, spec, t):
    """On the deck of a sailing ship at sea (pirates, sailors, Vikings with `viking: true`)."""
    gy = H * spec.get("ground_y", wd.GROUND)
    roll = math.sin(t * 0.9) * spec.get("roll", 0.015)
    wd.sky(ctx, spec, t, gy)
    ctx.save()
    ctx.translate(W / 2, gy)
    ctx.rotate(roll * 0.5)
    ctx.translate(-W / 2, -gy)
    hy = gy - 160
    for row in range(3):          # sea
        y = hy + row * 30
        ctx.move_to(-20, y)
        for x in range(-20, W + 81, 80):
            ctx.curve_to(x + 20, y - 12 + 5 * math.sin(t * 2 + row), x + 60, y + 12, x + 80, y)
        ctx.line_to(W + 80, gy)
        ctx.line_to(-20, gy)
        ctx.close_path()
        ink_fill(ctx, shade("water", 0.08 * row), 3)
    ctx.restore()
    ctx.save()
    ctx.translate(W / 2, gy)
    ctx.rotate(roll)
    ctx.translate(-W / 2, -gy)
    # mast + sail
    mx = W * spec.get("mast_x", 0.7)
    line(ctx, mx, gy, mx, 0, 26, "darkwood")
    if not spec.get("viking"):
        ctx.move_to(mx - 260, 60)
        ctx.curve_to(mx - 120, 120 + 12 * math.sin(t), mx + 120, 120 + 12 * math.sin(t), mx + 260, 60)
        ctx.line_to(mx + 240, 420)
        ctx.curve_to(mx + 100, 460, mx - 100, 460, mx - 240, 420)
        ctx.close_path()
        ink_fill(ctx, spec.get("sail", (0.95, 0.92, 0.85)), OUTLINE)
        if spec.get("pirate_flag"):
            poly(ctx, [(mx, 0), (mx + 150, 20), (mx + 150, 110), (mx, 90)])
            ink_fill(ctx, INK, 3)
            circ(ctx, mx + 75, 50, 16)
            ink_fill(ctx, "white", 0)
    else:
        rrect(ctx, mx - 240, 70, 480, 360, 6)
        ink_fill(ctx, "white", OUTLINE)
        for k in range(4):
            rrect(ctx, mx - 240 + k * 120, 70, 60, 360, 0)
            ink_fill(ctx, "red", 0)
        rrect(ctx, mx - 240, 70, 480, 360, 6)
        ink_fill(ctx, None, OUTLINE)
    # rail + deck
    rrect(ctx, -20, gy - 90, W + 40, 22, 4)
    ink_fill(ctx, "wood", OUTLINE)
    for x in range(30, W, 120):
        line(ctx, x, gy - 70, x, gy, 9, "darkwood")
    ctx.rectangle(-20, gy, W + 40, H - gy + 40)
    ctx.set_source_rgb(*c("wood"))
    ctx.fill()
    for y in range(int(gy) + 30, H + 40, 40):
        line(ctx, -20, y, W + 20, y, 2.5, "darkwood", 0.6)
    line(ctx, -20, gy, W + 20, gy, OUTLINE)
    ctx.restore()
    wd.weather(ctx, spec, t)


def bg_trench(ctx, spec, t):
    gy = H * spec.get("ground_y", wd.GROUND)
    wd.sky(ctx, {**spec, "time": spec.get("time", "grey"), "sun": False}, t, gy)
    top = gy - 420
    # back wall of the trench + sandbags + wire
    ctx.rectangle(0, top, W, gy - top)
    ctx.set_source_rgb(0.45, 0.36, 0.27)
    ctx.fill()
    for x in range(0, W, 60):
        line(ctx, x, top + 20, x, gy, 6, "darkwood", 0.7)
    for x in range(-30, W + 60, 110):
        rrect(ctx, x, top - 50, 110, 52, 22)
        ink_fill(ctx, (0.72, 0.65, 0.5), 3.5)
    for x in range(0, W, 220):
        line(ctx, x + 30, top - 50, x + 30, top - 150, 6, "darkwood")
    ctx.move_to(0, top - 110)
    for x in range(0, W + 30, 30):
        ctx.line_to(x, top - 110 + (14 if (x // 30) % 2 else -14))
    stroke(ctx, 3, "darkgrey")
    # duckboard floor + mud
    ctx.rectangle(0, gy, W, H - gy)
    ctx.set_source_rgb(0.38, 0.29, 0.21)
    ctx.fill()
    for x in range(0, W, 70):
        rrect(ctx, x + 6, gy + 20, 58, 20, 3)
        ink_fill(ctx, "wood", 3)
    line(ctx, 0, gy, W, gy, OUTLINE)
    wd.weather(ctx, {**spec, "weather": spec.get("weather", "rain")}, t)


def bg_factory(ctx, spec, t):
    gy = H * spec.get("ground_y", wd.GROUND)
    ctx.set_source_rgb(0.62, 0.58, 0.55)
    ctx.paint()
    for x in range(0, W, 180):       # brick wall
        for y in range(0, int(gy), 60):
            rrect(ctx, x + (90 if (y // 60) % 2 else 0), y, 176, 56, 3)
            ctx.set_source_rgba(0.55, 0.3, 0.25, 0.35)
            ctx.fill()
    for x in (300, 960, 1620):        # tall windows
        rrect(ctx, x - 110, 80, 220, 330, 6)
        ink_fill(ctx, (0.75, 0.78, 0.78), OUTLINE)
        line(ctx, x, 80, x, 410, 5)
        line(ctx, x - 110, 245, x + 110, 245, 5)
    # machines: belts and gears
    line(ctx, 0, 470, W, 470, 10, "darkgrey")
    for i, x in enumerate((180, 600, 1040, 1480, 1840)):
        gear(ctx, x, 470, 70 if i % 2 else 52, t, 1.4 if i % 2 else -1.9, "grey")
    rrect(ctx, 80, gy - 230, W - 160, 90, 8)
    ink_fill(ctx, "darkgrey", OUTLINE)
    for k in range(18):
        x = 120 + ((k * 98 + t * 120) % (W - 260))
        rrect(ctx, x, gy - 255, 50, 26, 4)
        ink_fill(ctx, "white", 2.5)
    ctx.rectangle(0, gy, W, H - gy)
    ctx.set_source_rgb(0.32, 0.3, 0.3)
    ctx.fill()
    line(ctx, 0, gy, W, gy, OUTLINE)
    ctx.rectangle(0, 0, W, H)
    ctx.set_source_rgba(0.25, 0.22, 0.2, 0.12 + 0.03 * math.sin(t))
    ctx.fill()


def bg_cave(ctx, spec, t):
    """Inside a cave by the fire (Stone Age)."""
    gy = H * spec.get("ground_y", wd.GROUND)
    ctx.set_source_rgb(0.25, 0.22, 0.2)
    ctx.paint()
    ctx.move_to(0, 0)
    ctx.curve_to(W * 0.3, 260, W * 0.7, 200, W, 0)
    ctx.line_to(W, gy)
    ctx.line_to(0, gy)
    ctx.close_path()
    ink_fill(ctx, (0.45, 0.4, 0.36), OUTLINE)
    if spec.get("paintings", True):   # cave paintings
        for i, (x, y) in enumerate(((520, 430), (760, 380), (1180, 420))):
            ctx.save()
            ctx.translate(x, y)
            ctx.scale(0.5, 0.5)
            ctx.set_source_rgba(0.7, 0.3, 0.15, 0.85)
            ctx.save()
            ctx.scale(1.6, 0.8)
            circ(ctx, 0, 0, 60)
            ctx.restore()
            ctx.fill()
            for lx in (-60, -20, 30, 70):
                line(ctx, lx, 30, lx, 110, 10, (0.7, 0.3, 0.15), 0.85)
            ctx.restore()
    ctx.rectangle(0, gy, W, H - gy)
    ctx.set_source_rgb(0.35, 0.3, 0.26)
    ctx.fill()
    line(ctx, 0, gy, W, gy, OUTLINE)
    if spec.get("fire", True):
        wd.fire(ctx, W * spec.get("fire_x", 0.5), gy + 10, 1.0, t)
        g = cairo.RadialGradient(W * spec.get("fire_x", 0.5), gy - 60, 40, W * spec.get("fire_x", 0.5), gy - 60, 900)
        g.add_color_stop_rgba(0, 1, 0.7, 0.3, 0.25)
        g.add_color_stop_rgba(1, 0, 0, 0, 0.35)
        ctx.set_source(g)
        ctx.paint()


# ---------------------------------------------------------------------------------------------- props
def p_column(ctx, p, t):
    column(ctx, 0, 0, p.get("h", 360), 54)


def p_temple(ctx, p, t):
    temple(ctx, 0, 0, 1.0)


def p_amphora(ctx, p, t):
    ctx.move_to(-18, -170)
    ctx.line_to(18, -170)
    ctx.curve_to(70, -130, 60, -40, 0, 0)
    ctx.curve_to(-60, -40, -70, -130, -18, -170)
    ink_fill(ctx, TERRA, OUTLINE)
    for sgn in (-1, 1):
        ctx.move_to(sgn * 16, -160)
        ctx.curve_to(sgn * 50, -165, sgn * 50, -130, sgn * 30, -120)
        stroke(ctx, 6, INK)


def p_pyramid(ctx, p, t):
    pyramid(ctx, 0, 0, 1.0)


def p_palm(ctx, p, t):
    palm(ctx, 0, 0, 1.0, t)


def p_mammoth(ctx, p, t):
    walk = p.get("walk", False)
    for k, lx in enumerate((-120, -60, 70, 130)):
        sw = 12 * math.sin(t * 3 + k * math.pi) if walk else 0
        rrect(ctx, lx - 22 + sw, -150, 44, 150, 16)
        ink_fill(ctx, (0.5, 0.36, 0.26), OUTLINE)
    ctx.save()
    ctx.translate(0, -230)
    ctx.scale(1.0, 0.72)
    circ(ctx, 0, 0, 190)
    ctx.restore()
    ink_fill(ctx, (0.55, 0.4, 0.28), OUTLINE)
    circ(ctx, 170, -260, 90)
    ink_fill(ctx, (0.55, 0.4, 0.28), OUTLINE)
    ctx.move_to(220, -240)
    ctx.curve_to(270, -150 + 10 * math.sin(t * 2), 250, -60, 220, -40)
    stroke(ctx, 26, (0.55, 0.4, 0.28))
    ctx.move_to(200, -200)
    ctx.curve_to(300, -170, 330, -280, 280, -320)
    stroke(ctx, 16, (0.97, 0.95, 0.88))
    circ(ctx, 190, -285, 8)
    ctx.set_source_rgb(*INK)
    ctx.fill()


def p_gear(ctx, p, t):
    gear(ctx, 0, -p.get("r", 80), p.get("r", 80), t, p.get("speed", 1.2), p.get("color", "grey"))


def p_sandbags(ctx, p, t):
    for row in range(3):
        for k in range(4 - row):
            rrect(ctx, -200 + row * 50 + k * 100, -50 - row * 46, 100, 50, 22)
            ink_fill(ctx, (0.72, 0.65, 0.5), 3.5)


def p_longship(ctx, p, t):
    bob = 5 * math.sin(t * 1.4)
    ctx.translate(0, bob)
    ctx.move_to(-330, -150)
    ctx.curve_to(-300, -40, -200, 0, 0, 0)
    ctx.curve_to(200, 0, 300, -40, 330, -150)
    ctx.curve_to(260, -90, -260, -90, -330, -150)
    ink_fill(ctx, "wood", OUTLINE)
    for x in range(-220, 240, 70):
        circ(ctx, x, -70, 22)
        ink_fill(ctx, ["red", "yellow", "blue"][(x // 70) % 3], 3)
    ctx.move_to(330, -150)
    ctx.curve_to(380, -200, 360, -260, 320, -250)
    stroke(ctx, 10, "darkwood")
    line(ctx, 0, -80, 0, -460, 12, "darkwood")
    rrect(ctx, -150, -440, 300, 230, 4)
    ink_fill(ctx, "white", OUTLINE)
    for k in range(3):
        rrect(ctx, -150 + k * 100, -440, 50, 230, 0)
        ink_fill(ctx, "red", 0)
    rrect(ctx, -150, -440, 300, 230, 4)
    ink_fill(ctx, None, OUTLINE)


def p_chariot(ctx, p, t):
    spin = t * 6
    p_horse = wd.PROPS["horse"]
    ctx.save()
    ctx.translate(230, 0)
    p_horse(ctx, {"walk": True, "color": "white"}, t * 2)
    ctx.restore()
    line(ctx, 40, -100, 170, -120, 8, "wood")
    poly(ctx, [(-90, -60), (60, -60), (40, -170), (-60, -150)])
    ink_fill(ctx, "red", OUTLINE)
    circ(ctx, -20, -45, 45)
    ink_fill(ctx, "wood", OUTLINE)
    for k in range(4):
        a = spin + k * math.pi / 4
        line(ctx, -20 - 38 * math.cos(a), -45 - 38 * math.sin(a), -20 + 38 * math.cos(a), -45 + 38 * math.sin(a), 4)


def p_latrine(ctx, p, t):
    """Roman public latrine bench with holes (and the sponge on a stick)."""
    rrect(ctx, -330, -110, 660, 110, 6)
    ink_fill(ctx, MARBLE, OUTLINE)
    for k in range(5):
        x = -260 + k * 130
        ctx.save()
        ctx.translate(x, -110)
        ctx.scale(1, 0.4)
        circ(ctx, 0, 0, 34)
        ctx.restore()
        ink_fill(ctx, INK, 0)
    rrect(ctx, -340, 0, 680, 30, 4)
    ink_fill(ctx, "water", 3)


def p_smokestack(ctx, p, t):
    rrect(ctx, -50, -520, 100, 520, 4)
    ink_fill(ctx, (0.6, 0.3, 0.25), OUTLINE)
    for y in range(-500, 0, 60):
        line(ctx, -50, y, 50, y, 2.5, (0.4, 0.2, 0.15))
    wd.smoke(ctx, 0, -560, t, 2.2, (0.35, 0.35, 0.38))


def p_dial(ctx, p, t):
    """Big 'survival time' dial for tier rankings: needle points to a fraction 0..1."""
    k = clamp(p.get("value", 0.5)) * ease_out(clamp(p.get("_age", 9) / 1.0))
    r = p.get("r", 160)
    ctx.arc(0, 0, r, math.pi, 2 * math.pi)
    ctx.close_path()
    ink_fill(ctx, "white", OUTLINE)
    for i, colr in enumerate(("red", "orange", "yellow", "lime", "green")):
        ctx.move_to(0, 0)
        ctx.arc(0, 0, r - 8, math.pi + i * math.pi / 5, math.pi + (i + 1) * math.pi / 5)
        ctx.close_path()
        ink_fill(ctx, colr, 2.5)
    a = math.pi + k * math.pi
    line(ctx, 0, 0, math.cos(a) * (r - 20), math.sin(a) * (r - 20), 9, INK)
    circ(ctx, 0, 0, 16)
    ink_fill(ctx, INK, 0)
    if p.get("label"):
        write(ctx, p["label"], 0, 50, 54, INK, MARKER, outline=5, outline_color="white")


BACKGROUNDS = {"rome": bg_rome, "baths": bg_baths, "arena": bg_arena, "ice_age": bg_ice_age, "desert": bg_desert,
               "deck": bg_deck, "trench": bg_trench, "factory": bg_factory, "cave": bg_cave}
PROPS = {"column": p_column, "temple": p_temple, "amphora": p_amphora, "pyramid": p_pyramid, "palm": p_palm,
         "mammoth": p_mammoth, "gear": p_gear, "sandbags": p_sandbags, "longship": p_longship, "chariot": p_chariot,
         "latrine": p_latrine, "smokestack": p_smokestack, "dial": p_dial}
wd.BACKGROUNDS.update(BACKGROUNDS)
wd.PROPS.update(PROPS)
