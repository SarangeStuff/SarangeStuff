"""Figures for the rolling doc. New: velocity profile, accelerations, gear on rack, spool. The rest are reused."""
import math
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
for sub in ("textbook", "guides/planekinetics", "guides/mock"):
    sys.path.insert(0, str(ROOT / sub))
from svgkit import Fig  # noqa: E402
from pk_figs import right_mark, curl  # noqa: E402
import figs  # noqa: E402
import figs2  # noqa: E402,F401  (registers the kinetics figures)
import pk_figs  # noqa: E402
import mock_figs  # noqa: E402

V = lambda x, y: np.array([float(x), float(y)])
T = lambda v: (float(v[0]), float(v[1]))
U = lambda d: V(math.cos(math.radians(d)), math.sin(math.radians(d)))


def ground(f, x1, x2, y=0.0):
    a, b = f.P((x1, y)), f.P((x2, y))
    f.hatch(a[0], a[1], b[0], b[1], side=1)


def k_vel():
    f = Fig(110, "Rolling without slip: every point moves as if pinned at the contact point C; speed grows with distance from C")
    O = V(0, 1.0); C = V(0, 0); r = 1.0
    ground(f, -1.8, 2.6)
    f.circle(T(O), r, "outline"); f.pin(T(O), 3)
    s = 0.55
    f.dot(T(C), r=4.5, cls="dotans"); f.text(T(C), "C: v = 0 (the IC)", "ans", dx=8, dy=14, anchor="start")
    f.arrow(T(O), T(O + V(s * 1.0 * 1.6, 0)), "abs", "v_{O} = rω", at=("N", 10), lpos=0.6)
    top = V(0, 2.0)
    f.arrow(T(top), T(top + V(s * 2.0 * 1.6, 0)), "abs", "2rω", at=("N", 10), lpos=0.6)
    f.line(T(C), T(top + V(s * 2.0 * 1.6, 0)), "cons")
    P = O + r * U(0)
    vP = s * 1.6 * math.sqrt(2) * U(-45 + 90 - 90)          # ⊥ CP, CW
    dirP = U(-45)
    f.line(T(C), T(P), "muted", dash="3 3")
    f.arrow(T(P), T(P + 0.9 * dirP), "abs", "√2 rω, ⊥ CP", at=("E", 6), lpos=1.0)
    f.arc(T(O), 26, 150, 30, "abs", "ω (CW)", arrow=True, ccw=False, lr=40, la=90)
    return f.svg()


def k_acc():
    f = Fig(110, "Rolling without slip: centre a = r alpha along the ground; contact point a = r omega squared straight up")
    O = V(0, 1.0); C = V(0, 0)
    ground(f, -1.8, 2.2)
    f.circle(T(O), 1.0, "outline"); f.pin(T(O), 3)
    f.arrow(T(O), T(O + V(0.9, 0)), "t", "a_{O} = rα (along the surface)", at=("N", 10), lpos=0.8)
    f.arrow(T(C), T(C + V(0, 0.75)), "n", "a_{C} = rω² (towards O)", at=("E", 6), lpos=0.6)
    f.dot(T(C), r=4, cls="dotans")
    f.text(T(C), "C: v = 0 but a ≠ 0", "ans", dx=-8, dy=14, anchor="end")
    return f.svg()


def k_rack():
    f = Fig(150, "L17 Example 1: gear rolling on a fixed rack; acceleration of the top point A (not to scale: 43.2 is huge)")
    O = V(0, 0.3 * 3); A = O + V(0, 0.9)
    f.line(T(V(-1.3, 0)), T(V(1.6, 0)), "ink"); ground(f, -1.3, 1.6)
    f.circle(T(O), 0.9, "outline"); f.pin(T(O), 3)
    f.dot(T(A)); f.text(T(A), "A", dx=-10, dy=-8, anchor="end")
    f.text(T(O), "O", dx=-10, dy=8, anchor="end")
    f.arrow(T(O), T(O + V(0.5, 0)), "t", "a_{O} = rα = 1.8", at=("S", 12), lpos=0.6)
    f.arrow(T(A), T(A + V(0.5, 0)), "t", "(a_{A/O})_{t} = rα = 1.8", at=("N", 10), lpos=0.6)
    f.arrow(T(A), T(A + V(0, -0.75)), "n", "(a_{A/O})_{n} = rω² = 43.2 (→ O)", at=("W", 6), lpos=0.5)
    f.text(T(V(0.9, 2.15)), "ω = 12 rad/s, α = 6 rad/s² (CW), r = 0.3 m", "muted")
    return f.svg()


def spool():
    f = Fig(120, "Spool pulled by a horizontal string from the top or the bottom of its hub: friction can point either way")
    for x0, top, F_dir, lab in ((0, True, +1, "string at TOP of hub: F = +1.92 N (forwards!)"),
                                (3.6, False, -1, "string at BOTTOM of hub: F = −32.7 N (backwards)")):
        O = V(x0, 1.0)
        ground(f, x0 - 1.4, x0 + 1.6)
        f.circle(T(O), 1.0, "outline"); f.circle(T(O), 0.5, "outline")
        f.pin(T(O), 3)
        y = 0.5 if top else -0.5
        f.line(T(O + V(0, y)), T(O + V(1.3, y)), "rope")
        f.arrow(T(O + V(1.0, y)), T(O + V(1.5, y)), "ans", "T", at=("N", 8), lpos=1.0)
        C = V(x0, 0)
        f.arrow(T(C), T(C + V(0.45 * F_dir, 0)), "ans", "F", at=("S", 12), lpos=1.0)
        f.arc(T(O), 24, 150, 30, "abs", "α (CW)", arrow=True, ccw=False, lr=38, la=90)
        f.text(T(V(x0 + 0.1, -0.55)), lab, "ans")
    return f.svg()


def build_all():
    out = {n: globals()[n]() for n in ("k_vel", "k_acc", "k_rack", "spool")}
    tb = figs.build_all()
    out["roll_fbd"], out["roll_kd"] = tb["k_roll_fbd"], tb["k_roll_kd"]
    pk = pk_figs.build_all()
    for k in ("w6_fbd", "w6_kd", "w6_graph", "w7_geom", "w7_fbd", "w7_kd", "w7_acc"):
        out[k] = pk[k]
    out["m8"] = mock_figs.build_all()["m8"]
    return out


if __name__ == "__main__":
    for k_, v_ in build_all().items():
        print(k_, len(v_))
