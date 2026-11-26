"""Catálogo «apagón mundial»: fondos nativos 16:9 (ciudad moderna que se apaga, salón, cocina, supermercado,
hospital, torres de alta tensión, tormenta solar, centro de control, metro y gasolinera) y props (torre eléctrica,
bombilla, nevera, vela, semáforo, generador, grifo, antena de móvil, batería, telégrafo, cajero, radio, ascensor,
la Tierra de noche, transformador, presa, bidón, garrafa, linterna y lata de conserva).

Los fondos se usan con `"native": True`: se dibujan directamente en coordenadas de pantalla (SW×SH), sin la franja
ampliada de los fondos verticales. Todos aceptan:
  · `lights` (0..1) y `off_at` (s): luces encendidas y momento en que se apagan, en cascada de izquierda a derecha.
  · `dark` (0..1): capa de oscuridad final; `glows`: [[x, y, r], …] huecos de luz cálida (velas, linternas).
"""
from __future__ import annotations

import math

import cairo
import numpy as np

from .draw import (INK, OUT, PAL, circle, clamp, col, darken, ellipse, fill_stroke, lerp, lighten, limb,
                   linear_grad, mix, noise1, radial_grad, rrect, saved, text)
from .screen import SH, SW
from .world import BACKGROUNDS, PROPS

MG = 160  # margen fuera de cuadro (movimientos de cámara)
WARM = (1.0, 0.78, 0.38)


# ============================================================================ utilidades
def _lit(p, t, k=0.0):
    """Factor de luz 0..1 de una fuente; `k` (0..1) retrasa su apagado dentro de la cascada."""
    base = clamp(p.get("lights", 1.0))
    off = p.get("off_at")
    if off is None:
        return base
    spread = p.get("off_spread", 1.2)
    return base * (1 - clamp((t - off - k * spread) / 0.12))


def _flicker(t, seed=1):
    return 0.85 + 0.15 * noise1(t * 11, seed)


def _fill_screen(ctx, c, a=1.0):
    ctx.rectangle(-MG, -MG, SW + 2 * MG, SH + 2 * MG)
    ctx.set_source_rgba(*col(c), a)
    ctx.fill()


def _vgrad(ctx, y0, y1, c0, c1):
    ctx.rectangle(-MG, -MG, SW + 2 * MG, SH + 2 * MG)
    ctx.set_source(linear_grad(ctx, 0, y0, 0, y1, [(0, c0), (1, c1)]))
    ctx.fill()


def _glow(ctx, x, y, r, c=WARM, a=0.55):
    circle(ctx, x, y, r)
    ctx.set_source(radial_grad(ctx, x, y, 0, r, [(0, col(c), a), (1, col(c), 0)]))
    ctx.fill()


def _darkness(ctx, p, t):
    """Oscuridad final con huecos de luz cálida (`glows`)."""
    d = clamp(p.get("dark", 0.0))
    off = p.get("dark_at")
    if off is not None:
        d *= clamp((t - off) / 0.25)
    if d <= 0:
        return
    glows = p.get("glows", [])
    ctx.push_group()
    _fill_screen(ctx, (0.03, 0.03, 0.09), d)
    ctx.set_operator(cairo.OPERATOR_DEST_OUT)
    for gx, gy, gr in glows:
        f = _flicker(t, int(gx) % 7)
        circle(ctx, gx, gy, gr * f)
        ctx.set_source(radial_grad(ctx, gx, gy, 0, gr * f, [(0, (0, 0, 0), 0.95), (0.6, (0, 0, 0), 0.5),
                                                              (1, (0, 0, 0), 0)]))
        ctx.fill()
    ctx.set_operator(cairo.OPERATOR_OVER)
    ctx.pop_group_to_source()
    ctx.paint()
    for gx, gy, gr in glows:
        _glow(ctx, gx, gy, gr * 0.8 * _flicker(t, int(gy) % 5), WARM, 0.22 * d)


def _stars(ctx, amount, seed=8, n=170, ymax=None, t=0.0):
    if amount <= 0.02:
        return
    rng = np.random.default_rng(seed)
    ymax = ymax or SH * 0.7
    for _ in range(n):
        x, y, r = rng.uniform(-MG, SW + MG), rng.uniform(-MG, ymax), rng.uniform(1.2, 3.6)
        tw = 0.7 + 0.3 * math.sin(t * rng.uniform(1, 3) + rng.uniform(0, 6))
        circle(ctx, x, y, r)
        ctx.set_source_rgba(1, 1, 0.95, amount * tw)
        ctx.fill()


def _milky_way(ctx, amount, t=0.0):
    """Banda de la Vía Láctea en diagonal."""
    if amount <= 0.02:
        return
    with saved(ctx):
        ctx.translate(SW * 0.5, SH * 0.25)
        ctx.rotate(-0.38)
        for k, (w, a) in enumerate(((260, 0.10), (170, 0.12), (90, 0.12))):
            ellipse(ctx, 0, 0, 1500, w)
            ctx.set_source_rgba(0.75, 0.7, 1.0, a * amount)
            ctx.fill()
        rng = np.random.default_rng(77)
        for _ in range(650):
            x, y = rng.uniform(-1400, 1400), rng.normal(0, 85)
            circle(ctx, x, y, rng.uniform(0.8, 2.4))
            ctx.set_source_rgba(1, 1, 1, amount * rng.uniform(0.35, 0.95))
            ctx.fill()
        for _ in range(9):  # polvo oscuro
            ellipse(ctx, rng.uniform(-1100, 1100), rng.normal(0, 20), rng.uniform(80, 200), 16)
            ctx.set_source_rgba(0.05, 0.04, 0.12, 0.35 * amount)
            ctx.fill()


def _skyline(ctx, p, t, base, hmin, hmax, seed, color, win=(1, 0.86, 0.45), wmin=110, wmax=230, gap=10,
             win_frac=0.55):
    """Edificios con ventanas encendidas según `_lit` (cascada por posición x)."""
    rng = np.random.default_rng(seed)
    x = -MG
    while x < SW + MG:
        w, h = rng.uniform(wmin, wmax), rng.uniform(hmin, hmax)
        k = clamp((x + MG) / (SW + 2 * MG))
        lit = _lit(p, t, k)
        rrect(ctx, x, base - h, w, h + 400, 4)
        fill_stroke(ctx, color, OUT * 0.6)
        if rng.random() < 0.3:  # antena
            limb(ctx, [(x + w / 2, base - h), (x + w / 2, base - h - 50)], 5, darken(color, 0.2), out=0)
            circle(ctx, x + w / 2, base - h - 52, 6)
            ctx.set_source_rgba(1, 0.2, 0.2, 0.9 * lit * (0.5 + 0.5 * math.sin(t * 4 + x)))
            ctx.fill()
        cols = max(1, int((w - 24) / 34))
        for wy in np.arange(base - h + 22, base - 26, 46):
            for c in range(cols):
                wx = x + 14 + c * (w - 28) / cols
                on = rng.random() < win_frac
                ctx.rectangle(wx, wy, (w - 28) / cols - 10, 26)
                if on and lit > 0:
                    ctx.set_source_rgba(*win, 0.9 * lit)
                else:
                    ctx.set_source_rgba(*darken(color, 0.35), 1)
                ctx.fill()
        x += w + gap


def _streetlamp(ctx, x, ground, lit, h=420):
    limb(ctx, [(x, ground), (x, ground - h), (x + 70, ground - h - 20)], 14, (0.22, 0.24, 0.3), out=OUT * 0.5)
    rrect(ctx, x + 40, ground - h - 34, 80, 24, 10)
    fill_stroke(ctx, mix((0.45, 0.45, 0.5), (1, 0.95, 0.7), lit), OUT * 0.5)
    if lit > 0:
        ctx.move_to(x + 50, ground - h - 12)
        ctx.line_to(x + 110, ground - h - 12)
        ctx.line_to(x + 260, ground)
        ctx.line_to(x - 100, ground)
        ctx.close_path()
        ctx.set_source(linear_grad(ctx, 0, ground - h, 0, ground, [(0, (1, 0.92, 0.6)), (1, (1, 0.92, 0.6))]))
        ctx.set_source_rgba(1, 0.92, 0.6, 0.12 * lit)
        ctx.fill()


def _window(ctx, x, y, w, h, p, t, night=True):
    """Ventana con la ciudad detrás (se apaga con la misma cascada)."""
    rrect(ctx, x, y, w, h, 10)
    fill_stroke(ctx, (0.95, 0.95, 0.98), OUT)
    with saved(ctx):
        ctx.rectangle(x + 16, y + 16, w - 32, h - 32)
        ctx.clip()
        if night:
            ctx.rectangle(x, y, w, h)
            ctx.set_source(linear_grad(ctx, 0, y, 0, y + h, [(0, (0.06, 0.06, 0.2)), (1, (0.2, 0.15, 0.36))]))
            ctx.fill()
            lit = _lit(p, t, 0.5)
            with saved(ctx):
                ctx.translate(x, y)
                _stars(ctx, 1 - lit, seed=3, n=40, ymax=h * 0.6, t=t)
                ctx.scale(w / SW, h / SH * 1.4)
                ctx.translate(0, -SH * 0.35)
                _skyline(ctx, p, t, SH, 260, 620, 12, (0.16, 0.14, 0.3), wmin=140, wmax=260, gap=14)
        else:
            ctx.rectangle(x, y, w, h)
            ctx.set_source(linear_grad(ctx, 0, y, 0, y + h, [(0, PAL["sky_top"]), (1, PAL["sky_bot"])]))
            ctx.fill()
            with saved(ctx):
                ctx.translate(x, y)
                ctx.scale(w / SW, h / SH * 1.4)
                ctx.translate(0, -SH * 0.35)
                _skyline(ctx, {"lights": 0}, t, SH, 260, 620, 12, (0.62, 0.66, 0.78), wmin=140, wmax=260, gap=14)
    ctx.move_to(x + w / 2, y + 10)
    ctx.line_to(x + w / 2, y + h - 10)
    ctx.move_to(x + 10, y + h / 2)
    ctx.line_to(x + w - 10, y + h / 2)
    ctx.set_source_rgb(0.95, 0.95, 0.98)
    ctx.set_line_width(14)
    ctx.stroke()


def _ceiling_lamp(ctx, x, lit, y1=120, kind="pendant"):
    if kind == "pendant":
        limb(ctx, [(x, -MG), (x, y1)], 6, INK, out=0)
        ctx.move_to(x - 90, y1 + 70)
        ctx.line_to(x - 40, y1)
        ctx.line_to(x + 40, y1)
        ctx.line_to(x + 90, y1 + 70)
        ctx.close_path()
        fill_stroke(ctx, "#F2EAD6", OUT * 0.8)
        circle(ctx, x, y1 + 74, 26)
        fill_stroke(ctx, mix((0.55, 0.55, 0.6), (1, 0.95, 0.7), lit), OUT * 0.6)
        if lit > 0:
            _glow(ctx, x, y1 + 80, 420, (1, 0.93, 0.7), 0.35 * lit)
    else:  # tubo fluorescente
        rrect(ctx, x - 170, y1, 340, 30, 14)
        fill_stroke(ctx, mix((0.6, 0.62, 0.68), (0.95, 1, 1), lit), OUT * 0.6)
        if lit > 0:
            _glow(ctx, x, y1 + 15, 330, (0.9, 1, 1), 0.22 * lit)


def _floor(ctx, y, c1, c2, tiles=True):
    ctx.rectangle(-MG, y, SW + 2 * MG, SH - y + MG)
    ctx.set_source(linear_grad(ctx, 0, y, 0, SH, [(0, col(c1)), (1, col(c2))]))
    ctx.fill()
    if tiles:
        for k in range(-12, 13):
            ctx.move_to(SW / 2 + k * 90, y)
            ctx.line_to(SW / 2 + k * 260, SH + MG)
        for yy in (y + 40, y + 100, y + 190):
            ctx.move_to(-MG, yy)
            ctx.line_to(SW + MG, yy)
        ctx.set_source_rgba(0, 0, 0, 0.08)
        ctx.set_line_width(3)
        ctx.stroke()
    ctx.move_to(-MG, y)
    ctx.line_to(SW + MG, y)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(OUT * 0.8)
    ctx.stroke()


