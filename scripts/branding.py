"""Genera la identidad visual del canal con el mismo motor que los vídeos.

Salidas en assets/branding/:
  profile.png        800x800   (YouTube lo recorta en círculo)
  banner.png         2560x1440 (zona segura central 1546x423 para móvil)
  watermark.png      150x150   (marca de agua opcional para los vídeos)
  banner_preview.png (banner con guías de zonas seguras, solo para revisar)
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import cairo  # noqa: E402

from fabrica.visuals.character import Character, Pose, act  # noqa: E402
from fabrica.visuals.draw import (INK, OUT, PAL, circle, fill_stroke, linear_grad, radial_grad, rrect,  # noqa: E402
                                  saved, star, text)
from fabrica.visuals.fonts import ensure_fonts  # noqa: E402
from fabrica.visuals.world import _earth_globe, draw_prop  # noqa: E402

OUTD = ROOT / "assets" / "branding"
OUTD.mkdir(parents=True, exist_ok=True)
NAME = "HIPOTÉTICOS"
TAGLINE = "¿Qué pasaría si...? en 60 segundos"
ch = Character()


def burst(ctx, cx, cy, c1, c2, n=18, rot=0.0, R=3000):
    ctx.set_source_rgb(*c1)
    ctx.paint()
    with saved(ctx):
        ctx.translate(cx, cy)
        ctx.rotate(rot)
        for i in range(n):
            a = i * 2 * math.pi / n
            ctx.move_to(0, 0)
            ctx.arc(0, 0, R, a, a + math.pi / n)
            ctx.close_path()
        ctx.set_source_rgb(*c2)
        ctx.fill()


def profile(size=800):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
    c = cairo.Context(s)
    k = size / 800
    c.scale(k, k)
    burst(c, 400, 430, PAL["yellow"], (1.0, 0.70, 0.18), n=16, rot=0.1)
    circle(c, 400, 430, 330)
    c.set_source(radial_grad(c, 400, 430, 120, 360, [(0, (1, 1, 1), 0.55), (1, (1, 1, 1), 0)]))
    c.fill()
    # Leo en primer plano (cabeza + hombros), sonriente y sorprendido
    p = act("present", 0.6, 2, Pose(x=400, y=1180, scale=2.35, expression="excited", look=(0.2, -0.1)))
    p.mouth_open = 0.55
    p.blink = 0
    p.head_tilt = -0.06
    p.arm_r = (0.3, 0.3)
    p.arm_l = (0.3, 0.3)
    ch.draw(c, p)
    # interrogación flotante
    with saved(c):
        c.translate(655, 175)
        c.rotate(0.25)
        text(c, "?", 0, 0, 230, color=PAL["red"], outline=14)
    for x, y, r in ((140, 170, 26), (690, 520, 18), (110, 560, 16)):
        star(c, x, y, r, n=4, inner=0.35)
        c.set_source_rgb(1, 1, 1)
        c.fill()
    s.write_to_png(str(OUTD / "profile.png"))
    return s


def banner():
    W, H = 2560, 1440
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(s)
    # fondo: espacio arriba, degradado a cálido abajo
    c.rectangle(0, 0, W, H)
    c.set_source(linear_grad(c, 0, 0, 0, H, [(0, (0.10, 0.08, 0.30)), (0.55, (0.36, 0.20, 0.62)), (1, (0.98, 0.45, 0.22))]))
    c.fill()
    import numpy as np
    rng = np.random.default_rng(3)
    for _ in range(260):
        x, y = rng.uniform(0, W), rng.uniform(0, H * 0.7)
        circle(c, x, y, rng.uniform(1.5, 4.5))
        c.set_source_rgba(1, 1, 0.9, rng.uniform(0.4, 1))
        c.fill()
    # elementos de temas del canal a los lados (fuera de la zona segura en móvil, visibles en TV/PC)
    _earth_globe(c, 330, 760, 230, 0.6, field=True)
    with saved(c):  # planeta rojo (Marte)
        circle(c, 2270, 470, 120)
        fill_stroke(c, (0.82, 0.32, 0.12), OUT)
        for x, y, r in ((2230, 430, 24), (2300, 510, 16), (2310, 420, 12)):
            circle(c, x, y, r)
            c.set_source_rgba(0.5, 0.15, 0.05, 0.6)
            c.fill()
    draw_prop(c, {"type": "sun", "x": 2330, "y": 1060, "abs": True, "scale": 1.1, "enter": "none"}, 0.4)
    draw_prop(c, {"type": "gem", "x": 640, "y": 330, "abs": True, "scale": 1.3, "enter": "none", "seed": 1}, 0.3)
    draw_prop(c, {"type": "bone", "x": 1900, "y": 300, "abs": True, "scale": 1.2, "rot": 0.4, "enter": "none"}, 0)
    draw_prop(c, {"type": "clock", "x": 610, "y": 1180, "abs": True, "scale": 0.8, "rot": -0.2, "enter": "none"}, 0.7)
    for x, y, r in ((900, 260, 22), (1700, 240, 18), (2050, 760, 20), (520, 520, 14)):
        star(c, x, y, r, n=4, inner=0.35)
        c.set_source_rgb(1, 1, 1)
        c.fill()
    # bocadillo central (zona segura: x 507-2053, y 508-931)
    cx, cy = 1280, 720
    with saved(c):
        c.translate(cx + 40, cy)
        c.rotate(-0.02)
        rrect(c, -640 + 14, -190 + 18, 1280, 380, 90)
        c.set_source_rgba(0, 0, 0, 0.3)
        c.fill()
        rrect(c, -640, -190, 1280, 380, 90)
        fill_stroke(c, PAL["yellow"], OUT * 1.6)
        text(c, NAME, 60, -45, 175, color="white", outline=16, max_w=1000)
        text(c, TAGLINE, 60, 110, 68, color=INK, outline=0, shadow_off=0, max_w=1000)
    # Leo asomando a la izquierda del bocadillo, señalándolo
    p = act("present", 0.6, 2, Pose(x=690, y=918, scale=0.92, expression="excited", look=(1, -0.2)))
    p.mouth_open = 0.5
    p.blink = 0
    ch.draw(c, p)
    s.write_to_png(str(OUTD / "banner.png"))
    # previsualización con zonas seguras
    pv = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    q = cairo.Context(pv)
    q.set_source_surface(s)
    q.paint()
    for (w, h, col, lab) in ((2560, 423, (0.2, 0.6, 1), "PC (2560x423)"), (1855, 423, (0, 1, 0), "Tablet (1855x423)"),
                             (1546, 423, (1, 0.2, 0.2), "Móvil / zona segura (1546x423)")):
        q.rectangle((W - w) / 2, (H - h) / 2, w, h)
        q.set_source_rgb(*col)
        q.set_line_width(6)
        q.stroke()
        text(q, lab, (W - w) / 2 + 20, (H - h) / 2 - 30, 36, color=col, align="left", outline=4, shadow_off=0)
    pv.write_to_png(str(OUTD / "banner_preview.png"))


def watermark():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 150, 150)
    c = cairo.Context(s)
    circle(c, 75, 75, 70)
    fill_stroke(c, PAL["yellow"], 6)
    text(c, "?", 75, 78, 120, color=PAL["red"], outline=7, shadow_off=0)
    s.write_to_png(str(OUTD / "watermark.png"))


if __name__ == "__main__":
    ensure_fonts()
    profile()
    banner()
    watermark()
    print("Generado en", OUTD)
