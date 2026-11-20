"""Screen-space overlays for long-form explainers: chapter cards, titles, facts, numbers, charts, grids.

Signature: f(ctx, spec, age, dur, t). Positions are fractions of the 1920×1080 frame.
"""
from __future__ import annotations

import math

import cairo

from ..visuals.draw import clamp, ease_back, ease_in, ease_io, ease_out, lerp
from .style import (BOLD, HAND, INK, MARKER, OUTLINE, P, H, W, c, circ, ink_fill, line, measure, poly, rrect,
                    shade, stroke, wrap, write, write_block)


def _out_k(age, dur, d=0.25):
    """1 while visible, easing to 0 during the last `d` seconds."""
    return 1 - ease_in(clamp((age - (dur - d)) / d)) if dur < 1e8 else 1.0


def o_chapter(ctx, s, age, dur, t):
    """Full-frame chapter card: 'CHAPTER 2' + title; slides away at the end."""
    k_in = ease_out(clamp(age / 0.45))
    k_out = ease_in(clamp((age - (dur - 0.35)) / 0.35))
    y_off = -H * k_out
    ctx.save()
    ctx.translate(0, y_off)
    ctx.rectangle(0, 0, W, H)
    ctx.set_source_rgba(*c(s.get("color", "navy")), 1.0 * k_in)
    ctx.fill()
    # torn-paper strip
    yy = H * 0.5
    ctx.move_to(-10, yy - 150)
    for x in range(0, W + 61, 60):
        ctx.line_to(x, yy - 150 + 10 * math.sin(x * 0.7))
    for x in range(W + 60, -61, -60):
        ctx.line_to(x, yy + 150 + 10 * math.sin(x * 0.5))
    ctx.close_path()
    sc = ease_back(clamp((age - 0.1) / 0.45))
    ctx.save()
    ctx.translate(W / 2, yy)
    ctx.scale(1, max(sc, 0.01))
    ctx.translate(-W / 2, -yy)
    ink_fill(ctx, "paper", OUTLINE * 1.4)
    ctx.restore()
    if sc > 0.3:
        a = clamp((age - 0.2) / 0.3)
        write(ctx, s.get("label", "CHAPTER"), W / 2, yy - 75, 54, s.get("accent", "red"), MARKER, alpha=a)
        write(ctx, s.get("title", ""), W / 2, yy + 30, 118, INK, MARKER, alpha=a, max_w=W - 200)
    ctx.restore()


def o_title(ctx, s, age, dur, t):
    """Big title text with optional second line; pops in."""
    k = ease_back(clamp(age / 0.4)) * _out_k(age, dur)
    if k <= 0.01:
        return
    x, y = s.get("x", 0.5) * W, s.get("y", 0.18) * H
    size = s.get("size", 110)
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(k, k)
    ctx.rotate(s.get("tilt", -0.02))
    lines = s.get("lines") or [s.get("text", "")]
    for i, ln in enumerate(lines):
        col_ = s.get("colors", [s.get("color", INK)] * 4)[i % len(s.get("colors", [s.get("color", INK)]))]
        write(ctx, ln, 0, i * size * 1.05, size, col_, s.get("font", MARKER), outline=s.get("outline", 7),
              outline_color=s.get("outline_color", "white"), max_w=s.get("max_w", W - 160))
    ctx.restore()


def o_label(ctx, s, age, dur, t):
    """Handwritten label with an arrow pointing at (to_x, to_y)."""
    k = clamp(age / 0.3) * _out_k(age, dur)
    if k <= 0.01:
        return
    x, y = s.get("x", 0.5) * W, s.get("y", 0.2) * H
    size = s.get("size", 58)
    w, _ = write(ctx, s.get("text", ""), x, y, size, s.get("color", INK), HAND, alpha=k, outline=5,
                 outline_color=s.get("outline_color", "paper"))
    if s.get("to_x") is not None:
        tx, ty = s["to_x"] * W, s["to_y"] * H
        sx = x + (w / 2 + 20) * (1 if tx > x + w / 2 else -1 if tx < x - w / 2 else 0)
        sy = y + (size * 0.6 if ty > y else -size * 0.6)
        g = ease_out(clamp((age - 0.15) / 0.35))
        ex, ey = lerp(sx, tx, g), lerp(sy, ty, g)
        mx, my = (sx + ex) / 2 + (ey - sy) * 0.2, (sy + ey) / 2 - (ex - sx) * 0.2
        ctx.move_to(sx, sy)
        ctx.curve_to(mx, my, mx, my, ex, ey)
        stroke(ctx, 6, s.get("color", INK), k)
        a = math.atan2(ey - my, ex - mx)
        for da in (2.6, -2.6):
            line(ctx, ex, ey, ex + math.cos(a + da) * 26, ey + math.sin(a + da) * 26, 6, s.get("color", INK), k)