# ============================================================================ FONDOS
def bg_modern_city(ctx, t, p):
    """Ciudad moderna (día o noche) con avenida; de noche las luces se apagan en cascada con `off_at`."""
    day = p.get("day", False)
    ground = p.get("ground", 860)
    if day:
        _vgrad(ctx, -MG, ground, PAL["sky_top"], PAL["sky_bot"])
        _glow(ctx, 1600, 170, 230, (1, 1, 0.8), 0.6)
        circle(ctx, 1600, 170, 80)
        fill_stroke(ctx, "#FFE070", OUT)
        lit_mean = 0.0
    else:
        _vgrad(ctx, -MG, ground, (0.04, 0.04, 0.14), (0.2, 0.14, 0.34))
        lit_mean = _lit(p, t, 0.5)
        dark_sky = clamp(1 - lit_mean)
        _milky_way(ctx, p.get("milky", 0.0) * dark_sky, t)
        _stars(ctx, max(p.get("stars", 0.25), dark_sky), seed=4, t=t)
        if p.get("moon", True):
            circle(ctx, 1650, 150, 60)
            fill_stroke(ctx, (1, 0.97, 0.85), OUT * 0.7)
        # resplandor de la ciudad
        ctx.set_source(linear_grad(ctx, 0, ground - 400, 0, ground, [(0, (1, 0.6, 0.3), 0.0), (1, (1, 0.55, 0.3), 0.35 * lit_mean)]))
        ctx.rectangle(-MG, ground - 400, SW + 2 * MG, 400)
        ctx.fill()
    far = (0.62, 0.66, 0.8) if day else (0.13, 0.12, 0.27)
    near = (0.5, 0.55, 0.72) if day else (0.2, 0.18, 0.36)
    q = p if not day else {"lights": 0}
    _skyline(ctx, q, t, ground, 220, 560, 21, far, wmin=90, wmax=170, gap=8, win_frac=0.5)
    _skyline(ctx, q, t, ground, 120, 330, 5, near, wmin=180, wmax=300, gap=26, win_frac=0.6)
    # acera y avenida
    ctx.rectangle(-MG, ground, SW + 2 * MG, 60)
    fill_stroke(ctx, (0.62, 0.62, 0.68) if day else (0.3, 0.3, 0.38), OUT * 0.7)
    ctx.rectangle(-MG, ground + 60, SW + 2 * MG, SH)
    ctx.set_source_rgb(*((0.33, 0.34, 0.4) if day else (0.15, 0.15, 0.22)))
    ctx.fill()
    for x in range(-MG, SW + MG, 220):
        rrect(ctx, x, ground + 150, 120, 14, 6)
        ctx.set_source_rgba(1, 1, 1, 0.75 if day else 0.4)
        ctx.fill()
    if p.get("crosswalk", True):
        for k in range(7):
            rrect(ctx, 780 + k * 60, ground + 70, 38, 160, 4)
            ctx.set_source_rgba(1, 1, 1, 0.8 if day else 0.35)
            ctx.fill()
    if not day:
        for i, x in enumerate((180, 1380)):
            _streetlamp(ctx, x, ground + 20, _lit(p, t, x / SW))
    _darkness(ctx, p, t)


def bg_living_room(ctx, t, p):
    """Salón de noche: ventana a la ciudad, sofá, tele y lámpara de pie."""
    lit = _lit(p, t, 0.0)
    _fill_screen(ctx, mix("#3A3F78", "#F4D9A8", max(0.82 * lit, 0.68 if p.get("day") else 0)))
    # zócalo y suelo de madera
    _floor(ctx, 880, "#9A6A40", "#6E4A2C", tiles=False)
    for k in range(10):
        ctx.move_to(-MG + k * 260, 880)
        ctx.line_to(-MG + k * 260 - 120, SH + MG)
    ctx.set_source_rgba(0, 0, 0, 0.12)
    ctx.set_line_width(3)
    ctx.stroke()
    _window(ctx, 1080, 120, 640, 520, p, t, night=not p.get("day", False))
    # cuadro
    rrect(ctx, 220, 170, 300, 210, 8)
    fill_stroke(ctx, "#FFD23F", OUT)
    ctx.move_to(250, 350)
    ctx.line_to(330, 250)
    ctx.line_to(400, 320)
    ctx.line_to(450, 270)
    ctx.line_to(490, 350)
    ctx.close_path()
    fill_stroke(ctx, "#4E9A3A", OUT * 0.5)
    # mueble y tele
    rrect(ctx, 1150, 760, 520, 120, 12)
    fill_stroke(ctx, "#6A4A30", OUT)
    rrect(ctx, 1210, 470, 400, 260, 14)
    fill_stroke(ctx, (0.1, 0.1, 0.14), OUT)
    tv = lit * p.get("tv", 1.0)
    rrect(ctx, 1228, 488, 364, 224, 6)
    if tv > 0:
        ctx.set_source(linear_grad(ctx, 0, 488, 0, 712, [(0, (0.35, 0.7, 1.0)), (1, (0.75, 0.4, 1.0))]))
        ctx.fill()
        text(ctx, "▶", 1410, 600, 90, color=(1, 1, 1), outline=0, shadow_off=0, alpha=tv)
    else:
        ctx.set_source_rgb(0.05, 0.05, 0.08)
        ctx.fill()
    limb(ctx, [(1410, 730), (1410, 760)], 30, (0.1, 0.1, 0.14), out=OUT * 0.5)
    # lámpara de pie
    limb(ctx, [(160, 880), (160, 420)], 12, INK, out=0)
    ctx.move_to(70, 430)
    ctx.line_to(110, 330)
    ctx.line_to(210, 330)
    ctx.line_to(250, 430)
    ctx.close_path()
    fill_stroke(ctx, mix("#C9B79A", "#FFF1C9", lit), OUT * 0.8)
    if lit > 0:
        _glow(ctx, 160, 430, 380, WARM, 0.35 * lit)
    # sofá (detrás de Leo, a la izquierda)
    if p.get("sofa", True):
        rrect(ctx, 330, 600, 620, 220, 50)
        fill_stroke(ctx, "#C0392B", OUT)
        rrect(ctx, 300, 720, 680, 170, 40)
        fill_stroke(ctx, "#D84A3A", OUT)
        for x in (300, 900):
            rrect(ctx, x, 660, 80, 230, 36)
            fill_stroke(ctx, "#B03428", OUT)
    _darkness(ctx, p, t)


def bg_kitchen(ctx, t, p):
    """Cocina: azulejos, armarios, encimera, horno con reloj digital y ventana; hueco a la derecha para la nevera."""
    lit = _lit(p, t, 0.0)
    _fill_screen(ctx, mix("#2E3466", "#F7EBD0", max(0.9 * lit, 0.72 if p.get("day") else 0)))
    for x in range(-MG, 1300, 70):  # azulejos
        for y in range(380, 640, 70):
            rrect(ctx, x + 4, y + 4, 62, 62, 6)
            ctx.set_source_rgba(1, 1, 1, 0.25)
            ctx.fill()
    _window(ctx, 470, 90, 420, 280, p, t, night=not p.get("day", False))
    for x in (-60, 180, 960):  # armarios altos
        rrect(ctx, x, 60, 220, 270, 10)
        fill_stroke(ctx, "#5BA4A0", OUT)
        circle(ctx, x + 190, 300, 8)
        fill_stroke(ctx, "#F2EAD6", OUT * 0.4)
    # encimera y muebles bajos
    rrect(ctx, -MG, 640, 1360 + MG, 40, 6)
    fill_stroke(ctx, "#E9E2D4", OUT)
    for x in range(-MG + 20, 1220, 230):
        rrect(ctx, x, 680, 220, 300, 10)
        fill_stroke(ctx, "#4E918D", OUT)
        rrect(ctx, x + 70, 700, 80, 14, 7)
        fill_stroke(ctx, "#F2EAD6", OUT * 0.4)
    # horno con reloj
    rrect(ctx, 700, 690, 300, 290, 12)
    fill_stroke(ctx, (0.85, 0.86, 0.9), OUT)
    rrect(ctx, 730, 770, 240, 170, 10)
    fill_stroke(ctx, (0.15, 0.15, 0.2), OUT * 0.7)
    rrect(ctx, 790, 705, 120, 50, 8)
    fill_stroke(ctx, (0.08, 0.08, 0.1), OUT * 0.6)
    if lit > 0:
        text(ctx, p.get("clock", "12:33"), 850, 730, 36, color=(0.3, 1, 0.5), outline=0, shadow_off=0, alpha=lit)
    elif p.get("blink"):
        if (t * 2) % 1 < 0.5:
            text(ctx, "00:00", 850, 730, 36, color=(0.3, 1, 0.5), outline=0, shadow_off=0)
    # fogones
    for x in (-40, 120):
        ellipse(ctx, x, 645, 60, 10)
        ctx.set_source_rgb(0.2, 0.2, 0.25)
        ctx.fill()
    _floor(ctx, 980, "#D9CBB0", "#B8A588")
    _ceiling_lamp(ctx, 680, lit, y1=-40)
    _darkness(ctx, p, t)


def bg_supermarket(ctx, t, p):
    """Pasillo de supermercado: estanterías con `stock` (0..1), tubos fluorescentes y señal de salida."""
    lit = _lit(p, t, 0.0)
    _fill_screen(ctx, mix("#33395E", "#EEF2F7", 0.75 * lit))
    rng = np.random.default_rng(14)
    stock = clamp(p.get("stock", 1.0))
    colors = ["#E8392F", "#FFD23F", "#22B573", "#3B82F6", "#FF8A3D", "#B388FF", "#F2EAD6", "#5CE1E6"]
    # dos estanterías enfrentadas en perspectiva + fondo
    for side in (-1, 1):
        x_out, x_in = (SW / 2 + side * 1200, SW / 2 + side * 330)
        for k, (y_out, y_in) in enumerate(((60, 300), (300, 430), (540, 560), (780, 690))):
            ctx.move_to(x_out, y_out)
            ctx.line_to(x_in, y_in)
            ctx.line_to(x_in, y_in + 14)
            ctx.line_to(x_out, y_out + 36)
            ctx.close_path()
            fill_stroke(ctx, "#C9CED8", OUT * 0.6)
            # productos sobre la balda
            n = 14
            for i in range(n):
                f0, f1 = i / n, (i + 0.8) / n
                if rng.random() > stock:
                    continue
                xa, xb = lerp(x_out, x_in, f0), lerp(x_out, x_in, f1)
                ya, yb = lerp(y_out, y_in, f0), lerp(y_out, y_in, f1)
                h = lerp(150, 80, (f0 + f1) / 2) * rng.uniform(0.7, 1.0)
                ctx.move_to(xa, ya)
                ctx.line_to(xb, yb)
                ctx.line_to(xb, yb - h * lerp(1, 0.55, f1))
                ctx.line_to(xa, ya - h * lerp(1, 0.55, f0))
                ctx.close_path()
                fill_stroke(ctx, colors[int(rng.integers(0, len(colors)))], OUT * 0.4)
        ctx.move_to(x_in, 260)
        ctx.line_to(x_in, 900)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(OUT * 0.6)
        ctx.stroke()
    # fondo: congeladores con puertas de cristal
    rrect(ctx, SW / 2 - 330, 300, 660, 400, 10)
    fill_stroke(ctx, (0.8, 0.9, 0.96) if lit else (0.25, 0.3, 0.4), OUT * 0.8)
    for k in range(4):
        rrect(ctx, SW / 2 - 310 + k * 160, 320, 140, 360, 6)
        ctx.set_source_rgba(*(0.6, 0.85, 1) if lit else (0.15, 0.2, 0.3), 0.6)
        ctx.fill()
    _floor(ctx, 860, "#DDE3EA", "#AEB7C4")
    # cartel de ofertas y techo
    for x in (SW / 2 - 700, SW / 2 + 700):
        _ceiling_lamp(ctx, x, lit, y1=20, kind="tube")
    _ceiling_lamp(ctx, SW / 2, lit, y1=150, kind="tube")
    if p.get("sign", True):
        rrect(ctx, SW / 2 - 160, 210, 320, 70, 14)
        fill_stroke(ctx, "#E8392F", OUT * 0.7)
        text(ctx, p.get("sign_text", "OFERTAS"), SW / 2, 245, 44, color="white", outline=0, shadow_off=0)
    # salida de emergencia (siempre encendida, va con batería)
    rrect(ctx, 1560, 140, 200, 70, 10)
    fill_stroke(ctx, "#1FA35A", OUT * 0.6)
    text(ctx, "SALIDA", 1660, 175, 40, color="white", outline=0, shadow_off=0)
    _darkness(ctx, p, t)
    if p.get("dark", 0) > 0:
        _glow(ctx, 1660, 175, 200, (0.3, 1, 0.5), 0.25)


