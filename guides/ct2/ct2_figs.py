"""Figures for the reconstructed CT2 2026 question and its clean memo (all true scale)."""
import math
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "textbook"))
sys.path.insert(0, str(ROOT / "guides" / "planekinetics"))
from svgkit import Fig  # noqa: E402
from pk_figs import true_size, ppu_for, right_mark  # noqa: E402

V = lambda x, y: np.array([float(x), float(y)])
T = lambda v: (float(v[0]), float(v[1]))
U = lambda d: V(math.cos(math.radians(d)), math.sin(math.radians(d)))
R, L = 0.5, 1.2
BETA = math.degrees(math.asin(0.25 / 1.2))
C0 = V(0, 0.5)                          # centre of the guide arc; the arc meets the track at (0, 0)
B = C0 + R * U(240)                     # 60 deg from the vertical, down-left of the centre
A = B + L * U(-BETA)


def mech(solution=False):
    f = Fig(ppu_for(0.1), "CT2 bar AB with B in a 0.5 m circular guide and A on the track, to scale 1:10")
    arc = [C0 + R * U(t) for t in range(180, 271, 3)]
    f.path_world([T(V(-R, 0.95))] + [T(p) for p in arc] + [T(V(A[0] + 0.35, 0))], "ink")
    f.line(T(C0 + V(-0.03, 0)), T(C0 + V(0.03, 0)), "muted"); f.line(T(C0 + V(0, -0.03)), T(C0 + V(0, 0.03)), "muted")
    f.line(T(C0), T(B), "muted", dash="4 4")
    f.line(T(C0), T(C0 + V(0, -0.42)), "muted", dash="4 4")
    f.arc(T(C0), 30, 240, 270, "muted", "60°", lr=44, la=255)
    f.text(T((C0 + B) / 2), "0.5 m", "muted", dx=-6, dy=-10, anchor="end")
    f.link(T(B), T(A), w=7)
    f.pin(T(B)); f.pin(T(A))
    f.text(T(B), "B", dx=-10, dy=-4, anchor="end"); f.text(T(A), "A", dx=4, dy=-14)
    f.text(T((A + B) / 2), "1.2 m", "muted", dx=6, dy=-12)
    f.arrow(T(A + V(0.06, 0.03)), T(A + V(0.3, 0.03)), "abs", "v_{A} = 3 m/s (constant)", at=("N", 10), lpos=0.6)
    if solution:
        f.dim(T(V(C0[0] + 0.12, C0[1])), T(V(C0[0] + 0.12, B[1])), "h₁ = 0.25", off=0, side="r")
        f.dim(T(V(A[0] + 0.08, B[1])), T(V(A[0] + 0.08, 0)), "h₂ = 0.25", off=0, side="r")
        f.line(T(B), T(V(A[0] + 0.15, B[1])), "muted", dash="3 3")
        f.arc(T(A), 60, 180 - BETA, 180, "ans", "β = 12°", lr=80, la=174)
        f.line(T(B), T(B + 0.32 * U(300)), "cons"); f.line(T(B), T(B + 0.32 * U(120)), "cons")
        f.line(T(B), T(B + 0.32 * U(258)), "cons"); f.line(T(B), T(B + 0.32 * U(78)), "cons")
        f.text(T(B + 0.33 * U(120)), "tangent to guide", "muted", dx=-4, anchor="end")
        f.text(T(B + 0.33 * U(78)), "⊥ AB", "muted", dy=-8)
    f.set_scalebar(0.1, "1 cm = 0.1 m")
    return true_size(f.svg())


