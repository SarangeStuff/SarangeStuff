"""Pictures for the 'oblique impact, slowly' explainer.

Colours: n-direction things = orange "n"; t-direction things = green "t"; given velocities = blue "abs";
results = red "ans"; axes, angles and helpers = grey "muted"/"cons".
"""
import math
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "textbook"))
sys.path.insert(0, str(ROOT / "guides" / "planekinetics"))
from svgkit import Fig  # noqa: E402
from pk_figs import right_mark  # noqa: E402

V = lambda x, y: np.array([float(x), float(y)])
T = lambda v: (float(v[0]), float(v[1]))
U = lambda d: V(math.cos(math.radians(d)), math.sin(math.radians(d)))


def axes_nt(f, P, nd, Ln=1.0, Lt=0.8, back=0.5):
    """Draw tilted n and t axes through P, with n at nd degrees and t at nd - 90."""
    n, t = U(nd), U(nd - 90)
    f.line(T(P - back * n), T(P + Ln * n), "cons"); f.line(T(P - back * t), T(P + Lt * t), "cons")
    f.arrow(T(P + (Ln - 0.25) * n), T(P + Ln * n), "n", "n", at=("N", 8), lpos=1.0)
    f.arrow(T(P + (Lt - 0.25) * t), T(P + Lt * t), "t", "t", at=("E", 6), lpos=1.0)


# ------------------------------------------------------------------ 1. what n and t are
def idea():
    f = Fig(70, "Two smooth balls touching: the push is only along the line of centres (n); nothing pushes along t")
    nd = 25
    A, B = V(0, 0), 1.8 * U(nd)
    Cc = A + 0.9 * U(nd)
    f.circle(T(A), 0.9, "outline"); f.circle(T(B), 0.9, "outline")
    f.dot(T(A)); f.dot(T(B)); f.text(T(A), "A", dx=-12, anchor="end"); f.text(T(B), "B", dx=12, anchor="start")
    f.line(T(A - 0.5 * U(nd)), T(B + 1.4 * U(nd)), "n")
    f.text(T(B + 1.45 * U(nd)), "n: line through both centres", "n", dx=6, anchor="start")
    tt = U(nd + 90)
    f.line(T(Cc - 1.6 * tt), T(Cc + 1.6 * tt), "t")
    f.text(T(Cc + 1.65 * tt), "t: along the touching surfaces", "t", dy=-10)
    f.arrow(T(Cc + 0.05 * U(nd)), T(Cc + 0.75 * U(nd)), "ans", "push on B", at=("SE", 4), lpos=1.0)
    f.arrow(T(Cc - 0.05 * U(nd)), T(Cc - 0.75 * U(nd)), "ans", "push on A", at=("NW", 4), lpos=1.0)
    right_mark(f, Cc, U(nd), tt)
    return f.svg()


# ------------------------------------------------------------------ 2. splitting an arrow
def resolve():
    f = Fig(110, "Splitting a velocity into its n part and t part: drop perpendiculars onto each axis")
    P = V(0, 0); nd = 20
    axes_nt(f, P, nd, Ln=2.3, Lt=1.5, back=0.3)
    phi = 50
    v = 2.0 * U(nd + phi)
    f.arrow(T(P), T(P + v), "abs", "v", at=("N", 10), lpos=1.0)
    n, t = U(nd), U(nd - 90)
    vn, vt = (v @ n) * n, (v @ t) * t
    f.line(T(P + v), T(P + vn), "muted", dash="3 3")
    f.arrow(T(P), T(P + vn), "n", "v_{n} = v cos φ", at=("S", 14), lpos=0.6)
    f.arrow(T(P), T(P + vt), "t", "v_{t} = v sin φ (negative here)", at=("W", 8), lpos=1.0)
    f.line(T(P + v), T(P + v - vn), "muted", dash="3 3")
    f.arc(T(P), 40, nd, nd + phi, "muted", "φ", lr=54)
    return f.svg()