def bg_hospital(ctx, t, p):
    """Habitación de hospital: cama, monitor con electro, gotero; `backup` tiñe la luz de ámbar (generador)."""
    lit = _lit(p, t, 0.0)
    backup = p.get("backup", False)
    wall = mix("#2E4A5A", "#CFEDE6", 0.75 * lit)
    _fill_screen(ctx, wall)
    ctx.rectangle(-MG, 520, SW + 2 * MG, 30)
    ctx.set_source_rgba(1, 1, 1, 0.35)
    ctx.fill()
    _window(ctx, 120, 110, 460, 330, p, t, night=not p.get("day", True))
    _floor(ctx, 880, "#B8D6D2", "#8AAEB0")
    # cama
    rrect(ctx, 1020, 560, 40, 340, 10)
    fill_stroke(ctx, PAL["metal"], OUT * 0.7)
    rrect(ctx, 1030, 640, 760, 110, 26)
    fill_stroke(ctx, (1, 1, 1), OUT)
    rrect(ctx, 1040, 600, 220, 70, 30)
    fill_stroke(ctx, "#EAF4FF", OUT * 0.7)
    rrect(ctx, 1280, 610, 520, 90, 30)
    fill_stroke(ctx, "#7FB8E6", OUT * 0.8)
    for x in (1070, 1740):
        limb(ctx, [(x, 750), (x, 880)], 14, PAL["metal_dk"], out=OUT * 0.5)
        circle(ctx, x, 890, 16)
        fill_stroke(ctx, INK, 0)
    # monitor con electrocardiograma
    limb(ctx, [(880, 880), (880, 400)], 12, PAL["metal_dk"], out=OUT * 0.5)
    rrect(ctx, 760, 220, 260, 190, 16)
    fill_stroke(ctx, (0.15, 0.17, 0.22), OUT)
    rrect(ctx, 780, 240, 220, 150, 8)
    ctx.set_source_rgb(0.02, 0.06, 0.05)
    ctx.fill()
    on = p.get("monitor", True)
    if on:
        ctx.move_to(785, 320)
        for i in range(60):
            x = 785 + i * 3.6
            ph = ((i / 60) * 2 - t * 0.9) % 1
            y = 320
            if 0.45 < ph < 0.5:
                y = 320 - 60 * math.sin((ph - 0.45) / 0.05 * math.pi)
            elif 0.5 < ph < 0.55:
                y = 320 + 25 * math.sin((ph - 0.5) / 0.05 * math.pi)
            ctx.line_to(x, y)
        ctx.set_source_rgb(0.3, 1, 0.5)
        ctx.set_line_width(4)
        ctx.stroke()
        text(ctx, "72", 960, 260, 30, color=(0.3, 1, 0.5), outline=0, shadow_off=0)
    # gotero
    limb(ctx, [(1880, 880), (1880, 230)], 8, PAL["metal_dk"], out=OUT * 0.4)
    rrect(ctx, 1830, 240, 70, 110, 20)
    fill_stroke(ctx, (0.85, 0.95, 1), OUT * 0.6)
    # luz de techo
    _ceiling_lamp(ctx, 1250, lit if not backup else 0.6, y1=20, kind="tube")
    if backup:
        _fill_screen(ctx, (1, 0.6, 0.2), 0.12)
        on2 = 0.5 + 0.5 * math.sin(t * 5)
        rrect(ctx, 1380, 60, 380, 90, 16)
        fill_stroke(ctx, (1, 0.55, 0.1), OUT * 0.7)
        text(ctx, "GENERADOR", 1570, 105, 52, color="white", outline=0, shadow_off=0)
        _glow(ctx, 1570, 105, 260, (1, 0.6, 0.1), 0.35 * on2)
    _darkness(ctx, p, t)


def _pylon_shape(ctx, x, base, h, c=(0.35, 0.38, 0.45), lw=1.0):
    """Torre de celosía; devuelve los puntos de amarre de los cables."""
    w = h * 0.32
    top = base - h
    legs = [(x - w / 2, base), (x - w * 0.08, top + h * 0.12), (x + w * 0.08, top + h * 0.12), (x + w / 2, base)]
    ctx.set_source_rgb(*col(c))
    ctx.set_line_width(max(1.5, 7 * lw))
    ctx.move_to(*legs[0])
    ctx.line_to(*legs[1])
    ctx.line_to(x, top)
    ctx.line_to(*legs[2])
    ctx.line_to(*legs[3])
    ctx.stroke()
    n = 7
    for i in range(n):  # celosía
        f0, f1 = i / n, (i + 1) / n
        ya, yb = lerp(base, top + h * 0.12, f0), lerp(base, top + h * 0.12, f1)
        wa, wb = lerp(w / 2, w * 0.08, f0), lerp(w / 2, w * 0.08, f1)
        ctx.move_to(x - wa, ya)
        ctx.line_to(x + wb, yb)
        ctx.move_to(x + wa, ya)
        ctx.line_to(x - wb, yb)
    ctx.set_line_width(max(1, 3.5 * lw))
    ctx.stroke()
    arms = []
    for k, (yf, aw) in enumerate(((0.2, 0.42), (0.38, 0.5))):
        y = top + h * yf
        ctx.move_to(x - h * aw * 0.5, y)
        ctx.line_to(x + h * aw * 0.5, y)
        ctx.set_line_width(max(1.5, 8 * lw))
        ctx.stroke()
        arms += [(x - h * aw * 0.5, y + 8 * lw), (x + h * aw * 0.5, y + 8 * lw)]
    return arms


def bg_grid_field(ctx, t, p):
    """Campo con una línea de alta tensión que se pierde en el horizonte; `aurora`, `sparks`, `night`."""
    night = p.get("night", False)
    hz = 700
    if night:
        _vgrad(ctx, -MG, hz, (0.03, 0.04, 0.14), (0.14, 0.12, 0.3))
        _stars(ctx, 0.9, seed=9, t=t, ymax=hz)
    else:
        _vgrad(ctx, -MG, hz, (0.98, 0.58, 0.35), (1.0, 0.85, 0.6))
        sx = p.get("sun_x", 1760)
        _glow(ctx, sx, 600, 260, (1, 0.9, 0.6), 0.6)
        circle(ctx, sx, 630, 70)
        fill_stroke(ctx, "#FFD45A", OUT * 0.7)
    a = clamp(p.get("aurora", 0.0))
    if a > 0:
        for k, (c, y0) in enumerate((((0.3, 1, 0.55), 160), ((0.6, 0.4, 1), 80), ((0.3, 1, 0.7), 260))):
            ctx.move_to(-MG, y0)
            pts = []
            for i in range(0, SW + 2 * MG + 1, 40):
                x = -MG + i
                y = y0 + 60 * math.sin(x * 0.004 + t * 0.8 + k) + 30 * math.sin(x * 0.011 - t * 1.3)
                pts.append((x, y))
            for x, y in pts:
                ctx.line_to(x, y)
            for x, y in reversed(pts):
                ctx.line_to(x, y + 260 + 60 * math.sin(x * 0.006 + k))
            ctx.close_path()
            g = cairo.LinearGradient(0, y0 - 60, 0, y0 + 330)
            g.add_color_stop_rgba(0, *c, 0.0)
            g.add_color_stop_rgba(0.35, *c, 0.55 * a)
            g.add_color_stop_rgba(1, *c, 0.0)
            ctx.set_source(g)
            ctx.fill()
    # colinas
    for k, (y, c) in enumerate(((hz, "#5E8C4A" if not night else "#1E3326"), (hz + 90, "#6FA052" if not night else "#24402C"))):
        ctx.move_to(-MG, y + 40)
        for x in range(-MG, SW + MG + 1, 60):
            ctx.line_to(x, y + 30 * math.sin(x * 0.004 + k * 2))
        ctx.line_to(SW + MG, SH + MG)
        ctx.line_to(-MG, SH + MG)
        ctx.close_path()
        fill_stroke(ctx, c, OUT * 0.6)
    # pueblo al fondo
    tl = _lit(p, t, 0.6) * p.get("town", 1.0 if night else 0.0)
    rng = np.random.default_rng(6)
    for i in range(26):
        x = 1050 + i * 28 + rng.uniform(-8, 8)
        y = hz + 10 + rng.uniform(-6, 10)
        rrect(ctx, x, y - 16, 20, 18, 3)
        ctx.set_source_rgb(*((0.12, 0.14, 0.2) if night else (0.85, 0.78, 0.7)))
        ctx.fill()
        if tl > 0:
            circle(ctx, x + 10, y - 7, 5)
            ctx.set_source_rgba(1, 0.85, 0.45, tl)
            ctx.fill()
    # torres de mayor a menor
    towers = [(330, 990, 780, 1.0), (980, 830, 420, 0.55), (1350, 760, 240, 0.33), (1590, 728, 140, 0.2),
              (1740, 712, 80, 0.12)]
    prev = None
    c = (0.28, 0.3, 0.38) if not night else (0.55, 0.58, 0.7)
    for x, base, h, lw in towers:
        arms = _pylon_shape(ctx, x, base, h, c, lw)
        if prev:
            for (ax, ay), (bx, by) in zip(prev, arms):
                ctx.move_to(ax, ay)
                mx, my = (ax + bx) / 2, max(ay, by) + 60 * lw + 30
                ctx.curve_to(lerp(ax, mx, 0.6), my, lerp(bx, mx, 0.6), my, bx, by)
            ctx.set_source_rgb(*darken(c, 0.2))
            ctx.set_line_width(max(1.2, 4 * lw))
            ctx.stroke()
        prev = arms
    if p.get("sparks"):
        for i, (ax, ay) in enumerate(_pylon_shape(ctx, 330, 990, 780, c, 1.0)):
            ph = (t * 2.5 + i * 0.37) % 1
            if ph < 0.35:
                _glow(ctx, ax, ay, 120, (0.6, 0.85, 1), 0.8 * (1 - ph / 0.35))
                for j in range(6):
                    ang = j * 1.05 + t * 7
                    ctx.move_to(ax, ay)
                    ctx.line_to(ax + 60 * math.cos(ang), ay + 60 * math.sin(ang))
                ctx.set_source_rgba(0.85, 0.95, 1, 0.9)
                ctx.set_line_width(4)
                ctx.stroke()
    _darkness(ctx, p, t)