def o_fact(ctx, s, age, dur, t):
    """Fact card (top-left by default): tag + text + small source line."""
    k = ease_out(clamp(age / 0.35)) * _out_k(age, dur)
    if k <= 0.01:
        return
    w = s.get("w", 760)
    x0 = s.get("x", 0.03) * W - (1 - k) * (w + 100)
    y0 = s.get("y", 0.05) * H
    size = s.get("size", 46)
    lines = wrap(ctx, s.get("text", ""), size, w - 60, HAND)
    h = 80 + len(lines) * size * 1.15 + (36 if s.get("source") else 0)
    rrect(ctx, x0, y0, w, h, 18)
    ink_fill(ctx, "white", OUTLINE)
    tag = s.get("tag", "FACT")
    tw = measure(ctx, tag, 36, MARKER).x_advance + 40
    rrect(ctx, x0 + 24, y0 - 24, tw, 52, 12)
    ink_fill(ctx, s.get("tag_color", "teal" if tag == "FACT" else "orange"), OUTLINE)
    write(ctx, tag, x0 + 24 + tw / 2, y0 + 2, 36, "white", MARKER)
    for i, ln in enumerate(lines):
        write(ctx, ln, x0 + 30, y0 + 64 + i * size * 1.15, size, INK, HAND, align="left")
    if s.get("source"):
        write(ctx, "Source: " + s["source"], x0 + 30, y0 + h - 30, 28, "darkgrey", HAND, align="left", max_w=w - 60)


def o_stat(ctx, s, age, dur, t):
    """Huge number that counts up (or a fixed string) + caption under it."""
    k = ease_back(clamp(age / 0.4)) * _out_k(age, dur)
    if k <= 0.01:
        return
    x, y = s.get("x", 0.5) * W, s.get("y", 0.42) * H
    val = s.get("value")
    if isinstance(val, (int, float)):
        cur = val * ease_out(clamp(age / s.get("count_time", 1.2)))
        dec = s.get("decimals", 0)
        txt = f"{s.get('prefix', '')}{cur:,.{dec}f}{s.get('suffix', '')}"
    else:
        txt = str(val)
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(k, k)
    write(ctx, txt, 0, 0, s.get("size", 220), s.get("color", "red"), MARKER, outline=10, outline_color="white")
    if s.get("caption"):
        write_block(ctx, s["caption"], 0, s.get("size", 220) * 0.72, s.get("caption_size", 60), s.get("max_w", 1300),
                    INK, HAND, outline=5, outline_color="white")
    ctx.restore()


def o_bars(ctx, s, age, dur, t):
    """Horizontal bar chart: items = [[label, value, colour?], ...]."""
    items = s.get("items", [])
    x0, y0 = s.get("x", 0.12) * W, s.get("y", 0.25) * H
    w = s.get("w", 0.62) * W
    bh = s.get("bar_h", 86)
    gap = s.get("gap", 40)
    vmax = s.get("max") or max(v[1] for v in items)
    if s.get("title"):
        write(ctx, s["title"], x0, y0 - 70, 64, INK, MARKER, align="left", outline=5, outline_color="white")
    for i, it in enumerate(items):
        lab, val = it[0], it[1]
        colr = it[2] if len(it) > 2 else ["teal", "orange", "red", "blue", "green", "purple"][i % 6]
        g = ease_out(clamp((age - 0.2 - i * 0.25) / 0.6)) * _out_k(age, dur)
        y = y0 + i * (bh + gap)
        write(ctx, lab, x0 - 20, y + bh / 2, 48, INK, HAND, align="right", outline=4, outline_color="white")
        bw = max(6, w * val / vmax * g)
        rrect(ctx, x0, y, bw, bh, 14)
        ink_fill(ctx, colr, OUTLINE)
        if g > 0.5:
            vt = it[3] if len(it) > 3 else f"{s.get('prefix', '')}{val:g}{s.get('suffix', '')}"
            write(ctx, vt, x0 + bw + 20, y + bh / 2, 52, INK, MARKER, align="left", alpha=clamp((g - 0.5) * 2))


