"""Overlays en espacio de pantalla (no les afecta la cámara): tarjetas de dato/ficción,
contadores, medidor de profundidad, sellos de MITO, títulos de gancho.

Zonas seguras de YouTube Shorts (1080x1920):
  - arriba ~0-160 px: barra de búsqueda/estado  → evitar
  - derecha x>930 entre y 900-1700: botones like/comentar → evitar
  - abajo y>1500: título/descripción/canal → evitar
"""
from __future__ import annotations

import math

from .draw import (INK, OUT, PAL, circle, clamp, col, darken, ease_back, ease_out, fill_stroke, lerp,
                   rrect, saved, text)

W, H = 1080, 1920


def _wrap(ctx, s: str, size: float, max_w: float, font="Lilita One") -> list[str]:
    ctx.select_font_face(font)
    ctx.set_font_size(size)
    words, lines, cur = s.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if ctx.text_extents(test).width > max_w and cur:
            lines.append(cur)
            cur = w
        else:
            cur = test
    if cur:
        lines.append(cur)
    return lines


def _card(ctx, age, dur, tag, tag_color, body, y=250, icon="check"):
    k_in = ease_back(clamp(age / 0.35))
    k_out = clamp((dur - age) / 0.2)
    s = k_in * k_out
    if s <= 0.01:
        return
    size = 56
    lines = _wrap(ctx, body, size, 780)
    h = 110 + 66 * len(lines)
    with saved(ctx):
        ctx.translate(W / 2, y + h / 2)
        ctx.scale(max(s, 1e-3), max(s, 1e-3))
        ctx.rotate(-0.02)
        ctx.translate(-W / 2, -(y + h / 2))
        rrect(ctx, 90 + 8, y + 12, 900, h, 40)
        ctx.set_source_rgba(0, 0, 0, 0.3)
        ctx.fill()
        rrect(ctx, 90, y, 900, h, 40)
        fill_stroke(ctx, (1, 1, 1), OUT)
        # etiqueta
        ctx.select_font_face("Lilita One")
        ctx.set_font_size(46)
        tw = ctx.text_extents(tag).width
        rrect(ctx, 130, y - 38, tw + 120, 76, 38)
        fill_stroke(ctx, tag_color, OUT)
        circle(ctx, 172, y, 22)
        fill_stroke(ctx, (1, 1, 1), 4)
        ctx.set_source_rgb(*col(tag_color))
        ctx.set_line_width(7)
        if icon == "check":
            ctx.move_to(161, y + 1)
            ctx.line_to(170, y + 10)
            ctx.line_to(185, y - 9)
            ctx.stroke()
        else:  # varita/estrella
            from .draw import star
            star(ctx, 172, y, 15)
            ctx.fill()
        text(ctx, tag, 205, y, 46, align="left", outline=6, shadow_off=0)
        for i, ln in enumerate(lines):
            text(ctx, ln, W / 2, y + 85 + i * 66, size, color=INK, outline=0, shadow_off=0)


def ov_fact(ctx, o, age, dur, t):
    _card(ctx, age, dur, o.get("label", "DATO REAL"), PAL["green"], o.get("text", ""), o.get("y", 230), "check")


def ov_fiction(ctx, o, age, dur, t):
    _card(ctx, age, dur, o.get("label", "FICCIÓN"), PAL["purple"], o.get("text", ""), o.get("y", 230), "star")


def ov_counter(ctx, o, age, dur, t):
    """Número que cuenta rápido hasta su valor final (p. ej. 6.371 km)."""
    a, b = float(o.get("from", 0)), float(o.get("to", 100))
    k = ease_out(clamp(age / o.get("over", 1.0)))
    v = a + (b - a) * k
    dec = int(o.get("decimals", 0))
    s = f"{v:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    label = o.get("prefix", "") + s + o.get("suffix", "")
    pop = ease_back(clamp(age / 0.3))
    y = o.get("y", 420)
    with saved(ctx):
        ctx.translate(W / 2, y)
        ctx.scale(max(pop, 1e-3), max(pop, 1e-3))
        ctx.rotate(0.03 * math.sin(t * 3))
        text(ctx, label, 0, 0, o.get("size", 150), color=o.get("color", "#FFD23F"), outline=14, max_w=950)
        if o.get("sub"):
            text(ctx, o["sub"], 0, o.get("size", 150) * 0.72, 56, color="white", outline=8, max_w=900)