def bg_solar_storm(ctx, t, p):
    """El Sol (izquierda) lanza una eyección de masa coronal hacia la Tierra (derecha) y su campo magnético."""
    _vgrad(ctx, -MG, SH + MG, (0.02, 0.02, 0.1), (0.08, 0.04, 0.2))
    _stars(ctx, 0.8, seed=31, t=t, ymax=SH + MG)
    sx, sy, sr = p.get("sun_x", -60), SH / 2, 430
    _glow(ctx, sx, sy, sr * 1.8, (1, 0.6, 0.15), 0.6)
    circle(ctx, sx, sy, sr)
    ctx.set_source(radial_grad(ctx, sx, sy, sr * 0.2, sr, [(0, (1, 0.95, 0.5), 1), (1, (1, 0.55, 0.1), 1)]))
    ctx.fill_preserve()
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(OUT)
    ctx.stroke()
    rng = np.random.default_rng(2)
    for _ in range(26):  # manchas y granulación
        a, r = rng.uniform(-1.3, 1.3), rng.uniform(0.2, 0.9) * sr
        circle(ctx, sx + r * math.cos(a), sy + r * math.sin(a), rng.uniform(8, 26))
        ctx.set_source_rgba(0.75, 0.3, 0.05, 0.45)
        ctx.fill()
    for k, a in enumerate((-0.7, 0.15, 0.85)):  # protuberancias
        x0, y0 = sx + sr * math.cos(a - 0.12), sy + sr * math.sin(a - 0.12)
        x1, y1 = sx + sr * math.cos(a + 0.12), sy + sr * math.sin(a + 0.12)
        hh = 120 + 30 * math.sin(t * 2 + k)
        cx, cy = sx + (sr + hh) * math.cos(a), sy + (sr + hh) * math.sin(a)
        ctx.move_to(x0, y0)
        ctx.curve_to(cx - 40, cy - 40, cx + 40, cy + 40, x1, y1)
        ctx.set_source_rgba(1, 0.45, 0.1, 0.9)
        ctx.set_line_width(16)
        ctx.stroke()
    ex, ey, er = p.get("earth_x", 1640), SH / 2, 120
    # eyección de masa coronal: frentes que viajan hacia la Tierra
    if p.get("cme", True):
        spd = p.get("speed", 0.5)
        for k in range(3):
            ph = (t * spd + k / 3) % 1
            r = sr + ph * (ex - sx - sr - 40)
            a = 0.85 * (1 - ph * 0.5)
            ctx.arc(sx, sy, r, -a * 0.55, a * 0.55)
            ctx.set_source_rgba(1, 0.65, 0.25, 0.75 * (1 - ph))
            ctx.set_line_width(30 * (1 - ph) + 8)
            ctx.stroke()
        for i in range(70):  # partículas
            ph = (t * spd * 1.3 + i / 70) % 1
            yy = sy + (i * 37 % 300 - 150) * (0.4 + ph)
            xx = sx + sr + ph * (ex - sx - sr)
            circle(ctx, xx, yy, 4)
            ctx.set_source_rgba(1, 0.85, 0.5, 0.8 * (1 - ph * 0.6))
            ctx.fill()
    # magnetosfera (líneas de campo comprimidas del lado del Sol)
    comp = 0.55 if p.get("impact") else 1.0
    for k in range(1, 5):
        r = er * (1.2 + k * 0.55)
        ctx.save()
        ctx.translate(ex, ey)
        for side, sc in ((-1, comp), (1, 1.6)):
            ctx.save()
            ctx.scale(side * sc, 1)
            ctx.move_to(0, -er * 0.9)
            ctx.curve_to(r * 1.2, -r * 1.1, r * 1.2, r * 1.1, 0, er * 0.9)
            ctx.restore()
        ctx.restore()
        ctx.set_source_rgba(0.45, 0.75, 1, 0.55)
        ctx.set_line_width(4)
        ctx.stroke()
    circle(ctx, ex, ey, er)
    ctx.set_source(radial_grad(ctx, ex - 30, ey - 30, 10, er, [(0, (0.4, 0.7, 1), 1), (1, (0.15, 0.4, 0.85), 1)]))
    ctx.fill_preserve()
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(OUT)
    ctx.stroke()
    with saved(ctx):
        circle(ctx, ex, ey, er)
        ctx.clip()
        for cx, cy, rx, ry in ((-40, -30, 50, 35), (40, 40, 45, 30), (60, -50, 30, 20)):
            ellipse(ctx, ex + cx, ey + cy, rx, ry)
            ctx.set_source_rgb(0.3, 0.7, 0.35)
            ctx.fill()
    if p.get("impact"):
        for s in (-1, 1):  # óvalos aurorales
            ellipse(ctx, ex, ey + s * er * 0.85, er * 0.55, 14)
            ctx.set_source_rgba(0.3, 1, 0.55, 0.6 + 0.3 * math.sin(t * 6))
            ctx.set_line_width(8)
            ctx.stroke()
    _darkness(ctx, p, t)


def bg_control_room(ctx, t, p):
    """Centro de control de la red: videowall con el mapa de la red; `restored` (0..1) la va poniendo en verde."""
    _fill_screen(ctx, (0.1, 0.12, 0.2))
    rrect(ctx, 160, 60, 1600, 560, 18)
    fill_stroke(ctx, (0.05, 0.07, 0.12), OUT)
    rng = np.random.default_rng(12)
    nodes = [(rng.uniform(260, 1660), rng.uniform(120, 560)) for _ in range(28)]
    rest = p.get("restored", 1.0)
    if isinstance(rest, (list, tuple)):  # [desde, hasta, segundos]
        rest = lerp(rest[0], rest[1], clamp(t / rest[2]))
    state = p.get("state", "mixed")
    edges = []
    for i, (x, y) in enumerate(nodes):
        d = sorted(range(len(nodes)), key=lambda j: (nodes[j][0] - x) ** 2 + (nodes[j][1] - y) ** 2)
        for j in d[1:3]:
            edges.append((i, j))
    for i, j in edges:
        f = nodes[i][0] / SW
        ok = state == "green" or (state == "mixed" and f < rest)
        bad = state == "red" or (state == "mixed" and not ok)
        ctx.move_to(*nodes[i])
        ctx.line_to(*nodes[j])
        if bad and state == "red":
            a = 0.5 + 0.5 * math.sin(t * 6 + i)
            ctx.set_source_rgba(1, 0.25, 0.25, 0.5 + 0.5 * a)
        elif ok:
            ctx.set_source_rgb(0.3, 1, 0.5)
        else:
            ctx.set_source_rgba(0.4, 0.45, 0.55, 0.6)
        ctx.set_line_width(6)
        ctx.stroke()
    for i, (x, y) in enumerate(nodes):
        f = x / SW
        ok = state == "green" or (state == "mixed" and f < rest)
        circle(ctx, x, y, 14)
        fill_stroke(ctx, (0.3, 1, 0.5) if ok else ((1, 0.3, 0.3) if state == "red" else (0.45, 0.5, 0.6)), 3)
    lab = p.get("label")
    if lab:
        rrect(ctx, 760, 80, 400, 64, 12)
        fill_stroke(ctx, (0.15, 0.18, 0.28), 3)
        text(ctx, lab, 960, 112, 34, color=(0.9, 0.95, 1), outline=0, shadow_off=0)
    # mesas con monitores
    rrect(ctx, -MG, 760, SW + 2 * MG, 60, 8)
    fill_stroke(ctx, (0.25, 0.27, 0.36), OUT)
    ctx.rectangle(-MG, 820, SW + 2 * MG, SH)
    ctx.set_source_rgb(0.14, 0.15, 0.22)
    ctx.fill()
    for x in range(40, SW, 300):
        rrect(ctx, x, 640, 200, 120, 8)
        fill_stroke(ctx, (0.08, 0.08, 0.12), OUT * 0.6)
        rrect(ctx, x + 12, 652, 176, 96, 4)
        ctx.set_source_rgba(0.3, 0.6, 1, 0.5)
        ctx.fill()
    _darkness(ctx, p, t)


def bg_metro(ctx, t, p):
    """Interior de un vagón de metro: asientos, barras, ventanas al túnel; se queda a oscuras con `off_at`."""
    lit = _lit(p, t, 0.0)
    _fill_screen(ctx, mix((0.18, 0.2, 0.3), (0.86, 0.9, 0.94), lit))
    moving = p.get("moving", False) and lit > 0.5
    for x in (60, 760, 1460):
        rrect(ctx, x, 170, 440, 300, 40)
        fill_stroke(ctx, (0.06, 0.06, 0.1), OUT)
        if moving:
            for k in range(4):
                xx = x + ((k * 150 - t * 1600) % 600) - 80
                ctx.move_to(xx, 190)
                ctx.line_to(xx + 40, 450)
            ctx.set_source_rgba(1, 0.85, 0.5, 0.4)
            ctx.set_line_width(10)
            ctx.stroke()
    # asientos
    for x in (-40, 660, 1360):
        rrect(ctx, x, 560, 560, 120, 30)
        fill_stroke(ctx, "#3B82F6", OUT)
        rrect(ctx, x + 20, 660, 520, 70, 24)
        fill_stroke(ctx, "#2F6AD0", OUT)
    _floor(ctx, 860, "#5A5E6A", "#3A3D46", tiles=False)
    for x in (590, 1290):  # barras
        limb(ctx, [(x, -MG), (x, 860)], 22, PAL["metal"], out=OUT * 0.6)
    for x in range(200, SW, 480):
        _ceiling_lamp(ctx, x, lit, y1=30, kind="tube")
    if lit < 0.5:  # luz de emergencia azulada
        _glow(ctx, 960, 40, 500, (0.5, 0.7, 1), 0.2)
    _darkness(ctx, p, t)


def bg_gas_station(ctx, t, p):
    """Gasolinera: marquesina, dos surtidores con pantalla y precio; sin luz las pantallas se apagan."""
    lit = _lit(p, t, 0.0)
    _vgrad(ctx, -MG, 760, PAL["sky_top"], PAL["sky_bot"])
    _floor(ctx, 760, "#9AA0AA", "#7C828C", tiles=False)
    rrect(ctx, 80, 80, 1760, 110, 16)
    fill_stroke(ctx, "#E8392F", OUT)
    rrect(ctx, 80, 190, 1760, 26, 6)
    fill_stroke(ctx, (1, 1, 1), OUT * 0.6)
    for x in (300, 1620):
        rrect(ctx, x - 26, 216, 52, 560, 8)
        fill_stroke(ctx, (0.92, 0.92, 0.95), OUT * 0.8)
    for x in (620, 1220):
        rrect(ctx, x - 110, 380, 220, 400, 18)
        fill_stroke(ctx, (0.95, 0.95, 0.97), OUT)
        rrect(ctx, x - 80, 410, 160, 110, 10)
        fill_stroke(ctx, (0.08, 0.08, 0.1), OUT * 0.6)
        if lit > 0:
            text(ctx, p.get("price", "1,59"), x, 450, 44, color=(1, 0.75, 0.2), outline=0, shadow_off=0, alpha=lit)
            text(ctx, "€/L", x, 495, 24, color=(1, 0.75, 0.2), outline=0, shadow_off=0, alpha=lit)
        elif p.get("error"):
            text(ctx, "ERROR", x, 465, 34, color=(1, 0.3, 0.3), outline=0, shadow_off=0)
        limb(ctx, [(x + 110, 560), (x + 170, 620), (x + 170, 760)], 12, INK, out=0)
        rrect(ctx, x + 115, 540, 50, 90, 10)
        fill_stroke(ctx, "#22B573", OUT * 0.6)
        rrect(ctx, x - 60, 560, 120, 120, 10)
        fill_stroke(ctx, "#E8392F", OUT * 0.6)
    _darkness(ctx, p, t)


# ============================================================================ PROPS
def _pylon(ctx, p, t):
    arms = _pylon_shape(ctx, 0, 0, 620, p.get("color", (0.3, 0.32, 0.4)), 1.0)
    if p.get("sparks"):
        for i, (ax, ay) in enumerate(arms):
            if (t * 3 + i * 0.3) % 1 < 0.3:
                _glow(ctx, ax, ay, 90, (0.6, 0.85, 1), 0.85)