# ------------------------------------------------------------------ 3. warm-up: ball on a wall
def wall():
    f = Fig(42, "Warm-up: a ball bouncing off a smooth wall keeps its t-speed; its n-speed reverses and shrinks by e")
    f.line((0, -4.8), (0, 4.8), "ink")
    x1, y1 = f.P((0, -4.8)); x2, y2 = f.P((0, 4.8))
    f.hatch(x1, y1, x2, y2, side=-1)
    P = V(0, 0)
    f.line(T(P), T(P + V(5.5, 0)), "cons"); f.text(T(P + V(5.5, 0)), "n (⊥ wall)", "n", dx=6, anchor="start")
    f.line(T(P + V(0, -0.2)), T(P + V(0, 0.2)), "cons")
    s = 0.46
    f.arrow(T(P + s * V(5, -8.66)), T(P), "abs", "before: 10 m/s", at=("E", 8), lpos=0.35)
    f.arrow(T(P), T(P + s * V(3, 8.66)), "ans", "after: 9.17 m/s", at=("E", 8), lpos=0.75)
    f.arc(T(P), 46, 270, 300, "muted", "30°", lr=62, la=286)
    f.arc(T(P), 46, 70.9, 90, "muted", "19.1°", lr=64, la=80)
    f.text((0, -4.8), "wall: t runs along it", "t", dy=16)
    return f.svg()


# ------------------------------------------------------------------ S25 Q6
TH = math.degrees(math.atan(5 / 12))            # 22.62 deg, n measured from the vertical
ND = 90 - TH                                   # n direction from +x: 67.38 deg


def s25_axes():
    f = Fig(62, "S25 Q6: tilted n and t axes through the contact point O")
    O = V(0, 0)
    A, B = O + 1.0 * U(ND), O - 1.0 * U(ND)
    f.circle(T(A), 1.0, "outline"); f.circle(T(B), 1.0, "outline")
    f.text(T(A), "A (8 kg)", dx=0, dy=-2); f.text(T(B), "B (6 kg)", dx=0, dy=-2)
    f.line(T(V(-3.2, 0)), T(V(3.4, 0)), "muted"); f.text((3.4, 0), "x", "muted", dx=6, anchor="start")
    f.line(T(V(0, -3.0)), T(V(0, 3.3)), "muted"); f.text((0, 3.3), "y", "muted", dy=-8)
    axes_nt(f, O, ND, Ln=3.2, Lt=2.8, back=2.6)
    f.arc(T(O), 70, ND, 90, "ans", "θ = 22.6°", lr=96, la=80)
    f.arrow(T(A + V(2.2, 0)), T(A + V(0.9, 0)), "abs", "v_{A} = 5 m/s", at=("N", 10), lpos=0.3)
    f.arrow(T(B + V(-2.3, 0)), T(B + V(-1.0, 0)), "abs", "v_{B} = 7 m/s", at=("S", 12), lpos=0.4)
    q = V(-2.6, 2.0)
    f.path_world([T(q), T(q + V(5 / 5 * 0.55, 0)), T(q + V(0.55, 12 / 5 * 0.55)), T(q)], "muted")
    f.text(T(q + V(0.28, 0)), "5", "muted", dy=12); f.text(T(q + V(0.55, 0.66)), "12", "muted", dx=8, anchor="start")
    f.text(T(q + V(0.2, 0.8)), "13", "muted", dx=-8, anchor="end")
    f.text(T(q + V(0.3, -0.7)), "slope of n: tan θ = 5/12", "muted")
    f.dot(T(O), r=3); f.text(T(O), "O", dx=-8, dy=10, anchor="end")
    return f.svg()


def s25_split():
    f = Fig(42, "S25 Q6: each horizontal velocity split into n and t parts")
    n, t = U(ND), U(ND - 90)
    for k, (v, name, x0) in enumerate(((-5.0, "A", 0.0), (7.0, "B", 13.0))):
        P = V(x0, 0)
        f.line(T(P - 3 * n), T(P + 4 * n), "cons"); f.line(T(P - 3.5 * t), T(P + 6.5 * t), "cons")
        f.text(T(P + 4 * n), "+n", "n", dy=-8); f.text(T(P + 6.5 * t), "+t", "t", dx=6, anchor="start")
        vv = V(v, 0)
        f.arrow(T(P), T(P + vv), "abs", f"v_{{{name}}} = {abs(v):g}", at=("N", 10), lpos=1.0)
        vn, vt = (vv @ n) * n, (vv @ t) * t
        f.line(T(P + vv), T(P + vn), "muted", dash="3 3"); f.line(T(P + vv), T(P + vt), "muted", dash="3 3")
        f.arrow(T(P), T(P + vn), "n", f"n: {vv @ n:+.3f}", at=("W" if v > 0 else "E", 6), lpos=1.0)
        f.arrow(T(P), T(P + vt), "t", f"t: {vv @ t:+.3f}", at=("S", 12), lpos=1.0)
    return f.svg()


