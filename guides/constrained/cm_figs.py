"""Diagrams for the constrained-motion + coordinate-vectors pack.

Colours: given/known velocities = blue "abs"; results = red "ans"; velocity lines and datums = dashed "cons";
coordinates and dimensions = grey "muted"; cable 1 / cable 2 highlights = "t" (green) / "n" (orange).
"""
import math
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "textbook"))
sys.path.insert(0, str(ROOT / "guides" / "planekinetics"))
sys.path.insert(0, str(ROOT / "guides" / "polar"))
from svgkit import Fig  # noqa: E402
from pk_figs import true_size, ppu_for, right_mark  # noqa: E402

V = lambda x, y: np.array([float(x), float(y)])
T = lambda v: (float(v[0]), float(v[1]))


def U(deg):
    return V(math.cos(math.radians(deg)), math.sin(math.radians(deg)))


def ceiling(f, x1, x2, y):
    a, b = f.P((x1, y)), f.P((x2, y))
    f.hatch(a[0], a[1], b[0], b[1], side=-1)


def pulley(f, c, r, label=None, ldx=0):
    f.circle(T(c), r, "outline")
    f.pin(T(c), 3.4)
    if label:
        f.text(T(c), label, dx=ldx, dy=-r * f.ppu - 9)


def block(f, c, w, h, label):
    f.path_world([(c[0] - w / 2, c[1] - h / 2), (c[0] + w / 2, c[1] - h / 2), (c[0] + w / 2, c[1] + h / 2),
                  (c[0] - w / 2, c[1] + h / 2), (c[0] - w / 2, c[1] - h / 2)], "block")
    f.text(T(c), label)


def rope(f, p, q, cls="rope"):
    f.line(T(p), T(q), cls)


def vel_line(f, c, r, vl, vr, s, lab_l=None, lab_r=None, lab_c=None, ic=True):
    """Velocity-line overlay on a pulley at c: strand arrows at the rim, centre arrow, dashed line through the tips."""
    L, R = c + V(-r, 0), c + V(r, 0)
    f.line(T(L - V(0.15, 0)), T(R + V(0.15, 0)), "muted", dash="3 4")
    vc = (vl + vr) / 2
    for p, vv, lab, cls in ((L, vl, lab_l, "abs"), (R, vr, lab_r, "abs"), (c, vc, lab_c, "ans")):
        if abs(vv) < 1e-9:
            f.dot(T(p), r=4, cls="dotans" if cls == "ans" else "dotk")
            if lab:
                f.text(T(p), lab, cls if cls != "abs" else "muted", dx=0, dy=16)
        else:
            f.arrow(T(p), T(p + V(0, vv * s)), cls, lab, at=("W" if p is L else "E", 6), lpos=1.0)
    tl, tr = L + V(0, vl * s), R + V(0, vr * s)
    d = (tr - tl) / np.linalg.norm(tr - tl)
    f.line(T(tl - 0.25 * d), T(tr + 0.25 * d), "cons")
    if ic and vl * vr < 0:
        x0 = L[0] + (2 * r) * (-vl) / (vr - vl)
        f.dot((x0, c[1]), r=3.6, cls="dotans")
        f.text((x0, c[1]), "0", "ans", dx=-6, dy=14, anchor="end")


# ------------------------------------------------------------------ the three cases (the sketch)
def hack_cases():
    f = Fig(46, "Velocity line across a pulley: one side fixed, axle fixed, both sides moving")
    r, s = 0.9, 1.0
    cases = [(0.0, 1.8, 0.0, "v", "0", "v/2", "one side tied off"),
             (4.0, 1.8, -1.8, "v", "v", "0", "axle fixed"),
             (8.0, -0.9, 1.8, "v₁", "v₂", "(v₂ − v₁)/2", "both sides moving")]
    for x, vl, vr, ll, lr, lc, title in cases:
        c = V(x, 0)
        f.circle(T(c), r, "outline")
        vel_line(f, c, r, vl, vr, s, ll, lr, lc)
        f.text(T(c + V(0, -2.3)), title, "muted")
    return f.svg()