def _bulb(ctx, p, t):
    lit = _lit(p, t)
    if p.get("flicker"):
        lit *= 1.0 if noise1(t * 14, 3) > -0.2 else 0.1
    if lit > 0:
        _glow(ctx, 0, -20, 260, (1, 0.9, 0.5), 0.6 * lit)
    circle(ctx, 0, -40, 95)
    fill_stroke(ctx, mix((0.85, 0.88, 0.92), (1, 0.93, 0.55), lit), OUT)
    ctx.move_to(-30, 0)
    ctx.line_to(-15, -50)
    ctx.line_to(0, -20)
    ctx.line_to(15, -50)
    ctx.line_to(30, 0)
    ctx.set_source_rgb(*mix((0.4, 0.4, 0.45), (1, 0.6, 0.1), lit))
    ctx.set_line_width(5)
    ctx.stroke()
    rrect(ctx, -45, 40, 90, 70, 10)
    fill_stroke(ctx, PAL["metal_dk"], OUT * 0.8)
    for y in (60, 82):
        ctx.move_to(-45, y)
        ctx.line_to(45, y)
    ctx.set_line_width(4)
    ctx.stroke()


def _fridge(ctx, p, t):
    """Nevera; `open` 0..1 (o `open_at` s) abre la puerta; con `lights` 0 el interior queda a oscuras."""
    op = p.get("open", 0.0)
    if p.get("open_at") is not None:
        op = clamp((p.get("_age", t) - p["open_at"]) / 0.4)
    lit = _lit(p, t)
    rrect(ctx, -170, -560, 340, 560, 24)
    fill_stroke(ctx, (0.93, 0.95, 0.98), OUT)
    # interior
    rrect(ctx, -150, -540, 300, 520, 14)
    ctx.set_source_rgb(*mix((0.25, 0.3, 0.4), (0.9, 0.97, 1), lit))
    ctx.fill()
    for y in (-400, -270, -150):
        ctx.rectangle(-150, y, 300, 8)
        ctx.set_source_rgba(1, 1, 1, 0.6)
        ctx.fill()
    for x, y, c, w, h in ((-110, -470, "#E8392F", 60, 70), (0, -460, "#FFD23F", 90, 60), (-100, -340, "#22B573", 80, 70),
                          (30, -350, "#F2EAD6", 70, 80), (-60, -220, "#FF8A3D", 110, 70), (80, -110, "#5CE1E6", 50, 90)):
        rrect(ctx, x, y, w, h, 10)
        fill_stroke(ctx, c, OUT * 0.5)
    if lit > 0:
        _glow(ctx, 0, -500, 200, (0.9, 1, 1), 0.4 * lit)
    # puerta (gira hacia la izquierda)
    xl, xr = -170 - 170 * op, lerp(170, -170, op)
    rrect(ctx, xl, -560, max(xr - xl, 30), 560, 24)
    fill_stroke(ctx, (0.98, 0.99, 1), OUT)
    if op < 0.5:
        rrect(ctx, 120 - op * 300, -420, 18, 180, 9)
        fill_stroke(ctx, PAL["metal_dk"], OUT * 0.5)
    temp = p.get("temp")
    if temp is not None and op < 0.5:
        rrect(ctx, -110, -520, 160, 60, 10)
        fill_stroke(ctx, (0.1, 0.12, 0.18), OUT * 0.5)
        text(ctx, temp, -30, -490, 34, color=p.get("temp_color", (0.4, 0.9, 1)), outline=0, shadow_off=0)
    if p.get("drip"):
        for k in range(3):
            ph = (t * 0.8 + k / 3) % 1
            ellipse(ctx, -120 + k * 110, 10 + ph * 60, 8, 12)
            ctx.set_source_rgba(0.5, 0.8, 1, 1 - ph)
            ctx.fill()


def _candle(ctx, p, t):
    fl = _flicker(t, p.get("seed", 2))
    _glow(ctx, 0, -190, 240 * fl, WARM, 0.5)
    rrect(ctx, -38, -150, 76, 160, 12)
    fill_stroke(ctx, "#F6F0E2", OUT * 0.8)
    ellipse(ctx, 0, -150, 38, 10)
    fill_stroke(ctx, "#FFF8EA", OUT * 0.5)
    limb(ctx, [(0, -152), (0, -170)], 4, INK, out=0)
    sway = 4 * math.sin(t * 9 + p.get("seed", 2))
    ctx.move_to(0, -168)
    ctx.curve_to(-22, -190, -8 + sway, -225 * fl, sway, -245 * fl)
    ctx.curve_to(8 + sway, -225 * fl, 22, -190, 0, -168)
    fill_stroke(ctx, (1, 0.75, 0.2), OUT * 0.4)
    ellipse(ctx, 0, -185, 7, 14)
    ctx.set_source_rgb(1, 0.97, 0.75)
    ctx.fill()
    ellipse(ctx, 0, 12, 70, 14)
    fill_stroke(ctx, PAL["metal"], OUT * 0.5)


def _traffic_light(ctx, p, t):
    state = p.get("state", "off")
    off_at = p.get("off_at")
    if off_at is not None and t >= off_at:
        state = "off"
    limb(ctx, [(0, 0), (0, -330)], 26, (0.2, 0.22, 0.28), out=OUT * 0.6)
    rrect(ctx, -70, -620, 140, 320, 26)
    fill_stroke(ctx, (0.14, 0.15, 0.2), OUT)
    for k, (name, c) in enumerate((("red", (1, 0.2, 0.2)), ("amber", (1, 0.7, 0.1)), ("green", (0.2, 1, 0.45)))):
        y = -560 + k * 100
        on = state == name or (state == "blink" and name == "amber" and (t * 2) % 1 < 0.5)
        if on:
            _glow(ctx, 0, y, 120, c, 0.6)
        circle(ctx, 0, y, 38)
        fill_stroke(ctx, c if on else darken(c, 0.7), OUT * 0.6)


def _generator(ctx, p, t):
    run = p.get("running", True)
    sh = 3 * noise1(t * 40, 1) if run else 0
    with saved(ctx):
        ctx.translate(sh, 0)
        rrect(ctx, -230, -260, 460, 240, 22)
        fill_stroke(ctx, "#FFB300", OUT)
        rrect(ctx, -190, -220, 220, 150, 14)
        fill_stroke(ctx, (0.2, 0.2, 0.25), OUT * 0.6)
        for y in range(-205, -80, 24):
            ctx.move_to(-180, y)
            ctx.line_to(20, y)
        ctx.set_source_rgba(1, 1, 1, 0.25)
        ctx.set_line_width(5)
        ctx.stroke()
        fuel = p.get("fuel", 0.7)
        if isinstance(fuel, (list, tuple)):
            fuel = lerp(fuel[0], fuel[1], clamp(p.get("_age", t) / fuel[2]))
        rrect(ctx, 70, -215, 130, 40, 10)
        fill_stroke(ctx, (1, 1, 1), OUT * 0.5)
        rrect(ctx, 76, -209, 118 * clamp(fuel), 28, 7)
        ctx.set_source_rgb(*mix(PAL["red"], PAL["green"], fuel))
        ctx.fill()
        text(ctx, "GASÓLEO", 135, -150, 24, color=INK, outline=0, shadow_off=0)
        limb(ctx, [(150, -260), (150, -330)], 22, (0.3, 0.3, 0.35), out=OUT * 0.6)
        for x in (-170, 170):
            rrect(ctx, x - 30, -24, 60, 30, 8)
            fill_stroke(ctx, (0.2, 0.2, 0.25), OUT * 0.5)
    if run:
        for k in range(4):
            ph = (t * 0.9 + k / 4) % 1
            circle(ctx, 150 + 40 * ph, -340 - ph * 220, 22 + 40 * ph)
            ctx.set_source_rgba(0.45, 0.45, 0.5, 0.55 * (1 - ph))
            ctx.fill()


def _tap(ctx, p, t):
    flow = p.get("flow", 1.0)
    if isinstance(flow, (list, tuple)):
        flow = lerp(flow[0], flow[1], clamp(p.get("_age", t) / flow[2]))
    limb(ctx, [(-160, -200), (0, -200), (40, -170), (40, -120)], 50, PAL["metal"], out=OUT)
    rrect(ctx, -60, -260, 60, 40, 10)
    fill_stroke(ctx, PAL["metal_dk"], OUT * 0.7)
    if flow > 0.05:
        w = 34 * flow
        ctx.rectangle(40 - w / 2, -100, w, 400)
        ctx.set_source_rgba(0.45, 0.75, 1, 0.85)
        ctx.fill()
        for k in range(5):
            y = -80 + ((t * 600 + k * 80) % 380)
            ellipse(ctx, 40, y, w * 0.25, 14)
            ctx.set_source_rgba(1, 1, 1, 0.6)
            ctx.fill()
    else:
        ph = (t * 0.7) % 1
        ellipse(ctx, 40, -90 + ph * 300, 12, 18)
        ctx.set_source_rgba(0.45, 0.75, 1, 1 - ph * 0.7)
        ctx.fill()


def _battery(ctx, p, t):
    lvl = p.get("level", 1.0)
    if isinstance(lvl, (list, tuple)):  # [desde, hasta, segundos]
        lvl = lerp(lvl[0], lvl[1], clamp(p.get("_age", t) / lvl[2]))
    lvl = clamp(lvl)
    rrect(ctx, -200, -100, 380, 200, 30)
    fill_stroke(ctx, (1, 1, 1), OUT)
    rrect(ctx, 180, -45, 40, 90, 12)
    fill_stroke(ctx, (1, 1, 1), OUT * 0.8)
    c = PAL["green"] if lvl > 0.5 else (PAL["yellow"] if lvl > 0.2 else PAL["red"])
    if lvl < 0.2 and (t * 2.5) % 1 < 0.3:
        c = lighten(c, 0.4)
    rrect(ctx, -180, -80, max(6, 340 * lvl), 160, 18)
    ctx.set_source_rgb(*c)
    ctx.fill()
    if p.get("show_pct", True):
        text(ctx, f"{int(round(lvl * 100))} %", 0, 0, 74, color="white", outline=8, shadow_off=0)
    if p.get("label"):
        text(ctx, p["label"], 0, 150, 40, color="white", outline=8, shadow_off=0, max_w=520)


def _cell_tower(ctx, p, t):
    on = p.get("on", True)
    for s in (-1, 1):
        ctx.move_to(s * 90, 0)
        ctx.line_to(s * 12, -560)
    ctx.set_source_rgb(0.45, 0.48, 0.56)
    ctx.set_line_width(14)
    ctx.stroke()
    for k in range(8):
        y0, y1 = -k * 70, -(k + 1) * 70
        w0, w1 = lerp(90, 12, k / 8), lerp(90, 12, (k + 1) / 8)
        ctx.move_to(-w0, y0)
        ctx.line_to(w1, y1)
        ctx.move_to(w0, y0)
        ctx.line_to(-w1, y1)
    ctx.set_line_width(5)
    ctx.stroke()
    for s in (-1, 1):
        rrect(ctx, s * 40 - 18, -540, 36, 120, 8)
        fill_stroke(ctx, (0.92, 0.92, 0.95), OUT * 0.6)
    if on:
        for k in range(3):
            ph = (t * 0.9 + k / 3) % 1
            r = 60 + ph * 260
            for s in (-1, 1):
                ctx.arc(0, -500, r, -0.5 + (0 if s > 0 else math.pi), 0.5 + (0 if s > 0 else math.pi))
                ctx.set_source_rgba(0.35, 0.8, 1, 0.9 * (1 - ph))
                ctx.set_line_width(10)
                ctx.stroke()
    else:
        circle(ctx, 0, -620, 50)
        fill_stroke(ctx, PAL["red"], OUT * 0.6)
        text(ctx, "✕", 0, -620, 56, color="white", outline=0, shadow_off=0)