def ov_depth(ctx, o, age, dur, t):
    """Medidor de profundidad (izquierda). Escala raíz cuadrada para que se vean km y miles de km."""
    total = 6371.0
    d0, d1 = float(o.get("from", 0)), float(o.get("to", 0))
    d = lerp(d0, d1, ease_out(clamp(age / o.get("over", max(0.3, dur * 0.8)))))
    x, y0, y1 = 80, 330, 1330
    slide = ease_out(clamp(age / 0.3))
    with saved(ctx):
        ctx.translate(-200 * (1 - slide), 0)
        rrect(ctx, x - 26, y0, 52, y1 - y0, 26)
        fill_stroke(ctx, (1, 1, 1), OUT)
        from .world import layer_color
        for i in range(40):
            dd0 = total * (i / 40) ** 2
            dd1 = total * ((i + 1) / 40) ** 2
            ya = y0 + 8 + (y1 - y0 - 16) * i / 40
            ctx.rectangle(x - 18, ya, 36, (y1 - y0 - 16) / 40 + 1)
            ctx.set_source_rgb(*layer_color((dd0 + dd1) / 2))
            ctx.fill()
        fy = y0 + 8 + (y1 - y0 - 16) * math.sqrt(clamp(d / total))
        ctx.move_to(x + 30, fy)
        ctx.line_to(x + 62, fy - 24)
        ctx.line_to(x + 62, fy + 24)
        ctx.close_path()
        fill_stroke(ctx, PAL["red"], 5)
        if d < 10:
            ds = f"{d:.1f}".replace(".", ",")
        else:
            ds = f"{d:,.0f}".replace(",", ".")
        rrect(ctx, x + 66, fy - 40, 300, 80, 24)
        fill_stroke(ctx, INK, 0)
        text(ctx, f"-{ds} km", x + 86, fy, 54, align="left", color="#FFD23F", outline=0, shadow_off=0)


def ov_myth(ctx, o, age, dur, t):
    """Texto tachado con sello de MITO."""
    y = o.get("y", 380)
    k = ease_back(clamp(age / 0.3))
    with saved(ctx):
        ctx.translate(W / 2, y)
        ctx.scale(max(k, 1e-3), max(k, 1e-3))
        text(ctx, o.get("text", "MAR DE LAVA"), 0, 0, 100, outline=11, max_w=880)
        ks = clamp((age - o.get("stamp_at", 0.6)) / 0.18)
        if ks > 0:
            ctx.set_line_cap(1)
            ctx.set_source_rgba(*PAL["red"], 1)
            ctx.set_line_width(22)
            ctx.move_to(-380, -60)
            ctx.line_to(lerp(-380, 380, ks), lerp(-60, 60, ks))
            ctx.stroke()
            if ks >= 1:
                ctx.rotate(-0.2)
                st = 1 + 0.6 * clamp(1 - (age - o.get("stamp_at", 0.6) - 0.18) / 0.15)
                ctx.scale(max(st, 1e-3), max(st, 1e-3))
                rrect(ctx, -170, 70, 340, 110, 20)
                ctx.set_source_rgb(*PAL["red"])
                ctx.set_line_width(12)
                ctx.stroke()
                text(ctx, o.get("stamp", "¡MITO!"), 0, 125, 84, color=PAL["red"], outline=0, shadow_off=0)


