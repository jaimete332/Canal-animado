"""Scene renderer for the stickman channel (16:9): camera, cast of stickmen, props, speech bubbles,
overlays and transitions. One MP4 per scene, so a single scene can be regenerated on its own.

Scene visual DSL (all times accept seconds, "wN" = start of word N, or "end-1.5"):
  background: {type: paper|field|village|castle|interior|church|town|forest|map|chalkboard|split|manor|solid, ...}
  cast: [{id, preset, x, y, scale, facing, action, actions: [[t, a]], expression, expressions: [[t, e]],
          path: [[t, x, y]], talking, say: [{text, at, until, kind, side}], enter, exit: {at, type}, item, ...look}]
  props: [{type, x, y, scale, at, until, enter, loop, layer: back|front, ...}]
  overlays: [{type, at, until, ...}]
  camera: {move: static|push_in|pull_out|pan_left|pan_right|pan_up|pan_down|zoom_to, focus: [x, y] | cast id,
           zoom_from, zoom_to, shake, impacts: [t]}
"""
from __future__ import annotations

import math
import subprocess
from pathlib import Path

import cairo
import numpy as np

from ..visuals.draw import clamp, ease_in, ease_io, ease_out, lerp, noise1
from .overlays import OVERLAYS
from .rig import ACTIONS, TALKY, Look, Placement, Pose, Stickman, skeleton
from .style import INK, P, H, W, c
from .world import GROUND, draw_background, draw_prop, px

TR_IN, TR_OUT = 0.3, 0.2

# Recurring characters (consistent look across every video)
PRESETS: dict[str, dict] = {
    "stan": {"scarf": True},                                            # the channel mascot
    "peasant": {"outfit": "tunic", "outfit_color": "brown", "hat": "hood", "hat_color": "tan"},
    "peasant_woman": {"outfit": "dress", "outfit_color": (0.55, 0.6, 0.45), "hat": "kerchief", "hair": "long"},
    "lord": {"outfit": "robe", "outfit_color": "purple", "hat": "cap", "hat_color": "red", "belly": 0.9,
             "beard": "short"},
    "king": {"outfit": "robe", "outfit_color": "red", "hat": "crown", "belly": 0.6, "beard": "long"},
    "priest": {"outfit": "robe", "outfit_color": "ink", "hat": "tonsure"},
    "bishop": {"outfit": "robe", "outfit_color": "white", "hat": "mitre", "belly": 0.7},
    "knight": {"outfit": "armor", "hat": "helmet", "item": "sword"},
    "reeve": {"outfit": "tunic", "outfit_color": "teal", "hat": "cap", "hat_color": "teal", "item": "scroll"},
    "doctor": {"outfit": "robe", "outfit_color": "ink", "hat": "plague_mask"},
    "child": {"outfit": "tunic", "outfit_color": "tan", "_scale": 0.66},
    "modern": {"outfit": "suit", "outfit_color": "navy"},
}
LOOK_FIELDS = set(Look.__dataclass_fields__)


def make_look(spec: dict) -> tuple[Look, float]:
    base = dict(PRESETS.get(spec.get("preset", spec.get("id", "")), {}))
    base.update({k: v for k, v in spec.items() if k in LOOK_FIELDS or k == "color"})
    scale_mul = base.pop("_scale", 1.0)
    if "color" in base:
        base["color"] = c(base["color"])
    if "head_fill" in base:
        base["head_fill"] = c(base["head_fill"])
    base.setdefault("seed", abs(hash(spec.get("id", "x"))) % 97)
    return Look(**{k: v for k, v in base.items() if k in LOOK_FIELDS}), scale_mul