def _telegraph(ctx, p, t):
    rrect(ctx, -240, -60, 480, 70, 14)
    fill_stroke(ctx, "#8A5A30", OUT)
    rrect(ctx, -180, -120, 120, 60, 10)
    fill_stroke(ctx, "#C8A24A", OUT * 0.7)
    press = 0.15 if (t * 4) % 1 < 0.4 else 0.0
    with saved(ctx):
        ctx.translate(-20, -100)
        ctx.rotate(-0.12 + press)
        limb(ctx, [(0, 0), (200, 0)], 22, "#C8A24A", out=OUT * 0.6)
        circle(ctx, 200, -10, 30)
        fill_stroke(ctx, (0.15, 0.15, 0.2), OUT * 0.6)
    for s in (-1, 1):  # cables
        ctx.move_to(-240 + (s + 1) * 30, -20)
        ctx.curve_to(-320, 40, -360, -40, -420, 20)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(5)
    ctx.stroke()
    if p.get("sparks"):
        for i in range(8):
            ph = (t * 3 + i / 8) % 1
            a = i * 0.8 + t * 5
            x0, y0 = -120, -130
            ctx.move_to(x0, y0)
            ctx.line_to(x0 + math.cos(a) * 90 * ph, y0 - abs(math.sin(a)) * 110 * ph)
            ctx.set_source_rgba(1, 0.95, 0.5, 1 - ph)
            ctx.set_line_width(5)
            ctx.stroke()
        _glow(ctx, -120, -130, 150, (0.7, 0.9, 1), 0.5 * (0.5 + 0.5 * math.sin(t * 20)))


def _atm(ctx, p, t):
    on = p.get("on", True)
    rrect(ctx, -170, -520, 340, 520, 24)
    fill_stroke(ctx, (0.3, 0.4, 0.6), OUT)
    rrect(ctx, -130, -470, 260, 170, 12)
    fill_stroke(ctx, (0.08, 0.1, 0.14), OUT * 0.6)
    if on:
        rrect(ctx, -118, -458, 236, 146, 8)
        ctx.set_source_rgb(0.35, 0.7, 1)
        ctx.fill()
        text(ctx, "€", 0, -385, 80, color="white", outline=0, shadow_off=0)
    else:
        text(ctx, "FUERA DE", 0, -405, 30, color=(1, 0.35, 0.35), outline=0, shadow_off=0)
        text(ctx, "SERVICIO", 0, -365, 30, color=(1, 0.35, 0.35), outline=0, shadow_off=0)
    for r in range(3):
        for c in range(3):
            rrect(ctx, -90 + c * 64, -270 + r * 50, 52, 38, 6)
            fill_stroke(ctx, (0.85, 0.87, 0.9), OUT * 0.4)
    rrect(ctx, -110, -110, 220, 24, 8)
    fill_stroke(ctx, (0.1, 0.1, 0.14), OUT * 0.5)


def _radio(ctx, p, t):
    rrect(ctx, -220, -230, 440, 230, 30)
    fill_stroke(ctx, "#E8392F", OUT)
    limb(ctx, [(140, -230), (240, -470)], 8, PAL["metal_dk"], out=OUT * 0.4)
    circle(ctx, 241, -472, 10)
    fill_stroke(ctx, PAL["metal_dk"], 0)
    circle(ctx, -95, -115, 80)
    fill_stroke(ctx, (0.2, 0.2, 0.25), OUT * 0.7)
    for r in (55, 30):
        circle(ctx, -95, -115, r)
        ctx.set_source_rgba(1, 1, 1, 0.15)
        ctx.set_line_width(5)
        ctx.stroke()
    rrect(ctx, 30, -190, 160, 60, 10)
    fill_stroke(ctx, (1, 0.95, 0.7), OUT * 0.5)
    ctx.move_to(60 + 100 * ((t * 0.1) % 1), -190)
    ctx.line_to(60 + 100 * ((t * 0.1) % 1), -130)
    ctx.set_source_rgb(*PAL["red"])
    ctx.set_line_width(4)
    ctx.stroke()
    for x in (60, 150):
        circle(ctx, x, -70, 26)
        fill_stroke(ctx, (0.92, 0.92, 0.95), OUT * 0.5)
    if p.get("on", True):
        for k in range(3):
            ph = (t * 1.2 + k / 3) % 1
            ctx.arc(-95, -115, 110 + ph * 160, -2.6, -1.9)
            ctx.set_source_rgba(1, 1, 1, 0.9 * (1 - ph))
            ctx.set_line_width(10)
            ctx.stroke()


def _elevator(ctx, p, t):
    rrect(ctx, -260, -700, 520, 700, 10)
    fill_stroke(ctx, (0.75, 0.78, 0.84), OUT)
    for s in (-1, 1):
        rrect(ctx, (0 if s > 0 else -230), -620, 230, 620, 6)
        fill_stroke(ctx, (0.86, 0.88, 0.92), OUT * 0.7)
    rrect(ctx, -90, -690, 180, 60, 10)
    fill_stroke(ctx, (0.05, 0.05, 0.08), OUT * 0.5)
    text(ctx, p.get("display", "--"), 0, -660, 40, color=(1, 0.4, 0.2), outline=0, shadow_off=0)
    if p.get("alarm"):
        a = 0.5 + 0.5 * math.sin(t * 10)
        circle(ctx, 330, -480, 50)
        fill_stroke(ctx, mix(PAL["yellow"], (1, 1, 1), a * 0.4), OUT * 0.6)
        text(ctx, "!", 330, -480, 60, color=INK, outline=0, shadow_off=0)


def _earth_night(ctx, p, t):
    """La Tierra de noche con las luces de las ciudades; `off_at` las apaga en cascada de este a oeste."""
    r = 300
    _glow(ctx, 0, 0, r * 1.25, (0.4, 0.6, 1), 0.35)
    circle(ctx, 0, 0, r)
    ctx.set_source(radial_grad(ctx, -80, -80, 20, r, [(0, (0.12, 0.2, 0.42), 1), (1, (0.04, 0.06, 0.16), 1)]))
    ctx.fill_preserve()
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(OUT)
    ctx.stroke()
    with saved(ctx):
        circle(ctx, 0, 0, r)
        ctx.clip()
        conts = [(-150, -110, 130, 80, -0.3), (-90, 60, 70, 140, 0.2), (90, -100, 160, 70, 0.1), (110, 60, 90, 100, 0.0),
                 (220, 140, 70, 40, 0.3)]
        for x, y, rx, ry, rot in conts:
            ellipse(ctx, x, y, rx, ry, rot)
            ctx.set_source_rgb(0.1, 0.16, 0.2)
            ctx.fill()
        rng = np.random.default_rng(4)
        for _ in range(520):
            x, y, rx, ry, rot = conts[int(rng.integers(0, len(conts)))]
            a, d = rng.uniform(0, 2 * math.pi), math.sqrt(rng.random())
            px, py = x + rx * d * math.cos(a), y + ry * d * math.sin(a)
            k = clamp((r - px) / (2 * r))  # se apaga primero el este (derecha)
            lit = _lit(p, t, k)
            if lit <= 0:
                continue
            circle(ctx, px, py, rng.uniform(1.5, 4.2))
            ctx.set_source_rgba(1, 0.82, 0.4, lit * rng.uniform(0.6, 1))
            ctx.fill()
        ctx.arc(0, 0, r, 0, 2 * math.pi)
        ctx.set_source(radial_grad(ctx, 0, 0, r * 0.8, r, [(0, (0.3, 0.5, 1), 0), (1, (0.4, 0.6, 1), 0.45)]))
        ctx.fill()


def _transformer(ctx, p, t):
    rrect(ctx, -260, -420, 520, 420, 18)
    fill_stroke(ctx, (0.55, 0.6, 0.55), OUT)
    for x in range(-230, 240, 46):
        rrect(ctx, x, -380, 26, 340, 8)
        fill_stroke(ctx, (0.48, 0.53, 0.48), OUT * 0.4)
    for x in (-150, 0, 150):
        limb(ctx, [(x, -420), (x, -560)], 30, (0.75, 0.55, 0.35), out=OUT * 0.6)
        for y in range(-540, -420, 26):
            ellipse(ctx, x, y, 34, 9)
            fill_stroke(ctx, (0.8, 0.6, 0.4), OUT * 0.3)
    rrect(ctx, -110, -250, 220, 80, 10)
    fill_stroke(ctx, (1, 0.85, 0.2), OUT * 0.6)
    text(ctx, "⚡", 0, -210, 54, color=INK, outline=0, shadow_off=0)
    if p.get("burning"):
        for k in range(4):
            ph = (t * 0.8 + k / 4) % 1
            circle(ctx, -60 + k * 40 + 30 * ph, -460 - ph * 260, 40 + 50 * ph)
            ctx.set_source_rgba(0.2, 0.2, 0.22, 0.6 * (1 - ph))
            ctx.fill()
        _glow(ctx, 0, -300, 320, (1, 0.5, 0.1), 0.45 + 0.15 * math.sin(t * 9))
    if p.get("label"):
        text(ctx, p["label"], 0, 60, 40, color="white", outline=8, shadow_off=0)


def _dam(ctx, p, t):
    """Presa hidroeléctrica con agua cayendo por los aliviaderos y la central encendida."""
    ctx.move_to(-520, -360)
    ctx.line_to(520, -360)
    ctx.line_to(600, 0)
    ctx.line_to(-600, 0)
    ctx.close_path()
    fill_stroke(ctx, (0.8, 0.8, 0.76), OUT)
    ctx.rectangle(-700, -420, 1400, 60)
    ctx.set_source_rgb(0.3, 0.55, 0.85)
    ctx.fill()
    for x in (-200, 0, 200):
        for k in range(6):
            y = -360 + ((t * 400 + k * 60) % 340)
            ellipse(ctx, x, y, 26, 18)
            ctx.set_source_rgba(0.85, 0.95, 1, 0.8)
            ctx.fill()
        rrect(ctx, x - 30, -360, 60, 360, 8)
        ctx.set_source_rgba(0.5, 0.8, 1, 0.55)
        ctx.fill()
    rrect(ctx, -560, -160, 260, 160, 10)
    fill_stroke(ctx, (0.92, 0.9, 0.86), OUT * 0.8)
    for k in range(3):
        rrect(ctx, -540 + k * 80, -130, 50, 40, 6)
        ctx.set_source_rgba(1, 0.85, 0.4, 0.95 if p.get("on", True) else 0.15)
        ctx.fill()


def _jerrycan(ctx, p, t):
    ctx.move_to(-130, 0)
    ctx.line_to(-130, -300)
    ctx.line_to(60, -300)
    ctx.line_to(130, -230)
    ctx.line_to(130, 0)
    ctx.close_path()
    fill_stroke(ctx, "#D7261E", OUT)
    rrect(ctx, -100, -360, 120, 60, 20)
    fill_stroke(ctx, "#B81E17", OUT * 0.7)
    limb(ctx, [(70, -300), (110, -360)], 30, "#222", out=OUT * 0.5)
    for s in (-1, 1):
        ctx.move_to(-90, -150 + s * 80)
        ctx.line_to(90, -150 - s * 80)
    ctx.set_source_rgba(0, 0, 0, 0.2)
    ctx.set_line_width(14)
    ctx.stroke()


def _water_bottle(ctx, p, t):
    rrect(ctx, -110, -380, 220, 380, 40)
    fill_stroke(ctx, (0.75, 0.9, 1), OUT)
    rrect(ctx, -40, -440, 80, 70, 14)
    fill_stroke(ctx, "#3B82F6", OUT * 0.7)
    rrect(ctx, -110, -250, 220, 100, 4)
    fill_stroke(ctx, "#3B82F6", OUT * 0.5)
    text(ctx, p.get("label", "AGUA"), 0, -200, 42, color="white", outline=0, shadow_off=0)
    ctx.rectangle(-102, -130, 204, 120)
    ctx.set_source_rgba(0.4, 0.7, 1, 0.35)
    ctx.fill()


def _flashlight(ctx, p, t):
    if p.get("on", True):
        ctx.move_to(170, -40)
        ctx.line_to(900, -260)
        ctx.line_to(900, 220)
        ctx.line_to(170, 40)
        ctx.close_path()
        g = cairo.LinearGradient(170, 0, 900, 0)
        g.add_color_stop_rgba(0, 1, 0.97, 0.75, 0.55)
        g.add_color_stop_rgba(1, 1, 0.97, 0.75, 0)
        ctx.set_source(g)
        ctx.fill()
    rrect(ctx, -170, -36, 260, 72, 26)
    fill_stroke(ctx, (0.2, 0.22, 0.3), OUT)
    ctx.move_to(90, -40)
    ctx.line_to(180, -62)
    ctx.line_to(180, 62)
    ctx.line_to(90, 40)
    ctx.close_path()
    fill_stroke(ctx, (0.3, 0.32, 0.4), OUT)
    rrect(ctx, -40, -50, 50, 20, 6)
    fill_stroke(ctx, PAL["yellow"], OUT * 0.5)


