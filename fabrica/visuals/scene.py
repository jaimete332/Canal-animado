"""Renderizador de escenas: cámara virtual, personaje, props, overlays y transiciones.

Cada escena se renderiza a su propio MP4 (output/<slug>/scenes/sNN.mp4), lo que permite
regenerar una única escena sin rehacer el vídeo completo.
"""
from __future__ import annotations

import math
import subprocess
from dataclasses import replace
from pathlib import Path

import cairo
import numpy as np

from ..core.log import get_logger
from .character import ACTIONS, Character, Pose, act
from .draw import bounce01, clamp, ease_back, ease_in, ease_io, ease_out, lerp, noise1, saved
from .overlays import OVERLAYS
from .world import H, W, draw_background, draw_prop

log = get_logger("scene")
TR_IN, TR_OUT = 0.22, 0.12
TALKY = {"talk", "present", "shrug", "wave", "smug", "think", "point_up", "point_down"}


def _px(x, y):
    """Fracciones (<=1.5) → píxeles."""
    return (x * W if abs(x) <= 1.5 else x, y * H if abs(y) <= 1.5 else y)


class SceneRenderer:
    def __init__(self, item: dict, fps: int = 30):
        self.it = item
        self.sc = item["scene"]
        self.vis = self.sc["visual"]
        self.dur = item["dur"]
        self.words = item.get("words", [])
        self.fps = fps
        self.mouth = item.get("mouth", [])
        self.char = Character()

    # -- tiempos sincronizados con palabras --------------------------------
    def at(self, spec: dict | list | str | float | int | None, key="at", default=0.0) -> float:
        if isinstance(spec, dict):
            if spec.get(f"{key}_word") is not None:
                return self._word_t(int(spec[f"{key}_word"]))
            v = spec.get(key, default)
        else:
            v = spec if spec is not None else default
        if isinstance(v, str):
            if v.startswith("w"):
                return self._word_t(int(v[1:]))
            if v.startswith("end-"):
                return self.dur - float(v[4:])
            return float(v)
        return float(v)

    def _word_t(self, i: int) -> float:
        if not self.words:
            return 0.0
        i = max(0, min(len(self.words) - 1, i))
        return self.words[i]["start"]

    # -- cámara ------------------------------------------------------------
    def camera(self, ctx, t):
        c = self.vis.get("camera", {}) or {}
        mv = c.get("move", "push_in")
        d = self.dur
        k = t / max(d, 1e-3)
        z = 1.0
        px = py = 0.0
        if mv == "push_in":
            z = lerp(c.get("zoom_from", 1.0), c.get("zoom_to", 1.12), ease_io(k))
        elif mv == "pull_out":
            z = lerp(c.get("zoom_from", 1.3), c.get("zoom_to", 1.0), ease_out(k))
        elif mv == "punch":
            z = lerp(c.get("zoom_from", 1.25), 1.0, ease_out(clamp(t / 0.35))) + 0.05 * ease_io(k)
        elif mv == "static":
            z = 1.0 + 0.04 * ease_io(k)
        elif mv in ("pan_down", "pan_up", "pan_left", "pan_right"):
            amt = c.get("amount", 260) * ease_io(k)
            z = c.get("zoom", 1.08)
            px, py = {"pan_down": (0, -amt), "pan_up": (0, amt), "pan_left": (amt, 0), "pan_right": (-amt, 0)}[mv]
        elif mv == "zoom_burst":
            z = 1.0 + 0.15 * ease_back(clamp(t / 0.4)) - 0.08 * ease_io(k)
        fx, fy = _px(*c.get("focus", (0.5, 0.5)))
        # temblor: continuo + impactos
        sh = c.get("shake", 0.0) * 14
        for imp in c.get("impacts", []):
            ti = self.at(imp) if not isinstance(imp, (int, float)) else float(imp)
            dt = t - ti
            if 0 <= dt < 0.5:
                sh += 40 * (1 - dt / 0.5) ** 2
        sx = sh * noise1(t * 28, 11)
        sy = sh * noise1(t * 28, 23)
        ctx.translate(W / 2 + sx + px, H / 2 + sy + py)
        ctx.scale(z, z)
        ctx.rotate(c.get("tilt", 0.0) * math.sin(t * 0.8) + (sh * 0.0006 * noise1(t * 20, 5)))
        ctx.translate(-fx, -fy)

    # -- personaje ---------------------------------------------------------
    def pose(self, t, frame) -> Pose | None:
        cs = self.vis.get("character")
        if not cs or cs.get("visible") is False:
            return None
        x, y = _px(cs.get("x", 0.5), cs.get("y", 0.74))
        path = cs.get("path")
        if path:
            pts = [(self.at(p[0]), *_px(p[1], p[2])) for p in path]
            if t <= pts[0][0]:
                x, y = pts[0][1], pts[0][2]
            else:
                x, y = pts[-1][1], pts[-1][2]
                for (t0, x0, y0), (t1, x1, y1) in zip(pts, pts[1:]):
                    if t0 <= t <= t1:
                        e = ease_io((t - t0) / max(1e-3, t1 - t0)) if cs.get("path_ease", "io") == "io" else (t - t0) / max(1e-3, t1 - t0)
                        x, y = lerp(x0, x1, e), lerp(y0, y1, e)
                        break
        action = cs.get("action", "idle")
        for tt, a in cs.get("actions", []):
            if t >= self.at(tt):
                action = a
        expr = cs.get("expression", "happy")
        for tt, e in cs.get("expressions", []):
            if t >= self.at(tt):
                expr = e
        base = Pose(x=x, y=y, scale=cs.get("scale", 1.35), facing=cs.get("facing", 1.0), expression=expr,
                    outfit=cs.get("outfit", "casual"), helmet=cs.get("helmet"), sweat=cs.get("sweat", 0.0),
                    extras=dict(cs.get("extras", {})))
        ad = cs.get("action_params", {})
        pose = act(action, t, self.dur, base, ad)
        for fld in ("beard", "cracks"):
            v = cs.get(fld)
            if isinstance(v, (list, tuple)):
                setattr(pose, fld, lerp(v[0], v[1], ease_io(clamp(t / max(0.1, v[2] if len(v) > 2 else self.dur)))))
            elif v is not None:
                setattr(pose, fld, float(v))
        talking = cs.get("talking", action in TALKY)
        if talking and self.mouth:
            pose.mouth_open = self.mouth[min(frame, len(self.mouth) - 1)]
        # entradas
        en = cs.get("enter")
        if en == "drop":
            pose.y = lerp(pose.y - 1500, pose.y, bounce01(clamp(t / 0.7)))
        elif en == "pop":
            pose.scale *= ease_back(clamp(t / 0.35))
        elif en == "rise":
            pose.y = lerp(pose.y + 1200, pose.y, ease_out(clamp(t / 0.5)))
        elif en == "slide_left":
            pose.x = lerp(pose.x - 900, pose.x, ease_out(clamp(t / 0.45)))
        if pose.scale <= 0.01:
            return None
        return pose

    # -- frame -------------------------------------------------------------
    def frame(self, i: int) -> cairo.ImageSurface:
        t = i / self.fps
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        ctx = cairo.Context(surf)
        ctx.set_antialias(cairo.ANTIALIAS_GOOD)
        with saved(ctx):
            self.camera(ctx, t)
            draw_background(ctx, self.vis.get("background", {"type": "color"}), t, self.dur)
            props = self.vis.get("props", [])
            for p in props:
                if p.get("layer", "back") == "back":
                    self._prop(ctx, p, t)
            pose = self.pose(t, i)
            if pose:
                self.char.draw(ctx, pose)
            for p in props:
                if p.get("layer") == "front":
                    self._prop(ctx, p, t)
        for o in self.vis.get("overlays", []):
            t0 = self.at(o)
            t1 = self.at(o, "until", self.dur) if (o.get("until") is not None or o.get("until_word") is not None) else self.dur
            if t0 <= t <= t1:
                f = OVERLAYS.get(o.get("type"))
                if f:
                    f(ctx, o, t - t0, t1 - t0, t)
        self._transitions(ctx, surf, t)
        surf.flush()
        return surf

    def _prop(self, ctx, p, t):
        t0 = self.at(p)
        t1 = self.at(p, "until", 1e9) if (p.get("until") is not None or p.get("until_word") is not None) else 1e9
        if t0 <= t <= t1:
            draw_prop(ctx, p, t, age=t - t0)

    def _transitions(self, ctx, surf, t):
        tin = self.it.get("trans_in", "cut")
        tout = self.it.get("trans_out", "cut")
        if t < TR_IN and tin != "cut":
            self._apply(ctx, surf, tin, 1 - ease_out(t / TR_IN), entering=True)
        rem = self.dur - t
        if rem < TR_OUT and tout != "cut":
            self._apply(ctx, surf, tout, ease_in(1 - rem / TR_OUT), entering=False)

    def _apply(self, ctx, surf, kind, k, entering):
        """k: 0 = sin efecto, 1 = efecto máximo."""
        if k <= 0.001:
            return
        if kind == "whip":
            snap = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
            sc = cairo.Context(snap)
            sc.set_source_surface(surf)
            sc.paint()
            ctx.set_source_rgb(0.1, 0.09, 0.16)
            ctx.paint()
            off = (1 if entering else -1) * k * H * 0.45
            n = 6
            for j in range(n):
                ctx.set_source_surface(snap, 0, off + (j - n / 2) * k * 60)
                ctx.paint_with_alpha(1.0 / n * 1.6 if j else 1.0 / n)
        elif kind in ("zoom", "flash"):
            if kind == "zoom":
                snap = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
                sc = cairo.Context(snap)
                sc.set_source_surface(surf)
                sc.paint()
                z = 1 + 0.5 * k
                with saved(ctx):
                    ctx.translate(W / 2, H / 2)
                    ctx.scale(z, z)
                    ctx.translate(-W / 2, -H / 2)
                    ctx.set_source_surface(snap)
                    ctx.paint()
            ctx.rectangle(0, 0, W, H)
            ctx.set_source_rgba(1, 1, 1, k * 0.9)
            ctx.fill()
        elif kind == "circle":
            r = (1 - k) * 1200
            ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
            ctx.rectangle(0, 0, W, H)
            ctx.arc(W / 2, H * 0.45, max(r, 0.1), 0, 2 * math.pi)
            ctx.set_source_rgb(0.1, 0.09, 0.16)
            ctx.fill()
            ctx.set_fill_rule(cairo.FILL_RULE_WINDING)
        elif kind == "slide":
            snap = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
            sc = cairo.Context(snap)
            sc.set_source_surface(surf)
            sc.paint()
            ctx.set_source_rgb(0.1, 0.09, 0.16)
            ctx.paint()
            ctx.set_source_surface(snap, (1 if entering else -1) * k * W, 0)
            ctx.paint()