def o_people(ctx, s, age, dur, t):
    """Pictogram grid: n stickmen, the first `k` highlighted (e.g. 9 out of 10 were peasants)."""
    from .rig import Look, Placement, Pose, Stickman
    n, k = s.get("n", 10), s.get("k", 1)
    cols = s.get("cols", min(n, 10))
    rows = math.ceil(n / cols)
    gx, gy = s.get("gap_x", 175), s.get("gap_y", 330)
    x0 = s.get("x", 0.5) * W - (cols - 1) * gx / 2
    y0 = s.get("y", 0.62) * H - (rows - 1) * gy / 2
    for i in range(n):
        r, cc = divmod(i, cols)
        g = ease_back(clamp((age - i * s.get("stagger", 0.05)) / 0.3)) * _out_k(age, dur)
        if g <= 0.01:
            continue
        hl = (i < k) if not s.get("from_end") else (i >= n - k)
        col_ = c(s.get("color", "red")) if hl and age > s.get("reveal_at", 0) else c(s.get("dim", (0.62, 0.62, 0.65)))
        look = Look(color=col_, seed=i, outfit=s.get("outfit"), outfit_color=s.get("outfit_color", "brown"))
        Stickman(look).draw(ctx, Pose(), Placement(x0 + cc * gx, y0 + r * gy + 120, s.get("fig_scale", 0.95) * g, 1,
                                                    "happy" if hl else "neutral"), t + i)
    if s.get("caption"):
        write_block(ctx, s["caption"], W / 2, s.get("caption_y", 0.12) * H, 64, W - 300, INK, MARKER,
                    outline=5, outline_color="white")


def o_checklist(ctx, s, age, dur, t):
    """Items appear one by one with a tick or a cross."""
    items = s.get("items", [])
    x0, y0 = s.get("x", 0.55) * W, s.get("y", 0.25) * H
    step = s.get("step", 0.6)
    size = s.get("size", 58)
    if s.get("title"):
        write(ctx, s["title"], x0, y0 - 90, 70, INK, MARKER, align="left", outline=5, outline_color="white")
    for i, it in enumerate(items):
        txt, ok = (it, True) if isinstance(it, str) else (it[0], it[1])
        at = s.get("times", [None] * len(items))[i] if s.get("times") else i * step
        a = age - (at if at is not None else i * step)
        if a < 0:
            continue
        g = ease_back(clamp(a / 0.3)) * _out_k(age, dur)
        if g <= 0.01:
            continue
        y = y0 + i * size * 1.6
        ctx.save()
        ctx.translate(x0 + 30, y)
        ctx.scale(g, g)
        rrect(ctx, -30, -30, 60, 60, 10)
        ink_fill(ctx, "white", OUTLINE)
        if ok is True:
            poly(ctx, [(-16, 0), (-4, 14), (20, -18)], close=False)
            stroke(ctx, 9, "green")
        elif ok is False:
            line(ctx, -15, -15, 15, 15, 9, "red")
            line(ctx, -15, 15, 15, -15, 9, "red")
        ctx.restore()
        write(ctx, txt, x0 + 90, y, size, INK, HAND, align="left", alpha=clamp(a / 0.3), outline=4,
              outline_color="white")