# ------------------------------------------------------------------ EA1 movable pulley
def ea1():
    f = Fig(62, "Movable pulley: one end tied to the ceiling, the other pulled up")
    top = 4.0
    ceiling(f, -1.6, 1.4, top)
    c, r = V(0, 1.6), 0.5
    rope(f, V(-r, top), c + V(-r, 0)); rope(f, c + V(r, 0), V(r, 3.3))
    f.arrow(T(V(r, 3.3)), T(V(r, 3.9)), "abs", "pulled up at v", at=("E", 6), lpos=0.7)
    pulley(f, c, r)
    rope(f, c, c + V(0, -0.7))
    block(f, c + V(0, -1.0), 0.7, 0.5, "load")
    f.line(T(V(-1.6, top)), T(V(1.4, top)), "cons")
    f.text(T(V(-1.6, top)), "datum", "muted", dx=-4, anchor="end")
    f.dim(T(V(-1.25, top)), T(V(-1.25, c[1])), "s_{P}", off=0, side="l")
    f.dim(T(V(1.15, top)), T(V(1.15, 3.3)), "s_{E}", off=0, side="r")
    return f.svg()


def ea1_line():
    f = Fig(80, "EA1 velocity line")
    c, r = V(0, 0), 0.5
    f.circle(T(c), r, "outline")
    vel_line(f, c, r, 0.0, 1.4, 1.0, None, "v", "v/2")
    f.text(T(c + V(-r, 0)), "tied: 0", "muted", dx=-8, dy=14, anchor="end")
    return f.svg()


# ------------------------------------------------------------------ EA2 two ropes
def ea2():
    f = Fig(56, "Two ropes: end A pulled down, pulley C, block B")
    top = 5.2
    ceiling(f, -1.2, 2.5, top)
    F, rF = V(0, 4.5), 0.4
    C, rC = V(0.9, 2.9), 0.5
    B, rB = V(1.4, 1.2), 0.5
    f.line(T(V(0, top)), T(F), "ink")
    rope(f, F + V(-rF, 0), V(-rF, 0.9), "t"); rope(f, F + V(rF, 0), C + V(-rC, 0), "t"); rope(f, C + V(rC, 0), V(C[0] + rC, top), "t")
    rope(f, C, B + V(-rB, 0), "n"); rope(f, B + V(rB, 0), V(B[0] + rB, top), "n")
    pulley(f, F, rF, "F (fixed)", ldx=-40); pulley(f, C, rC, "C", ldx=-18); pulley(f, B, rB)
    rope(f, B, B + V(0, -0.6)); block(f, B + V(0, -0.85), 0.7, 0.5, "B")
    f.arrow(T(V(-rF, 0.9)), T(V(-rF, 0.3)), "abs", "A: 2 m/s ↓", at=("W", 6), lpos=0.6)
    f.line(T(V(-1.2, top)), T(V(2.5, top)), "cons")
    f.dim(T(V(-0.95, top)), T(V(-0.95, 0.9)), "s_{A}", off=0, side="l")
    f.dim(T(V(2.25, top)), T(V(2.25, C[1])), "s_{C}", off=0, side="r")
    f.dim(T(V(2.6, top)), T(V(2.6, B[1])), "s_{B}", off=0, side="r")
    return f.svg()


