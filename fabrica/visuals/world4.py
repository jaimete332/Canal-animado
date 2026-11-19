"""Catálogo «anuncios / marca»: mundo de cómic, espejo-portal, fotos de producto y clip real.

- bg comic:   ciudad de cómic con tramas de puntos (halftone), viñeta y líneas de acción.
- bg photo:   foto real de producto «contenida» (sin recortar) con fondo a juego y Ken Burns.
- bg clip:    vídeo real (p. ej. una persona hablando). Si el archivo no existe, usa `fallback`.
- prop mirror: espejo de cómic con marco dorado; dentro muestra una foto o un clip y ondula.
- prop pow:    onomatopeya de cómic (¡ZAS!, ¡POP!...).
"""
from __future__ import annotations

import math
import subprocess
from pathlib import Path

import cairo
import numpy as np

from .draw import (INK, OUT, PAL, circle, clamp, col, darken, ellipse, fill_stroke, lighten, linear_grad,
                   radial_grad, rrect, saved, star, text)
from .world import BACKGROUNDS, H, M, PROPS, W, _sky

ROOT = Path(__file__).resolve().parents[2]


# ----------------------------------------------------------------------------- utilidades de imagen/vídeo
_IMG: dict = {}


def _load_surface(path: str, max_w: int | None = None) -> cairo.ImageSurface:
    key = (path, max_w)
    if key not in _IMG:
        from PIL import Image
        p = Path(path) if Path(path).is_absolute() else ROOT / path
        im = Image.open(p).convert("RGB")
        if max_w and im.width > max_w:
            im = im.resize((max_w, int(im.height * max_w / im.width)), Image.LANCZOS)
        im.putalpha(255)
        b = bytearray(im.tobytes("raw", "BGRA"))
        _IMG[key] = cairo.ImageSurface.create_for_data(b, cairo.FORMAT_ARGB32, im.width, im.height)
    return _IMG[key]


class ClipReader:
    """Lee fotogramas de un vídeo de forma secuencial (el render de una escena es secuencial)."""
    _cache: dict = {}

    def __init__(self, path: Path, w=W, h=H, fps=30):
        self.path, self.w, self.h, self.fps = path, w, h, fps
        self.proc = None
        self.idx = -1
        self.last = None

    @classmethod
    def get(cls, path: Path):
        if path not in cls._cache:
            cls._cache[path] = ClipReader(path)
        return cls._cache[path]

    def _start(self):
        vf = f"scale={self.w}:{self.h}:force_original_aspect_ratio=increase,crop={self.w}:{self.h},fps={self.fps}"
        self.proc = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(self.path), "-vf", vf, "-f", "rawvideo",
                                      "-pix_fmt", "bgra", "-"], stdout=subprocess.PIPE,
                                     stderr=subprocess.DEVNULL)
        self.idx = -1

    def frame(self, t: float) -> cairo.ImageSurface | None:
        want = int(t * self.fps)
        if self.proc is None or want < self.idx:
            self._start()
        n = self.w * self.h * 4
        while self.idx < want:
            buf = self.proc.stdout.read(n)
            if len(buf) < n:
                break  # fin del clip: se queda el último fotograma
            self.idx += 1
            self.last = cairo.ImageSurface.create_for_data(bytearray(buf), cairo.FORMAT_ARGB32, self.w, self.h)
        return self.last


def _clip_path(p) -> Path | None:
    if not p:
        return None
    q = Path(p) if Path(p).is_absolute() else ROOT / p
    return q if q.exists() else None