def o_counter(ctx, s, age, dur, t):
    """Corner HUD counter (e.g. 'DAY 47', 'MONEY: 3 pennies', 'SURVIVAL ODDS: 62%')."""
    k = ease_out(clamp(age / 0.3)) * _out_k(age, dur)
    if k <= 0.01:
        return
    val_from, val_to = s.get("from"), s.get("to")
    if val_from is not None and val_to is not None:
        g = ease_io(clamp((age - s.get("delay", 0.3)) / s.get("time", 1.2)))
        v = lerp(val_from, val_to, g)
        val = f"{v:,.{s.get('decimals', 0)}f}"
    else:
        val = str(s.get("value", ""))
    txt = f"{s.get('label', '')} {s.get('prefix', '')}{val}{s.get('suffix', '')}".strip()
    size = s.get("size", 54)
    w = measure(ctx, txt, size, MARKER).x_advance + 70
    corner = s.get("corner", "tr")
    x = W - w - 40 if corner.endswith("r") else 40
    y = 40 if corner.startswith("t") else H - 40 - size * 1.6
    y -= (1 - k) * 160 * (1 if corner.startswith("t") else -1)
    rrect(ctx, x, y, w, size * 1.6, 16)
    ink_fill(ctx, s.get("color", "yellow"), OUTLINE)
    if s.get("icon") == "coin":
        circ(ctx, x, y + size * 0.8, 26)
        ink_fill(ctx, "gold", OUTLINE)
    write(ctx, txt, x + w / 2, y + size * 0.8, size, INK, MARKER)


def o_meter(ctx, s, age, dur, t):
    """Horizontal meter from `from` to `to` (0..1): hunger, survival odds, happiness..."""
    k = ease_out(clamp(age / 0.3)) * _out_k(age, dur)
    if k <= 0.01:
        return
    x, y = s.get("x", 0.5) * W, s.get("y", 0.12) * H
    w, h = s.get("w", 700), 56
    g = ease_io(clamp((age - s.get("delay", 0.3)) / s.get("time", 1.0)))
    v = clamp(lerp(s.get("from", 0.5), s.get("to", 0.5), g))
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(k, k)
    write(ctx, s.get("label", ""), 0, -62, 52, INK, MARKER, outline=5, outline_color="white")
    rrect(ctx, -w / 2, -h / 2, w, h, h / 2)
    ink_fill(ctx, "white", OUTLINE)
    colr = s.get("color") or ("green" if v > 0.6 else "yellow" if v > 0.3 else "red")
    if v > 0.02:
        rrect(ctx, -w / 2 + 6, -h / 2 + 6, (w - 12) * v, h - 12, (h - 12) / 2)
        ink_fill(ctx, colr, 0)
    if s.get("show_pct", True):
        write(ctx, f"{v * 100:.0f}%", w / 2 + 70, 0, 50, INK, MARKER, outline=4, outline_color="white")
    ctx.restore()


def o_timeline(ctx, s, age, dur, t):
    """Months/seasons strip with a marker that moves to `at` (index)."""
    items = s.get("items", ["SPRING", "SUMMER", "AUTUMN", "WINTER"])
    k = ease_out(clamp(age / 0.3)) * _out_k(age, dur)
    if k <= 0.01:
        return
    y = s.get("y", 0.08) * H - (1 - k) * 150
    w = s.get("w", 1000)
    x0 = W / 2 - w / 2
    seg = w / len(items)
    cols = s.get("colors", ["green", "yellow", "orange", "blue"])
    for i, it in enumerate(items):
        rrect(ctx, x0 + i * seg + 4, y - 32, seg - 8, 64, 14)
        cur = s.get("at", 0)
        ink_fill(ctx, cols[i % len(cols)] if i <= cur else "white", OUTLINE)
        write(ctx, it, x0 + i * seg + seg / 2, y, 40, INK if i <= cur else "grey", MARKER, max_w=seg - 24)
    a0 = s.get("from_at", s.get("at", 0))
    g = ease_io(clamp((age - 0.3) / 0.8))
    mx = x0 + (lerp(a0, s.get("at", 0), g) + 0.5) * seg
    poly(ctx, [(mx - 22, y + 44), (mx + 22, y + 44), (mx, y + 72)])
    ink_fill(ctx, "red", 3)