# ------------------------------------------------------------------ EA3 both strands moving
def ea3():
    f = Fig(56, "Pulley P with both strands moving: A down 4 m/s, C down 2 m/s")
    top = 5.2
    ceiling(f, -1.2, 2.3, top)
    F, rF = V(0, 4.5), 0.4
    P, rP = V(0.9, 1.7), 0.5
    Cc = V(P[0] + rP, 3.7)
    f.line(T(V(0, top)), T(F), "ink")
    rope(f, F + V(-rF, 0), V(-rF, 1.3)); rope(f, F + V(rF, 0), P + V(-rP, 0)); rope(f, P + V(rP, 0), Cc + V(0, -0.25))
    pulley(f, F, rF, "fixed", ldx=-34); pulley(f, P, rP, "P", ldx=-18)
    block(f, V(-rF, 1.05), 0.55, 0.5, "A")
    block(f, Cc, 0.5, 0.5, "C")
    f.line(T(Cc + V(0.45, -0.8)), T(Cc + V(0.45, 1.2)), "guide")
    rope(f, P, P + V(0, -0.6)); block(f, P + V(0, -0.85), 0.6, 0.5, "W")
    f.arrow(T(V(-rF - 0.45, 1.05)), T(V(-rF - 0.45, 0.4)), "abs", "4 m/s", at=("W", 6), lpos=0.6)
    f.arrow(T(Cc + V(0.75, 0.3)), T(Cc + V(0.75, -0.35)), "abs", "2 m/s", at=("E", 6), lpos=0.6)
    f.line(T(V(-1.2, top)), T(V(2.3, top)), "cons")
    f.dim(T(V(-1.2, top)), T(V(-1.2, 1.05)), "s_{A}", off=0, side="l")
    f.dim(T(V(0.25, top)), T(V(0.25, P[1])), "s_{P}", off=0, side="l")
    f.dim(T(V(2.2, top)), T(V(2.2, Cc[1])), "s_{C}", off=0, side="r")
    return f.svg()


def ea3_line():
    f = Fig(58, "EA3 velocity line on pulley P")
    c, r = V(0, 0), 0.7
    f.circle(T(c), r, "outline")
    vel_line(f, c, r, 2.0, -1.0, 1.0, "4 ↑", "2 ↓", "1 ↑")
    return f.svg()


# ------------------------------------------------------------------ EA4 CT1 Q1 (and F25 Q2)
def ea4():
    f = Fig(58, "CT1 Q1 schematic: motor, fixed pulleys, pulley B and the load pulley")
    top = 5.6
    ceiling(f, -1.0, 2.4, top)
    P1, r1 = V(0, 5.0), 0.45
    P2, r2 = V(1.2, 4.4), 0.25
    B, rB = V(0.95, 2.9), 0.5
    D, rD = V(1.45, 1.3), 0.5
    f.line(T(V(0, top)), T(P1), "ink"); f.line(T(V(1.2, top)), T(P2), "ink")
    rope(f, P1 + V(-r1, 0), V(-r1, 0.45), "t"); rope(f, P1 + V(r1, 0), B + V(-rB, 0), "t")
    rope(f, B + V(rB, 0), P2 + V(r2, 0), "t"); rope(f, P2 + V(-r2, 0), B + V(0, 0.15), "t")
    rope(f, B + V(0, -0.15), D + V(-rD, 0), "n"); rope(f, D + V(rD, 0), V(D[0] + rD, top), "n")
    pulley(f, P1, r1); pulley(f, P2, r2); pulley(f, B, rB, "B", ldx=-24); pulley(f, D, rD)
    rope(f, D, D + V(0, -0.6)); block(f, D + V(0, -0.85), 0.5, 0.5, "L")
    block(f, V(-r1 - 0.1, 0.25), 0.8, 0.4, "M")
    f.arrow(T(V(-r1 - 0.35, 1.6)), T(V(-r1 - 0.35, 1.0)), "abs", "100 mm/s ↓", at=("W", 6), lpos=0.5)
    f.line(T(V(-1.0, top)), T(V(2.4, top)), "cons")
    f.dim(T(V(2.25, top)), T(V(2.25, B[1])), "y_{B}", off=0, side="r")
    f.dim(T(V(2.6, top)), T(V(2.6, D[1])), "y_{L}", off=0, side="r")
    f.text(T(V(-0.95, 3.5)), "cable 1", "t", anchor="end")
    f.text(T(V(2.05, 0.9)), "cable 2", "n", anchor="start")
    return f.svg()