def _food_can(ctx, p, t):
    rrect(ctx, -110, -260, 220, 260, 16)
    fill_stroke(ctx, PAL["metal"], OUT)
    rrect(ctx, -110, -210, 220, 150, 4)
    fill_stroke(ctx, p.get("color", "#E8392F"), OUT * 0.5)
    text(ctx, p.get("label", "LENTEJAS"), 0, -135, 30, color="white", outline=0, shadow_off=0, max_w=190)
    ellipse(ctx, 0, -260, 110, 20)
    fill_stroke(ctx, PAL["metal_dk"], OUT * 0.6)


def _cow(ctx, p, t):
    """Vaca lechera (granjas que dependen de ordeñadoras eléctricas)."""
    rrect(ctx, -200, -300, 380, 190, 80)
    fill_stroke(ctx, (1, 1, 1), OUT)
    for x, y, r in ((-120, -250, 40), (40, -200, 50), (120, -270, 30)):
        circle(ctx, x, y, r)
        ctx.set_source_rgb(*INK)
        ctx.fill()
    for x in (-160, -90, 80, 140):
        limb(ctx, [(x, -130), (x, 0)], 34, (1, 1, 1), out=OUT * 0.8)
    with saved(ctx):
        ctx.translate(210, -300)
        ctx.rotate(0.15 * math.sin(t * 1.5))
        rrect(ctx, -40, -70, 130, 130, 50)
        fill_stroke(ctx, (1, 1, 1), OUT)
        rrect(ctx, 20, -10, 90, 70, 30)
        fill_stroke(ctx, "#F7A8B8", OUT * 0.7)
        for x in (50, 80):
            circle(ctx, x, 20, 7)
            ctx.set_source_rgb(*INK)
            ctx.fill()
        circle(ctx, 20, -30, 10)
        ctx.set_source_rgb(*INK)
        ctx.fill()
        for s in (-1, 1):
            ellipse(ctx, 0 + s * 0, -80, 18, 10)
        ellipse(ctx, -50, -50, 30, 14, -0.4)
        fill_stroke(ctx, (1, 1, 1), OUT * 0.6)
    ellipse(ctx, -40, -100, 40, 22)
    fill_stroke(ctx, "#F7A8B8", OUT * 0.6)


BACKGROUNDS.update({"modern_city": bg_modern_city, "living_room": bg_living_room, "kitchen": bg_kitchen,
                    "supermarket": bg_supermarket, "hospital": bg_hospital, "grid_field": bg_grid_field,
                    "solar_storm": bg_solar_storm, "control_room": bg_control_room, "metro": bg_metro,
                    "gas_station": bg_gas_station})
PROPS.update({"pylon": _pylon, "bulb": _bulb, "fridge": _fridge, "candle": _candle, "traffic_light": _traffic_light,
              "generator": _generator, "tap": _tap, "battery": _battery, "cell_tower": _cell_tower,
              "telegraph": _telegraph, "atm": _atm, "radio": _radio, "elevator": _elevator,
              "earth_night": _earth_night, "transformer": _transformer, "dam": _dam, "jerrycan": _jerrycan,
              "water_bottle": _water_bottle, "flashlight": _flashlight, "food_can": _food_can, "cow": _cow})


# ============================================================================ FONDOS VERTICALES (Shorts)
# Estos usan el lienzo vertical de siempre (world.W×world.H = 1080×1920), no la pantalla nativa.
def _wv():
    from .world import H as HH, W as WW
    return WW, HH


def bg_sky_fall(ctx, t, p):
    """Caída libre: cielo que oscurece con la altura (`alt` 1 = 10 km, 0 = suelo), nubes y rayas que suben, y un suelo
    que sube desde abajo con `ground` 0..1 (`snow`: ladera nevada con pinos)."""
    WW, HH = _wv()
    alt = clamp(p.get("alt", 1.0))
    top = mix((0.30, 0.62, 0.98), (0.03, 0.07, 0.28), alt)
    bot = mix((0.74, 0.90, 1.0), (0.22, 0.38, 0.70), alt)
    ctx.rectangle(-500, -500, WW + 1000, HH + 1000)
    ctx.set_source(linear_grad(ctx, 0, 0, 0, HH, [(0, top), (1, bot)]))
    ctx.fill()
    sp = p.get("speed", 1.0)
    rng = np.random.default_rng(7)
    n_cl = int(5 + 9 * (1 - alt))
    for i in range(n_cl):  # nubes que suben (parallax); a 10 km hay pocas
        k = 0.4 + 1.6 * (i / max(1, n_cl - 1))
        x = rng.uniform(-100, WW + 100)
        y = HH + 300 - ((t * 420 * sp * k + rng.uniform(0, 2400)) % (HH + 700))
        with saved(ctx):
            ctx.translate(x, y)
            ctx.scale(0.8 * k, 0.8 * k)
            for cx, cy, r in ((0, 0, 70), (70, -35, 80), (150, 0, 62), (75, 20, 70)):
                circle(ctx, cx, cy, r)
            ctx.set_source_rgba(1, 1, 1, 0.40 + 0.2 * (k / 2))
            ctx.fill()
    for i in range(26):  # rayas de velocidad
        x = rng.uniform(0, WW)
        y = HH - ((t * 1800 * sp * (0.6 + rng.random()) + rng.uniform(0, 2400)) % (HH + 500)) + 100
        ctx.move_to(x, y)
        ctx.line_to(x, y + rng.uniform(90, 220))
        ctx.set_source_rgba(1, 1, 1, 0.22)
        ctx.set_line_width(4)
        ctx.stroke()
    g = clamp(p.get("ground", 0.0))
    if g > 0:
        snow = p.get("snow", False)
        y0 = HH - g * 1500
        ctx.move_to(-300, y0 + 80)
        for x in range(-300, WW + 400, 100):
            ctx.line_to(x, y0 + 60 * math.sin(x * 0.006) - 40 * math.sin(x * 0.015))
        ctx.line_to(WW + 400, HH + 600)
        ctx.line_to(-300, HH + 600)
        ctx.close_path()
        fill_stroke(ctx, "#F4F8FF" if snow else "#5FA84A", OUT)
        sc_ = 0.4 + g * 1.4
        for i in range(14):
            x = (i * 177) % (WW + 200) - 60
            y = y0 + 140 + (i * 83) % 500 * g + 40
            with saved(ctx):
                ctx.translate(x, y)
                ctx.scale(sc_, sc_)
                for k in range(3):
                    ctx.move_to(0, -150 + k * 45)
                    ctx.line_to(-55 + k * 8, -80 + k * 45)
                    ctx.line_to(55 - k * 8, -80 + k * 45)
                    ctx.close_path()
                    fill_stroke(ctx, "#2E7D45", OUT * 0.6)
                rrect(ctx, -8, -20, 16, 30, 3)
                fill_stroke(ctx, "#6B4226", OUT * 0.5)


def bg_jupiter(ctx, t, p):
    """Júpiter. mode «approach»: espacio con el limbo del planeta abajo; mode «clouds»: bandas que suben (caída) y
    que se oscurecen y enrojecen con `depth` 0..1; `spot` muestra la Gran Mancha Roja; `lightning` activa rayos."""
    WW, HH = _wv()
    mode = p.get("mode", "clouds")
    bands = ["#F2E3C6", "#D9A066", "#F6EBD6", "#C97B4A", "#EBD2A8", "#A8603A", "#F0DFC0", "#B5703F"]
    if mode == "approach":
        ctx.rectangle(-500, -500, WW + 1000, HH + 1000)
        ctx.set_source(linear_grad(ctx, 0, 0, 0, HH, [(0, (0.02, 0.02, 0.1)), (1, (0.08, 0.05, 0.16))]))
        ctx.fill()
        rng = np.random.default_rng(3)
        for _ in range(110):
            circle(ctx, rng.uniform(0, WW), rng.uniform(0, HH * 0.8), rng.uniform(1.2, 3.2))
            ctx.set_source_rgba(1, 1, 0.95, rng.uniform(0.4, 1.0))
            ctx.fill()
        cy = p.get("cy", 2350) - p.get("rise", 0.0) * 900
        R = 1650
        with saved(ctx):
            circle(ctx, WW / 2, cy, R)
            ctx.clip()
            for k, c in enumerate(bands * 2):
                y = cy - R + k * 190
                ctx.rectangle(0, y, WW, 190)
                ctx.set_source_rgb(*col(c))
                ctx.fill()
                ctx.move_to(0, y)
                for x in range(0, WW + 40, 40):
                    ctx.line_to(x, y + 8 * math.sin(x * 0.02 + t * 0.6 + k))
                ctx.set_source_rgba(0.4, 0.2, 0.1, 0.25)
                ctx.set_line_width(5)
                ctx.stroke()
            ellipse(ctx, 700, cy - R + 760, 190, 105)
            ctx.set_source_rgb(0.78, 0.3, 0.2)
            ctx.fill()
            circle(ctx, WW / 2 - 260, cy + 400, R)
            ctx.set_source_rgba(0, 0, 0.1, 0.5)
            ctx.fill()
        circle(ctx, WW / 2, cy, R)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(OUT * 1.4)
        ctx.stroke()
        return
    depth = clamp(p.get("depth", 0.0))
    scroll = t * p.get("speed", 520)
    ctx.rectangle(-500, -500, WW + 1000, HH + 1000)
    ctx.fill()
    for k in range(-1, 14):
        y = (k * 230 + scroll) % (230 * 14) - 230
        c = col(bands[k % len(bands)])
        c = mix(c, (0.55, 0.12, 0.05), depth * 0.75)
        c = mix(c, (0.04, 0.02, 0.03), depth * depth * 0.8)
        ctx.move_to(-100, y)
        for x in range(-100, WW + 160, 60):
            ctx.line_to(x, y + 14 * math.sin(x * 0.013 + t * 1.1 + k * 1.7))
        ctx.line_to(WW + 100, y + 230)
        for x in range(WW + 100, -160, -60):
            ctx.line_to(x, y + 230 + 14 * math.sin(x * 0.013 + t * 1.1 + (k + 1) * 1.7))
        ctx.close_path()
        ctx.set_source_rgb(*c)
        ctx.fill()
    if p.get("spot"):
        yy = (HH * 0.55 + scroll * 0.4) % (HH + 500) - 100
        ellipse(ctx, WW * 0.62, yy, 330, 190)
        ctx.set_source_rgb(0.76, 0.28, 0.18)
        ctx.fill_preserve()
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(OUT)
        ctx.stroke()
        ellipse(ctx, WW * 0.62, yy, 190, 105)
        ctx.set_source_rgba(0.9, 0.5, 0.3, 0.6)
        ctx.fill()
    if p.get("lightning") and (t * 2.3) % 1 < 0.12:
        ctx.rectangle(-100, -100, WW + 200, HH + 200)
        ctx.set_source_rgba(1, 1, 0.85, 0.45)
        ctx.fill()
    # humo de la entrada: se oscurece por los bordes
    ctx.rectangle(-100, -100, WW + 200, HH + 200)
    ctx.set_source(radial_grad(ctx, WW / 2, HH / 2, 300, 1300, [(0, (0, 0, 0), 0), (1, (0.05, 0.0, 0.0), 0.55 * (0.3 + depth))]))
    ctx.fill()