def o_vignette(ctx, s, age, dur, t):
    g = cairo.RadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, H * 1.0)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, s.get("alpha", 0.5))
    ctx.set_source(g)
    ctx.paint()


def o_tint(ctx, s, age, dur, t):
    """Colour wash over the whole frame (flashback sepia, night blue, plague green...)."""
    k = clamp(age / 0.4) * _out_k(age, dur, 0.3)
    ctx.rectangle(0, 0, W, H)
    ctx.set_source_rgba(*c(s.get("color", (0.45, 0.3, 0.1))), s.get("alpha", 0.25) * k)
    ctx.fill()


def o_caption(ctx, s, age, dur, t):
    """Lower-third text strip (quotes, names, translations)."""
    k = ease_out(clamp(age / 0.3)) * _out_k(age, dur)
    if k <= 0.01:
        return
    size = s.get("size", 50)
    txt = s.get("text", "")
    w = min(W - 200, measure(ctx, txt, size, HAND).x_advance + 80)
    y = s.get("y", 0.9) * H + (1 - k) * 200
    rrect(ctx, W / 2 - w / 2, y - size * 0.8, w, size * 1.6, 18)
    ink_fill(ctx, s.get("color", INK), 0, 0.82)
    write(ctx, txt, W / 2, y, size, "white", HAND, max_w=w - 60)


def o_fiction(ctx, s, age, dur, t):
    """Small corner tag that marks imagined scenes: 'STORY', 'REENACTMENT', 'WHAT IF'."""
    k = ease_out(clamp(age / 0.3)) * _out_k(age, dur)
    if k <= 0.01:
        return
    txt = s.get("text", "WHAT IF")
    size = 34
    w = measure(ctx, txt, size, MARKER).x_advance + 40
    x = W - w - 30
    y = H - 80 + (1 - k) * 120
    rrect(ctx, x, y, w, 52, 12)
    ink_fill(ctx, "orange", OUTLINE)
    write(ctx, txt, x + w / 2, y + 26, size, "white", MARKER)


def o_money(ctx, s, age, dur, t):
    """'+3d' / '-1 shilling' floating text that rises and fades (income / taxes)."""
    k = clamp(age / 1.2)
    x, y = s.get("x", 0.5) * W, s.get("y", 0.4) * H - 120 * ease_out(k)
    neg = str(s.get("text", "")).startswith("-")
    write(ctx, s.get("text", ""), x, y, s.get("size", 80), "red" if neg else "green", MARKER, alpha=1 - k * k,
          outline=6, outline_color="white")


def o_quote(ctx, s, age, dur, t):
    """Big quotation card (historical quote) with attribution."""
    k = ease_back(clamp(age / 0.4)) * _out_k(age, dur)
    if k <= 0.01:
        return
    w, size = s.get("w", 1300), s.get("size", 62)
    lines = wrap(ctx, s.get("text", ""), size, w - 120, HAND)
    h = len(lines) * size * 1.2 + 150
    ctx.save()
    ctx.translate(W / 2, s.get("y", 0.45) * H)
    ctx.scale(k, k)
    rrect(ctx, -w / 2, -h / 2, w, h, 24)
    ink_fill(ctx, "parchment", OUTLINE)
    write(ctx, "“", -w / 2 + 50, -h / 2 + 50, 160, "red", MARKER)
    for i, ln in enumerate(lines):
        write(ctx, ln, 0, -h / 2 + 70 + i * size * 1.2, size, INK, HAND)
    if s.get("by"):
        write(ctx, "— " + s["by"], w / 2 - 60, h / 2 - 45, 40, "darkgrey", HAND, align="right")
    ctx.restore()


OVERLAYS = {
    "chapter": o_chapter, "title": o_title, "label": o_label, "fact": o_fact, "stat": o_stat, "bars": o_bars,
    "people": o_people, "checklist": o_checklist, "counter": o_counter, "meter": o_meter, "timeline": o_timeline,
    "vignette": o_vignette, "tint": o_tint, "caption": o_caption, "fiction": o_fiction, "money": o_money,
    "quote": o_quote,
}