def ea4_lines():
    f = Fig(58, "CT1 Q1 velocity lines on pulley B and on the load pulley")
    rB = 0.8
    B = V(0, 0)
    f.circle(T(B), rB, "outline")
    vel_line(f, B, rB, 1.8, -0.6, 1.0, "100 ↑", "33.3 ↓", "33.3 ↑")
    f.text(T(B + V(0, -1.6)), "pulley B", "muted")
    D = V(4.4, 0)
    f.circle(T(D), rB, "outline")
    vel_line(f, D, rB, 0.6, 0.0, 1.0, "33.3 ↑", "0", "16.7 ↑")
    f.text(T(D + V(0, -1.6)), "load pulley", "muted")
    return f.svg()


# ------------------------------------------------------------------ EA5 S25 Q2 slanted rope (TRUE SCALE)
def ea5():
    f = Fig(ppu_for(0.5), "S25 Q2 geometry at s = 2 m, to scale 1 cm = 0.5 m")
    Pu, B, A = V(0, 5), V(3, 5), V(3, 1)
    crate = V(0, 2)
    f.line(T(V(-1, 0)), T(V(3.6, 0)), "ink")
    f.line(T(V(3.25, 0)), T(V(3.25, 5.6)), "ink")
    f.circle(T(Pu), 0.15, "outline")
    rope(f, crate + V(0, 0.25), Pu + V(0, -0.15))
    rope(f, Pu, A)
    block(f, crate, 0.6, 0.5, "C")
    f.dot(T(A), r=5, cls="dotk"); f.text(T(A), "A", dx=12, anchor="start")
    f.dot(T(B), r=3); f.text(T(B), "B", dx=12, dy=-6, anchor="start")
    f.line(T(Pu), T(B), "cons")
    f.text(T((Pu + B) / 2), "3 m", "muted", dy=-10)
    f.dim(T(B), T(A), "x_{A} = 4 m", off=30, side="l")
    f.text(T((Pu + A) / 2), "√(x_A² + 9) = 5 m", "muted", dx=-14, dy=10, anchor="end")
    f.dim(T(V(0, 5)), T(V(0, 2.25)), "x_{C} = 3 m", off=40, side="l")
    f.dim(T(V(0, 0)), T(V(0, 1.75)), "s = 2 m", off=40, side="l")
    f.arrow(T(A + V(0.0, -0.1)), T(A + V(0, -0.9)), "abs", "v_{A} = 2.5 m/s", at=("W", 8), lpos=0.6)
    f.arrow(T(crate + V(0.55, 0)), T(crate + V(0.55, 0.8)), "ans", "v_{C} = 2 m/s", at=("E", 6), lpos=0.6)
    f.set_scalebar(0.5, "1 cm = 0.5 m")
    return true_size(f.svg())


# ------------------------------------------------------------------ B: unit-vector pictures
def b_polar():
    f = Fig(90, "S25 Q1a: v projected onto e_r and e_theta")
    O, P = V(0, 0), 2.2 * U(45)
    f.line(T(O), T(P), "ink")
    f.line(T(O), T(V(0.9, 0)), "muted", dash="4 4")
    f.arc(T(O), 36, 0, 45, "muted", "θ = 45°", lr=56)
    er, eth = U(45), U(135)
    f.arrow(T(P), T(P + 0.75 * er), "muted", "e_{r}", at=("E", 4), lpos=1.0)
    f.arrow(T(P), T(P + 0.75 * eth), "muted", "e_{θ}", at=("N", 8), lpos=1.0)
    v = 1.6 * U(-15)
    f.line(T(P), T(P + V(0.9, 0)), "muted", dash="3 3")
    f.arrow(T(P), T(P + v), "abs", "v = 75 m/s", at=("E", 6), lpos=1.0)
    f.arc(T(P), 46, 345, 360, "muted", "15°", lr=60, la=352)
    vr = (v @ er) * er
    f.line(T(P + v), T(P + vr), "cons")
    f.arrow(T(P), T(P + vr), "t", "v_{r} = 37.5", at=("NW", 4), lpos=0.6)
    vth = (v @ eth) * eth
    f.line(T(P + v), T(P + vth), "cons")
    f.arrow(T(P), T(P + vth), "n", "v_{θ} = −64.95", at=("W", 8), lpos=0.8)
    f.dot(T(O)); f.text(T(O), "radar", "muted", dy=14)
    return f.svg()


