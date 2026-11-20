"""Visual identity of the English stickman channel, drawn with the same engine as the videos.

Outputs in assets/branding_en/:
  profile.png         800x800   (YouTube crops it to a circle)
  banner.png          2560x1440 (safe area: centre 1546x423, visible on every device)
  watermark.png       150x150
  banner_preview.png  banner with the safe-area guides (for review only)
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import cairo  # noqa: E402

from fabrica.stick.rig import ACTIONS, Look, Placement, Stickman  # noqa: E402
from fabrica.stick.style import INK, P, c, circ, ink_fill, rrect  # noqa: E402
from fabrica.stick.world import cloud, hut, castle, tree  # noqa: E402
from fabrica.visuals.fonts import ensure_fonts  # noqa: E402

OUTD = ROOT / "assets" / "branding_en"
OUTD.mkdir(parents=True, exist_ok=True)
NAME = "STICKPOTHETICAL"
TAGLINE = "What if history happened to YOU?"
FONT = "Luckiest Guy"
STAN = Look(scarf=True, seed=3)


def big_text(ctx, s, x, y, size, color, max_w=None, outline=0.11):
    ctx.select_font_face(FONT)
    ctx.set_font_size(size)
    e = ctx.text_extents(s)
    if max_w and e.width > max_w:
        size *= max_w / e.width
        ctx.set_font_size(size)
        e = ctx.text_extents(s)
    tx, ty = x - e.width / 2 - e.x_bearing, y - e.height / 2 - e.y_bearing
    for dx, dy, lw, col_ in ((size * 0.05, size * 0.07, size * outline * 2.2, (0, 0, 0, 0.35)),
                             (0, 0, size * outline * 2, (*INK, 1)), (0, 0, 0, (*c(color), 1))):
        ctx.new_path()
        ctx.move_to(tx + dx, ty + dy)
        ctx.text_path(s)
        ctx.set_source_rgba(*col_)
        if lw:
            ctx.set_line_width(lw)
            ctx.set_line_join(cairo.LINE_JOIN_ROUND)
            ctx.stroke_preserve()
        ctx.fill()


def rays(ctx, cx, cy, c1, c2, n=20, R=3000):
    ctx.set_source_rgb(*c(c1))
    ctx.paint()
    ctx.save()
    ctx.translate(cx, cy)
    for i in range(n):
        a = i * 2 * math.pi / n
        ctx.move_to(0, 0)
        ctx.arc(0, 0, R, a, a + math.pi / n)
        ctx.close_path()
    ctx.set_source_rgb(*c(c2))
    ctx.fill()
    ctx.restore()


def profile():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 800)
    ctx = cairo.Context(s)
    rays(ctx, 400, 430, (0.99, 0.84, 0.3), (0.99, 0.78, 0.2))
    circ(ctx, 400, 400, 330)
    ink_fill(ctx, P["paper"], 14)
    # Stan, big, waving, with a "?" thought
    Stickman(STAN).draw(ctx, ACTIONS["wave"](0.35, 2, {}), Placement(370, 700, 1.3, 1, "grin"), 0.35)
    ctx.select_font_face(FONT)
    ctx.set_font_size(230)
    ctx.move_to(490, 360)
    ctx.text_path("?")
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(16)
    ctx.stroke_preserve()
    ctx.set_source_rgb(*P["red"])
    ctx.fill()
    s.write_to_png(str(OUTD / "profile.png"))
    wm = cairo.ImageSurface(cairo.FORMAT_ARGB32, 150, 150)
    w = cairo.Context(wm)
    w.scale(150 / 800, 150 / 800)
    w.arc(400, 400, 400, 0, 2 * math.pi)
    w.clip()
    w.set_source_surface(s)
    w.paint()
    wm.write_to_png(str(OUTD / "watermark.png"))


def banner(preview=False):
    W, H = 2560, 1440
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(s)
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.55, 0.78, 0.96)
    g.add_color_stop_rgb(1, 0.88, 0.95, 0.99)
    ctx.set_source(g)
    ctx.paint()
    for x, y, k in ((300, 330, 1.3), (2200, 300, 1.1), (1250, 260, 0.9)):
        cloud(ctx, x, y, k)
    gy = 1010
    # scenery across eras: castle, hut, trees
    castle(ctx, 2150, gy - 30, 0.75)
    hut(ctx, 430, gy - 20, 0.7, smoke_=False)
    tree(ctx, 1080, gy - 10, 0.75)
    tree(ctx, 1480, gy - 10, 0.7)
    ctx.move_to(0, gy)
    for x in range(0, W + 1, 80):
        ctx.line_to(x, gy + 8 * math.sin(x / 140))
    ctx.line_to(W, H)
    ctx.line_to(0, H)
    ctx.close_path()
    ink_fill(ctx, P["grass"], 6)
    # cast: knight, peasant, Stan (centre), king, plague doctor
    people = [(Look(outfit="armor", hat="helmet", item="sword", seed=1), "swing", 700, "determined", 1),
              (Look(outfit="tunic", outfit_color="brown", hat="hood", hat_color="tan", item="hoe", seed=2), "dig",
               880, "tired", 1),
              (Look(outfit="robe", outfit_color="red", hat="crown", belly=0.6, beard="long", seed=4), "laugh", 1680,
               "laughing", -1),
              (Look(outfit="robe", outfit_color="ink", hat="plague_mask", seed=5), "idle", 1860, "neutral", -1)]
    for look, act, x, ex, f in people:
        Stickman(look).draw(ctx, ACTIONS[act](0.6, 2, {}), Placement(x, gy + 40, 0.68, f, ex), 0.6)
    big_text(ctx, NAME, W / 2, 575, 170, "white", max_w=1400)
    big_text(ctx, TAGLINE, W / 2, 690, 70, (0.99, 0.82, 0.25), max_w=1300, outline=0.09)
    Stickman(STAN).draw(ctx, ACTIONS["wave"](0.5, 2, {}), Placement(1280, gy + 50, 0.78, 1, "grin"), 0.5)
    if preview:
        for (w, h, col_) in ((1546, 423, (1, 0, 0)), (2560, 423, (0, 0.6, 0)), (1855, 423, (0, 0, 1))):
            ctx.rectangle((W - w) / 2, (H - h) / 2, w, h)
            ctx.set_source_rgba(*col_, 0.9)
            ctx.set_line_width(6)
            ctx.stroke()
    s.write_to_png(str(OUTD / ("banner_preview.png" if preview else "banner.png")))


if __name__ == "__main__":
    ensure_fonts()
    profile()
    banner()
    banner(preview=True)
    print("OK →", OUTD)
