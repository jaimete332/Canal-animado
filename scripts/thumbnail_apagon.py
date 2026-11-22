"""Miniatura 16:9 del vídeo largo «¿Qué pasaría si se apagara la electricidad en todo el mundo?».

Ciudad partida en diagonal: a la izquierda con todas las luces, a la derecha apagada y con la Vía Láctea;
Leo asustado con una vela, título corto y sello «DATOS REALES».
Salida: output/apagon-mundial/thumbnail.png y thumbnail_16x9.png (1280×720).
Uso: python3 scripts/thumbnail_apagon.py
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
SLUG = "apagon-mundial"


def frame(bg):
    it = {"scene": {"visual": {"background": bg, "props": [], "character": {"visible": False},
                               "camera": {"move": "static"}}}, "dur": 2, "words": [], "frames": 60}
    return SceneRenderer(it).frame(20)


def main():
    ensure_fonts()
    out = ROOT / "output" / SLUG
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    lit = frame({"type": "modern_city", "native": True, "moon": False, "crosswalk": False})
    dark = frame({"type": "modern_city", "native": True, "lights": 0, "stars": 1, "milky": 1, "moon": False,
                  "crosswalk": False, "dark": 0.55})
    ctx.set_source_surface(lit)
    ctx.paint()
    x0, x1 = 760, 1060  # corte diagonal
    with saved(ctx):
        ctx.move_to(x1, -10)
        ctx.line_to(W + 10, -10)
        ctx.line_to(W + 10, H + 10)
        ctx.line_to(x0, H + 10)
        ctx.close_path()
        ctx.clip()
        ctx.set_source_surface(dark)
        ctx.paint()
    # rayo de corte en la frontera
    ctx.move_to(x1, -10)
    for k, (dx, y) in enumerate(((-90, 260), (40, 300), (-120, 600), (30, 640), (-200, 1090))):
        ctx.line_to(x1 + dx, y)
    ctx.set_source_rgb(*PAL["yellow"])
    ctx.set_line_width(26)
    ctx.stroke_preserve()
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(8)
    ctx.stroke()
    # viñeta para el texto
    ctx.rectangle(0, 0, W, H)
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgba(0, 0.03, 0.03, 0.1, 0.55)
    g.add_color_stop_rgba(0.5, 0.03, 0.03, 0.1, 0.05)
    g.add_color_stop_rgba(1, 0.03, 0.03, 0.1, 0.5)
    ctx.set_source(g)
    ctx.fill()
    # Tierra de noche apagándose (arriba a la derecha)
    draw_prop(ctx, {"type": "earth_night", "x": 1600, "y": 300, "abs": True, "scale": 0.72, "off_at": 0.0,
                    "off_spread": 2.0, "enter": "none"}, 1.0)
    # vela y Leo asustado
    draw_prop(ctx, {"type": "candle", "x": 1130, "y": 1010, "abs": True, "scale": 1.25, "enter": "none"}, 2.0)
    p = act("shock", 0.4, 2, Pose(x=1560, y=1330, scale=1.8, expression="shock", outfit="casual", sweat=1.0))
    p.mouth_open = 1.0
    p.blink = 0
    Character().draw(ctx, p)
    # título
    text(ctx, "¿EL MUNDO", 520, 210, 190, color="white", outline=16, font="Lilita One")
    text(ctx, "SIN LUZ?", 520, 420, 230, color=PAL["yellow"], outline=16, font="Lilita One")
    # contador de tiempo
    with saved(ctx):
        ctx.translate(520, 680)
        ctx.rotate(-0.03)
        rrect(ctx, -380, -70, 760, 140, 34)
        fill_stroke(ctx, (1, 1, 1), OUT * 1.2)
        text(ctx, "DE 1 MINUTO A 1 AÑO", 0, 4, 78, color=INK, outline=0, shadow_off=0, max_w=700)
    with saved(ctx):
        ctx.translate(430, 900)
        ctx.rotate(-0.06)
        rrect(ctx, -250, -62, 500, 124, 40)
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