def b_nt():
    f = Fig(ppu_for(2), "S25 Q1b: a = a_t e_t + a_n e_n drawn head to tail, to scale 1 cm = 2 m/s^2")
    et = U(-15); en = V(et[1], -et[0])
    o = V(0, 0)
    at = -7.644 * et; an = 9.375 * en
    f.line(T(o - 3 * et), T(o + 4.5 * et), "cons")
    f.text(T(o + 4.5 * et), "tangent (direction of travel →)", "muted", dx=4, dy=10, anchor="start")
    f.arrow(T(o), T(o + at), "t", "a_{t} e_{t} = 7.64 (backwards: slowing)", at=("N", 10), lpos=0.5)
    f.arrow(T(o + at), T(o + at + an), "n", "a_{n} e_{n} = 9.375", at=("W", 8), lpos=0.5)
    a = at + an
    f.arrow(T(o), T(o + a), "ans", "a = (−9.81, −7.08)", at=("E", 8), lpos=0.6, dashed=True)
    f.line(T(o + a), T(V(a[0], 0)), "muted", dash="3 3"); f.line(T(o), T(V(a[0], 0)), "muted", dash="3 3")
    f.text(T(V(a[0] / 2, 0)), "a_x = −9.81", "muted", dy=-10)
    f.text(T(V(a[0], a[1] / 2)), "a_y = −7.08", "muted", dx=-6, anchor="end")
    f.set_scalebar(2, "1 cm = 2 m/s²")
    return true_size(f.svg())


def b_cars_geom():
    f = Fig(0.55, "CT1 Q2 track geometry: A on the 375 m lane at 25 degrees, B on the 360 m lane at 0 degrees")
    O = V(0, 0); A = 375 * U(25); B = 360 * U(0)
    for rr in (360, 375):
        pts = [rr * U(t) for t in range(-12, 52, 2)]
        f.path_world([T(p) for p in pts], "muted")
    f.line(T(O), T(A), "ink"); f.line(T(O), T(B), "ink")
    f.arc(T(O), 60, 0, 25, "muted", "25°", lr=76)
    f.dot(T(O)); f.text(T(O), "O", dx=-8, anchor="end")
    f.dot(T(A)); f.text(T(A), "A (r = 375 m)", dx=10, dy=12, anchor="start")
    f.dot(T(B)); f.text(T(B), "B (r = 360 m)", dx=10, dy=14, anchor="start")
    f.arrow(T(A), T(A + 70 * U(115)), "abs", "v_{A} ⊥ OA", at=("W", 6), lpos=1.0)
    f.arrow(T(B), T(B + 70 * U(90)), "abs", "v_{B} ↑", at=("E", 6), lpos=1.0)
    return f.svg()


def b_cars_v():
    f = Fig(ppu_for(5), "CT1 Q2 velocity diagram to scale 1 cm = 5 m/s")
    o = V(0, 0); vA = 26.667 * U(115); vB = V(0, 26.667)
    f.arrow(T(o), T(vB), "abs", "v_{B} = 26.67", at=("E", 6), lpos=0.5)
    f.arrow(T(o), T(vA), "abs", "v_{A} = 26.67", at=("W", 6), lpos=0.5)
    f.arrow(T(vB), T(vA), "ans", "v_{A/B} = 11.54 m/s", at=("N", 10), lpos=0.5)
    f.arc(T(o), 30, 90, 115, "muted", "25°", lr=44)
    f.text(T(o), "o", dx=6, dy=10, anchor="start")
    f.set_scalebar(5, "1 cm = 5 m/s")
    return true_size(f.svg())


