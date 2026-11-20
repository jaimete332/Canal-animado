"""16:9 thumbnail (1280×720) for long-form stickman videos.

story.metadata["thumbnail"] = {
    "scene": "s12" | "visual": {...custom scene DSL...},   # what to draw
    "t": 1.5,                                               # time inside that scene
    "lines": ["1 YEAR AS A", "PEASANT"],                    # big text (2-4 words per line)
    "colors": ["white", "yellow"], "side": "left" | "right",
    "badge": "90% DIED?", "badge_color": "red",
    "zoom": 1.2, "focus": [0.6, 0.5],
}
"""
from __future__ import annotations

import json
import math

import cairo

from ..visuals.draw import saved
from .scene import StickScene
from .style import INK, H, W, c, rrect, ink_fill

TW, TH = 1280, 720
FONT = "Luckiest Guy"


def _big_text(ctx, s, x, y, size, color, align="left", max_w=None):
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    ext = ctx.text_extents(s)
    if max_w and ext.width > max_w:
        size *= max_w / ext.width
        ctx.set_font_size(size)
        ext = ctx.text_extents(s)
    tx = x - ext.x_bearing if align == "left" else (x - ext.width - ext.x_bearing if align == "right"
                                                     else x - ext.width / 2 - ext.x_bearing)
    ty = y - ext.height / 2 - ext.y_bearing
    for dx, dy, lw, col_ in ((7, 9, 26, (0, 0, 0, 0.45)), (0, 0, 24, (*INK, 1)), (0, 0, 0, (*c(color), 1))):
        ctx.new_path()
        ctx.move_to(tx + dx, ty + dy)
        ctx.text_path(s)
        ctx.set_source_rgba(*col_)
        if lw:
            ctx.set_line_width(lw)
            ctx.set_line_join(cairo.LINE_JOIN_ROUND)
            ctx.stroke_preserve()
        ctx.fill()
    return size


def render_thumb(item: dict, spec: dict, out_path, fps: int = 30):
    item = json.loads(json.dumps(item))
    item["trans_in"] = item["trans_out"] = "cut"
    vis = item["scene"]["visual"]
    if spec.get("visual"):
        vis = item["scene"]["visual"] = spec["visual"]
    if not spec.get("keep_overlays"):
        vis["overlays"] = []
    vis["camera"] = {"move": "static", "zoom": spec.get("zoom", 1.0), "focus": spec.get("focus", [0.5, 0.5])}
    r = StickScene(item, fps)
    base = r.frame(int(spec.get("t", item["dur"] * 0.5) * fps))
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, TW, TH)
    ctx = cairo.Context(surf)
    with saved(ctx):
        ctx.scale(TW / W, TH / H)
        ctx.set_source_surface(base)
        ctx.paint()
    side = spec.get("side", "left")
    lines = spec.get("lines", [])
    colors = spec.get("colors", ["white", "yellow", "yellow"])
    size = spec.get("size", 112)
    x = 44 if side == "left" else TW - 44
    y0 = spec.get("y", 150)
    for i, ln in enumerate(lines):
        _big_text(ctx, ln, x, y0 + i * size * 1.02, size, colors[i % len(colors)], side, max_w=TW * 0.56)
    if spec.get("badge"):
        bs = 54
        ctx.select_font_face(FONT)
        ctx.set_font_size(bs)
        w = ctx.text_extents(spec["badge"]).width + 50
        bx, by = spec.get("badge_pos", [x if side == "left" else x - w, y0 + len(lines) * size * 1.02 + 10])
        with saved(ctx):
            ctx.translate(bx + w / 2, by)
            ctx.rotate(-0.04)
            rrect(ctx, -w / 2, -bs * 0.75, w, bs * 1.5, 16)
            ink_fill(ctx, spec.get("badge_color", "red"), 6)
            _big_text(ctx, spec["badge"], 0, 4, bs, "white", "center")
    surf.write_to_png(str(out_path))
    return out_path


def stick_thumbnail(pipe, meta: dict) -> None:
    spec = dict(pipe.story.metadata.get("thumbnail") or {})
    items = {i["id"]: i for i in pipe.scene_items()}
    item = items.get(spec.get("scene")) or next(
        (i for i, s in zip(items.values(), pipe.story.scenes) if s.beat == "climax"), next(iter(items.values())))
    if not spec.get("lines"):
        words = meta["thumbnail_text"].split()
        half = math.ceil(len(words) / 2)
        spec["lines"] = [" ".join(words[:half]), " ".join(words[half:])] if len(words) > 2 else [meta["thumbnail_text"]]
    render_thumb(item, spec, pipe.paths.thumbnail, pipe.fps)
    # alternative versions for YouTube's "Test & compare"
    for k, alt in enumerate(pipe.story.metadata.get("thumbnail_alts", []) or [], start=2):
        it = items.get(alt.get("scene"), item)
        render_thumb(it, alt, pipe.paths.root / f"thumbnail_{k}.png", pipe.fps)
