"""Leo, la mascota del canal: personaje 2D con rig (huesos + IK), expresiones y lip-sync.

Unidades locales: 1 u = 100 px * escala. Origen = punto entre los pies; y negativo = arriba.
Ángulos de extremidad: 0 = colgando hacia abajo, positivo = hacia fuera del cuerpo.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field, replace

import cairo

from .draw import (INK, OUT, PAL, circle, clamp, col, darken, ellipse, fill_stroke, lerp, lighten,
                   limb, noise1, rrect, saved, smooth_closed)

U_ARM1, U_ARM2 = 0.62, 0.58
U_LEG1, U_LEG2 = 0.52, 0.50
SHOULDER = (0.66, -2.02)
HIP = (0.30, -0.98)
HEAD_C = (0.0, -3.18)


@dataclass
class Pose:
    x: float = 540
    y: float = 1500
    scale: float = 1.3
    facing: float = 1.0            # mira a la derecha (+) o izquierda (-): desplaza rasgos
    rot: float = 0.0               # rotación del cuerpo entero (rad) sobre la cadera
    squash: float = 0.0            # >0 aplasta, <0 estira
    head_tilt: float = 0.0
    lean: float = 0.0              # inclinación del torso
    arm_l: tuple[float, float] = (0.25, 0.25)    # (hombro, codo) brazo izquierdo (pantalla)
    arm_r: tuple[float, float] = (0.25, 0.25)
    hand_l: tuple[float, float] | None = None    # objetivo IK en unidades locales (anula arm_l)
    hand_r: tuple[float, float] | None = None
    leg_l: tuple[float, float] = (0.08, 0.0)
    leg_r: tuple[float, float] = (0.08, 0.0)
    expression: str = "happy"
    mouth_open: float = 0.0
    blink: float = 0.0
    look: tuple[float, float] = (0.0, 0.0)
    outfit: str = "casual"         # casual | suit
    helmet: str | None = None      # None | hardhat | dome
    cracks: float = 0.0            # grietas en el casco (0..1)
    beard: float = 0.0             # barba (gag del paso del tiempo)
    sweat: float = 0.0             # 0..1
    tool: dict | None = None       # {"type": "shovel", "angle": rad, "grip": (x,y)} ...
    t: float = 0.0
    extras: dict = field(default_factory=dict)


def ik2(sx, sy, tx, ty, l1, l2, bend=1.0):
    """IK de dos huesos. Devuelve (codo, mano)."""
    dx, dy = tx - sx, ty - sy
    d = math.hypot(dx, dy)
    d = clamp(d, abs(l1 - l2) + 1e-3, l1 + l2 - 1e-3)
    base = math.atan2(dy, dx)
    a = math.acos(clamp((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d), -1, 1))
    ang = base + a * bend
    ex, ey = sx + l1 * math.cos(ang), sy + l1 * math.sin(ang)
    k = l2 / math.hypot(tx - ex, ty - ey) if (tx - ex or ty - ey) else 0
    hx, hy = ex + (tx - ex) * min(1, k), ey + (ty - ey) * min(1, k)
    return (ex, ey), (hx, hy)


def chain(sx, sy, side, a1, a2, l1, l2):
    """FK: ángulos 'hacia fuera' -> puntos codo/mano. side=-1 izquierda, +1 derecha."""
    A1 = side * a1
    ex, ey = sx + l1 * math.sin(A1), sy + l1 * math.cos(A1)
    A2 = side * (a1 + a2)
    return (ex, ey), (ex + l2 * math.sin(A2), ey + l2 * math.cos(A2))


class Character:
    def __init__(self, palette: dict | None = None):
        self.p = dict(PAL)
        if palette:
            self.p.update(palette)

    # ------------------------------------------------------------------
    def draw(self, ctx: cairo.Context, pose: Pose) -> None:
        u = 100 * pose.scale
        with saved(ctx):
            ctx.translate(pose.x, pose.y)
            ctx.scale(u, u)
            hip_y = -1.0
            ctx.translate(0, hip_y)
            ctx.rotate(pose.rot)
            ctx.translate(0, -hip_y)
            sq = pose.squash
            ctx.scale(1 + sq * 0.6, 1 - sq)
            lw = OUT / u * 1.15
            self._legs(ctx, pose, lw)
            with saved(ctx):
                ctx.translate(0, hip_y)
                ctx.rotate(pose.lean)
                ctx.translate(0, -hip_y)
                self._torso(ctx, pose, lw)
                arms = self._arm_points(pose)
                # brazos detrás de la herramienta, manos delante
                for side in (-1, 1):
                    s, e, h = arms[side]
                    limb(ctx, [s, e, h], 0.30, self._c("sleeve", pose), out=lw)
                if pose.tool:
                    self._tool(ctx, pose, lw)
                for side in (-1, 1):
                    self._hand(ctx, *arms[side][2], lw, pose, side)
                with saved(ctx):
                    ctx.translate(HEAD_C[0], HEAD_C[1] + 0.85)
                    ctx.rotate(pose.head_tilt)
                    ctx.translate(-HEAD_C[0], -(HEAD_C[1] + 0.85))
                    self._head(ctx, pose, lw)

    # ------------------------------------------------------------------
    def _c(self, part: str, pose: Pose):
        if pose.outfit == "suit":
            return {"sleeve": self.p["suit"], "torso": self.p["suit"], "pants": self.p["suit"],
                    "shoe": self.p["suit_acc"]}[part]
        return {"sleeve": self.p["hoodie"], "torso": self.p["hoodie"], "pants": self.p["pants"],
                "shoe": self.p["shoe"]}[part]

    def _arm_points(self, pose: Pose):
        out = {}
        for side, ang, tgt in ((-1, pose.arm_l, pose.hand_l), (1, pose.arm_r, pose.hand_r)):
            sx, sy = SHOULDER[0] * side, SHOULDER[1]
            if tgt is not None:
                e, h = ik2(sx, sy, tgt[0], tgt[1], U_ARM1, U_ARM2, bend=-side)
            else:
                e, h = chain(sx, sy, side, ang[0], ang[1], U_ARM1, U_ARM2)
            out[side] = ((sx, sy), e, h)
        return out

    def _legs(self, ctx, pose: Pose, lw):
        for side, (a1, a2) in ((-1, pose.leg_l), (1, pose.leg_r)):
            hx, hy = HIP[0] * side, HIP[1]
            knee, foot = chain(hx, hy, side, a1, -a2, U_LEG1, U_LEG2)
            limb(ctx, [(hx, hy), knee, foot], 0.34, self._c("pants", pose), out=lw)
            # zapatilla (encima de la pierna, apuntando hacia fuera)
            with saved(ctx):
                ctx.translate(*foot)
                ctx.rotate(side * (a1 - a2) * 0.5)
                ctx.scale(side, 1)
                ctx.new_path()
                ctx.move_to(-0.2, 0.1)
                ctx.curve_to(-0.26, -0.14, 0.02, -0.2, 0.14, -0.1)
                ctx.curve_to(0.3, -0.06, 0.42, 0.0, 0.4, 0.1)
                ctx.close_path()
                fill_stroke(ctx, self._c("shoe", pose), lw)
                rrect(ctx, -0.22, 0.06, 0.64, 0.09, 0.04)
                fill_stroke(ctx, (1, 1, 1), lw * 0.8)

    def _torso(self, ctx, pose: Pose, lw):
        c = self._c("torso", pose)
        ctx.new_path()
        ctx.move_to(-0.42, -2.28)
        ctx.curve_to(-0.9, -2.1, -0.82, -1.1, -0.68, -0.92)
        ctx.curve_to(-0.3, -0.78, 0.3, -0.78, 0.68, -0.92)
        ctx.curve_to(0.82, -1.1, 0.9, -2.1, 0.42, -2.28)
        ctx.close_path()
        fill_stroke(ctx, c, lw)
        # sombra lateral
        with saved(ctx):
            ctx.move_to(0.42, -2.28)
            ctx.curve_to(0.9, -2.1, 0.82, -1.1, 0.68, -0.92)
            ctx.curve_to(0.5, -0.86, 0.45, -1.5, 0.42, -2.28)
            ctx.set_source_rgba(*darken(c, 0.18), 0.6)
            ctx.fill()
        if pose.outfit == "suit":
            # franjas del traje y emblema
            ctx.set_source_rgb(*self.p["suit_acc"])
            rrect(ctx, -0.72, -1.38, 1.44, 0.16, 0.06)
            ctx.fill()
            circle(ctx, 0, -1.78, 0.2)
            fill_stroke(ctx, self.p["blue"], lw * 0.8)
            circle(ctx, 0, -1.78, 0.08)
            ctx.set_source_rgba(1, 1, 1, 0.8 + 0.2 * math.sin(pose.t * 6))
            ctx.fill()
        else:
            # emblema "?" del canal
            circle(ctx, 0, -1.72, 0.25)
            fill_stroke(ctx, self.p["yellow"], lw * 0.8)
            ctx.select_font_face("Lilita One")
            ctx.set_font_size(0.38)
            ext = ctx.text_extents("?")
            ctx.move_to(-ext.width / 2 - ext.x_bearing, -1.72 - ext.height / 2 - ext.y_bearing)
            ctx.set_source_rgb(*INK)
            ctx.show_text("?")
            # cordones capucha
            ctx.set_line_width(0.045)
            for s in (-1, 1):
                ctx.move_to(0.16 * s, -2.22)
                ctx.line_to(0.19 * s, -2.0)
            ctx.stroke()
            # banda inferior de la sudadera
            ctx.move_to(-0.66, -1.08)
            ctx.curve_to(-0.3, -0.98, 0.3, -0.98, 0.66, -1.08)
            ctx.set_source_rgba(*INK, 0.55)
            ctx.set_line_width(lw * 0.6)
            ctx.stroke()

    def _hand(self, ctx, x, y, lw, pose, side):
        circle(ctx, x, y, 0.17)
        fill_stroke(ctx, self.p["skin"] if pose.outfit != "suit" else self.p["suit_acc"], lw)

    # ------------------------------------------------------------------
    def _tool(self, ctx, pose: Pose, lw):
        tl = pose.tool or {}
        typ = tl.get("type")
        if typ == "shovel":
            gx, gy = tl.get("grip", (0.4, -1.6))
            ang = tl.get("angle", 0.3)
            with saved(ctx):
                ctx.translate(gx, gy)
                ctx.rotate(ang)
                # mango
                limb(ctx, [(0, -0.75), (0, 1.25)], 0.10, (0.72, 0.48, 0.25), out=lw)
                # empuñadura en T
                limb(ctx, [(-0.16, -0.78), (0.16, -0.78)], 0.09, (0.25, 0.25, 0.3), out=lw)
                # pala
                ctx.new_path()
                ctx.move_to(-0.22, 1.2)
                ctx.line_to(0.22, 1.2)
                ctx.curve_to(0.26, 1.55, 0.12, 1.75, 0.0, 1.82)
                ctx.curve_to(-0.12, 1.75, -0.26, 1.55, -0.22, 1.2)
                ctx.close_path()
                fill_stroke(ctx, self.p["metal"], lw)
                ctx.move_to(-0.08, 1.3)
                ctx.line_to(-0.04, 1.6)
                ctx.set_source_rgba(1, 1, 1, 0.8)
                ctx.set_line_width(0.05)
                ctx.stroke()
                if tl.get("dirt", 0) > 0:
                    ellipse(ctx, 0, 1.3, 0.2, 0.1 * tl["dirt"] + 0.02)
                    fill_stroke(ctx, self.p["dirt"], lw * 0.7)
        elif typ == "drill":
            # taladradora gigante: cuerpo naranja + broca giratoria hacia abajo
            gx, gy = tl.get("pos", (0.0, -1.25))
            spin = tl.get("spin", 0.0)
            with saved(ctx):
                ctx.translate(gx, gy)
                # broca
                ctx.new_path()
                ctx.move_to(-0.32, 0.35)
                ctx.line_to(0.32, 0.35)
                ctx.line_to(0.0, 1.35)
                ctx.close_path()
                fill_stroke(ctx, self.p["metal"], lw)
                with saved(ctx):
                    ctx.move_to(-0.32, 0.35)
                    ctx.line_to(0.32, 0.35)
                    ctx.line_to(0.0, 1.35)
                    ctx.close_path()
                    ctx.clip()
                    ctx.set_line_width(0.09)
                    ctx.set_source_rgb(*self.p["metal_dk"])
                    for k in range(-2, 8):
                        yy = 0.35 + ((k * 0.17 + spin * 0.17) % 1.36)
                        ctx.move_to(-0.4, yy)
                        ctx.line_to(0.4, yy + 0.14)
                    ctx.stroke()
                # cuerpo
                rrect(ctx, -0.55, -0.35, 1.1, 0.72, 0.18)
                fill_stroke(ctx, self.p["orange"], lw)
                rrect(ctx, -0.42, -0.2, 0.84, 0.16, 0.07)
                ctx.set_source_rgb(*darken(self.p["orange"], 0.25))
                ctx.fill()
                circle(ctx, 0.3, 0.14, 0.07)
                ctx.set_source_rgb(*self.p["green"])
                ctx.fill()
                # asas
                for s in (-1, 1):
                    limb(ctx, [(0.55 * s, -0.1), (0.78 * s, -0.1)], 0.12, (0.25, 0.25, 0.3), out=lw)

    # ------------------------------------------------------------------
    def _head(self, ctx, pose: Pose, lw):
        hx, hy = HEAD_C
        fx = pose.facing * 0.10   # desplazamiento 3/4 de los rasgos
        # cuello
        rrect(ctx, -0.2, -2.42, 0.4, 0.3, 0.1)
        fill_stroke(ctx, self.p["skin_sh"], lw)
        # orejas
        for s in (-1, 1):
            ellipse(ctx, hx + 0.98 * s, hy + 0.08, 0.17, 0.22)
            fill_stroke(ctx, self.p["skin"], lw)
        # cara
        ctx.new_path()
        smooth_closed(ctx, [(hx, hy - 0.98), (hx + 0.86, hy - 0.62), (hx + 1.0, hy + 0.12),
                            (hx + 0.72, hy + 0.74), (hx, hy + 0.9), (hx - 0.72, hy + 0.74),
                            (hx - 1.0, hy + 0.12), (hx - 0.86, hy - 0.62)])
        fill_stroke(ctx, self.p["skin"], lw)
        # barba (paso del tiempo)
        if pose.beard > 0.02:
            b = pose.beard
            ctx.new_path()
            smooth_closed(ctx, [(hx - 0.8, hy + 0.3), (hx - 0.6, hy + 0.75 + 0.6 * b),
                                (hx, hy + 0.95 + 1.3 * b), (hx + 0.6, hy + 0.75 + 0.6 * b),
                                (hx + 0.8, hy + 0.3), (hx + 0.4, hy + 0.55), (hx, hy + 0.62),
                                (hx - 0.4, hy + 0.55)])
            fill_stroke(ctx, lighten((0.55, 0.55, 0.6), 0.35 * b), lw)
        # pelo (tupé característico)
        self._hair(ctx, pose, lw)
        # mejillas
        for s in (-1, 1):
            ellipse(ctx, hx + 0.58 * s + fx, hy + 0.32, 0.17, 0.10)
            ctx.set_source_rgba(*self.p["cheek"], 0.45)
            ctx.fill()
        self._eyes(ctx, pose, lw, fx)
        # nariz
        ctx.new_path()
        ctx.arc(hx + fx * 1.4, hy + 0.17, 0.09, math.pi * 0.1, math.pi * 0.95)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(lw * 0.8)
        ctx.stroke()
        self._mouth(ctx, pose, lw, fx)
        # sudor
        if pose.sweat > 0.05:
            for i, (sx, sy) in enumerate(((0.9, -0.4), (-0.95, -0.2), (0.75, 0.25))):
                ph = (pose.t * 1.3 + i * 0.37) % 1
                if i / 3 > pose.sweat:
                    continue
                yy = hy + sy + ph * 0.6
                with saved(ctx):
                    ctx.translate(hx + sx, yy)
                    ctx.scale(0.12, 0.17)
                    ctx.move_to(0, -1)
                    ctx.curve_to(0.9, 0.2, 0.7, 1, 0, 1)
                    ctx.curve_to(-0.7, 1, -0.9, 0.2, 0, -1)
                    ctx.close_path()
                    ctx.set_source_rgba(0.55, 0.85, 1, 1 - ph * 0.5)
                    ctx.fill_preserve()
                    ctx.set_source_rgba(*INK, 1 - ph * 0.5)
                    ctx.set_line_width(lw / 0.14)
                    ctx.stroke()
        # casco
        if pose.helmet == "hardhat":
            ctx.new_path()
            ctx.move_to(hx - 0.95, hy - 0.42)
            ctx.curve_to(hx - 0.95, hy - 1.45, hx + 0.95, hy - 1.45, hx + 0.95, hy - 0.42)
            ctx.close_path()
            fill_stroke(ctx, self.p["yellow"], lw)
            rrect(ctx, hx - 1.12, hy - 0.5, 2.24, 0.16, 0.08)
            fill_stroke(ctx, self.p["yellow"], lw)
            rrect(ctx, hx - 0.15, hy - 1.14, 0.3, 0.22, 0.06)
            fill_stroke(ctx, (1, 1, 0.85), lw * 0.8)
        elif pose.helmet == "diving":
            # gafas de buceo (cristal casi transparente: los ojos siguen viéndose) + tubo
            for sd in (-1, 1):
                rrect(ctx, hx + sd * 0.98 - (0.0 if sd > 0 else -0.0) - 0.06, hy - 0.26, 0.12, 0.14, 0.05)
            ctx.set_source_rgb(*self.p["red"])
            ctx.fill()
            rrect(ctx, hx - 0.7 + fx, hy - 0.58, 1.4, 0.8, 0.3)
            ctx.set_source_rgba(0.7, 0.95, 1.0, 0.18)
            ctx.fill_preserve()
            ctx.set_source_rgb(*self.p["red"])
            ctx.set_line_width(0.09)
            ctx.stroke_preserve()
            ctx.set_source_rgb(*INK)
            ctx.set_line_width(lw * 0.6)
            ctx.stroke()
            ctx.move_to(hx - 0.45 + fx, hy - 0.48)
            ctx.line_to(hx - 0.25 + fx, hy - 0.48)
            ctx.set_source_rgba(1, 1, 1, 0.8)
            ctx.set_line_width(0.06)
            ctx.stroke()
            limb(ctx, [(hx + 0.95, hy + 0.2), (hx + 1.15, hy - 0.4), (hx + 1.12, hy - 1.2)], 0.14,
                 self.p["yellow"], out=lw)
        elif pose.helmet == "dome":
            ellipse(ctx, hx, hy - 0.02, 1.32, 1.28)
            ctx.set_source_rgba(0.7, 0.9, 1.0, 0.22)
            ctx.fill_preserve()
            ctx.set_source_rgba(*INK, 1)
            ctx.set_line_width(lw)
            ctx.stroke()
            ctx.new_path()
            ctx.arc(hx, hy - 0.02, 1.12, math.pi * 1.1, math.pi * 1.45)
            ctx.set_source_rgba(1, 1, 1, 0.75)
            ctx.set_line_width(0.12)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.stroke()
            # cuello del traje
            rrect(ctx, hx - 0.75, hy + 0.95, 1.5, 0.32, 0.14)
            fill_stroke(ctx, self.p["metal_dk"], lw)
            # antena con luz
            ctx.move_to(hx + 0.5, hy - 1.15)
            ctx.line_to(hx + 0.7, hy - 1.6)
            ctx.set_source_rgb(*INK)
            ctx.set_line_width(lw)
            ctx.stroke()
            circle(ctx, hx + 0.7, hy - 1.62, 0.09)
            blink_on = (pose.t * 2) % 1 < 0.5
            fill_stroke(ctx, self.p["red"] if blink_on else darken(self.p["red"], 0.5), lw * 0.7)
            if pose.cracks > 0:
                self._cracks(ctx, pose.cracks, lw)

    def _cracks(self, ctx, amount, lw):
        hx, hy = HEAD_C
        ctx.set_source_rgba(1, 1, 1, 0.95)
        ctx.set_line_width(0.045)
        segs = [[(0.6, -0.9), (0.45, -0.6), (0.62, -0.42), (0.4, -0.15)],
                [(-0.9, -0.5), (-0.65, -0.45), (-0.7, -0.2), (-0.45, -0.05)],
                [(0.95, 0.2), (0.7, 0.3), (0.78, 0.55)],
                [(-0.3, -1.2), (-0.2, -0.95), (-0.35, -0.8)]]
        nseg = max(1, int(round(amount * len(segs))))
        for s in segs[:nseg]:
            ctx.move_to(hx + s[0][0], hy + s[0][1])
            for p in s[1:]:
                ctx.line_to(hx + p[0], hy + p[1])
            ctx.stroke()

    def _hair(self, ctx, pose: Pose, lw):
        hx, hy = HEAD_C
        if pose.helmet == "hardhat":
            return
        wob = 0.03 * math.sin(pose.t * 5)
        ctx.new_path()
        ctx.move_to(hx - 0.92, hy - 0.42)
        ctx.curve_to(hx - 1.0, hy - 1.05, hx - 0.4, hy - 1.18, hx - 0.1, hy - 1.05)
        ctx.curve_to(hx - 0.2, hy - 1.5 + wob, hx + 0.35, hy - 1.62 + wob, hx + 0.62, hy - 1.38 + wob)
        ctx.curve_to(hx + 0.42, hy - 1.32, hx + 0.38, hy - 1.18, hx + 0.48, hy - 1.08)
        ctx.curve_to(hx + 0.75, hy - 1.18, hx + 1.0, hy - 0.9, hx + 0.94, hy - 0.42)
        ctx.curve_to(hx + 0.7, hy - 0.72, hx + 0.3, hy - 0.66, hx + 0.12, hy - 0.8)
        ctx.curve_to(hx - 0.1, hy - 0.6, hx - 0.6, hy - 0.62, hx - 0.92, hy - 0.42)
        ctx.close_path()
        fill_stroke(ctx, self.p["hair"], lw)
        ctx.move_to(hx + 0.05, hy - 1.18)
        ctx.curve_to(hx + 0.2, hy - 1.35, hx + 0.35, hy - 1.4, hx + 0.48, hy - 1.38)
        ctx.set_source_rgba(1, 1, 1, 0.45)
        ctx.set_line_width(0.06)
        ctx.stroke()

    def _eyes(self, ctx, pose: Pose, lw, fx):
        hx, hy = HEAD_C
        ex = pose.expression
        lx, ly = pose.look
        big = ex in ("surprised", "scared", "wow", "shock")
        rx, ry = (0.27, 0.34) if big else (0.24, 0.30)
        pr = 0.10 if big else 0.13
        for s in (-1, 1):
            cx, cy = hx + 0.38 * s + fx, hy - 0.18
            if ex in ("happy_closed", "laugh"):
                ctx.new_path()
                ctx.arc(cx, cy + 0.05, 0.17, math.pi * 1.1, math.pi * 1.9)
                ctx.set_source_rgb(*INK)
                ctx.set_line_width(lw * 1.2)
                ctx.stroke()
            elif ex == "dizzy":
                ctx.new_path()
                for k in range(30):
                    a = k * 0.5 + pose.t * 8
                    r = 0.01 + k * 0.007
                    (ctx.move_to if k == 0 else ctx.line_to)(cx + r * math.cos(a), cy + r * math.sin(a))
                ctx.set_source_rgb(*INK)
                ctx.set_line_width(lw * 0.8)
                ctx.stroke()
            else:
                b = clamp(pose.blink)
                if ex in ("smug", "tired", "hot"):
                    b = max(b, 0.42)
                ellipse(ctx, cx, cy, rx, ry * max(0.08, 1 - b))
                fill_stroke(ctx, WHITE_(), lw)
                if b < 0.85:
                    with saved(ctx):
                        ellipse(ctx, cx, cy, rx, ry * max(0.08, 1 - b))
                        ctx.clip()
                        px = cx + (lx + pose.facing * 0.35) * 0.09
                        py = cy + ly * 0.12 + (0.02 if ex == "hot" else 0)
                        circle(ctx, px, py, pr)
                        ctx.set_source_rgb(*INK)
                        ctx.fill()
                        circle(ctx, px + 0.04, py - 0.05, pr * 0.35)
                        ctx.set_source_rgb(1, 1, 1)
                        ctx.fill()
                        if ex == "wow":
                            from .draw import star
                            star(ctx, px, py, pr * 1.1)
                            ctx.set_source_rgb(*PAL["yellow"])
                            ctx.fill()
        # cejas
        brow = {
            "happy": (0.05, 0.0), "excited": (0.15, 0.1), "surprised": (0.28, 0.0), "scared": (0.22, -0.3),
            "worried": (0.12, -0.35), "determined": (0.0, 0.32), "angry": (-0.02, 0.45), "smug": (0.05, 0.2),
            "hot": (0.05, -0.2), "wow": (0.25, 0.0), "shock": (0.32, -0.1), "neutral": (0.05, 0.0),
            "dizzy": (0.12, -0.2), "laugh": (0.12, 0.0), "happy_closed": (0.1, 0.0), "tired": (0.0, -0.15),
        }.get(ex, (0.05, 0.0))
        raise_, tilt = brow
        for s in (-1, 1):
            cx = hx + 0.38 * s + fx
            y0 = hy - 0.6 - raise_
            ctx.move_to(cx - 0.2 * s - 0.0, y0 + (tilt * 0.12 if s == -1 else tilt * 0.12) * (1))
            inner_y = y0 + tilt * 0.12
            outer_y = y0 - tilt * 0.08
            ctx.new_path()
            ctx.move_to(cx + 0.2 * s, outer_y)
            ctx.curve_to(cx + 0.05 * s, outer_y - 0.08, cx - 0.1 * s, inner_y - 0.05, cx - 0.2 * s, inner_y)
            ctx.set_source_rgb(*darken(self.p["hair"], 0.55))
            ctx.set_line_width(0.11)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.stroke()

    def _mouth(self, ctx, pose: Pose, lw, fx):
        hx, hy = HEAD_C
        mx, my = hx + fx * 1.2, hy + 0.48
        ex = pose.expression
        o = clamp(pose.mouth_open)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        open_shapes = {"surprised", "scared", "shock", "wow"}
        if o > 0.06 or ex in open_shapes or ex in ("laugh", "excited"):
            base = {"surprised": 0.22, "scared": 0.18, "shock": 0.3, "wow": 0.16,
                    "laugh": 0.2, "excited": 0.14}.get(ex, 0.0)
            h = max(base, 0.05 + 0.3 * o)
            w = 0.3 if ex in ("surprised", "scared", "shock", "wow") else 0.36 + 0.06 * o
            if ex in ("happy", "excited", "laugh", "smug", "determined", "neutral", "hot", "happy_closed"):
                # boca en D (sonriente hablando)
                ctx.new_path()
                ctx.move_to(mx - w, my - 0.05)
                ctx.curve_to(mx - w * 0.6, my - 0.1, mx + w * 0.6, my - 0.1, mx + w, my - 0.05)
                ctx.curve_to(mx + w * 0.9, my + h * 1.5, mx - w * 0.9, my + h * 1.5, mx - w, my - 0.05)
                ctx.close_path()
            else:
                ellipse(ctx, mx, my + h * 0.4, w * 0.75, h)
            fill_stroke(ctx, (0.45, 0.08, 0.15), lw)
            with saved(ctx):
                if ex in ("happy", "excited", "laugh", "smug", "determined", "neutral", "hot", "happy_closed"):
                    ctx.new_path()
                    ctx.move_to(mx - w, my - 0.05)
                    ctx.curve_to(mx - w * 0.6, my - 0.1, mx + w * 0.6, my - 0.1, mx + w, my - 0.05)
                    ctx.curve_to(mx + w * 0.9, my + h * 1.5, mx - w * 0.9, my + h * 1.5, mx - w, my - 0.05)
                    ctx.close_path()
                else:
                    ellipse(ctx, mx, my + h * 0.4, w * 0.75, h)
                ctx.clip()
                # dientes y lengua
                rrect(ctx, mx - w, my - 0.12, 2 * w, 0.1, 0.03)
                ctx.set_source_rgb(1, 1, 1)
                ctx.fill()
                ellipse(ctx, mx + 0.04, my + h * 1.1, w * 0.6, h * 0.55)
                ctx.set_source_rgb(1.0, 0.45, 0.5)
                ctx.fill()
                if ex == "hot":
                    pass
        else:
            ctx.new_path()
            if ex in ("worried", "scared", "tired", "dizzy"):
                ctx.move_to(mx - 0.25, my + 0.05)
                ctx.curve_to(mx - 0.1, my - 0.06, mx + 0.08, my + 0.12, mx + 0.25, my + 0.0)
            elif ex in ("angry",):
                ctx.move_to(mx - 0.22, my + 0.08)
                ctx.curve_to(mx - 0.1, my - 0.05, mx + 0.1, my - 0.05, mx + 0.22, my + 0.08)
            elif ex == "smug":
                ctx.move_to(mx - 0.22, my + 0.02)
                ctx.curve_to(mx - 0.05, my + 0.1, mx + 0.15, my + 0.05, mx + 0.3, my - 0.1)
            elif ex == "determined":
                ctx.move_to(mx - 0.22, my + 0.04)
                ctx.line_to(mx + 0.22, my + 0.01)
            else:
                ctx.move_to(mx - 0.3, my - 0.02)
                ctx.curve_to(mx - 0.15, my + 0.2, mx + 0.15, my + 0.2, mx + 0.3, my - 0.02)
            ctx.set_source_rgb(*INK)
            ctx.set_line_width(lw * 1.1)
            ctx.stroke()


def WHITE_():
    return (1, 1, 1)


# ======================================================================
# Acciones: funciones puras t -> Pose (animación procedimental)
# ======================================================================
def act(action: str, t: float, dur: float, base: Pose, p: dict | None = None) -> Pose:
    p = p or {}
    f = ACTIONS.get(action, a_idle)
    pose = f(t, dur, replace(base, t=t), p)
    # parpadeo natural
    bt = (t + (hash(action) % 7) * 0.31) % 3.1
    if bt < 0.12 and pose.blink == 0:
        pose.blink = math.sin(bt / 0.12 * math.pi)
    return pose


def a_idle(t, d, b: Pose, p):
    br = math.sin(t * 2 * math.pi * 0.9)
    b.squash = 0.012 * br
    b.arm_l = (0.22 + 0.03 * br, 0.3)
    b.arm_r = (0.22 + 0.03 * br, 0.3)
    b.head_tilt = 0.04 * math.sin(t * 1.3)
    return b


def a_talk(t, d, b: Pose, p):
    b = a_idle(t, d, b, p)
    g = 0.5 + 0.5 * math.sin(t * 3.1)
    g2 = 0.5 + 0.5 * math.sin(t * 2.3 + 1.0)
    b.arm_r = (0.5 + 0.8 * g, 1.3 + 0.3 * g)
    b.arm_l = (0.3 + 0.5 * g2, 0.9 + 0.5 * g2)
    b.head_tilt = 0.08 * math.sin(t * 2.2)
    b.lean = 0.03 * math.sin(t * 1.7)
    return b


def a_present(t, d, b: Pose, p):
    b = a_idle(t, d, b, p)
    k = min(1, t / 0.25)
    b.arm_r = (lerp(0.2, 1.75, k), lerp(0.3, -0.25, k))
    b.arm_l = (0.35, 0.9)
    b.head_tilt = 0.1
    b.look = (1, -0.2)
    return b


def a_point_up(t, d, b: Pose, p):
    b = a_idle(t, d, b, p)
    k = min(1, t / 0.2)
    b.arm_r = (lerp(0.2, 2.9, k), 0.1 + 0.05 * math.sin(t * 6))
    b.arm_l = (0.3, 1.0)
    b.look = (0.3, -1)
    b.head_tilt = -0.1
    return b


def a_point_down(t, d, b: Pose, p):
    b = a_idle(t, d, b, p)
    b.arm_r = (0.7, 0.4 + 0.08 * math.sin(t * 6))
    b.look = (0.6, 1)
    b.head_tilt = 0.12
    return b


def a_dig(t, d, b: Pose, p):
    period = p.get("period", 0.62)
    ph = (t % period) / period
    if ph < 0.45:     # clavar
        k = ph / 0.45
        ang = lerp(-0.15, 0.35, k)
        gy = lerp(-2.0, -1.45, k ** 2)
        dirt = 0.0
    else:             # levantar y lanzar
        k = (ph - 0.45) / 0.55
        ang = lerp(0.35, -1.25, math.sin(k * math.pi / 2)) if k < 0.7 else lerp(-1.25, -0.15, (k - 0.7) / 0.3)
        gy = lerp(-1.45, -2.0, math.sin(min(1, k) * math.pi / 2))
        dirt = 1.0 if k < 0.55 else 0.0
    gx = 0.55
    b.tool = {"type": "shovel", "angle": ang, "grip": (gx, gy), "dirt": dirt}
    # manos sobre el mango
    ca, sa = math.cos(ang), math.sin(ang)
    h1 = (gx - sa * -0.6, gy + ca * -0.6)
    h2 = (gx - sa * 0.35, gy + ca * 0.35)
    b.hand_l, b.hand_r = h1, h2
    b.lean = 0.12 + 0.1 * math.sin(ph * 2 * math.pi)
    b.squash = 0.04 * math.sin(ph * 2 * math.pi)
    b.leg_l, b.leg_r = (0.2, 0.25), (0.15, 0.1)
    b.look = (0.8, 0.7)
    return b


def a_drill(t, d, b: Pose, p):
    j = p.get("intensity", 1.0)
    b.x += 6 * j * noise1(t * 40, 1)
    b.y += 4 * j * noise1(t * 37, 2)
    b.squash = 0.03 * j * math.sin(t * 50)
    b.tool = {"type": "drill", "pos": (0.0, -1.15), "spin": t * 9}
    b.hand_l, b.hand_r = (-0.78, -1.25), (0.78, -1.25)
    b.leg_l, b.leg_r = (0.32, 0.2), (0.32, 0.2)
    b.head_tilt = 0.05 * noise1(t * 20, 3)
    b.look = (0, 0.6)
    return b


def a_fall(t, d, b: Pose, p):
    fl = math.sin(t * 14)
    b.arm_l = (2.5 + 0.35 * fl, 0.4 + 0.3 * math.sin(t * 11))
    b.arm_r = (2.5 - 0.35 * fl, 0.4 + 0.3 * math.cos(t * 11))
    b.leg_l = (0.4 + 0.3 * math.sin(t * 12), 0.6)
    b.leg_r = (0.4 - 0.3 * math.sin(t * 12), 0.6)
    b.rot = p.get("spin", 0.5) * math.sin(t * 2.0)
    b.squash = -0.06
    b.look = (0, -1)
    return b


def a_float(t, d, b: Pose, p):
    b.arm_l = (1.35 + 0.2 * math.sin(t * 1.6), 0.25)
    b.arm_r = (1.35 + 0.2 * math.sin(t * 1.6 + 1), 0.25)
    b.leg_l = (0.35 + 0.1 * math.sin(t * 1.3), 0.3)
    b.leg_r = (0.35 + 0.1 * math.sin(t * 1.3 + 2), 0.3)
    b.rot = 0.18 * math.sin(t * 0.9) + p.get("spin_rate", 0.0) * t
    b.y += 18 * math.sin(t * 1.8)
    return b


def a_swim(t, d, b: Pose, p):
    s = math.sin(t * 5)
    b.arm_l = (2.2 + 0.9 * s, 0.4)
    b.arm_r = (2.2 - 0.9 * s, 0.4)
    b.leg_l = (0.3 + 0.25 * s, 0.4)
    b.leg_r = (0.3 - 0.25 * s, 0.4)
    b.y += 12 * math.sin(t * 3)
    b.rot = 0.08 * math.sin(t * 2.5)
    return b


def a_shock(t, d, b: Pose, p):
    k = min(1, t / 0.35)
    jump = math.sin(k * math.pi) * 60 if t < 0.35 else 0
    b.y -= jump
    b.squash = 0.18 * math.sin(k * math.pi * 2) if t < 0.35 else 0.012 * math.sin(t * 6)
    b.arm_l = (2.3 + 0.1 * math.sin(t * 20), 0.5)
    b.arm_r = (2.3 + 0.1 * math.cos(t * 20), 0.5)
    b.leg_l, b.leg_r = (0.25, 0.1), (0.25, 0.1)
    b.x += 3 * noise1(t * 30)
    return b


def a_celebrate(t, d, b: Pose, p):
    ph = (t % 0.7) / 0.7
    b.y -= abs(math.sin(ph * math.pi)) * 70
    b.squash = -0.06 * math.sin(ph * math.pi) + (0.12 if ph < 0.08 else 0)
    b.arm_l = (2.6 + 0.2 * math.sin(t * 9), 0.3)
    b.arm_r = (2.6 + 0.2 * math.cos(t * 9), 0.3)
    b.leg_l = (0.2 + 0.2 * math.sin(ph * math.pi), 0.5 * math.sin(ph * math.pi))
    b.leg_r = b.leg_l
    return b


def a_smug(t, d, b: Pose, p):
    b = a_idle(t, d, b, p)
    b.hand_l = (0.3, -1.68)
    b.hand_r = (-0.3, -1.6)
    b.head_tilt = -0.12 + 0.03 * math.sin(t * 2)
    b.lean = -0.04
    return b


def a_sweat(t, d, b: Pose, p):
    b = a_idle(t, d, b, p)
    w = math.sin(t * 7)
    b.hand_r = (0.55 + 0.25 * w, -3.55)
    b.arm_l = (0.3, 0.3)
    b.head_tilt = 0.1
    b.sweat = 1.0
    return b


def a_squished(t, d, b: Pose, p):
    b.squash = -0.18 + 0.06 * math.sin(t * 4)
    b.arm_l = (0.1, 0.1)
    b.arm_r = (0.1, 0.1)
    b.x += 2 * noise1(t * 25)
    return b


def a_look_up(t, d, b: Pose, p):
    b = a_idle(t, d, b, p)
    b.hand_r = (0.3, -3.6)
    b.look = (0, -1)
    b.head_tilt = -0.12
    return b


def a_wave(t, d, b: Pose, p):
    b = a_idle(t, d, b, p)
    b.arm_r = (2.4, 0.5 + 0.5 * math.sin(t * 12))
    b.look = (1, 0)
    return b


def a_think(t, d, b: Pose, p):
    b = a_idle(t, d, b, p)
    b.hand_r = (0.1, -2.75)
    b.hand_l = (0.25, -1.55)
    b.look = (0.6, -0.8)
    b.head_tilt = 0.12
    return b


def a_shrug(t, d, b: Pose, p):
    b = a_idle(t, d, b, p)
    k = 0.5 + 0.5 * math.sin(t * 3)
    b.arm_l = (1.0 + 0.2 * k, 1.6)
    b.arm_r = (1.0 + 0.2 * k, 1.6)
    b.head_tilt = 0.15 * math.sin(t * 1.5)
    b.y -= 8 * k
    return b


def a_walk(t, d, b: Pose, p):
    s = math.sin(t * 9)
    b.leg_l = (0.5 * s, 0.3 * max(0, -s) + 0.1)
    b.leg_r = (-0.5 * s, 0.3 * max(0, s) + 0.1)
    b.arm_l = (-0.4 * s + 0.2, 0.4)
    b.arm_r = (0.4 * s + 0.2, 0.4)
    b.y -= abs(math.cos(t * 9)) * 10
    return b


ACTIONS = {
    "idle": a_idle, "talk": a_talk, "present": a_present, "point_up": a_point_up,
    "point_down": a_point_down, "dig": a_dig, "drill": a_drill, "fall": a_fall, "float": a_float,
    "swim": a_swim, "shock": a_shock, "celebrate": a_celebrate, "smug": a_smug, "sweat": a_sweat,
    "squished": a_squished, "look_up": a_look_up, "wave": a_wave, "think": a_think,
    "shrug": a_shrug, "walk": a_walk,
}
EXPRESSIONS = ["happy", "excited", "surprised", "scared", "worried", "determined", "angry", "smug",
               "hot", "wow", "shock", "neutral", "dizzy", "laugh", "happy_closed", "tired"]