def b_cars_a():
    f = Fig(ppu_for(0.25), "CT1 Q2 acceleration diagram to scale 1 cm = 0.25 m/s^2")
    o = V(0, 0)
    aBn = V(-1.9753, 0); aB = V(-1.9753, 0.762); aA = 1.8963 * U(205)
    f.arrow(T(o), T(aBn), "n", "(a_{B})_{n} = 1.975 (→ O)", at=("N", 10), lpos=0.45)
    f.arrow(T(aBn), T(aB), "t", "(a_{B})_{t} = 0.762", at=("W", 6), lpos=0.6)
    f.arrow(T(o), T(aA), "n", "a_{A} = 1.896 (→ O, 25° below)", at=("S", 12), lpos=0.55)
    f.arrow(T(aB), T(aA), "ans", "a_{A/B} = 1.584", at=("E", 8), lpos=0.45)
    f.line(T(aB), T(aB + V(0.6, 0)), "muted", dash="3 3")
    f.arc(T(aB), 26, 279.3, 360, "muted", "80.7°", lr=44, la=330)
    f.text(T(o), "o", dx=6, dy=-8, anchor="start")
    f.set_scalebar(0.25, "1 cm = 0.25 m/s²")
    return true_size(f.svg())


def b_helix():
    f = Fig(14, "CT1 Q3: one half-turn of the helix unrolled into a right triangle")
    L, H = 7.2 * math.pi, 3.0
    f.path_world([(0, 0), (L, 0), (L, H), (0, 0)], "ink")
    f.arc((0, 0), 70, 0, 7.555, "ans", "γ = 7.56°", lr=96, la=4)
    f.text((L / 2, 0), "half a turn of arc: rπ = 7.2π = 22.62 m", "muted", dy=14)
    f.text((L, H / 2), "rise 3 m", "muted", dx=8, anchor="start")
    p = V(L * 0.32, H * 0.32)
    d = U(7.555)
    f.arrow(T(p), T(p + 7 * d), "abs", "v", at=("N", 8), lpos=1.0)
    f.arrow(T(p), T(p + V(7 * math.cos(math.radians(7.555)), 0)), "t", "v_{θ} = v cos γ", at=("S", 12), lpos=0.6)
    return f.svg()


def b_helix_top():
    f = Fig(14, "CT1 Q3 top view: the car on a circle of radius 7.2 m")
    O = V(0, 0); th = 50; P = 7.2 * U(th)
    f.circle(T(O), 7.2, "outline thin", dash="5 4")
    f.line(T(O), T(P), "ink"); f.dot(T(O)); f.text(T(O), "axis", "muted", dy=14)
    f.dot(T(P)); f.text(T(P), "car", dx=8, dy=-8, anchor="start")
    f.arrow(T(P), T(P + 3 * U(th)), "muted", "e_{r}", at=("E", 4), lpos=1.0)
    f.arrow(T(P), T(P + 3 * U(th + 90)), "muted", "e_{θ}", at=("W", 6), lpos=1.0)
    f.arrow(T(P), T(P - 4.5 * U(th)), "ans", "a_{r} = −rθ̇² = −6.58", at=("E", 8), lpos=0.55)
    f.arrow(T(P), T(P - 1.6 * U(th + 90)), "n", "a_{θ} = −0.826", at=("SE", 6), lpos=1.0)
    return f.svg()


def build_all():
    import polar_figs
    out = {n: globals()[n]() for n in ("hack_cases", "ea1", "ea1_line", "ea2", "ea3", "ea3_line", "ea4", "ea4_lines", "ea5",
                                       "b_polar", "b_nt", "b_cars_geom", "b_cars_v", "b_cars_a", "b_helix", "b_helix_top")}
    out["sph_geom"] = polar_figs.build_all()["sph_geom"]
    return out


if __name__ == "__main__":
    for k, v in build_all().items():
        print(k, len(v))