def ov_title(ctx, o, age, dur, t):
    """Título grande de gancho, palabra a palabra con rebote."""
    lines = o.get("lines") or [o.get("text", "")]
    y = o.get("y", 330)
    size = o.get("size", 120)
    for i, ln in enumerate(lines):
        k = ease_back(clamp((age - i * 0.18) / 0.3))
        if k <= 0:
            continue
        with saved(ctx):
            ctx.translate(W / 2, y + i * size * 1.05)
            ctx.scale(max(k, 1e-3), max(k, 1e-3))
            ctx.rotate(0.03 * math.sin(t * 4 + i) - 0.02)
            colr = o.get("colors", ["white", "#FFD23F", "white"])[i % 3]
            text(ctx, ln, 0, 0, size, color=colr, outline=14, max_w=960)


def ov_label(ctx, o, age, dur, t):
    """Etiqueta con fondo (texto corto con flecha opcional)."""
    k = ease_back(clamp(age / 0.3))
    x, y = o.get("x", W / 2), o.get("y", 400)
    with saved(ctx):
        ctx.translate(x, y)
        ctx.scale(max(k, 1e-3), max(k, 1e-3))
        ctx.rotate(o.get("rot", -0.03))
        size = o.get("size", 64)
        ctx.select_font_face("Lilita One")
        ctx.set_font_size(size)
        tw = min(900, ctx.text_extents(o["text"]).width)
        rrect(ctx, -tw / 2 - 36, -size * 0.75, tw + 72, size * 1.5, size * 0.4)
        fill_stroke(ctx, o.get("bg", PAL["red"]), OUT)
        text(ctx, o["text"], 0, 0, size, color=o.get("color", "white"), outline=6, shadow_off=0, max_w=900)
        if o.get("arrow") == "down":
            ctx.move_to(-30, size * 0.75)
            ctx.line_to(30, size * 0.75)
            ctx.line_to(0, size * 0.75 + 50 + 10 * math.sin(t * 8))
            ctx.close_path()
            fill_stroke(ctx, o.get("bg", PAL["red"]), OUT)


def ov_timer(ctx, o, age, dur, t):
    k = ease_back(clamp(age / 0.3))
    x, y = o.get("x", 840), o.get("y", 420)
    with saved(ctx):
        ctx.translate(x, y)
        ctx.scale(max(k, 1e-3), max(k, 1e-3))
        circle(ctx, 0, 0, 120)
        fill_stroke(ctx, (1, 1, 1), OUT)
        rrect(ctx, -25, -165, 50, 45, 10)
        fill_stroke(ctx, PAL["red"], OUT)
        prog = clamp(age / o.get("over", 1.2))
        ctx.move_to(0, 0)
        ctx.arc(0, 0, 100, -math.pi / 2, -math.pi / 2 + prog * 2 * math.pi)
        ctx.close_path()
        ctx.set_source_rgba(*PAL["green"], 0.8)
        ctx.fill()
        text(ctx, o.get("text", "5 MIN"), 0, 0, 60, outline=7, shadow_off=0, max_w=200)


def ov_flash(ctx, o, age, dur, t):
    a = clamp(1 - age / o.get("over", 0.25))
    if a > 0:
        ctx.rectangle(0, 0, W, H)
        ctx.set_source_rgba(*col(o.get("color", (1, 1, 1))), a * o.get("alpha", 0.85))
        ctx.fill()


def ov_vignette(ctx, o, age, dur, t):
    from .draw import radial_grad
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(radial_grad(ctx, W / 2, H / 2, 500, 1250,
                               [(0, (0, 0, 0), 0), (1, col(o.get("color", (0, 0, 0))), o.get("alpha", 0.5))]))
    ctx.fill()


OVERLAYS = {
    "fact": ov_fact, "fiction": ov_fiction, "counter": ov_counter, "depth": ov_depth, "myth": ov_myth,
    "title": ov_title, "label": ov_label, "timer": ov_timer, "flash": ov_flash, "vignette": ov_vignette,
}