def render_scene(item: dict, out: Path, fps: int = 30, crf: int = 16) -> Path:
    r = SceneRenderer(item, fps)
    n = item["frames"]
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
           "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf),
           "-pix_fmt", "yuv420p", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    try:
        for i in range(n):
            s = r.frame(i)
            p.stdin.write(bytes(s.get_data()))
    finally:
        p.stdin.close()
        p.wait()
    if p.returncode != 0:
        raise RuntimeError(f"ffmpeg falló renderizando {out.name}")
    return out


def render_still(item: dict, t: float, path: Path, fps: int = 30) -> Path:
    r = SceneRenderer(item, fps)
    r.frame(int(t * fps)).write_to_png(str(path))
    return path


def mouth_curve(voice: np.ndarray, sr: int, start: float, frames: int, fps: int) -> list[float]:
    """Apertura de boca por frame a partir de la energía de la voz (lip-sync)."""
    out = []
    hop = sr // fps
    s0 = int(start * sr)
    prev = 0.0
    for i in range(frames):
        seg = voice[s0 + i * hop: s0 + (i + 1) * hop]
        v = float(np.sqrt((seg ** 2).mean())) if len(seg) else 0.0
        v = clamp((v - 0.015) / 0.12)
        v = 0.55 * v + 0.45 * prev
        prev = v
        out.append(round(v, 3))
    return out
