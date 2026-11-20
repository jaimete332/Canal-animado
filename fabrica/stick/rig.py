"""Stickman rig: forward kinematics, actions (procedural animation), faces, hats, outfits and held items.

Local coordinates: origin = point between the feet on the ground, +x = the direction the character faces,
+y = down. Angles are measured from "straight down" and grow towards the front, so an arm at 0 hangs, at
pi/2 points forward and at pi points up. Every action is a pure function of time, so scenes can be rendered
in parallel and any frame can be previewed on its own.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import cairo

from ..visuals.draw import clamp, ease_back, ease_io, ease_out, lerp, noise1
from .style import INK, LW, P, c, circ, ink_fill, line, poly, rrect, shade, stroke

# body proportions (px at scale 1)
HEAD_R = 34.0
NECK = 8.0
TORSO = 108.0
UPPER_ARM, FOREARM = 60.0, 56.0
THIGH, SHIN = 68.0, 66.0
LEG = THIGH + SHIN
TAU = 2 * math.pi

JOINTS = ("lean", "neck", "sh_b", "el_b", "sh_f", "el_f", "hp_b", "kn_b", "hp_f", "kn_f", "dx", "dy", "rot")


@dataclass
class Pose:
    lean: float = 0.0      # torso tilt (forward +)
    neck: float = 0.0      # extra head tilt
    sh_b: float = -0.12    # back arm (shoulder, elbow)
    el_b: float = 0.15
    sh_f: float = 0.12     # front arm
    el_f: float = 0.15
    hp_b: float = -0.06    # back leg (hip, knee)
    kn_b: float = 0.0
    hp_f: float = 0.06     # front leg
    kn_f: float = 0.0
    dx: float = 0.0        # body offset (px, scale 1)
    dy: float = 0.0        # negative = up
    rot: float = 0.0       # whole-body rotation around the hips (falls, lying down)

    def blend(self, o: "Pose", k: float) -> "Pose":
        return Pose(**{j: lerp(getattr(self, j), getattr(o, j), k) for j in JOINTS})


def _wave(t, f, ph=0.0):
    return math.sin(TAU * f * t + ph)


# ---------------------------------------------------------------------------
# Actions: f(t, dur, params) -> Pose
# ---------------------------------------------------------------------------
def a_idle(t, d, p):
    b = _wave(t, 0.33)
    return Pose(sh_b=-0.12 + 0.03 * b, sh_f=0.12 - 0.03 * b, dy=1.5 * b, neck=0.03 * _wave(t, 0.21, 1))


def a_talk(t, d, p):
    """Explaining: alternating hand gestures."""
    g = noise1(t * 1.6, 3)
    h = noise1(t * 1.3, 9)
    return Pose(sh_f=0.75 + 0.35 * g, el_f=0.9 + 0.4 * h, sh_b=0.25 + 0.2 * h, el_b=0.7 + 0.3 * g,
                lean=0.03 * g, neck=0.05 * noise1(t * 2, 4), dy=1.5 * _wave(t, 0.5))


def a_point(t, d, p):
    up = p.get("height", 0.0)  # -1 down … 1 up
    k = ease_out(clamp(t / 0.3))
    a = lerp(0.2, math.pi / 2 + up * 0.8, k)
    return Pose(sh_f=a + 0.02 * _wave(t, 1.5), el_f=0.05, sh_b=-0.15, el_b=0.2, lean=0.04 * k,
                neck=-0.05 * up)


def a_point_up(t, d, p):
    return a_point(t, d, {"height": 1.0})


def a_wave(t, d, p):
    return Pose(sh_f=2.6, el_f=0.5 + 0.45 * _wave(t, 2.2), sh_b=-0.1, dy=1.5 * _wave(t, 0.5))


def a_walk(t, d, p):
    f = p.get("speed", 1.0) * 1.05
    s = _wave(t, f)
    s2 = _wave(t, f, math.pi / 2)
    return Pose(hp_f=0.42 * s, hp_b=-0.42 * s, kn_f=0.5 * max(0, -s2), kn_b=0.5 * max(0, s2),
                sh_f=-0.38 * s, sh_b=0.38 * s, el_f=0.35, el_b=0.35, lean=0.06,
                dy=-3 * abs(_wave(t, f * 2 / 2, math.pi / 2)) + 2)


def a_run(t, d, p):
    f = p.get("speed", 1.0) * 1.7
    s = _wave(t, f)
    s2 = _wave(t, f, math.pi / 2)
    return Pose(hp_f=0.75 * s + 0.15, hp_b=-0.75 * s + 0.15, kn_f=0.3 + 0.9 * max(0, -s2), kn_b=0.3 + 0.9 * max(0, s2),
                sh_f=-0.9 * s, sh_b=0.9 * s, el_f=1.3, el_b=1.3, lean=0.28,
                dy=-9 * abs(_wave(t, f, math.pi / 2)) + 4)


def a_panic(t, d, p):
    """Running in place, arms flailing above the head."""
    r = a_run(t, d, {"speed": 1.3})
    r.sh_f = 2.6 + 0.4 * _wave(t, 3.1)
    r.sh_b = 2.5 + 0.4 * _wave(t, 2.7, 1)
    r.el_f = 0.4 * _wave(t, 3.3)
    r.el_b = 0.4 * _wave(t, 2.9)
    r.lean = 0.05
    return r


def a_jump(t, d, p):
    ph = (t * p.get("speed", 1.0)) % 1.0
    h = math.sin(ph * math.pi)
    return Pose(dy=-90 * h, hp_f=0.3 * h, hp_b=-0.1 + 0.4 * h, kn_f=0.9 * h, kn_b=0.9 * h,
                sh_f=0.3 + 2.4 * h, sh_b=0.2 + 2.3 * h, el_f=0.2, el_b=0.2)


def a_cheer(t, d, p):
    b = abs(_wave(t, 1.4))
    return Pose(sh_f=2.25 + 0.2 * b, sh_b=-2.3 - 0.2 * b, el_f=0.25, el_b=-0.25, dy=-28 * b,
                kn_f=0.3 * b, kn_b=0.3 * b, hp_f=0.1, hp_b=-0.1, neck=-0.1)


def a_shrug(t, d, p):
    k = ease_io(clamp(t / 0.4)) * (1 - 0.3 * ease_io(clamp((t - 1.6) / 0.5)))
    return Pose(sh_f=lerp(0.1, 0.55, k), el_f=lerp(0.1, 2.0, k), sh_b=lerp(-0.1, 0.45, k), el_b=lerp(0.1, 2.0, k),
                neck=0.12 * k, dy=-4 * k)


def a_think(t, d, p):
    return Pose(sh_f=0.35, el_f=2.55, sh_b=0.45, el_b=1.4, neck=-0.12 + 0.03 * _wave(t, 0.4), lean=-0.02,
                dy=1.2 * _wave(t, 0.33))


def a_facepalm(t, d, p):
    k = ease_out(clamp(t / 0.3))
    return Pose(sh_f=lerp(0.1, 1.05, k), el_f=lerp(0.1, 2.35, k), neck=0.25 * k, lean=0.12 * k, sh_b=-0.05)


def a_sad(t, d, p):
    return Pose(lean=0.16, neck=0.32, sh_f=0.05, sh_b=-0.02, el_f=0.05, el_b=0.05, dy=4 + 1.5 * _wave(t, 0.25))


def a_cower(t, d, p):
    j = 2.5 * noise1(t * 20, 2)
    return Pose(sh_f=2.3, el_f=1.9, sh_b=2.1, el_b=1.9, lean=0.25, neck=0.35, kn_f=0.6, kn_b=0.6,
                hp_f=0.45, hp_b=0.2, dy=26 + j, dx=j)


def a_shiver(t, d, p):
    j = 2.2 * noise1(t * 26, 5)
    return Pose(sh_f=0.7, el_f=2.3, sh_b=0.55, el_b=2.3, lean=0.1, neck=0.15, dx=j, dy=2 + abs(j),
                hp_f=0.04, hp_b=-0.04)


def a_angry(t, d, p):
    s = _wave(t, 3.0)
    return Pose(sh_f=0.6 + 0.25 * s, el_f=2.2, sh_b=0.4 - 0.25 * s, el_b=2.2, lean=0.12, dy=-3 * abs(s),
                hp_f=0.18, hp_b=-0.18)


def a_laugh(t, d, p):
    s = abs(_wave(t, 2.3))
    return Pose(lean=-0.18 + 0.06 * s, neck=-0.2, sh_f=0.6, el_f=1.9, sh_b=0.5, el_b=1.9, dy=-5 * s,
                hp_f=0.1, hp_b=-0.1)


def a_sit(t, d, p):
    """Sitting on a stool/ground (hips lowered, thighs forward)."""
    b = _wave(t, 0.3)
    return Pose(dy=p.get("drop", 62), hp_f=1.45, kn_f=1.5, hp_b=1.35, kn_b=1.45, sh_f=0.6, el_f=0.8,
                sh_b=0.4, el_b=0.8, lean=-0.04 + 0.02 * b)


def a_sit_talk(t, d, p):
    s = a_sit(t, d, p)
    tk = a_talk(t, d, p)
    s.sh_f, s.el_f, s.sh_b, s.el_b = tk.sh_f, tk.el_f, tk.sh_b, tk.el_b
    return s


def a_kneel(t, d, p):
    return Pose(dy=58, hp_f=1.5, kn_f=1.5, hp_b=0.15, kn_b=1.6, lean=0.05, sh_f=0.3, sh_b=0.1)


def a_pray(t, d, p):
    k = a_kneel(t, d, p)
    k.sh_f, k.el_f, k.sh_b, k.el_b, k.neck = 0.7, 1.7, 0.55, 1.85, 0.22
    k.dy += 1.2 * _wave(t, 0.3)
    return k


def a_bow(t, d, p):
    k = ease_io(clamp(t / 0.5))
    return Pose(lean=0.9 * k, neck=0.2 * k, sh_f=0.3 * k, sh_b=0.2 * k, hp_f=-0.05, hp_b=0.05)


def a_lie(t, d, p):
    """Lying on the back (sleeping, sick, or dead)."""
    b = _wave(t, 0.25) * p.get("breathe", 1.0)
    return Pose(rot=-math.pi / 2, dy=LEG - 14, dx=-50, sh_f=0.25, sh_b=-0.2, hp_f=0.04, hp_b=-0.04,
                el_f=0.1 + 0.03 * b, lean=0.01 * b, neck=-0.05)


def a_fall(t, d, p):
    k = clamp(t / p.get("time", 0.7))
    k = k * k
    return Pose(rot=-math.pi / 2 * k, dy=(LEG - 14) * k, dx=-50 * k, sh_f=lerp(0.2, 2.4, min(1, k * 2)) if k < 1 else 0.25,
                sh_b=lerp(-0.1, 2.0, min(1, k * 2)) if k < 1 else -0.2, hp_f=0.3 * (1 - k), kn_f=0.4 * (1 - k))


def a_dig(t, d, p):
    """Hoeing / digging / chopping: tool raised then struck down."""
    f = p.get("speed", 0.9)
    ph = (t * f) % 1.0
    raise_ = ease_io(clamp(ph / 0.55))
    strike = ease_out(clamp((ph - 0.55) / 0.2))
    k = raise_ - strike
    return Pose(sh_f=lerp(0.65, 2.75, k), el_f=lerp(0.25, 0.45, k), sh_b=lerp(0.55, 2.55, k), el_b=lerp(0.4, 0.6, k),
                lean=lerp(0.35, -0.05, k), neck=0.1, hp_f=0.3, hp_b=-0.25, kn_f=0.15, dy=lerp(6, 0, k))


def a_carry(t, d, p):
    """Carrying something heavy in front (arms forward), slow walk if walking."""
    w = a_walk(t, d, {"speed": 0.8}) if p.get("walking", True) else a_idle(t, d, p)
    w.sh_f, w.el_f, w.sh_b, w.el_b = 1.1, 0.6, 1.0, 0.6
    w.lean = 0.12
    return w


def a_hold(t, d, p):
    """Holding an item out in front, showing it to the camera."""
    b = _wave(t, 0.4)
    return Pose(sh_f=1.25 + 0.03 * b, el_f=0.45, sh_b=-0.1, el_b=0.2, dy=1.2 * b)


def a_hold_up(t, d, p):
    k = ease_back(clamp(t / 0.4))
    return Pose(sh_f=lerp(0.2, 2.95, k), el_f=0.1, sh_b=0.3 * k, el_b=0.6, dy=-4 * k + 1.5 * _wave(t, 0.6))


def a_eat(t, d, p):
    ph = (t * 1.1) % 1.0
    k = math.sin(ph * math.pi) ** 2
    return Pose(sh_f=lerp(0.9, 0.55, k), el_f=lerp(0.9, 2.55, k), sh_b=0.1, el_b=0.4, neck=-0.06 * k,
                dy=1.2 * _wave(t, 0.4))


def a_drink(t, d, p):
    k = ease_io(clamp(t / 0.5))
    return Pose(sh_f=lerp(0.8, 1.5, k), el_f=lerp(0.8, 2.2, k), neck=-0.35 * k, lean=-0.08 * k, sh_b=-0.1)


def a_sick(t, d, p):
    """Bent over, coughing."""
    cough = max(0, _wave(t, 1.3)) ** 6
    return Pose(lean=0.45 + 0.12 * cough, neck=0.2, sh_f=0.9, el_f=1.6, sh_b=0.7, el_b=1.0, kn_f=0.25, kn_b=0.25,
                hp_f=0.25, hp_b=0.0, dy=6 + 4 * cough)


def a_punch(t, d, p):
    ph = (t * 1.6) % 1.0
    k = ease_out(clamp(ph / 0.25)) * (1 - ease_io(clamp((ph - 0.4) / 0.5)))
    return Pose(sh_f=lerp(1.0, 1.6, k), el_f=lerp(2.2, 0.05, k), sh_b=0.9, el_b=2.2, lean=lerp(0.05, 0.25, k),
                hp_f=0.35, hp_b=-0.3, kn_f=0.2)


def a_swing(t, d, p):
    """Sword / club swing."""
    ph = (t * p.get("speed", 1.1)) % 1.0
    k = ease_io(clamp(ph / 0.45)) - ease_out(clamp((ph - 0.45) / 0.18))
    return Pose(sh_f=lerp(0.9, 2.9, k), el_f=lerp(0.2, 0.7, k), sh_b=0.6, el_b=1.6, lean=lerp(0.25, -0.05, k),
                hp_f=0.35, hp_b=-0.3, kn_f=0.2)


def a_push(t, d, p):
    w = a_walk(t, d, {"speed": 0.55})
    w.sh_f, w.el_f, w.sh_b, w.el_b, w.lean = 1.45, 0.5, 1.35, 0.6, 0.38
    return w


def a_pull(t, d, p):
    s = _wave(t, 0.9)
    return Pose(sh_f=1.4, el_f=0.2 + 0.25 * s, sh_b=1.3, el_b=0.3 + 0.25 * s, lean=-0.35 - 0.05 * s,
                hp_f=0.5, kn_f=0.3, hp_b=-0.1, dx=-6 * s)


def a_write(t, d, p):
    j = noise1(t * 7, 3)
    s = a_sit(t, d, p) if p.get("sitting", True) else a_idle(t, d, p)
    s.sh_f, s.el_f, s.sh_b, s.el_b, s.neck = 1.0 + 0.05 * j, 1.3, 0.9, 1.2, 0.3
    s.lean = 0.12
    return s


def a_count(t, d, p):
    """Counting coins in the palm."""
    j = abs(_wave(t, 2.2))
    return Pose(sh_f=0.7, el_f=1.4 + 0.25 * j, sh_b=0.6, el_b=1.6, neck=0.3, lean=0.05)


def a_sleep(t, d, p):
    return a_lie(t, d, {"breathe": 2.0})


def a_dead(t, d, p):
    return a_lie(t, d, {"breathe": 0.0})


def a_dance(t, d, p):
    s = _wave(t, 1.8)
    s2 = _wave(t, 0.9)
    return Pose(sh_f=1.5 + 1.1 * s, sh_b=1.5 - 1.1 * s, el_f=0.8, el_b=0.8, hp_f=0.3 * max(0, s2), kn_f=0.6 * max(0, s2),
                hp_b=-0.3 * max(0, -s2), kn_b=0.6 * max(0, -s2), dy=-8 * abs(s), lean=0.08 * s2)


def a_sneak(t, d, p):
    w = a_walk(t, d, {"speed": 0.6})
    w.lean, w.dy = 0.35, w.dy + 18
    w.kn_f += 0.5
    w.kn_b += 0.5
    w.sh_f, w.el_f, w.sh_b, w.el_b = 0.9, 1.8, 0.7, 1.8
    return w


def a_stir(t, d, p):
    """Stirring a pot / working at a table."""
    a = TAU * 0.7 * t
    return Pose(sh_f=0.95 + 0.12 * math.sin(a), el_f=0.8 + 0.2 * math.cos(a), sh_b=0.5, el_b=1.0, lean=0.15, neck=0.2)


def a_scratch(t, d, p):
    """Scratching the head (confused or itchy)."""
    j = _wave(t, 4.0)
    return Pose(sh_f=2.1, el_f=2.0 + 0.2 * j, sh_b=-0.1, neck=0.12, lean=-0.03)


def a_itch(t, d, p):
    """Scratching all over (fleas!)."""
    j = _wave(t, 5.0)
    j2 = _wave(t, 4.3, 1)
    return Pose(sh_f=0.8 + 0.2 * j, el_f=2.2, sh_b=1.0 + 0.2 * j2, el_b=1.9, lean=0.1 + 0.05 * j, dx=2 * j2,
                kn_f=0.15 * max(0, j))


ACTIONS = {
    "idle": a_idle, "talk": a_talk, "point": a_point, "point_up": a_point_up, "wave": a_wave, "walk": a_walk,
    "run": a_run, "panic": a_panic, "jump": a_jump, "cheer": a_cheer, "shrug": a_shrug, "think": a_think,
    "facepalm": a_facepalm, "sad": a_sad, "cower": a_cower, "shiver": a_shiver, "angry": a_angry,
    "laugh": a_laugh, "sit": a_sit, "sit_talk": a_sit_talk, "kneel": a_kneel, "pray": a_pray, "bow": a_bow,
    "lie": a_lie, "sleep": a_sleep, "dead": a_dead, "fall": a_fall, "dig": a_dig, "chop": a_dig,
    "carry": a_carry, "hold": a_hold, "hold_up": a_hold_up, "eat": a_eat, "drink": a_drink, "sick": a_sick,
    "punch": a_punch, "swing": a_swing, "push": a_push, "pull": a_pull, "write": a_write, "count": a_count,
    "dance": a_dance, "sneak": a_sneak, "stir": a_stir, "scratch": a_scratch, "itch": a_itch,
}
TALKY = {"talk", "sit_talk", "point", "point_up", "shrug", "wave", "angry", "laugh", "hold", "hold_up"}

EXPRESSIONS = ("neutral", "happy", "grin", "sad", "angry", "scared", "surprised", "worried", "smug", "dead",
               "sleepy", "disgusted", "sick", "crying", "thinking", "laughing", "determined", "tired")


# ---------------------------------------------------------------------------
# Character description
# ---------------------------------------------------------------------------
@dataclass
class Look:
    color: tuple = INK                 # line colour (grey for background extras)
    head_fill: tuple = P["skin"]
    outfit: str | None = None          # tunic | dress | robe | armor | apron | suit | rags
    outfit_color: str = "brown"
    hat: str | None = None             # hood | straw_hat | crown | helmet | mitre | tonsure | coif | kerchief | ...
    hat_color: str | None = None
    hair: str | None = None            # long | bun | spiky | messy
    beard: str | None = None           # short | long
    scarf: bool = False                # Stan's signature red scarf
    scarf_color: str = "red"
    item: str | None = None            # held in the front hand
    item_back: str | None = None       # held in the back hand
    belly: float = 0.0                 # 0..1 (rich and well fed)
    seed: int = 0


@dataclass
class Placement:
    x: float
    y: float
    scale: float = 1.0
    facing: float = 1.0
    expression: str = "neutral"
    mouth_open: float = 0.0
    alpha: float = 1.0
    extras: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Drawing
# ---------------------------------------------------------------------------
def _dir(a):
    """Unit vector for an angle measured from straight down, + towards the front."""
    return math.sin(a), math.cos(a)


def skeleton(pose: Pose) -> dict:
    """Joint positions in local space (before the global body rotation, which is applied around the hips)."""
    hx, hy = pose.dx, -LEG + pose.dy
    tx, ty = math.sin(pose.lean), -math.cos(pose.lean)
    neck = (hx + tx * TORSO, hy + ty * TORSO)
    sh = (hx + tx * TORSO * 0.88, hy + ty * TORSO * 0.88)
    ha = pose.lean + pose.neck
    head = (neck[0] + math.sin(ha) * (HEAD_R + NECK), neck[1] - math.cos(ha) * (HEAD_R + NECK))
    j = {"hip": (hx, hy), "neck": neck, "sh": sh, "head": head, "head_a": ha}
    for side in ("b", "f"):
        a1 = getattr(pose, f"sh_{side}") + pose.lean
        a2 = a1 + getattr(pose, f"el_{side}")
        d1, d2 = _dir(a1), _dir(a2)
        el = (sh[0] + d1[0] * UPPER_ARM, sh[1] + d1[1] * UPPER_ARM)
        hd = (el[0] + d2[0] * FOREARM, el[1] + d2[1] * FOREARM)
        j[f"el_{side}"], j[f"hand_{side}"], j[f"fa_{side}"] = el, hd, a2
        l1 = getattr(pose, f"hp_{side}")
        l2 = l1 - getattr(pose, f"kn_{side}")
        e1, e2 = _dir(l1), _dir(l2)
        kn = (hx + e1[0] * THIGH, hy + e1[1] * THIGH)
        ft = (kn[0] + e2[0] * SHIN, kn[1] + e2[1] * SHIN)
        j[f"kn_{side}"], j[f"ft_{side}"], j[f"shin_{side}"] = kn, ft, l2
    return j


class Stickman:
    def __init__(self, look: Look):
        self.look = look

    def draw(self, ctx: cairo.Context, pose: Pose, pl: Placement, t: float = 0.0):
        lk = self.look
        j = skeleton(pose)
        if abs(pl.scale) < 0.01:
            return j
        ctx.save()
        ctx.translate(pl.x, pl.y)
        ctx.scale(pl.scale * pl.facing, pl.scale)
        if pose.rot:
            ctx.translate(*j["hip"])
            ctx.rotate(pose.rot)
            ctx.translate(-j["hip"][0], -j["hip"][1])
        if pl.alpha < 1:
            ctx.push_group()
        col_ = lk.color

        def limb(a, b, cc, w=LW):
            ctx.move_to(*a)
            ctx.line_to(*b)
            ctx.line_to(*cc)
            stroke(ctx, w, col_)

        # back limbs
        limb(j["sh"], j["el_b"], j["hand_b"])
        if lk.item_back:
            draw_item(ctx, lk.item_back, j["hand_b"], j["fa_b"], t)
        if lk.outfit not in ("dress", "robe"):
            limb(j["hip"], j["kn_b"], j["ft_b"])
            limb(j["hip"], j["kn_f"], j["ft_f"])
        else:
            # long garments: only the shins peek out
            limb(j["hip"], j["kn_b"], j["ft_b"])
            limb(j["hip"], j["kn_f"], j["ft_f"])
        # torso
        if lk.belly > 0 and not lk.outfit:
            mx, my = lerp(j["hip"][0], j["neck"][0], 0.45), lerp(j["hip"][1], j["neck"][1], 0.45)
            ctx.save()
            ctx.translate(mx + 16 * lk.belly, my)
            ctx.scale(1, 1.25)
            circ(ctx, 0, 0, 30 * lk.belly + 4)
            ctx.restore()
            ink_fill(ctx, P["paper"], LW * 0.9, ink=col_)
        line(ctx, *j["hip"], *j["neck"], LW, col_)
        if lk.outfit:
            draw_outfit(ctx, lk, j, pose)
        if lk.scarf:
            draw_scarf(ctx, lk, j, t)
        # head
        hx, hy = j["head"]
        if lk.hair in ("long", "bun"):
            draw_hair_back(ctx, lk, hx, hy, j["head_a"])
        ctx.save()
        ctx.translate(hx, hy)
        ctx.rotate(j["head_a"])
        if lk.hat in ("hood",):
            draw_hat(ctx, lk, t, back=True)
        circ(ctx, 0, 0, HEAD_R)
        fill = P["sick"] if pl.expression == "sick" else lk.head_fill
        ink_fill(ctx, fill, LW * 0.95, ink=col_)
        if lk.beard:
            draw_beard(ctx, lk)
        draw_face(ctx, pl.expression, pl.mouth_open, t, lk.seed, col_)
        if lk.hair in ("spiky", "messy", "bun", "long"):
            draw_hair_top(ctx, lk)
        if lk.hat:
            draw_hat(ctx, lk, t)
        ctx.restore()
        # front arm + item
        limb(j["sh"], j["el_f"], j["hand_f"])
        if lk.item:
            draw_item(ctx, lk.item, j["hand_f"], j["fa_f"], t)
        if pl.alpha < 1:
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(pl.alpha)
        ctx.restore()
        return j


# ---------------------------------------------------------------------------
# Face
# ---------------------------------------------------------------------------
def _blink(t, seed):
    ph = (t + seed * 1.37) % 3.7
    return ph < 0.12


def draw_face(ctx, expr, mouth_open, t, seed, color=INK):
    ex, ey, gap = 11.0, -5.0, 13.0          # eyes shifted towards the front (3/4 view)
    eyes = [(ex - gap, ey), (ex + gap, ey)]
    blink = _blink(t, seed) and expr not in ("dead", "sleepy", "laughing")
    ctx.set_source_rgb(*color)

    def dots(r=4.6):
        for x, y in eyes:
            circ(ctx, x, y, r)
        ctx.set_source_rgb(*color)
        ctx.fill()

    def closed(curve=1.0):
        for x, y in eyes:
            ctx.move_to(x - 6, y)
            ctx.curve_to(x - 3, y + 4 * curve, x + 3, y + 4 * curve, x + 6, y)
        stroke(ctx, 3.6, color)

    def big_eyes(r=9.0, pupil=3.6):
        for x, y in eyes:
            circ(ctx, x, y - 1, r)
            ink_fill(ctx, "white", 3.2, ink=color)
            circ(ctx, x + 1.5, y - 1, pupil)
            ctx.set_source_rgb(*color)
            ctx.fill()

    def brows(inner, outer, lift=0.0):
        """inner/outer: vertical offsets of each brow end (negative = higher)."""
        for i, (x, y) in enumerate(eyes):
            sgn = 1 if i == 0 else -1       # inner end is towards the other eye
            ctx.move_to(x - sgn * 8, y - 13 + outer - lift)
            ctx.line_to(x + sgn * 6, y - 13 + inner - lift)
        stroke(ctx, 3.4, color)

    mx, my = ex + 1, 15.0

    def mouth_arc(w, curve):
        ctx.move_to(mx - w, my)
        ctx.curve_to(mx - w / 2, my + curve, mx + w / 2, my + curve, mx + w, my)
        stroke(ctx, 3.6, color)

    def mouth_open_shape(w, h, fill=INK):
        ctx.save()
        ctx.translate(mx, my + h * 0.3)
        ctx.scale(max(w, 1), max(h, 1))
        circ(ctx, 0, 0, 1)
        ctx.restore()
        ink_fill(ctx, (0.35, 0.08, 0.1) if fill is INK else fill, 3.0, ink=color)

    # eyes + brows
    if expr == "dead":
        for x, y in eyes:
            line(ctx, x - 5, y - 5, x + 5, y + 5, 3.6, color)
            line(ctx, x - 5, y + 5, x + 5, y - 5, 3.6, color)
    elif expr in ("sleepy", "tired"):
        for x, y in eyes:
            line(ctx, x - 6, y + 1, x + 6, y + 1, 3.6, color)
        if expr == "tired":
            brows(-2, 3)
    elif expr == "laughing" or (expr == "happy" and blink):
        for x, y in eyes:
            ctx.move_to(x - 6, y + 2)
            ctx.curve_to(x - 3, y - 5, x + 3, y - 5, x + 6, y + 2)
        stroke(ctx, 3.6, color)
    elif blink:
        closed(0.4)
    elif expr in ("scared", "surprised"):
        big_eyes(8.5 if expr == "scared" else 8.0, 3.0 if expr == "scared" else 3.6)
        brows(-6, -2, 3)
    elif expr == "smug":
        for x, y in eyes:
            line(ctx, x - 6, y, x + 6, y, 3.6, color)
            circ(ctx, x + 1, y + 2.5, 3)
            ctx.fill()
        brows(1, -3)
    elif expr == "disgusted":
        for x, y in eyes:
            line(ctx, x - 6, y - 2, x + 6, y + 2, 3.6, color)
        brows(4, -2)
    else:
        dots()
        if expr in ("sad", "worried", "crying", "sick"):
            brows(-5, 2)
        elif expr in ("angry", "determined"):
            brows(5, -3)
        elif expr == "thinking":
            for i, (x, y) in enumerate(eyes):
                ctx.move_to(x - 7, y - 13 - (6 if i else 0))
                ctx.line_to(x + 7, y - 13 - (6 if i else 0))
            stroke(ctx, 3.4, color)
    # mouth
    mo = clamp(mouth_open)
    if expr == "dead":
        line(ctx, mx - 9, my + 2, mx + 9, my + 2, 3.6, color)
    elif mo > 0.08 and expr not in ("sleepy",):
        w = 7 + 4 * mo + (3 if expr in ("happy", "grin", "laughing") else 0)
        mouth_open_shape(w, 3 + 8 * mo)
    elif expr in ("happy", "smug"):
        mouth_arc(10 if expr == "happy" else 7, 9)
    elif expr in ("grin", "laughing"):
        ctx.move_to(mx - 13, my - 3)
        ctx.curve_to(mx - 8, my + 15, mx + 8, my + 15, mx + 13, my - 3)
        ctx.close_path()
        ink_fill(ctx, "white", 3.4, ink=color)
    elif expr in ("sad", "crying", "tired"):
        ctx.move_to(mx - 9, my + 5)
        ctx.curve_to(mx - 4, my - 4, mx + 4, my - 4, mx + 9, my + 5)
        stroke(ctx, 3.6, color)
    elif expr in ("scared", "worried", "sick", "disgusted"):
        ctx.move_to(mx - 11, my + 2)
        for k in range(1, 5):
            ctx.line_to(mx - 11 + k * 5.5, my + (-3 if k % 2 else 3))
        stroke(ctx, 3.2, color)
    elif expr == "surprised":
        mouth_open_shape(5.5, 7)
    elif expr == "angry":
        ctx.move_to(mx - 10, my + 4)
        ctx.curve_to(mx - 4, my - 1, mx + 4, my - 1, mx + 10, my + 4)
        stroke(ctx, 3.6, color)
    elif expr == "thinking":
        line(ctx, mx - 2, my + 1, mx + 9, my - 2, 3.6, color)
    elif expr == "sleepy":
        circ(ctx, mx + 2, my + 2, 3.5)
        stroke(ctx, 3.0, color)
    else:
        line(ctx, mx - 7, my + 1, mx + 7, my + 1, 3.6, color)
    if expr == "crying":
        for i, (x, y) in enumerate(eyes):
            k = (t * 1.4 + i * 0.5) % 1.0
            ctx.move_to(x, y + 6)
            ctx.line_to(x, y + 6 + 26 * k)
            stroke(ctx, 3.6, (0.35, 0.65, 0.95), 0.9)
    if expr in ("scared", "worried", "sick") and (expr != "sick" or True):
        k = (t * 0.8 + seed * 0.3) % 1.0
        if expr != "worried" or k < 0.6:
            ctx.save()
            ctx.translate(-HEAD_R * 0.75, -HEAD_R * 0.35 + 18 * k)
            ctx.move_to(0, -7)
            ctx.curve_to(5, 0, 4, 6, 0, 6)
            ctx.curve_to(-4, 6, -5, 0, 0, -7)
            ctx.restore()
            ink_fill(ctx, (0.55, 0.8, 1.0), 2.0, ink=color)


# ---------------------------------------------------------------------------
# Hair, beards, hats
# ---------------------------------------------------------------------------
def draw_hair_back(ctx, lk, hx, hy, a):
    hc = c(lk.hat_color if lk.hair == "long" and False else "darkwood")
    ctx.save()
    ctx.translate(hx, hy)
    ctx.rotate(a)
    if lk.hair == "long":
        ctx.move_to(-HEAD_R * 0.2, -HEAD_R * 1.02)
        ctx.curve_to(-HEAD_R * 1.5, -HEAD_R * 0.9, -HEAD_R * 1.45, HEAD_R * 1.2, -HEAD_R * 0.9, HEAD_R * 1.75)
        ctx.line_to(-HEAD_R * 0.2, HEAD_R * 1.1)
        ctx.close_path()
        ink_fill(ctx, hc, 3.5)
    else:
        circ(ctx, -HEAD_R * 0.95, -HEAD_R * 0.55, HEAD_R * 0.42)
        ink_fill(ctx, hc, 3.5)
    ctx.restore()


def draw_hair_top(ctx, lk):
    hc = c("darkwood")
    R = HEAD_R
    if lk.hair == "spiky":
        pts = []
        for k in range(7):
            a = math.pi * (1.1 + 0.8 * k / 6)
            r = R * (1.32 if k % 2 else 1.0)
            pts.append((math.cos(a) * r, math.sin(a) * r))
        poly(ctx, pts, close=False)
        stroke(ctx, 3.6, INK)
    elif lk.hair == "messy":
        for k in range(5):
            a = math.pi * (1.15 + 0.7 * k / 4)
            ctx.move_to(math.cos(a) * R * 0.95, math.sin(a) * R * 0.95)
            ctx.line_to(math.cos(a + 0.1) * R * 1.3, math.sin(a + 0.1) * R * 1.3)
        stroke(ctx, 3.6, INK)
    else:  # long / bun: fringe cap
        ctx.arc(0, 0, R, math.pi * 1.0, math.pi * 1.9)
        ctx.curve_to(R * 0.5, -R * 0.55, -R * 0.4, -R * 0.45, -R, 0)
        ctx.close_path()
        ink_fill(ctx, hc, 3.5)


def draw_beard(ctx, lk):
    R = HEAD_R
    long_ = lk.beard == "long"
    ctx.move_to(-R * 0.55, R * 0.25)
    ctx.curve_to(-R * 0.3, R * (1.9 if long_ else 1.3), R * 0.9, R * (1.9 if long_ else 1.3), R * 0.95, R * 0.2)
    ctx.curve_to(R * 0.6, R * 0.75, -R * 0.1, R * 0.8, -R * 0.55, R * 0.25)
    ink_fill(ctx, "grey" if lk.beard == "grey" else "darkwood", 3.0)


def draw_hat(ctx, lk, t, back=False):
    h, R = lk.hat, HEAD_R
    hc = lk.hat_color
    if h == "hood":
        col_ = hc or "brown"
        if back:   # drawn behind the head: the hood's back and shoulder drape
            ctx.move_to(R * 0.75, -R * 0.75)
            ctx.curve_to(R * 0.2, -R * 1.65, -R * 1.6, -R * 1.45, -R * 1.35, R * 0.6)
            ctx.line_to(-R * 1.2, R * 1.35)
            ctx.line_to(R * 0.6, R * 1.35)
            ctx.close_path()
            ink_fill(ctx, col_, 3.8)
        else:      # rim around the face
            ctx.arc(R * 0.12, 0, R * 1.08, math.pi * 1.12, math.pi * 1.86)
            ctx.arc_negative(R * 0.12, 0, R * 0.88, math.pi * 1.86, math.pi * 1.12)
            ctx.close_path()
            ink_fill(ctx, shade(col_, 0.15), 3.2)
    elif h == "straw_hat":
        ctx.save()
        ctx.translate(0, -R * 0.62)
        ctx.scale(1, 0.24)
        circ(ctx, 0, 0, R * 1.75)
        ctx.restore()
        ink_fill(ctx, hc or "wheat", 3.6)
        ctx.move_to(-R * 0.8, -R * 0.62)
        ctx.curve_to(-R * 0.8, -R * 1.55, R * 0.8, -R * 1.55, R * 0.8, -R * 0.62)
        ctx.close_path()
        ink_fill(ctx, hc or "wheat", 3.6)
        line(ctx, -R * 0.78, -R * 0.82, R * 0.78, -R * 0.82, 5, "red")
    elif h == "crown":
        pts = [(-R * 0.85, -R * 0.7), (-R * 0.95, -R * 1.65), (-R * 0.45, -R * 1.15), (0, -R * 1.8),
               (R * 0.45, -R * 1.15), (R * 0.95, -R * 1.65), (R * 0.85, -R * 0.7)]
        poly(ctx, pts)
        ink_fill(ctx, hc or "gold", 3.6)
        for x in (-R * 0.95, 0, R * 0.95):
            circ(ctx, x, -R * 1.72 if x else -R * 1.86, 4.5)
            ink_fill(ctx, "red", 2.5)
    elif h == "helmet":
        ctx.arc(0, -R * 0.05, R * 1.12, math.pi, 2 * math.pi)
        ctx.line_to(R * 1.12, R * 0.15)
        ctx.line_to(-R * 1.12, R * 0.15)
        ctx.close_path()
        ink_fill(ctx, hc or "grey", 3.8)
        rrect(ctx, R * 0.18, -R * 0.15, R * 0.28, R * 0.95, 4)
        ink_fill(ctx, shade(hc or "grey", 0.2), 3.2)
    elif h == "mitre":
        ctx.move_to(-R * 0.75, -R * 0.75)
        ctx.curve_to(-R * 0.9, -R * 1.6, -R * 0.2, -R * 2.2, 0, -R * 2.45)
        ctx.curve_to(R * 0.2, -R * 2.2, R * 0.9, -R * 1.6, R * 0.75, -R * 0.75)
        ctx.close_path()
        ink_fill(ctx, hc or "white", 3.6)
        line(ctx, 0, -R * 0.8, 0, -R * 2.3, 5, "gold")
        line(ctx, -R * 0.5, -R * 1.5, R * 0.5, -R * 1.5, 5, "gold")
    elif h == "tonsure":
        ctx.arc(0, 0, R * 1.04, math.pi * 1.05, math.pi * 1.95)
        ctx.arc_negative(0, 0, R * 0.8, math.pi * 1.95, math.pi * 1.05)
        ctx.close_path()
        ink_fill(ctx, "darkwood", 3.0)
    elif h in ("coif", "kerchief"):
        col_ = hc or ("white" if h == "coif" else "tan")
        ctx.arc(0, 0, R * 1.1, math.pi * 0.95, math.pi * 2.02)
        ctx.curve_to(R * 0.6, -R * 0.3, -R * 0.6, -R * 0.35, -R * 1.1, R * 0.05)
        ctx.close_path()
        ink_fill(ctx, col_, 3.4)
        if h == "kerchief":
            poly(ctx, [(-R * 0.95, -R * 0.1), (-R * 1.55, R * 0.25), (-R * 1.2, R * 0.55)])
            ink_fill(ctx, col_, 3.0)
    elif h == "top_hat":
        rrect(ctx, -R * 0.75, -R * 2.2, R * 1.5, R * 1.5, 4)
        ink_fill(ctx, hc or "ink", 3.4)
        rrect(ctx, -R * 1.2, -R * 0.82, R * 2.4, R * 0.24, 5)
        ink_fill(ctx, hc or "ink", 3.4)
    elif h == "cap":
        ctx.arc(0, -R * 0.2, R * 1.0, math.pi * 1.05, math.pi * 1.95)
        ctx.close_path()
        ink_fill(ctx, hc or "red", 3.4)
        rrect(ctx, R * 0.3, -R * 0.5, R * 1.1, R * 0.22, 5)
        ink_fill(ctx, hc or "red", 3.0)
    elif h == "plague_mask":
        ctx.move_to(R * 0.55, -R * 0.35)
        ctx.curve_to(R * 1.6, -R * 0.1, R * 2.3, R * 0.6, R * 2.4, R * 1.0)
        ctx.curve_to(R * 1.7, R * 0.75, R * 1.0, R * 0.6, R * 0.55, R * 0.45)
        ctx.close_path()
        ink_fill(ctx, "white", 3.4)
        for x in (R * 0.1, R * 0.6):
            circ(ctx, x, -R * 0.2, 7.5)
            ink_fill(ctx, (0.75, 0.85, 0.9), 3.0)
        # wide-brim hat
        ctx.save()
        ctx.translate(0, -R * 0.75)
        ctx.scale(1, 0.22)
        circ(ctx, 0, 0, R * 1.7)
        ctx.restore()
        ink_fill(ctx, "ink", 3.0)
        rrect(ctx, -R * 0.8, -R * 1.6, R * 1.6, R * 0.9, 6)
        ink_fill(ctx, "ink", 3.0)
    elif h == "wizard":
        poly(ctx, [(-R * 1.0, -R * 0.65), (R * 0.1, -R * 2.6), (R * 1.0, -R * 0.65)])
        ink_fill(ctx, hc or "purple", 3.6)
    elif h == "headband":
        ctx.arc(0, 0, R * 1.0, math.pi * 1.12, math.pi * 1.88)
        stroke(ctx, 9, hc or "red")
    elif h == "laurel":
        for k in range(9):
            a = math.pi * (1.05 + 0.9 * k / 8)
            x, y = math.cos(a) * R * 1.02, math.sin(a) * R * 1.02
            ctx.save()
            ctx.translate(x, y)
            ctx.rotate(a + math.pi / 2)
            ctx.scale(0.45, 1)
            circ(ctx, 0, 0, 9)
            ctx.restore()
            ink_fill(ctx, "green", 2.2)
    elif h == "legion":          # Roman legionary helmet with red crest
        ctx.arc(0, -R * 0.05, R * 1.1, math.pi, 2 * math.pi)
        ctx.close_path()
        ink_fill(ctx, hc or (0.78, 0.66, 0.36), 3.6)
        poly(ctx, [(-R * 1.1, -R * 0.05), (-R * 1.25, R * 0.45), (-R * 0.8, R * 0.4)])
        ink_fill(ctx, hc or (0.78, 0.66, 0.36), 3.0)
        ctx.move_to(-R * 0.7, -R * 1.0)
        ctx.curve_to(-R * 0.4, -R * 1.75, R * 0.4, -R * 1.75, R * 0.7, -R * 1.0)
        ctx.close_path()
        ink_fill(ctx, "red", 3.0)
    elif h == "viking":
        ctx.arc(0, -R * 0.05, R * 1.08, math.pi, 2 * math.pi)
        ctx.close_path()
        ink_fill(ctx, hc or "grey", 3.6)
        line(ctx, 0, -R * 1.1, 0, -R * 0.1, 5, "darkgrey")
        rrect(ctx, R * 0.15, -R * 0.2, R * 0.2, R * 0.7, 3)
        ink_fill(ctx, "darkgrey", 2.5)
    elif h == "tricorn":         # pirate hat
        ctx.move_to(-R * 1.5, -R * 0.55)
        ctx.curve_to(-R * 0.8, -R * 0.9, -R * 0.6, -R * 1.9, 0, -R * 1.7)
        ctx.curve_to(R * 0.6, -R * 1.9, R * 0.8, -R * 0.9, R * 1.5, -R * 0.55)
        ctx.curve_to(R * 0.6, -R * 0.75, -R * 0.6, -R * 0.75, -R * 1.5, -R * 0.55)
        ink_fill(ctx, hc or "ink", 3.4)
        circ(ctx, 0, -R * 1.2, 6)
        ink_fill(ctx, "white", 2)
    elif h == "brodie":          # WW1 steel helmet
        ctx.save()
        ctx.translate(0, -R * 0.55)
        ctx.scale(1, 0.26)
        circ(ctx, 0, 0, R * 1.55)
        ctx.restore()
        ink_fill(ctx, hc or (0.45, 0.48, 0.36), 3.4)
        ctx.arc(0, -R * 0.55, R * 0.85, math.pi, 2 * math.pi)
        ctx.close_path()
        ink_fill(ctx, hc or (0.45, 0.48, 0.36), 3.4)
    elif h == "flat_cap":
        ctx.arc(0, -R * 0.25, R * 1.0, math.pi * 1.05, math.pi * 1.95)
        ctx.close_path()
        ink_fill(ctx, hc or "darkgrey", 3.2)
        ctx.save()
        ctx.translate(R * 0.75, -R * 0.45)
        ctx.scale(1, 0.3)
        circ(ctx, 0, 0, R * 0.55)
        ctx.restore()
        ink_fill(ctx, hc or "darkgrey", 3.0)
    elif h == "fur_hood":
        ctx.arc(R * 0.1, 0, R * 1.18, math.pi * 1.0, math.pi * 1.95)
        ctx.arc_negative(R * 0.1, 0, R * 0.9, math.pi * 1.95, math.pi * 1.0)
        ctx.close_path()
        ink_fill(ctx, (0.62, 0.47, 0.32), 3.2)
    elif h == "nemes":           # Egyptian striped headcloth
        ctx.move_to(-R * 1.15, R * 0.9)
        ctx.line_to(-R * 1.2, -R * 0.2)
        ctx.arc(0, -R * 0.1, R * 1.15, math.pi, 2 * math.pi)
        ctx.line_to(R * 0.95, R * 0.1)
        ctx.line_to(R * 0.75, -R * 0.35)
        ctx.arc_negative(0, -R * 0.1, R * 0.82, -0.3, math.pi + 0.2)
        ctx.line_to(-R * 0.75, R * 0.9)
        ctx.close_path()
        ink_fill(ctx, hc or "gold", 3.2)
        for k in range(-2, 3):
            line(ctx, k * R * 0.32, -R * 1.1, k * R * 0.36, -R * 0.75, 3, "blue")


def draw_outfit(ctx, lk, j, pose):
    hx, hy = j["hip"]
    nx, ny = j["neck"]
    a = pose.lean
    ca, sa = math.cos(a), math.sin(a)

    def P_(u, v):  # u along the torso (0 hips → 1 neck), v across (+ = front)
        return (hx + sa * TORSO * u + ca * v, hy - ca * TORSO * u + sa * v)

    o = lk.outfit
    colr = lk.outfit_color
    extra = None
    # era outfits built on the base garments
    if o == "toga":
        o, colr, extra = "robe", (colr if colr != "brown" else "white"), "toga"
    elif o in ("fur", "sailor", "uniform", "overalls"):
        extra = o
        colr = {"fur": (0.6, 0.45, 0.3), "sailor": "white", "uniform": (0.55, 0.52, 0.36),
                "overalls": (0.3, 0.4, 0.6)}[o] if colr == "brown" else colr
        o = "rags" if o == "fur" else "tunic"
    if o in ("tunic", "rags", "apron", "suit", "armor"):
        bottom = -0.32 if o in ("tunic", "rags") else -0.05
        w_top, w_bot = 17, 27 if o in ("tunic", "rags") else 21
        b = 24 * lk.belly
        pts = [P_(0.92, -w_top), P_(0.92, w_top), P_(0.4, w_bot + b), P_(bottom, w_bot + b * 0.3), P_(bottom, -w_bot)]
        if o == "rags":
            pts = pts[:2] + [P_(bottom, w_bot), P_(bottom + 0.08, w_bot * 0.5), P_(bottom - 0.02, 0),
                             P_(bottom + 0.1, -w_bot * 0.5), P_(bottom, -w_bot)]
        poly(ctx, pts)
        ink_fill(ctx, "grey" if o == "armor" else colr, 4.0)
        if o in ("tunic", "rags"):
            a0, a1 = P_(0.18, -w_bot * 0.9), P_(0.18, w_bot * 0.9)
            line(ctx, *a0, *a1, 5, shade(colr, 0.35))
        if o == "armor":
            line(ctx, *P_(0.5, -18), *P_(0.5, 18), 3, "darkgrey")
            line(ctx, *P_(0.25, -20), *P_(0.25, 20), 3, "darkgrey")
        if o == "suit":
            poly(ctx, [P_(0.92, -3), P_(0.92, 5), P_(0.45, 1)])
            ink_fill(ctx, "red", 2.5)
        if o == "apron":
            poly(ctx, [P_(0.6, -10), P_(0.6, 14), P_(-0.25, 18), P_(-0.25, -12)])
            ink_fill(ctx, "white", 3.0)
    elif o in ("dress", "robe"):
        # the top follows the torso, the hem hangs from the hips towards the knees/feet
        w_bot = 40 if o == "dress" else 32
        kx = (j["kn_b"][0] + j["kn_f"][0]) / 2
        ky = max(j["kn_b"][1], j["kn_f"][1])
        fy = max(j["ft_b"][1], j["ft_f"][1])
        hem = lerp(ky, fy, 0.75 if o == "dress" else 0.85)
        hem_x = lerp(hx, kx, 0.6)
        hem = max(hem, hy + 30)
        spread = w_bot + 0.35 * abs(j["kn_f"][0] - j["kn_b"][0])
        b = 26 * lk.belly
        pts = [P_(0.92, -16), P_(0.92, 16), P_(0.45, 20 + b), P_(0.0, 22 + b * 0.6), (hem_x + spread, hem),
               (hem_x - spread, hem), P_(0.0, -22)]
        poly(ctx, pts)
        ink_fill(ctx, colr, 4.0)
        if o == "robe" and extra != "toga":
            line(ctx, *P_(0.1, -21), *P_(0.1, 21), 5, "tan")
    if extra == "toga":      # draped sash over one shoulder
        poly(ctx, [P_(0.95, -14), P_(0.95, 2), P_(0.05, 26), P_(-0.12, 18)])
        ink_fill(ctx, lk.hat_color if lk.hat_color in ("purple", "red") else "purple", 3.0)
    elif extra == "sailor":
        for u in (0.7, 0.45, 0.2):
            line(ctx, *P_(u, -19), *P_(u, 21), 5, "navy")
    elif extra == "uniform":
        line(ctx, *P_(0.05, -22), *P_(0.05, 23), 6, "darkwood")
        line(ctx, *P_(0.92, 8), *P_(0.05, 20), 4, "darkwood")
    elif extra == "fur":
        for u in (0.6, 0.25):
            for v in (-10, 6):
                line(ctx, *P_(u, v), *P_(u - 0.08, v + 4), 3, "darkwood")
    elif extra == "overalls":
        line(ctx, *P_(0.92, -6), *P_(0.4, -6), 5, "navy")
        line(ctx, *P_(0.92, 10), *P_(0.4, 10), 5, "navy")


def draw_scarf(ctx, lk, j, t):
    nx, ny = j["neck"]
    w = math.sin(t * 5.0) * 4
    ctx.move_to(nx - 14, ny - 4)
    ctx.line_to(nx + 15, ny - 4)
    ctx.line_to(nx + 13, ny + 9)
    ctx.line_to(nx - 13, ny + 9)
    ctx.close_path()
    ink_fill(ctx, lk.scarf_color, 3.2)
    ctx.move_to(nx - 10, ny + 4)
    ctx.curve_to(nx - 28, ny + 8 + w, nx - 40, ny + 4 - w, nx - 52, ny + 14 + w)
    ctx.line_to(nx - 47, ny + 26 + w)
    ctx.curve_to(nx - 35, ny + 16, nx - 22, ny + 20 + w, nx - 6, ny + 10)
    ctx.close_path()
    ink_fill(ctx, lk.scarf_color, 3.2)


# ---------------------------------------------------------------------------
# Held items (grip at the hand, drawn along the forearm direction)
# ---------------------------------------------------------------------------
def draw_item(ctx, name, hand, fa, t):
    ctx.save()
    ctx.translate(*hand)
    name = {"gladius": "sword", "pickaxe": "hoe", "oar": "staff"}.get(name, name)
    up = name in ("hoe", "pitchfork", "scythe", "spear", "sword", "torch", "axe", "shovel", "staff", "flag",
                  "hammer", "club", "broom", "candle", "sickle", "crook", "musket")
    # tools stay roughly perpendicular to the forearm (held like a real handle)
    ctx.rotate(-fa + (math.pi / 2 if up else 0) + math.pi)
    if name in ("hoe", "shovel", "pitchfork", "scythe", "spear", "staff", "flag", "broom", "axe", "hammer",
                "club", "crook", "sickle"):
        L = {"spear": 230, "staff": 200, "flag": 210, "broom": 170, "axe": 120, "hammer": 100, "club": 95,
             "sickle": 40, "crook": 200}.get(name, 170)
        if name not in ("sickle",):
            line(ctx, 0, 40 if name not in ("axe", "hammer", "club") else 20, 0, -L, 6.5, "wood")
            line(ctx, 0, 40 if name not in ("axe", "hammer", "club") else 20, 0, -L, 2.0, "darkwood")
        if name == "hoe":
            poly(ctx, [(0, -L), (28, -L + 4), (34, -L + 22), (4, -L + 12)])
            ink_fill(ctx, "grey", 3)
        elif name == "shovel":
            rrect(ctx, -15, -L - 38, 30, 42, 10)
            ink_fill(ctx, "grey", 3)
        elif name == "pitchfork":
            for dx in (-14, 0, 14):
                line(ctx, dx, -L, dx, -L - 34, 4, "grey")
            line(ctx, -14, -L, 14, -L, 4, "grey")
        elif name == "scythe":
            ctx.move_to(0, -L)
            ctx.curve_to(40, -L - 20, 90, -L - 5, 110, -L + 30)
            ctx.curve_to(80, -L + 5, 40, -L + 2, 0, -L + 12)
            ctx.close_path()
            ink_fill(ctx, "lightgrey", 3)
        elif name == "sickle":
            ctx.arc(14, -30, 26, math.pi * 0.9, math.pi * 2.1)
            stroke(ctx, 7, "lightgrey")
            line(ctx, 0, 10, 0, -12, 7, "wood")
        elif name == "spear":
            poly(ctx, [(-9, -L), (0, -L - 36), (9, -L)])
            ink_fill(ctx, "grey", 3)
        elif name == "flag":
            w = math.sin(t * 4) * 6
            ctx.move_to(0, -L)
            ctx.curve_to(40, -L - 10 + w, 70, -L + 10 - w, 100, -L + w)
            ctx.line_to(100, -L + 60 + w)
            ctx.curve_to(70, -L + 70 - w, 40, -L + 50 + w, 0, -L + 60)
            ctx.close_path()
            ink_fill(ctx, "red", 3)
        elif name == "broom":
            poly(ctx, [(-6, 40), (6, 40), (22, 95), (-22, 95)])
            ink_fill(ctx, "wheat", 3)
        elif name == "axe":
            ctx.move_to(0, -L + 6)
            ctx.curve_to(30, -L - 14, 42, -L + 6, 38, -L + 40)
            ctx.curve_to(26, -L + 30, 12, -L + 28, 0, -L + 30)
            ctx.close_path()
            ink_fill(ctx, "lightgrey", 3)
        elif name == "hammer":
            rrect(ctx, -22, -L - 16, 44, 26, 4)
            ink_fill(ctx, "darkgrey", 3)
        elif name == "club":
            ctx.save()
            ctx.translate(0, -L)
            ctx.scale(0.6, 1)
            circ(ctx, 0, 0, 28)
            ctx.restore()
            ink_fill(ctx, "wood", 3)
        elif name == "crook":
            ctx.arc(18, -L, 18, math.pi, 2 * math.pi)
            stroke(ctx, 6.5, "wood")
    elif name == "musket":
        line(ctx, 0, 40, 0, -150, 7, "darkwood")
        line(ctx, 3, -60, 3, -175, 4, "darkgrey")
    elif name == "sword":
        line(ctx, 0, 14, 0, -16, 7, "darkwood")
        line(ctx, -16, -16, 16, -16, 7, "gold")
        poly(ctx, [(-6, -18), (6, -18), (5, -130), (0, -145), (-5, -130)])
        ink_fill(ctx, "lightgrey", 3)
    elif name == "torch":
        line(ctx, 0, 30, 0, -70, 8, "wood")
        f = 1 + 0.15 * math.sin(t * 17) + 0.1 * math.sin(t * 11)
        ctx.move_to(0, -70)
        ctx.curve_to(-22 * f, -80, -10, -115 * f, 0, -128 * f)
        ctx.curve_to(10, -115 * f, 22 * f, -80, 0, -70)
        ink_fill(ctx, "fire", 3)
    elif name == "candle":
        rrect(ctx, -6, -40, 12, 40, 3)
        ink_fill(ctx, "white", 2.5)
        f = 1 + 0.15 * math.sin(t * 15)
        ctx.move_to(0, -42)
        ctx.curve_to(-7, -48, -3, -60 * f, 0, -64 * f)
        ctx.curve_to(3, -60 * f, 7, -48, 0, -42)
        ink_fill(ctx, "yellow", 2)
    else:
        # small things held in the palm, drawn upright
        ctx.restore()
        ctx.save()
        ctx.translate(*hand)
        draw_small(ctx, name, t)
    ctx.restore()


def draw_small(ctx, name, t):
    if name == "mug":
        rrect(ctx, -14, -30, 28, 34, 4)
        ink_fill(ctx, "wood", 3)
        ctx.arc(16, -14, 9, -math.pi / 2, math.pi / 2)
        stroke(ctx, 4, INK)
        ctx.save()
        ctx.translate(0, -32)
        ctx.scale(1, 0.4)
        circ(ctx, 0, 0, 14)
        ctx.restore()
        ink_fill(ctx, "white", 2.5)
    elif name == "bread":
        ctx.save()
        ctx.translate(4, -10)
        ctx.scale(1.4, 0.8)
        circ(ctx, 0, 0, 18)
        ctx.restore()
        ink_fill(ctx, "tan", 3)
        for dx in (-8, 4, 16):
            line(ctx, dx - 4, -16, dx + 2, -6, 3, "brown")
    elif name == "coin":
        circ(ctx, 0, -12, 14)
        ink_fill(ctx, "gold", 3)
        line(ctx, -4, -12, 4, -12, 3, "brown")
    elif name == "bag":
        ctx.move_to(-8, -40)
        ctx.curve_to(-34, -20, -30, 8, 0, 8)
        ctx.curve_to(30, 8, 34, -20, 8, -40)
        ctx.close_path()
        ink_fill(ctx, "tan", 3.4)
        line(ctx, -10, -40, 10, -40, 4, "brown")
        circ(ctx, 0, -14, 9)
        ink_fill(ctx, "gold", 2.5)
    elif name == "book":
        rrect(ctx, -22, -40, 44, 34, 3)
        ink_fill(ctx, "red", 3)
        line(ctx, 0, -40, 0, -6, 2.5, "darkwood")
    elif name == "scroll":
        rrect(ctx, -20, -54, 40, 54, 3)
        ink_fill(ctx, "parchment", 3)
        for k in range(3):
            line(ctx, -11, -42 + k * 12, 11, -42 + k * 12, 2.5, "brown")
    elif name == "bucket":
        poly(ctx, [(-20, -36), (20, -36), (15, 6), (-15, 6)])
        ink_fill(ctx, "wood", 3)
        ctx.arc(0, -36, 20, math.pi, 2 * math.pi)
        stroke(ctx, 3, INK)
    elif name == "flower":
        line(ctx, 0, 0, 0, -40, 3.5, "green")
        for k in range(5):
            a = k * TAU / 5
            circ(ctx, math.cos(a) * 8, -44 + math.sin(a) * 8, 6)
            ink_fill(ctx, "pink", 2)
        circ(ctx, 0, -44, 5)
        ink_fill(ctx, "yellow", 2)
    elif name == "rat":
        ctx.save()
        ctx.translate(0, -12)
        ctx.scale(1.5, 1)
        circ(ctx, 0, 0, 12)
        ctx.restore()
        ink_fill(ctx, "grey", 3)
        ctx.move_to(-18, -10)
        ctx.curve_to(-34, -6, -30, 10, -44, 4)
        stroke(ctx, 2.5, INK)
    elif name == "egg":
        ctx.save()
        ctx.translate(0, -14)
        ctx.scale(0.8, 1)
        circ(ctx, 0, 0, 13)
        ctx.restore()
        ink_fill(ctx, "white", 3)
    elif name == "apple":
        circ(ctx, 0, -14, 13)
        ink_fill(ctx, "red", 3)
        line(ctx, 0, -27, 3, -34, 3, "darkwood")
    elif name == "letter":
        rrect(ctx, -24, -34, 48, 32, 2)
        ink_fill(ctx, "white", 3)
        poly(ctx, [(-24, -34), (0, -16), (24, -34)], close=False)
        stroke(ctx, 2.5, INK)