def s25_after():
    f = Fig(42, "S25 Q6: velocities just after impact rebuilt from their n and t parts")
    n, t = U(ND), U(ND - 90)
    for name, an, at_, x0 in (("A", 1.044, -4.615, 0.0), ("B", -1.264, 6.462, 12.0)):
        P = V(x0, 0)
        f.line(T(P - 3 * n), T(P + 3 * n), "cons"); f.line(T(P - 5 * t), T(P + 6.6 * t), "cons")
        vn, vt = an * n, at_ * t
        f.arrow(T(P), T(P + vn), "n", f"n: {an:+.3f}", at=("W", 6), lpos=1.0)
        f.arrow(T(P), T(P + vt), "t", f"t: {at_:+.3f}", at=("S", 12) if at_ > 0 else ("N", 10), lpos=1.0)
        v = vn + vt
        f.line(T(P + vn), T(P + v), "muted", dash="3 3"); f.line(T(P + vt), T(P + v), "muted", dash="3 3")
        sp = math.hypot(an, at_)
        f.arrow(T(P), T(P + v), "ans", f"v′_{{{name}}} = {sp:.2f} m/s", at=("N", 10) if name == "A" else ("E", 6), lpos=1.0)
    return f.svg()


# ------------------------------------------------------------------ F25 Q8
def f25_axes():
    f = Fig(70, "F25 Q8: bat A in a horizontal slot, ball B, line of impact at 20 degrees")
    A = V(0, 0); B = 1.95 * U(20); O = A + 1.0 * U(20)
    f.line(T(V(-2.4, 1.15)), T(V(0.7, 1.15)), "ink"); f.line(T(V(-2.4, -1.15)), T(V(0.7, -1.15)), "ink")
    f.text((-2.4, 1.15), "slot", "muted", dx=-6, anchor="end")
    f.circle(T(A), 1.0, "outline"); f.circle(T(B), 0.95, "outline")
    f.text(T(A), "A (bat, 0.5 kg)", dy=26); f.text(T(B), "B (ball, 0.146 kg)", dy=-26)
    axes_nt(f, O, 20, Ln=3.0, Lt=2.4, back=1.7)
    f.line(T(O), T(O + V(2.4, 0)), "muted", dash="3 3")
    f.arc(T(O), 60, 0, 20, "ans", "20°", lr=78, la=8)
    f.arrow(T(A + V(-2.2, -0.1)), T(A + V(-1.1, -0.1)), "abs", "v_{A} = 18 m/s", at=("S", 12), lpos=0.4)
    f.arrow(T(B + V(2.4, -0.1)), T(B + V(1.05, -0.1)), "abs", "v_{B} = 38 m/s", at=("S", 12), lpos=0.4)
    f.dot(T(O), r=3)
    return f.svg()


def f25_after():
    f = Fig(6.2, "F25 Q8: the ball after impact rebuilt from n = 27.05 and t = 13.00")
    n, t = U(20), U(110)
    P = V(0, 0)
    f.line(T(P - 6 * n), T(P + 34 * n), "cons"); f.line(T(P - 4 * t), T(P + 18 * t), "cons")
    f.text(T(P + 34 * n), "+n", "n", dx=6, anchor="start"); f.text(T(P + 18 * t), "+t", "t", dy=-8)
    vn, vt = 27.045 * n, 12.997 * t
    v = vn + vt
    f.arrow(T(P), T(P + vn), "n", "n: 27.05", at=("S", 12), lpos=0.6)
    f.arrow(T(P), T(P + vt), "t", "t: 13.00 (unchanged)", at=("W", 6), lpos=0.8)
    f.line(T(P + vn), T(P + v), "muted", dash="3 3"); f.line(T(P + vt), T(P + v), "muted", dash="3 3")
    f.arrow(T(P), T(P + v), "ans", "v′_{B} = 30.0 m/s", at=("W", 8), lpos=0.9)
    f.line(T(P), T(P + V(24, 0)), "muted", dash="3 3")
    f.arc(T(P), 46, 0, 45.66, "ans", "β = 45.7°", lr=62, la=30)
    return f.svg()


def build_all():
    names = ("idea", "resolve", "wall", "s25_axes", "s25_split", "s25_after", "f25_axes", "f25_after")
    return {n_: globals()[n_]() for n_ in names}


if __name__ == "__main__":
    for k_, v_ in build_all().items():
        print(k_, len(v_))
