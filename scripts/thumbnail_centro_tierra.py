"""Miniatura personalizada del Short «centro de la Tierra».

Salidas (output/centro-de-la-tierra/ y samples/):
  thumbnail.png       1080x1920 (Shorts)
  thumbnail_16x9.png  1280x720  (vista en escritorio / pestaña Vídeos)
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import cairo  # noqa: E402

from fabrica.visuals.character import Character, Pose, act  # noqa: E402
from fabrica.visuals.draw import INK, OUT, PAL, circle, fill_stroke, radial_grad, rrect, saved, star, text  # noqa: E402
from fabrica.visuals.fonts import ensure_fonts  # noqa: E402
from fabrica.visuals.world import bg_earth_section, draw_prop  # noqa: E402


def scene(ctx, W, H, cx, cy, R, leo_y, leo_scale, title_y, title_size, show_title=True, badge=True):
    with saved(ctx):
        ctx.translate((W - 1080) / 2, 0)
        bg_earth_section(ctx, 0.0, {"cx": cx, "cy": cy, "R": R, "hole": None})
    ox = (W - 1080) / 2
    hx = ox + cx
    # brillo del núcleo
    circle(ctx, hx, cy, R * 0.5)
    ctx.set_source(radial_grad(ctx, hx, cy, R * 0.1, R * 0.5, [(0, (1, 1, 0.9), 0.9), (1, (1, 0.8, 0.3), 0)]))
    ctx.fill()
    # túnel desde la superficie hasta el centro
    top = cy - R - 14
    rrect(ctx, hx - 34, top - 10, 68, R + 10, 30)
    fill_stroke(ctx, (0.12, 0.06, 0.04), OUT)
    # líneas de velocidad dentro del túnel
    for i, (dx, y0, ln) in enumerate(((-12, leo_y - 330, 120), (14, leo_y - 260, 160), (0, leo_y - 420, 90))):
        ctx.move_to(hx + dx, y0)
        ctx.line_to(hx + dx, y0 + ln)
        ctx.set_source_rgba(1, 1, 1, 0.7)
        ctx.set_line_width(6)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()
    # Leo cayendo (traje y casco), aterrado
    p = act("fall", 0.35, 2, Pose(x=hx, y=leo_y, scale=leo_scale, expression="scared", outfit="suit", helmet="dome"))
    p.rot = -0.35
    p.mouth_open = 0.8
    p.blink = 0
    p.look = (0.2, 1)
    Character().draw(ctx, p)
    # destellos alrededor del núcleo
    for a in range(8):
        ang = a * math.pi / 4 + 0.3
        star(ctx, hx + R * 0.42 * math.cos(ang), cy + R * 0.42 * math.sin(ang), 18, n=4, inner=0.3)
        ctx.set_source_rgb(1, 1, 1)
        ctx.fill()
    if badge:
        with saved(ctx):
            ctx.translate(hx + R * 0.42, cy - R * 0.62)
            ctx.rotate(0.12)
            rrect(ctx, -170, -62, 340, 124, 40)
            fill_stroke(ctx, PAL["red"], OUT * 1.2)
            text(ctx, "6.371 km", 0, 2, 82, outline=7, shadow_off=0)
        draw_prop(ctx, {"type": "arrow", "x": hx + R * 0.22, "y": cy - R * 0.43, "abs": True, "rot": 2.2,
                        "scale": 0.55, "enter": "none", "color": PAL["red"]}, 0)
    if show_title:
        for i, (ln, colr) in enumerate((("¿Y SI CAVAS", "white"), ("HASTA EL CENTRO", PAL["yellow"]),
                                        ("DE LA TIERRA?", PAL["yellow"]))):
            with saved(ctx):
                ctx.translate(W / 2, title_y + i * title_size * 1.05)
                ctx.rotate(-0.03)
                text(ctx, ln, 0, 0, title_size, color=colr, outline=16, max_w=W - 70)


def main():
    ensure_fonts()
    out = ROOT / "output" / "centro-de-la-tierra"
    smp = ROOT / "samples" / "centro-de-la-tierra"
    for d in (out, smp):
        d.mkdir(parents=True, exist_ok=True)
    # vertical (Shorts)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 1920)
    c = cairo.Context(s)
    scene(c, 1080, 1920, cx=540, cy=1560, R=860, leo_y=1290, leo_scale=1.45, title_y=250, title_size=150)
    for d in (out, smp):
        s.write_to_png(str(d / "thumbnail.png"))
    # horizontal 16:9
    s2 = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 720)
    c2 = cairo.Context(s2)
    with saved(c2):
        c2.translate(300, 0)
        scene(c2, 1080, 720, cx=540, cy=760, R=560, leo_y=560, leo_scale=0.62, title_y=0, title_size=0,
              show_title=False, badge=False)
    text(c2, "¿Y SI CAVAS HASTA EL", 330, 250, 92, color="white", outline=12, max_w=600)
    text(c2, "CENTRO DE", 330, 355, 92, color=PAL["yellow"], outline=12, max_w=600)
    text(c2, "LA TIERRA?", 330, 460, 92, color=PAL["yellow"], outline=12, max_w=600)
    with saved(c2):
        c2.translate(330, 575)
        c2.rotate(-0.04)
        rrect(c2, -150, -48, 300, 96, 34)
        fill_stroke(c2, PAL["red"], OUT)
        text(c2, "6.371 km", 0, 2, 64, outline=6, shadow_off=0)
    for d in (out, smp):
        s2.write_to_png(str(d / "thumbnail_16x9.png"))
    print("ok")


if __name__ == "__main__":
    main()