class StickScene:
    def __init__(self, item: dict, fps: int = 30):
        self.it = item
        self.sc = item["scene"]
        self.vis = self.sc["visual"]
        self.dur = item["dur"]
        self.words = item.get("words", [])
        self.fps = fps
        self.mouth = item.get("mouth", [])
        self.cast = []
        for spec in self.vis.get("cast", []) or []:
            look, mul = make_look(spec)
            self.cast.append((spec, Stickman(look), mul))

    # -- word-synced times -------------------------------------------------
    def at(self, v, default=0.0) -> float:
        if v is None:
            return default
        if isinstance(v, str):
            if v.startswith("w"):
                return self._word_t(int(v[1:]))
            if v.startswith("end-"):
                return self.dur - float(v[4:])
            return float(v)
        return float(v)

    def spec_t(self, spec: dict, key="at", default=0.0) -> float:
        if spec.get(f"{key}_word") is not None:
            return self._word_t(int(spec[f"{key}_word"]))
        return self.at(spec.get(key), default)

    def _word_t(self, i: int) -> float:
        if not self.words:
            return 0.0
        i = max(0, min(len(self.words) - 1, i))
        return self.words[i]["start"]

    # -- cast ---------------------------------------------------------------
    def _pos(self, spec, t):
        x, y = px(spec.get("x", 0.5), spec.get("y", GROUND))
        facing = spec.get("facing", 1)
        path = spec.get("path")
        moving = False
        if path:
            pts = [(self.at(p[0]), *px(p[1], p[2])) for p in path]
            if t <= pts[0][0]:
                x, y = pts[0][1], pts[0][2]
            elif t >= pts[-1][0]:
                x, y = pts[-1][1], pts[-1][2]
            else:
                for (t0, x0, y0), (t1, x1, y1) in zip(pts, pts[1:]):
                    if t0 <= t <= t1:
                        k = (t - t0) / max(1e-3, t1 - t0)
                        e = k if spec.get("path_ease") == "linear" else ease_io(k)
                        x, y = lerp(x0, x1, e), lerp(y0, y1, e)
                        moving = abs(x1 - x0) > 1
                        if spec.get("auto_face", True) and abs(x1 - x0) > 1:
                            facing = 1 if x1 > x0 else -1
                        break
        return x, y, facing, moving

    def _action_at(self, spec, t):
        """(action, start time, previous action, previous start)."""
        cur, start = spec.get("action", "idle"), 0.0
        prev, pstart = None, 0.0
        for tt, a in spec.get("actions", []):
            ts = self.at(tt)
            if t >= ts:
                prev, pstart = cur, start
                cur, start = a, ts
        return cur, start, prev, pstart

    def pose(self, spec, t) -> Pose:
        a, s0, prev, ps0 = self._action_at(spec, t)
        params = spec.get("action_params", {})
        f = ACTIONS.get(a, ACTIONS["idle"])
        p = f(t - s0 if a in ("fall", "shrug", "point", "point_up", "facepalm", "bow", "hold_up", "drink") else t,
              self.dur, params)
        if prev is not None and t - s0 < 0.25:
            fp = ACTIONS.get(prev, ACTIONS["idle"])
            pp = fp(t - ps0 if prev in ("fall", "shrug", "point", "facepalm", "bow") else t, self.dur, params)
            p = pp.blend(p, ease_io((t - s0) / 0.25))
        return p

    def expression(self, spec, t):
        e = spec.get("expression", "neutral")
        for tt, x in spec.get("expressions", []):
            if t >= self.at(tt):
                e = x
        return e

    def draw_cast(self, ctx, t, frame):
        heads = {}
        order = sorted(self.cast, key=lambda m: (m[0].get("layer", 0), px(0, m[0].get("y", GROUND))[1]))
        for spec, man, mul in order:
            t_in = self.spec_t(spec, "at", 0.0)
            if t < t_in:
                continue
            ex = spec.get("exit")
            t_out = self.at(ex.get("at"), self.dur) if ex else 1e9
            x, y, facing, moving = self._pos(spec, t)
            pose = self.pose(spec, t)
            scale = spec.get("scale", 1.0) * mul
            alpha = 1.0
            age = t - t_in
            en = spec.get("enter")
            if en == "pop":
                scale *= min(1.0, ease_out(clamp(age / 0.3)) * 1.1) if age < 0.3 else 1.0
            elif en == "fade":
                alpha = clamp(age / 0.4)
            elif en == "slide_left":
                x += (1 - ease_out(clamp(age / 0.6))) * 1100
            elif en == "slide_right":
                x -= (1 - ease_out(clamp(age / 0.6))) * 1100
            elif en == "drop":
                y -= (1 - ease_out(clamp(age / 0.45))) * 900
            if ex and t >= t_out:
                k = clamp((t - t_out) / 0.5)
                if ex.get("type", "fade") == "fade":
                    alpha *= 1 - k
                elif ex["type"] == "slide_right":
                    x += ease_in(k) * 1300
                elif ex["type"] == "slide_left":
                    x -= ease_in(k) * 1300
                if k >= 1:
                    continue
            expr = self.expression(spec, t)
            a, *_ = self._action_at(spec, t)
            talking = spec.get("talking", False)
            mo = 0.0
            if talking and self.mouth:
                ts = [self.at(w) for w in spec.get("talk_window", [0, self.dur])]
                if ts[0] <= t <= ts[1]:
                    mo = self.mouth[min(frame, len(self.mouth) - 1)]
            pl = Placement(x, y, scale, facing, expr, mo, alpha)
            j = man.draw(ctx, pose, pl, t + man.look.seed)
            hx, hy = j["head"]
            if not pose.rot:
                heads[spec.get("id", "")] = (x + facing * scale * hx, y + scale * (hy - 34) - 10, facing, scale)
            else:
                heads[spec.get("id", "")] = (x, y - 120 * scale, facing, scale)
        return heads

    def draw_bubbles(self, ctx, t, heads):
        for spec, _man, _ in self.cast:
            hid = spec.get("id", "")
            if hid not in heads:
                continue
            hx, hy, facing, scale = heads[hid]
            for b in spec.get("say", []) or []:
                t0 = self.spec_t(b)
                t1 = self.spec_t(b, "until", self.dur) if (b.get("until") is not None or b.get("until_word") is not None) else self.dur
                if not (t0 <= t <= t1):
                    continue
                side = b.get("side", 1 if hx < W * 0.62 else -1)
                q = {"type": "bubble", "x": hx + side * 25, "y": hy - 6, "text": b.get("text", ""),
                     "kind": b.get("kind", "speech"), "side": side, "size": b.get("size", 50), "w": b.get("w", 520),
                     "enter": "none"}
                draw_prop(ctx, q, t, t - t0)

    # -- camera -------------------------------------------------------------
    def camera(self, ctx, t, heads_hint=None):
        cam = self.vis.get("camera", {}) or {}
        mv = cam.get("move", "static")
        k = t / max(self.dur, 1e-3)
        z, pxo, pyo = 1.0, 0.0, 0.0
        if mv == "push_in":
            z = lerp(cam.get("zoom_from", 1.0), cam.get("zoom_to", 1.08), ease_io(k))
        elif mv == "pull_out":
            z = lerp(cam.get("zoom_from", 1.18), cam.get("zoom_to", 1.0), ease_out(k))
        elif mv == "zoom_to":
            t0 = self.at(cam.get("at"), 0.0)
            z = lerp(cam.get("zoom_from", 1.0), cam.get("zoom_to", 1.6), ease_io(clamp((t - t0) / cam.get("time", 0.8))))
        elif mv == "punch":
            z = lerp(cam.get("zoom_from", 1.18), 1.0, ease_out(clamp(t / 0.35)))
        elif mv in ("pan_left", "pan_right", "pan_up", "pan_down"):
            amt = cam.get("amount", 200) * ease_io(k)
            z = cam.get("zoom", 1.1)
            pxo, pyo = {"pan_left": (amt, 0), "pan_right": (-amt, 0), "pan_up": (0, amt), "pan_down": (0, -amt)}[mv]
        else:
            z = cam.get("zoom", 1.0) + 0.015 * ease_io(k)
        focus = cam.get("focus", [0.5, 0.5])
        if isinstance(focus, str):
            spec = next((s for s, _, _ in self.cast if s.get("id") == focus), None)
            if spec:
                x, y, _, _ = self._pos(spec, t)
                focus = [x, y - 170 * spec.get("scale", 1.0)]
            else:
                focus = [0.5, 0.5]
        fx, fy = px(*focus)
        # keep the frame covered: clamp the focus so no border is shown when zoomed
        if z >= 1.0:
            hw, hh = W / 2 / z, H / 2 / z
            fx = min(max(fx, hw - pxo / z), W - hw - pxo / z)
            fy = min(max(fy, hh - pyo / z), H - hh - pyo / z)
        sh = cam.get("shake", 0.0) * 10
        for imp in cam.get("impacts", []):
            dt = t - self.at(imp)
            if 0 <= dt < 0.45:
                sh += 28 * (1 - dt / 0.45) ** 2
        ctx.translate(W / 2 + sh * noise1(t * 26, 11) + pxo, H / 2 + sh * noise1(t * 26, 23) + pyo)
        ctx.scale(z, z)
        ctx.translate(-fx, -fy)

    # -- frame ----------------------------------------------------------------
    def frame(self, i: int) -> cairo.ImageSurface:
        t = i / self.fps
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        ctx = cairo.Context(surf)
        ctx.set_antialias(cairo.ANTIALIAS_GOOD)
        ctx.save()
        self.camera(ctx, t)
        draw_background(ctx, self.vis.get("background", {"type": "paper"}), t)
        props = self.vis.get("props", []) or []
        for p in props:
            if p.get("layer", "back") == "back":
                self._prop(ctx, p, t)
        heads = self.draw_cast(ctx, t, i)
        for p in props:
            if p.get("layer") == "front":
                self._prop(ctx, p, t)
        self.draw_bubbles(ctx, t, heads)
        ctx.restore()
        for o in self.vis.get("overlays", []) or []:
            t0 = self.spec_t(o)
            has_until = o.get("until") is not None or o.get("until_word") is not None
            t1 = self.spec_t(o, "until", self.dur) if has_until else self.dur + 1e9
            if t0 <= t <= (t1 if has_until else self.dur):
                f = OVERLAYS.get(o.get("type"))
                if f:
                    f(ctx, o, t - t0, (t1 - t0) if has_until else 1e9, t)
        self._transitions(ctx, surf, t)
        surf.flush()
        return surf

    def _prop(self, ctx, p, t):
        t0 = self.spec_t(p)
        has_until = p.get("until") is not None or p.get("until_word") is not None
        t1 = self.spec_t(p, "until", 1e9) if has_until else 1e9
        if t0 <= t <= t1:
            q = p
            if has_until and t1 - t < 0.25 and p.get("exit", "pop") == "pop":
                q = dict(p)
                q["scale"] = p.get("scale", 1.0) * ease_out(clamp((t1 - t) / 0.25))
            draw_prop(ctx, q, t, t - t0)

    # -- transitions ----------------------------------------------------------
    def _transitions(self, ctx, surf, t):
        tin, tout = self.it.get("trans_in", "cut"), self.it.get("trans_out", "cut")
        if t < TR_IN and tin != "cut":
            self._apply(ctx, surf, tin, 1 - ease_out(t / TR_IN), True)
        rem = self.dur - t
        if rem < TR_OUT and tout != "cut":
            self._apply(ctx, surf, tout, ease_in(1 - rem / TR_OUT), False)

    def _apply(self, ctx, surf, kind, k, entering):
        if k <= 0.001:
            return
        if kind in ("fade", "dip"):
            ctx.rectangle(0, 0, W, H)
            ctx.set_source_rgba(*P["paper"], k)
            ctx.fill()
        elif kind == "flash":
            ctx.rectangle(0, 0, W, H)
            ctx.set_source_rgba(1, 1, 1, k * 0.9)
            ctx.fill()
        elif kind in ("wipe", "slide", "whip"):
            # a paper sheet sweeps in from the left and leaves through the right
            x0, w = (W * (1 - k), W * k) if entering else (0, W * k)
            ctx.rectangle(x0, -10, w, H + 20)
            ctx.set_source_rgb(*P["paper"])
            ctx.fill_preserve()
            ctx.set_source_rgb(*INK)
            ctx.set_line_width(8)
            ctx.stroke()
        elif kind == "zoom":
            snap = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
            sc = cairo.Context(snap)
            sc.set_source_surface(surf)
            sc.paint()
            z = 1 + 0.35 * k
            ctx.save()
            ctx.translate(W / 2, H / 2)
            ctx.scale(z, z)
            ctx.translate(-W / 2, -H / 2)
            ctx.set_source_surface(snap)
            ctx.paint()
            ctx.restore()
            ctx.rectangle(0, 0, W, H)
            ctx.set_source_rgba(1, 1, 1, k * 0.7)
            ctx.fill()
        elif kind == "circle":
            r = (1 - k) * 1200
            ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
            ctx.rectangle(0, 0, W, H)
            ctx.arc(W / 2, H * 0.5, max(r, 0.1), 0, 2 * math.pi)
            ctx.set_source_rgb(*INK)
            ctx.fill()
            ctx.set_fill_rule(cairo.FILL_RULE_WINDING)


def render_scene(item: dict, out: Path, fps: int = 30, crf: int = 17) -> Path:
    r = StickScene(item, fps)
    n = item["frames"]
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(fps),
           "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf), "-pix_fmt", "yuv420p", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    try:
        for i in range(n):
            p.stdin.write(bytes(r.frame(i).get_data()))
    finally:
        p.stdin.close()
        p.wait()
    if p.returncode != 0:
        raise RuntimeError(f"ffmpeg failed rendering {out.name}")
    return out


def render_still(item: dict, t: float, path: Path, fps: int = 30) -> Path:
    StickScene(item, fps).frame(int(t * fps)).write_to_png(str(path))
    return path


def mouth_curve(voice: np.ndarray, sr: int, start: float, frames: int, fps: int) -> list[float]:
    from ..visuals.scene import mouth_curve as mc
    return mc(voice, sr, start, frames, fps)