# ----------------------------------------------------------------------------- fondos
def _halftone(ctx, color, alpha=0.25, step=34, rmax=7, x0=-M, y0=-M, x1=W + M, y1=H + M, grad=True):
    ctx.set_source_rgba(*col(color), alpha)
    for j, y in enumerate(range(int(y0), int(y1), step)):
        for x in range(int(x0) + (step // 2 if j % 2 else 0), int(x1), step):
            r = rmax * ((y - y0) / (y1 - y0) if grad else 1)
            if r > 0.6:
                ctx.arc(x, y, r, 0, 2 * math.pi)
                ctx.new_sub_path()
    ctx.fill()


def bg_comic(ctx, t, p):
    """Ciudad de cómic: cielo con trama, edificios planos de colores, acera y marco de viñeta."""
    _sky(ctx, "#7FD3FF", "#FFE66D")
    _halftone(ctx, "#FFFFFF", 0.35, rmax=9)
    # sol pop-art
    with saved(ctx):
        ctx.translate(820, 360)
        ctx.rotate(t * 0.3)
        for i in range(16):
            ctx.rotate(math.pi / 8)
            ctx.move_to(0, -100)
            ctx.line_to(-24, -200)
            ctx.line_to(24, -200)
            ctx.close_path()
        ctx.set_source_rgba(1, 0.55, 0.2, 0.9)
        ctx.fill()
    circle(ctx, 820, 360, 100)
    fill_stroke(ctx, "#FF6B6B", OUT)
    g = p.get("ground", 1360)
    cols = ["#FF6B9A", "#6C63FF", "#2EC4B6", "#FF9F1C", "#9D4EDD"]
    x = -M
    rng = np.random.default_rng(14)
    i = 0
    while x < W + M:
        w, h = rng.uniform(170, 260), rng.uniform(420, 820)
        c = cols[i % len(cols)]
        rrect(ctx, x, g - h, w, h + 200, 10)
        fill_stroke(ctx, c, OUT)
        _halftone(ctx, darken(c, 0.35), 0.5, step=22, rmax=4, x0=x + 8, y0=g - h + 8, x1=x + w - 8, y1=g, grad=True)
        for wy in range(int(g - h + 50), int(g - 60), 110):
            for wx in range(int(x + 30), int(x + w - 60), 80):
                rrect(ctx, wx, wy, 46, 64, 8)
                fill_stroke(ctx, "#FFF7C2" if rng.random() < 0.5 else "#BDE0FE", OUT * 0.6)
        x += w + 14
        i += 1
    ctx.rectangle(-M, g, W + 2 * M, H)
    ctx.set_source_rgb(0.85, 0.85, 0.9)
    ctx.fill()
    _halftone(ctx, "#9AA0B5", 0.5, step=26, rmax=5, y0=g, y1=H + M)
    ctx.move_to(-M, g)
    ctx.line_to(W + M, g)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(OUT * 1.4)
    ctx.stroke()
    if p.get("speedlines"):
        rng2 = np.random.default_rng(3)
        for k in range(40):
            a = rng2.uniform(0, 2 * math.pi)
            r0 = rng2.uniform(500, 700)
            ctx.move_to(540 + r0 * math.cos(a), 960 + r0 * math.sin(a))
            ctx.line_to(540 + 1600 * math.cos(a), 960 + 1600 * math.sin(a))
            ctx.set_source_rgba(1, 1, 1, 0.7)
            ctx.set_line_width(rng2.uniform(4, 14))
            ctx.stroke()


def bg_photo(ctx, t, p):
    """Foto real de producto, contenida (sin recortes), con fondo del color de la foto y Ken Burns."""
    path = p["path"]
    surf = _load_surface(path, 1400)
    bgc = col(p.get("bg", "#D7D7D7"))
    ctx.rectangle(-M, -M, W + 2 * M, H + 2 * M)
    ctx.set_source_rgb(*bgc)
    ctx.fill()
    fit = p.get("fit", "width")
    sc = (W / surf.get_width()) if fit == "width" else (H / surf.get_height())
    sc *= p.get("scale", 1.0)
    dur = max(0.1, p.get("_dur", 3))
    k = p.get("kenburns", 0.08) * t / dur
    with saved(ctx):
        ctx.translate(W / 2 + p.get("dx", 0), H * p.get("cy", 0.5))
        ctx.scale(sc * (1 + k), sc * (1 + k))
        ctx.translate(-surf.get_width() / 2, -surf.get_height() / 2)
        ctx.set_source_surface(surf, 0, 0)
        ctx.get_source().set_filter(cairo.FILTER_GOOD)
        ctx.paint()


def bg_clip(ctx, t, p):
    """Vídeo real a pantalla completa. Si no existe, dibuja el fondo `fallback`."""
    path = _clip_path(p.get("path"))
    if path is None:
        fb = dict(p.get("fallback", {"type": "color"}))
        fb["_dur"] = p.get("_dur", 3)
        BACKGROUNDS[fb.get("type", "color")](ctx, t, fb)
        return
    f = ClipReader.get(path).frame(t + p.get("start", 0.0))
    if f is not None:
        ctx.set_source_surface(f, 0, 0)
        ctx.paint()


# ----------------------------------------------------------------------------- props
def _mirror(ctx, p, t):
    """Espejo-portal: marco dorado ovalado; el cristal muestra `image`/`clip` y ondula con `ripple`."""
    rx, ry = p.get("rx", 300), p.get("ry", 470)
    ripple = p.get("ripple", 0.0)
    if p.get("ripple_anim"):
        ripple = 0.5 + 0.5 * math.sin(t * 3)
    # pie del espejo
    if p.get("stand", True):
        ctx.move_to(-rx * 0.5, ry + 180)
        ctx.line_to(0, ry - 20)
        ctx.line_to(rx * 0.5, ry + 180)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(OUT * 3)
        ctx.stroke_preserve()
        ctx.set_source_rgb(0.75, 0.55, 0.2)
        ctx.set_line_width(OUT * 1.4)
        ctx.stroke()
    ellipse(ctx, 0, 0, rx + 46, ry + 46)
    fill_stroke(ctx, "#E0A93A", OUT * 1.3)
    for k in range(18):  # adornos del marco
        a = k * 2 * math.pi / 18
        circle(ctx, (rx + 23) * math.cos(a), (ry + 23) * math.sin(a), 11)
        fill_stroke(ctx, "#FFD86B", OUT * 0.5)
    star(ctx, 0, -ry - 60, 40, n=5)
    fill_stroke(ctx, "#FFD86B", OUT * 0.8)
    with saved(ctx):
        ellipse(ctx, 0, 0, rx, ry)
        ctx.clip()
        inner = None
        cp = _clip_path(p.get("clip"))
        if cp is not None:
            inner = ClipReader.get(cp).frame(t)
            iw, ih = W, H
        elif p.get("image"):
            inner = _load_surface(p["image"], 1000)
            iw, ih = inner.get_width(), inner.get_height()
        if inner is not None:
            ctx.rectangle(-rx, -ry, 2 * rx, 2 * ry)
            ctx.set_source_rgb(0.84, 0.84, 0.84)
            ctx.fill()
            s = max(2 * rx / iw, 2 * ry / ih) * p.get("zoom", 1.0)
            with saved(ctx):
                wob = 10 * ripple * math.sin(t * 6)
                ctx.translate(wob, p.get("img_dy", 0))
                ctx.scale(s, s)
                ctx.translate(-iw / 2, -ih / 2)
                ctx.set_source_surface(inner, 0, 0)
                ctx.paint()
        else:
            ctx.rectangle(-rx, -ry, 2 * rx, 2 * ry)
            ctx.set_source(linear_grad(ctx, -rx, -ry, rx, ry, [(0, "#BDE0FE"), (1, "#E0C3FC")]))
            ctx.fill()
        # brillo diagonal que recorre el cristal
        sh = ((t * 0.5) % 1.4 - 0.2) * 2 * rx * 2 - 2 * rx
        ctx.move_to(sh - 80, -ry)
        ctx.line_to(sh + 40, -ry)
        ctx.line_to(sh + 40 - 300, ry)
        ctx.line_to(sh - 80 - 300, ry)
        ctx.close_path()
        ctx.set_source_rgba(1, 1, 1, 0.35)
        ctx.fill()
        if ripple > 0.02:  # ondas
            for k in range(5):
                r = ((t * 0.9 + k * 0.2) % 1)
                ellipse(ctx, 0, ry * 0.1, rx * r * 1.2, ry * r * 1.2)
                ctx.set_source_rgba(1, 1, 1, 0.5 * ripple * (1 - r))
                ctx.set_line_width(10)
                ctx.stroke()
    ellipse(ctx, 0, 0, rx, ry)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(OUT)
    ctx.stroke()


def _pow(ctx, p, t):
    """Onomatopeya de cómic en estrella."""
    c = col(p.get("color", "#FFD23F"))
    with saved(ctx):
        ctx.rotate(p.get("tilt", -0.12))
        star(ctx, 0, 0, p.get("r", 190), n=12, inner=0.72)
        fill_stroke(ctx, c, OUT * 1.2)
        text(ctx, p.get("text", "¡POP!"), 0, 0, p.get("size", 96), color=p.get("text_color", "#E8392F"),
             outline=8, shadow_off=4, max_w=p.get("r", 190) * 1.5, font="Luckiest Guy")


def _logo(ctx, p, t):
    """Logotipo de marca en texto (para cierres de anuncio)."""
    c = col(p.get("color", "#C4EDC9"))
    ctx.select_font_face(p.get("font", "Michroma"))
    ctx.set_font_size(100)
    txt = p.get("text", "BLOWFISH")
    ext = ctx.text_extents(txt)
    k = p.get("width", 860) / ext.width
    with saved(ctx):
        ctx.scale(k, k)
        ctx.move_to(-ext.width / 2 - ext.x_bearing, -ext.height / 2 - ext.y_bearing)
        ctx.text_path(txt)
        if p.get("shadow", True):
            with saved(ctx):
                ctx.set_source_rgba(0, 0, 0, 0.25)
                ctx.set_line_width(14 / k)
                ctx.stroke_preserve()
        ctx.set_source_rgb(*c)
        ctx.fill_preserve()
        ctx.set_line_width(2.5)
        ctx.stroke()
    if p.get("sub"):
        ctx.select_font_face("Jost")
        ctx.set_font_size(p.get("sub_size", 56))
        sub = p["sub"]
        x = 0
        sp = p.get("sub_spacing", 14)
        wsum = sum(ctx.text_extents(ch).x_advance + sp for ch in sub) - sp
        x = -wsum / 2
        ctx.set_source_rgb(*c)
        for ch in sub:
            ctx.move_to(x, ext.height * k * 0.5 + p.get("sub_size", 56) * 1.4)
            ctx.show_text(ch)
            x += ctx.text_extents(ch).x_advance + sp


def _jp_text(ctx, p, t):
    """Texto japonés (o cualquier texto) con fuente Noto Sans JP."""
    ctx.select_font_face("Noto Sans JP")
    ctx.set_font_size(p.get("size", 64))
    s = p.get("text", "")
    ext = ctx.text_extents(s)
    if ext.width > p.get("max_w", 960):
        ctx.set_font_size(p.get("size", 64) * p.get("max_w", 960) / ext.width)
        ext = ctx.text_extents(s)
    ctx.move_to(-ext.width / 2 - ext.x_bearing, -ext.height / 2 - ext.y_bearing)
    ctx.text_path(s)
    ctx.set_source_rgba(*INK, 0.6)
    ctx.set_line_width(10)
    ctx.stroke_preserve()
    ctx.set_source_rgb(*col(p.get("color", "#C4EDC9")))
    ctx.fill()


BACKGROUNDS.update({"comic": bg_comic, "photo": bg_photo, "clip": bg_clip})
PROPS.update({"mirror": _mirror, "pow": _pow, "logo": _logo, "jp_text": _jp_text})