def vel():
    f = Fig(ppu_for(1.0), "CT2 velocity diagram to scale 1 cm = 1 m/s")
    o = V(0, 0); a = V(3, 0); b = 4.383 * U(300)
    f.arrow(T(o), T(a), "abs", "v_{A} = 3", at=("N", 10), lpos=0.5)
    f.arrow(T(a), T(b), "t", "v_{B/A} = 3.88 @ 258°", at=("E", 8), lpos=0.5)
    f.arrow(T(o), T(b), "ans", "v_{B} = 4.38 @ 300°", at=("W", 8), lpos=0.5)
    f.arc(T(o), 26, 300, 360, "muted", "60°", lr=40, la=330)
    f.arc(T(a), 24, 180, 258, "muted", "78°", lr=38, la=220)
    f.arc(T(b), 26, 78, 120, "muted", "42°", lr=40, la=99)
    f.text(T(o), "o", dx=-8, anchor="end"); f.text(T(a), "a", dx=8, anchor="start"); f.text(T(b), "b", dy=14)
    f.set_scalebar(1, "1 cm = 1 m/s")
    return true_size(f.svg())


def acc():
    f = Fig(ppu_for(5), "CT2 acceleration diagram to scale 1 cm = 5 m/s^2")
    o = V(0, 0)
    p = 12.551 * U(360 - BETA)
    q = 38.421 * U(30)
    b = q + (-23.885) * U(300)
    f.line(T(p - 6 * U(90 - BETA)), T(b + 8 * U(90 - BETA)), "cons")
    f.line(T(q - 8 * U(120)), T(b + 8 * U(120)), "cons")
    f.arrow(T(o), T(p), "n", "(a_{B/A})_{n} 12.55", at=("S", 12), lpos=0.5)
    f.arrow(T(p), T(b), "t", "(a_{B/A})_{t} 43.5", at=("W", 8), lpos=0.2)
    f.arrow(T(o), T(q), "n", "(a_{B})_{n} 38.4", at=("SE", 6), lpos=0.7)
    f.arrow(T(q), T(b), "t", "(a_{B})_{t} 23.9", at=("E", 8), lpos=0.5)
    f.arrow(T(o), T(b), "ans", "a_{B} = 45.2", at=("W", 8), lpos=0.6, dashed=True)
    f.text(T(o), "o (= a, since a_A = 0)", dx=-8, dy=6, anchor="end"); f.text(T(b), "b", dx=-8, dy=-6, anchor="end")
    f.set_scalebar(5, "1 cm = 5 m/s²")
    return true_size(f.svg())


def ic():
    f = Fig(ppu_for(0.1), "CT2 velocity check: instantaneous centre of AB, to scale 1:10")
    arc = [C0 + R * U(t) for t in range(180, 271, 3)]
    f.path_world([T(V(-R, 0.95))] + [T(p) for p in arc] + [T(V(A[0] + 0.3, 0))], "ink")
    Ic = V(A[0], C0[1] + (A[0] - C0[0]) * math.tan(math.radians(30)))
    f.line(T(B), T(Ic + 0.08 * U(30)), "cons")
    f.line(T(A), T(Ic + V(0, 0.08)), "cons")
    f.link(T(B), T(A), w=7)
    f.dot(T(C0)); f.text(T(C0), "guide centre", "muted", dx=-8, dy=-10, anchor="end")
    f.dot(T(Ic), r=5, cls="dotans"); f.text(T(Ic), "IC of AB", "ans", dx=10, anchor="start")
    f.pin(T(B)); f.pin(T(A))
    f.text(T(B), "B", dx=-10, dy=-4, anchor="end"); f.text(T(A), "A", dx=10, dy=10, anchor="start")
    f.text(T((A + Ic) / 2), "0.928 m", "ans", dx=8, anchor="start")
    f.text(T((B + Ic) / 2), "1.355 m", "ans", dx=-4, dy=-12, anchor="end")
    f.arrow(T(A), T(A + V(0.3, 0)), "abs", "v_{A} = 3", at=("S", 12), lpos=0.6)
    f.arrow(T(B), T(B + 0.44 * U(300)), "ans", "v_{B} = 4.38", at=("W", 8), lpos=0.9)
    f.arc(T(Ic), 24, 200, 330, "ans", "ω (CCW)", arrow=True, ccw=True, lr=38, la=265)
    f.set_scalebar(0.1, "1 cm = 0.1 m")
    return true_size(f.svg())


def build_all():
    return {"ct2_q": mech(False), "ct2_geom": mech(True), "ct2_vel": vel(), "ct2_acc": acc(), "ct2_ic": ic()}
