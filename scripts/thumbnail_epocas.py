"""Miniatura 16:9 del vídeo largo «¿Cuánto durarías en cada época de la historia?».

Collage en franjas diagonales (Egipto, peste negra, barco pirata, Londres), Leo asustado en primer plano,
título grande y medidor. Salida: output/cuanto-durarias-en-cada-epoca/thumbnail.png y thumbnail_16x9.png (1280×720).
Uso: FABRICA_FORMAT=landscape python3 scripts/thumbnail_epocas.py
"""
import os
import sys
from pathlib import Path

os.environ.setdefault("FABRICA_FORMAT", "landscape")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import cairo  # noqa: E402

from fabrica.visuals.character import Character, Pose, act  # noqa: E402
from fabrica.visuals.draw import INK, OUT, PAL, fill_stroke, rrect, saved, text  # noqa: E402
from fabrica.visuals.fonts import ensure_fonts  # noqa: E402
from fabrica.visuals.scene import SceneRenderer  # noqa: E402
from fabrica.visuals.world import draw_prop  # noqa: E402

W, H = 1920, 1080
PANELS = [({"type": "egypt", "progress": 0.75, "window": 1000, "zoom": 0.5}, []),
          ({"type": "village", "mode": "plague", "window": 1000, "zoom": 0.5}, [{"type": "rat", "x": 0.5, "y": 0.8, "scale": 1.2, "enter": "none"}]),
          ({"type": "ocean", "window": 1000, "zoom": 0.5}, [{"type": "sailing_ship", "x": 0.5, "y": 0.6, "scale": 0.9, "enter": "none"}]),
          ({"type": "london", "smog": 0.5, "window": 1000, "zoom": 0.5}, [{"type": "water_pump", "x": 0.5, "y": 0.95, "scale": 1.0, "enter": "none"}])]


def panel(bg, props):
    it = {"scene": {"visual": {"background": bg, "props": props, "character": {"visible": False},
                               "camera": {"move": "static"}}}, "dur": 2, "words": [], "frames": 60}
    return SceneRenderer(it).frame(20)


def main():
    ensure_fonts()
    out = ROOT / "output" / "cuanto-durarias-en-cada-epoca"
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    n, slant = len(PANELS), 160
    for i, (bg, props) in enumerate(PANELS):
        x0 = i * W / n
        with saved(ctx):
            ctx.move_to(x0 - slant / 2, 0)
            ctx.line_to(x0 + W / n + slant / 2, 0)
            ctx.line_to(x0 + W / n - slant / 2, H)
            ctx.line_to(x0 - slant * 1.5, H)
            ctx.close_path()
            ctx.clip()
            ctx.translate(x0 + W / n / 2, H / 2)
            ctx.set_source_surface(panel(bg, props), -W / 2, -H / 2)
            ctx.paint()
        ctx.move_to(x0 - slant / 2, 0)
        ctx.line_to(x0 - slant * 1.5, H)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(14)
        ctx.stroke()
    # viñeta para que el texto respire
    ctx.rectangle(0, 0, W, H)
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgba(0, 0.05, 0.04, 0.1, 0.75)
    g.add_color_stop_rgba(0.45, 0.05, 0.04, 0.1, 0.05)
    g.add_color_stop_rgba(1, 0.05, 0.04, 0.1, 0.55)
    ctx.set_source(g)
    ctx.fill()
    # etiqueta de cada época al pie de su franja (la última la tapa Leo)
    tags = [("EGIPTO", "2560 a. C."), ("PESTE NEGRA", "1348"), ("PIRATAS", "1720")]
    for i, (name, year) in enumerate(tags):
        x = max(190, i * W / n + W / n / 2 - slant * 0.9)
        with saved(ctx):
            ctx.translate(x, 985)
            ctx.rotate(-0.04)
            rrect(ctx, -165, -52, 330, 104, 24)
            fill_stroke(ctx, (1, 1, 1), OUT * 1.1)
            text(ctx, name, 0, -12, 50, color=INK, outline=0, shadow_off=0, max_w=300)
            text(ctx, year, 0, 30, 30, color=PAL["red"], outline=0, shadow_off=0)
    # Leo asustado, grande, abajo a la derecha, sudando
    p = act("shock", 0.4, 2, Pose(x=1480, y=1330, scale=1.85, expression="shock", outfit="casual", sweat=1.0))
    p.mouth_open = 1.0
    p.blink = 0
    Character().draw(ctx, p)
    # título
    text(ctx, "¿CUÁNTO", 620, 190, 190, color="white", outline=16, font="Lilita One")
    text(ctx, "DURARÍAS?", 620, 390, 200, color=PAL["yellow"], outline=16, font="Lilita One")
    # medidor
    draw_prop(ctx, {"type": "survival_meter", "x": 620, "y": 680, "abs": True, "scale": 1.05, "value": 0.32,
                    "label": "9 ÉPOCAS DE LA HISTORIA", "enter": "none", "animate": False}, 2.0)
    with saved(ctx):
        ctx.translate(1580, 120)
        ctx.rotate(0.08)
        rrect(ctx, -230, -62, 460, 124, 40)
        fill_stroke(ctx, PAL["red"], OUT * 1.3)
        text(ctx, "DATOS REALES", 0, 4, 74, color="white", outline=8, shadow_off=0)
    small = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 720)
    c2 = cairo.Context(small)
    c2.scale(1280 / W, 720 / H)
    c2.set_source_surface(surf)
    c2.get_source().set_filter(cairo.FILTER_BEST)
    c2.paint()
    out.mkdir(parents=True, exist_ok=True)
    for name in ("thumbnail.png", "thumbnail_16x9.png"):
        small.write_to_png(str(out / name))
    print(out / "thumbnail.png")


if __name__ == "__main__":
    main()