def bg_polar(ctx, t, p):
    """Noche polar: estrellas, aurora (`aurora`), suelo de nieve y una estación; `sun` muestra un resplandor en el horizonte."""
    WW, HH = _wv()
    ctx.rectangle(-500, -500, WW + 1000, HH + 1000)
    ctx.set_source(linear_grad(ctx, 0, 0, 0, HH, [(0, (0.02, 0.03, 0.12)), (0.6, (0.07, 0.10, 0.26)), (1, (0.12, 0.16, 0.36))]))
    ctx.fill()
    rng = np.random.default_rng(9)
    for _ in range(150):
        circle(ctx, rng.uniform(0, WW), rng.uniform(0, HH * 0.65), rng.uniform(1.2, 3.4))
        ctx.set_source_rgba(1, 1, 0.95, rng.uniform(0.3, 1.0) * (0.8 + 0.2 * math.sin(t * 2 + rng.uniform(0, 6))))
        ctx.fill()
    hz = HH * 0.66
    if p.get("sun"):
        for r, a in ((520, 0.18), (330, 0.28), (170, 0.5)):
            circle(ctx, WW * 0.5, hz, r)
            ctx.set_source_rgba(1, 0.55, 0.2, a)
            ctx.fill()
    a_ = clamp(p.get("aurora", 0.0))
    for k, (c, y0) in enumerate((((0.3, 1.0, 0.55), 420), ((0.55, 0.4, 1.0), 300), ((0.3, 1.0, 0.75), 560))):
        if a_ <= 0:
            break
        pts = [(x, y0 + 80 * math.sin(x * 0.006 + t * 0.7 + k) + 40 * math.sin(x * 0.014 - t * 1.2)) for x in range(-100, WW + 200, 40)]
        ctx.move_to(*pts[0])
        for x, y in pts:
            ctx.line_to(x, y)
        for x, y in reversed(pts):
            ctx.line_to(x, y + 360 + 70 * math.sin(x * 0.01 + k))
        ctx.close_path()
        g = cairo.LinearGradient(0, y0 - 80, 0, y0 + 450)
        g.add_color_stop_rgba(0, *c, 0.0)
        g.add_color_stop_rgba(0.4, *c, 0.5 * a_)
        g.add_color_stop_rgba(1, *c, 0.0)
        ctx.set_source(g)
        ctx.fill()
    ctx.rectangle(-300, hz, WW + 600, HH - hz + 300)
    ctx.set_source(linear_grad(ctx, 0, hz, 0, HH, [(0, (0.80, 0.86, 0.98)), (1, (0.55, 0.62, 0.82))]))
    ctx.fill_preserve()
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(OUT)
    ctx.stroke()
    # estación
    bx, by = WW * 0.62, hz + 60
    rrect(ctx, bx - 190, by - 130, 380, 130, 14)
    fill_stroke(ctx, "#C9494A", OUT)
    for k in range(4):
        rrect(ctx, bx - 160 + k * 85, by - 100, 55, 45, 6)
        fill_stroke(ctx, (1, 0.85, 0.45) if p.get("lit", True) else (0.15, 0.15, 0.25), OUT * 0.6)
    limb(ctx, [(bx + 120, by - 130), (bx + 120, by - 290)], 10, "#6A6F80", out=OUT * 0.5)
    rrect(ctx, bx + 120, by - 290, 90, 52, 4)
    fill_stroke(ctx, "#FFD23F", OUT * 0.5)
    for i in range(6):  # patas
        limb(ctx, [(bx - 150 + i * 60, by), (bx - 150 + i * 60, by + 40)], 12, "#6A6F80", out=OUT * 0.4)


def bg_cave(ctx, t, p):
    """Cueva oscura con estalactitas, suelo de roca, una tienda y un farolillo (`lantern`)."""
    WW, HH = _wv()
    ctx.rectangle(-500, -500, WW + 1000, HH + 1000)
    ctx.set_source(linear_grad(ctx, 0, 0, 0, HH, [(0, (0.07, 0.06, 0.09)), (1, (0.20, 0.16, 0.18))]))
    ctx.fill()
    rng = np.random.default_rng(11)
    for i in range(9):  # estalactitas
        x = i * WW / 8 + rng.uniform(-40, 40)
        h = rng.uniform(220, 520)
        w = rng.uniform(70, 130)
        ctx.move_to(x - w, -50)
        ctx.line_to(x + w, -50)
        ctx.line_to(x + rng.uniform(-20, 20), h)
        ctx.close_path()
        fill_stroke(ctx, (0.30, 0.27, 0.32), OUT)
    gy = HH * 0.72
    ctx.move_to(-100, gy)
    for x in range(-100, WW + 200, 60):
        ctx.line_to(x, gy + 25 * math.sin(x * 0.012) + 18 * math.sin(x * 0.03))
    ctx.line_to(WW + 100, HH + 100)
    ctx.line_to(-100, HH + 100)
    ctx.close_path()
    fill_stroke(ctx, (0.34, 0.30, 0.33), OUT)
    for i in range(7):  # estalagmitas
        x = (i * 211 + 90) % (WW + 100)
        h = 90 + (i * 53) % 150
        ctx.move_to(x - 50, gy + 80)
        ctx.line_to(x + 50, gy + 80)
        ctx.line_to(x, gy + 80 - h)
        ctx.close_path()
        fill_stroke(ctx, (0.40, 0.36, 0.40), OUT * 0.7)
    if p.get("tent", True):
        tx = WW * 0.72
        ctx.move_to(tx - 200, gy + 120)
        ctx.line_to(tx, gy - 130)
        ctx.line_to(tx + 200, gy + 120)
        ctx.close_path()
        fill_stroke(ctx, "#E8A33A", OUT)
        ctx.move_to(tx, gy - 130)
        ctx.line_to(tx - 55, gy + 120)
        ctx.line_to(tx + 55, gy + 120)
        ctx.close_path()
        fill_stroke(ctx, "#8A5A1A", OUT * 0.7)
    if p.get("lantern", True):
        lx, ly = WW * 0.30, gy + 20
        fl = _flicker(t, 4)
        _glow(ctx, lx, ly - 60, 520 * fl, (1, 0.8, 0.4), 0.45)
        rrect(ctx, lx - 28, ly - 90, 56, 80, 10)
        fill_stroke(ctx, (1, 0.85, 0.4), OUT * 0.8)


def _plane_tail(ctx, p, t):
    """Cola de un avión rota con un carrito de comida dentro (Vesna Vulović); `smoke` añade humo."""
    ctx.move_to(-260, -40)
    ctx.curve_to(-120, -90, 120, -80, 300, -20)
    ctx.line_to(300, 140)
    ctx.curve_to(120, 190, -120, 190, -260, 120)
    ctx.close_path()
    fill_stroke(ctx, "#E9EEF5", OUT)
    ctx.move_to(190, -60)
    ctx.line_to(330, -330)
    ctx.line_to(410, -330)
    ctx.line_to(330, 0)
    ctx.close_path()
    fill_stroke(ctx, "#C9494A", OUT)
    ctx.move_to(-260, -40)
    ctx.line_to(-300, -20)
    ctx.line_to(-270, 20)
    ctx.line_to(-310, 60)
    ctx.line_to(-260, 120)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(OUT)
    ctx.stroke()
    rrect(ctx, -140, 10, 150, 90, 8)
    fill_stroke(ctx, "#C8CCD6", OUT * 0.8)
    for x in (-120, -20):
        circle(ctx, x, 112, 14)
        fill_stroke(ctx, INK, 0)
    for k in range(3):
        rrect(ctx, -125 + k * 45, 24, 38, 26, 4)
        fill_stroke(ctx, "#FF8A3D", OUT * 0.4)
    if p.get("smoke", True):
        for k in range(4):
            ph = (t * 0.7 + k / 4) % 1
            circle(ctx, -290 - 60 * ph, -10 - 120 * ph, 30 + 60 * ph)
            ctx.set_source_rgba(0.25, 0.25, 0.28, 0.55 * (1 - ph))
            ctx.fill()


def _probe(ctx, p, t):
    """Sonda de entrada (cápsula cónica con escudo térmico); `fire` 0..1 añade la llama del frenazo."""
    f = clamp(p.get("fire", 1.0))
    if f > 0:
        for k in range(7):
            ph = (t * 2.2 + k / 7) % 1
            ellipse(ctx, 18 * math.sin(k * 3 + t * 9), -170 - ph * 330, 120 * (1 - ph * 0.6) * f, 140 * f)
            ctx.set_source_rgba(1, 0.55 + 0.35 * ph, 0.1, 0.65 * (1 - ph))
            ctx.fill()
    ctx.move_to(-140, -90)
    ctx.line_to(140, -90)
    ctx.line_to(0, 150)
    ctx.close_path()
    fill_stroke(ctx, "#B8BDC9", OUT)
    ctx.move_to(-140, -90)
    ctx.curve_to(-70, -150, 70, -150, 140, -90)
    ctx.close_path()
    fill_stroke(ctx, "#8A4A2A", OUT)
    circle(ctx, 0, -20, 34)
    fill_stroke(ctx, "#5CE1E6", OUT * 0.7)


BACKGROUNDS.update({"sky_fall": bg_sky_fall, "jupiter": bg_jupiter, "polar": bg_polar, "cave": bg_cave})
def _jupiter_ball(ctx, p, t):
    """Júpiter con bandas y Gran Mancha Roja (radio `r`)."""
    r = p.get("r", 360)
    bands = ["#F2E3C6", "#D9A066", "#F6EBD6", "#C97B4A", "#EBD2A8", "#A8603A", "#F0DFC0"]
    with saved(ctx):
        circle(ctx, 0, 0, r)
        ctx.clip()
        h = 2 * r / len(bands)
        for k, c in enumerate(bands):
            y = -r + k * h
            ctx.rectangle(-r, y, 2 * r, h + 1)
            ctx.set_source_rgb(*col(c))
            ctx.fill()
            ctx.move_to(-r, y)
            for x in range(-int(r), int(r) + 20, 20):
                ctx.line_to(x, y + 5 * math.sin(x * 0.03 + t * 0.5 + k))
            ctx.set_source_rgba(0.4, 0.2, 0.1, 0.3)
            ctx.set_line_width(4)
            ctx.stroke()
        ellipse(ctx, r * 0.28, r * 0.30, r * 0.22, r * 0.12)
        ctx.set_source_rgb(0.78, 0.3, 0.2)
        ctx.fill()
        circle(ctx, -r * 0.35, -r * 0.3, r * 1.15)
        ctx.set_source_rgba(0, 0, 0.1, 0.35)
        ctx.fill()
    circle(ctx, 0, 0, r)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(OUT)
    ctx.stroke()


PROPS.update({"plane_tail": _plane_tail, "probe": _probe, "jupiter_ball": _jupiter_ball})


# ============================================================================ zanahoria (Shorts de «comer X cada día»)
def _carrot(ctx, p, t):
    """Zanahoria(s) con hojas: `n` (1-6) en montón y `angle` (rad). El origen está en la punta, crece hacia arriba."""
    n = max(1, min(6, int(p.get("n", 1))))
    for i in range(n):
        k = i - (n - 1) / 2
        with saved(ctx):
            ctx.translate(k * 78, (i % 2) * 26)
            ctx.rotate(p.get("angle", 0.0) + k * 0.2)
            for a in (-0.5, 0.0, 0.5):  # hojas
                with saved(ctx):
                    ctx.translate(0, -216)
                    ctx.rotate(a)
                    ellipse(ctx, 0, -58, 17, 62)
                    fill_stroke(ctx, "#4E9A3A", OUT * 0.6)
            ctx.new_path()
            ctx.move_to(-48, -208)
            ctx.curve_to(-54, -120, -16, -30, 0, 0)
            ctx.curve_to(16, -30, 54, -120, 48, -208)
            ctx.curve_to(32, -230, -32, -230, -48, -208)
            ctx.close_path()
            fill_stroke(ctx, "#FF8A1F", OUT)
            for y, w in ((-170, 30), (-120, 24), (-70, 14)):  # surcos
                ctx.move_to(-w, y)
                ctx.line_to(-w + 22, y + 6)
                ctx.set_source_rgba(0.62, 0.28, 0.02, 0.7)
                ctx.set_line_width(OUT * 0.45)
                ctx.stroke()
            ellipse(ctx, -22, -150, 8, 34)
            ctx.set_source_rgba(1, 1, 1, 0.3)
            ctx.fill()


PROPS.update({"carrot": _carrot})
