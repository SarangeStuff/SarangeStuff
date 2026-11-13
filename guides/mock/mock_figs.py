"""Figures for the mock exam (clean question drawings) and its memo (constructions, true scale where it matters)."""
import math
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
for sub in ("textbook", "guides/planekinetics"):
    sys.path.insert(0, str(ROOT / sub))
from svgkit import Fig  # noqa: E402
from pk_figs import true_size, ppu_for, right_mark, curl  # noqa: E402

V = lambda x, y: np.array([float(x), float(y)])
T = lambda v: (float(v[0]), float(v[1]))
U = lambda d: V(math.cos(math.radians(d)), math.sin(math.radians(d)))


def ceiling(f, x1, x2, y):
    a, b = f.P((x1, y)), f.P((x2, y))
    f.hatch(a[0], a[1], b[0], b[1], side=-1)


def box(f, c, w, h, cls="block", label=None):
    f.path_world([(c[0] - w / 2, c[1] - h / 2), (c[0] + w / 2, c[1] - h / 2), (c[0] + w / 2, c[1] + h / 2),
                  (c[0] - w / 2, c[1] + h / 2), (c[0] - w / 2, c[1] - h / 2)], cls)
    if label:
        f.text(T(c), label)


# ================================================================ geometry used by several figures
Q3A = 0.2 * U(30); Q3B = V(0.45, 0.1 + math.sqrt(0.25 - (0.45 - 0.2 * math.cos(math.radians(30))) ** 2))
Q4A = 0.15 * U(60); Q4C = V(0.45, 0); Q4B = V(0.4052, 0.2460)


# ================================================================ EXAM FIGURES
def e1():
    f = Fig(0.42, "Q1 radar at O tracking a drone")
    O = V(0, 0); P = 600 * U(40)
    pts = [P + V(t, -t * t / (2 * 500)) for t in range(-260, 261, 20)]
    f.path_world([T(p) for p in pts], "muted", dash="6 5")
    f.line(T(O), T(P), "ink"); f.line(T(O), T(V(200, 0)), "muted", dash="4 4")
    f.line(T(V(-60, 0)), T(V(560, 0)), "ink")
    f.arc(T(O), 40, 0, 40, "muted", "θ = 40°", lr=58)
    f.dot(T(O)); f.text(T(O), "radar O", dx=-6, dy=14, anchor="end")
    f.dot(T(P)); f.text(T(P), "drone", dx=-8, dy=-12, anchor="end")
    f.text(T(P * 0.5), "r = 600 m", "muted", dx=-10, anchor="end")
    f.arrow(T(P), T(P + V(110, 0)), "abs", "v = 30 m/s", at=("N", 10), lpos=0.8)
    f.text(T(P + V(150, -60)), "path (ρ = 500 m)", "muted", anchor="start")
    return f.svg()


def e2():
    f = Fig(85, "Q2 collar A on a horizontal bar, rope over pulley P to block B")
    P = V(0, 0)
    ceiling(f, -0.6, 0.6, 0.35); f.line((0, 0.35), (0, 0.12), "ink")
    f.circle(T(P), 0.12, "outline"); f.pin(T(P), 3)
    f.line(T(V(-0.6, -2)), T(V(3.0, -2)), "guide")
    A = V(1.5, -2)
    box(f, A, 0.3, 0.2, "block", "A")
    f.line(T(P + V(0.07, -0.1)), T(A + V(-0.05, 0.1)), "rope")
    f.line(T(P + V(-0.12, 0)), T(V(-0.12, -1.3)), "rope")
    box(f, V(-0.12, -1.5), 0.4, 0.4, "block", "B")
    f.dim(T(V(0.0, -2)), T(V(1.5, -2)), "x", off=26, side="r")
    f.dim(T(V(2.4, 0)), T(V(2.4, -2)), "h = 2 m", off=0, side="l")
    f.line(T(P), T(V(2.6, 0)), "muted", dash="3 4")
    f.arrow(T(A + V(0.2, 0.18)), T(A + V(0.75, 0.18)), "abs", "v_{A} = 1.5 m/s (constant)", at=("N", 10), lpos=0.5)
    return f.svg()


def e3():
    f = Fig(520, "Q3 crank OA, rod AB, slider B in a vertical guide")
    O, A, B = V(0, 0), Q3A, Q3B
    f.link(T(O), T(A), w=8); f.link(T(A), T(B), w=7)
    f.line(T(V(0.43, 0.25)), T(V(0.43, 0.7)), "guide"); f.line(T(V(0.47, 0.25)), T(V(0.47, 0.7)), "guide")
    box(f, B, 0.035, 0.06, "block")
    f.pivot(T(O)); f.pin(T(A)); f.pin(T(B))
    f.text(T(O), "O", dx=-10, dy=-4, anchor="end"); f.text(T(A), "A", dx=-6, dy=-12, anchor="end"); f.text(T(B), "B", dx=-10, anchor="end")
    f.line(T(O), T(V(0.2, 0)), "muted", dash="4 4"); f.arc(T(O), 40, 0, 30, "muted", "30°", lr=56)
    f.arc(T(O), 22, 300, 40, "abs", "6 rad/s", arrow=True, ccw=True, lr=36, la=-10)
    f.dim(T(V(0, -0.06)), T(V(0.45, -0.06)), "450 mm", off=0, side="r")
    f.text(T(A * 0.5), "200 mm", "muted", dx=8, dy=10, anchor="start")
    f.text(T((A + B) / 2), "500 mm", "muted", dx=-8, anchor="end")
    return f.svg()


def e4():
    f = Fig(700, "Q4 four-bar OABC")
    O, A, B, C = V(0, 0), Q4A, Q4B, Q4C
    f.link(T(O), T(A), w=8); f.link(T(A), T(B), w=7); f.link(T(C), T(B), w=8)
    f.pivot(T(O)); f.pivot(T(C)); f.pin(T(A)); f.pin(T(B))
    for p, s, dx, dy in ((O, "O", -10, -4), (A, "A", -8, -12), (B, "B", 6, -12), (C, "C", 12, -4)):
        f.text(T(p), s, dx=dx, dy=dy, anchor="end" if dx < 0 else "start")
    f.line(T(O), T(V(0.12, 0)), "muted", dash="4 4"); f.arc(T(O), 36, 0, 60, "muted", "60°", lr=52)
    f.arc(T(O), 20, 250, 340, "abs", "ω = 10 rad/s, α = 40 rad/s² (CCW)", arrow=True, ccw=True, lr=34, la=300)
    f.dim(T(V(0, -0.07)), T(V(0.45, -0.07)), "OC = 450 mm", off=0, side="r")
    f.text(T(A * 0.5), "150", "muted", dx=10, anchor="start")
    f.text(T((A + B) / 2), "AB = 350 mm", "muted", dy=-14)
    f.text(T((B + C) / 2), "CB = 250", "muted", dx=10, anchor="start")
    return f.svg()


def e5():
    f = Fig(70, "Q5 two smooth pucks at the instant of impact")
    A = V(0, 0); B = 1.6 * U(30)
    f.circle(T(A), 0.8, "outline"); f.circle(T(B), 0.8, "outline")
    f.text(T(A), "A (0.5 kg)", dy=0); f.text(T(B), "B (0.8 kg)", dy=0)
    f.line(T(A - 0.6 * U(30)), T(B + 1.2 * U(30)), "cons")
    f.line(T(A + 0.8 * U(30)), T(A + 0.8 * U(30) + V(1.6, 0)), "muted", dash="3 3")
    f.arc(T(A + 0.8 * U(30)), 50, 0, 30, "muted", "30°", lr=66, la=12)
    f.arrow(T(A + V(-2.4, -0.2)), T(A + V(-1.0, -0.2)), "abs", "4 m/s", at=("S", 12), lpos=0.5)
    f.arrow(T(B + V(0.2, -2.2)), T(B + V(0.2, -1.0)), "abs", "2 m/s", at=("E", 6), lpos=0.4)
    f.line((-2.8, 0), (3.6, 0), "muted"); f.text((3.6, 0), "x", "muted", dx=6, anchor="start")
    f.text(T(B + 1.25 * U(30)), "line of centres", "muted", dx=6, anchor="start")
    return f.svg()


def e6():
    f = Fig(150, "Q6 block on a 30 degree incline above a spring")
    u, nrm = U(30), U(120)
    base = V(0, 0)
    f.line(T(base - 0.3 * u), T(base + 2.9 * u), "ink")
    f.line(T(base - V(0.3, 0)), T(base + V(2.9 * math.cos(math.radians(30)), 0)), "ink")
    f.line(T(base), T(base + 0.5 * nrm), "ink")
    a, b = f.P(T(base - 0.05 * u)), f.P(T(base - 0.05 * u + 0.5 * nrm)); f.hatch(a[0], a[1], b[0], b[1], side=-1)
    free = base + 0.6 * u
    n = 10
    pts = [base + 0.12 * nrm] + [base + 0.12 * nrm + u * (0.6 * i / n) + nrm * (0.05 if i % 2 else -0.05) for i in range(1, n)] + [free + 0.12 * nrm]
    f.path_world([T(q) for q in pts], "ink")
    f.line(T(free + 0.02 * nrm), T(free + 0.22 * nrm), "ink")
    A = free + 1.2 * u
    c = A + 0.14 * nrm + 0.17 * u
    corners = [A, A + 0.34 * u, A + 0.34 * u + 0.28 * nrm, A + 0.28 * nrm, A]
    f.path_world([T(q) for q in corners], "block")
    f.text(T(c), "4 kg")
    f.dim(T(free), T(A), "1.2 m", off=26, side="r")
    f.arc(T(base), 60, 0, 30, "muted", "30°", lr=78, la=12)
    f.text(T(free * 0.5 + 0.35 * nrm), "k = 1500 N/m", "muted", dx=-6, anchor="end")
    f.text(T(A + 0.7 * u + 0.5 * nrm), "μ_k = 0.25, μ_s = 0.30", "muted", anchor="start")
    f.text(T(A + 0.55 * nrm), "released from rest", "muted", dx=10, anchor="start")
    return f.svg()


def e7():
    f = Fig(150, "Q7 bar AB with a disc welded at B, pinned at A and held by a cable at B")
    A, B = V(0, 0), V(2, 0)
    ceiling(f, 1.7, 2.3, 1.0)
    f.link(T(A), T(B), w=9); f.circle(T(B), 0.2, "body")
    f.line(T(B + V(0, 0.2)), T(V(2, 1.0)), "rope")
    f.pivot(T(A)); f.pin(T(B), 3)
    f.text(T(A), "A", dx=-10, dy=-6, anchor="end"); f.text(T(B), "B", dx=12, dy=8, anchor="start")
    f.dim(T(A), T(B), "2 m", off=30, side="r")
    f.text(T(V(1, 0)), "bar: 6 kg", "muted", dy=-14)
    f.text(T(B + V(0.25, -0.15)), "disc: 4 kg, r = 0.2 m", "muted", anchor="start")
    f.text(T(V(2.08, 0.6)), "cable", "muted", anchor="start")
    return f.svg()


def e8():
    f = Fig(300, "Q8 solid cylinder on a rough floor pushed at its centre")
    G = V(0, 0.25)
    f.line(T(V(-0.6, 0)), T(V(0.9, 0)), "ink")
    a, b = f.P((-0.6, 0)), f.P((0.9, 0)); f.hatch(a[0], a[1], b[0], b[1], side=1)
    f.circle(T(G), 0.25, "body"); f.pin(T(G), 3)
    f.arrow(T(G + V(-0.55, 0)), T(G), "abs", "P", at=("N", 10), lpos=0.4)
    f.text(T(G + V(0.32, 0.05)), "30 kg, r = 250 mm", "muted", anchor="start")
    f.text(T(V(0.3, -0.06)), "μ_s = 0.20, μ_k = 0.15", "muted", anchor="start")
    return f.svg()


# ================================================================ MEMO FIGURES
def m1():
    f = Fig(130, "Memo Q1: e_r and e_theta at the drone, with v and a split into r and theta parts")
    P = V(0, 0)
    er, eth = U(40), U(130)
    f.line(T(P - 2.2 * er), T(P + 1.4 * er), "cons"); f.text(T(P - 2.2 * er), "to radar O", "muted", dy=12)
    f.arrow(T(P), T(P + 0.9 * er), "muted", "e_{r}", at=("E", 4), lpos=1.0)
    f.arrow(T(P), T(P + 0.9 * eth), "muted", "e_{θ}", at=("N", 8), lpos=1.0)
    v = V(1.5, 0)
    f.arrow(T(P), T(P + v), "abs", "v = 30", at=("S", 12), lpos=1.0)
    f.line(T(P + v), T(P + (v @ er) * er), "muted", dash="3 3"); f.line(T(P + v), T(P + (v @ eth) * eth), "muted", dash="3 3")
    f.arrow(T(P), T(P + (v @ er) * er), "t", "v_{r} = +22.98", at=("NW", 4), lpos=0.6)
    f.arrow(T(P), T(P + (v @ eth) * eth), "n", "v_{θ} = −19.28", at=("SW", 4), lpos=1.0)
    right_mark(f, P, er, eth)
    return f.svg()


def m1a():
    f = Fig(ppu_for(0.5), "Memo Q1: a = 2 (along v) + 1.8 (towards the centre of curvature), resolved on e_r and e_theta, 1 cm = 0.5 m/s^2")
    P = V(0, 0); a = V(2, -1.8); er, eth = U(40), U(130)
    f.line(T(P - 1.5 * er), T(P + 2.6 * er), "cons"); f.line(T(P - 3.2 * eth), T(P + 1.2 * eth), "cons")
    f.text(T(P + 2.6 * er), "+r", "muted", dx=6, anchor="start"); f.text(T(P + 1.2 * eth), "+θ", "muted", dy=-8)
    f.arrow(T(P), T(P + V(2, 0)), "t", "a_{t} = 2", at=("N", 10), lpos=0.6)
    f.arrow(T(P + V(2, 0)), T(P + a), "n", "a_{n} = 1.8", at=("E", 6), lpos=0.5)
    f.arrow(T(P), T(P + a), "ans", "a", at=("SW", 4), lpos=0.6)
    f.line(T(P + a), T(P + (a @ er) * er), "muted", dash="3 3"); f.line(T(P + a), T(P + (a @ eth) * eth), "muted", dash="3 3")
    f.arrow(T(P), T(P + (a @ eth) * eth), "abs", "a_{θ} = −2.664", at=("W", 6), lpos=1.0)
    f.arrow(T(P), T(P + (a @ er) * er), "abs", "a_{r} = +0.375", at=("N", 10), lpos=1.0)
    f.set_scalebar(0.5, "1 cm = 0.5 m/s²")
    return true_size(f.svg())


def m2():
    f = Fig(85, "Memo Q2: datum at P; the rope = slanted part S + hanging part y_B")
    P = V(0, 0)
    f.circle(T(P), 0.12, "outline"); f.pin(T(P), 3)
    f.line(T(V(-0.8, 0)), T(V(2.6, 0)), "cons"); f.text((2.6, 0), "datum", "muted", dx=6, anchor="start")
    f.line(T(V(-0.6, -2)), T(V(2.8, -2)), "guide")
    A = V(1.5, -2)
    box(f, A, 0.3, 0.2, "block", "A")
    f.line(T(P), T(A), "t"); f.text(T((P + A) / 2), "S = √(x² + h²) = 2.5 m", "t", dx=10, anchor="start")
    f.line(T(V(-0.12, 0)), T(V(-0.12, -1.3)), "n")
    box(f, V(-0.12, -1.5), 0.4, 0.4, "block", "B")
    f.dim(T(V(-0.5, 0)), T(V(-0.5, -1.3)), "y_{B}", off=0, side="l")
    f.dim(T(V(0, -2)), T(V(1.5, -2)), "x = 1.5 m", off=26, side="r")
    f.dim(T(V(2.3, 0)), T(V(2.3, -2)), "h = 2 m", off=0, side="l")
    return f.svg()


def m3():
    f = Fig(ppu_for(0.1), "Memo Q3: IC of AB, to scale 1:10")
    O, A, B = V(0, 0), Q3A, Q3B
    C = V(B[1] / math.tan(math.radians(30)), B[1])
    f.line(T(O), T(C + 0.06 * U(30)), "cons"); f.line(T(B), T(C + V(0.06, 0)), "cons")
    f.link(T(O), T(A), w=7); f.link(T(A), T(B), w=6)
    f.pivot(T(O)); f.pin(T(A)); f.pin(T(B))
    f.dot(T(C), r=5, cls="dotans"); f.text(T(C), "C (IC)", "ans", dx=10, anchor="start")
    f.text(T(O), "O", dx=-10, anchor="end"); f.text(T(A), "A", dx=-4, dy=-14, anchor="end"); f.text(T(B), "B", dx=-10, anchor="end")
    f.arrow(T(A), T(A + 0.12 * U(120)), "abs", "v_{A} = 1.2", at=("W", 6), lpos=1.0)
    f.arrow(T(B), T(B + V(0, 0.08)), "ans", "v_{B} = 0.640 ↑", at=("W", 6), lpos=1.0)
    f.text(T((A + C) / 2), "r_{A/C} = 0.833 m", "ans", dx=10, dy=12, anchor="start")
    f.text(T((B + C) / 2), "r_{B/C} = 0.444 m", "ans", dy=-12)
    f.arc(T(C), 26, 200, 100, "ans", "ω_{AB} CW", arrow=True, ccw=False, lr=44, la=150)
    f.set_scalebar(0.1, "1 cm = 0.1 m")
    return true_size(f.svg())


def m4geom():
    f = Fig(ppu_for(0.04), "Memo Q4: geometry to scale 1:4 with the two link angles")
    O, A, B, C = V(0, 0), Q4A, Q4B, Q4C
    f.link(T(O), T(A), w=7); f.link(T(A), T(B), w=6); f.link(T(C), T(B), w=7)
    f.pivot(T(O)); f.pivot(T(C)); f.pin(T(A)); f.pin(T(B))
    f.line(T(A), T(A + V(0.12, 0)), "muted", dash="3 3"); f.arc(T(A), 40, 0, 19.36, "ans", "19.4°", lr=58, la=8)
    f.line(T(C), T(C + V(0.1, 0)), "muted", dash="3 3"); f.arc(T(C), 34, 0, 100.32, "ans", "100.3°", lr=52, la=50)
    for p, s, dx, dy in ((O, "O", -10, -4), (A, "A", -8, -10), (B, "B", 6, -12), (C, "C", 12, 8)):
        f.text(T(p), s, dx=dx, dy=dy, anchor="end" if dx < 0 else "start")
    f.set_scalebar(0.04, "1 cm = 40 mm")
    return true_size(f.svg())


def m4v():
    f = Fig(ppu_for(0.25), "Memo Q4: velocity polygon, 1 cm = 0.25 m/s")
    o = V(0, 0); a = 1.5 * U(150); b = 0.9892 * U(190.3)
    f.line(T(a - 0.3 * U(289.4)), T(b + 0.3 * U(289.4)), "cons"); f.line(T(o - 0.2 * U(190.3)), T(b + 0.3 * U(190.3)), "cons")
    f.arrow(T(o), T(a), "abs", "v_{A} = 1.5 (⊥ OA)", at=("N", 10), lpos=0.5)
    f.arrow(T(a), T(b), "t", "v_{B/A} = 0.983 (⊥ AB)", at=("W", 8), lpos=0.5)
    f.arrow(T(o), T(b), "ans", "v_{B} = 0.989 (⊥ CB)", at=("S", 12), lpos=0.5)
    f.text(T(o), "o", dx=6, dy=-8, anchor="start"); f.text(T(a), "a", dx=-8, anchor="end"); f.text(T(b), "b", dx=-8, dy=8, anchor="end")
    f.set_scalebar(0.25, "1 cm = 0.25 m/s")
    return true_size(f.svg())


def m4a():
    f = Fig(ppu_for(2.5), "Memo Q4: acceleration polygon, 1 cm = 2.5 m/s^2")
    o = V(0, 0)
    aAn = 15 * U(240); aA = aAn + 6 * U(150)
    p = aA + 2.76 * U(199.36)
    q = 3.9138 * U(280.32)
    b = q + 17.6548 * U(190.3)
    f.line(T(p - 2 * U(109.4)), T(b + 3 * U(109.4)), "cons"); f.line(T(q - 3 * U(190.3)), T(b + 3 * U(190.3)), "cons")
    f.arrow(T(o), T(aAn), "n", "(a_{A})_{n} = 15", at=("E", 6), lpos=0.5)
    f.arrow(T(aAn), T(aA), "t", "(a_{A})_{t} = 6", at=("S", 12), lpos=0.5)
    f.arrow(T(aA), T(p), "n", "(a_{B/A})_{n} = 2.76", at=("W", 8), lpos=0.6)
    f.arrow(T(p), T(b), "t", "(a_{B/A})_{t} = 4.12", at=("W", 8), lpos=0.6)
    f.arrow(T(o), T(q), "n", "(a_{B})_{n} = 3.91", at=("E", 6), lpos=0.5)
    f.arrow(T(q), T(b), "t", "(a_{B})_{t} = 17.65", at=("N", 10), lpos=0.5)
    f.arrow(T(o), T(b), "ans", "a_{B} = 18.1", at=("N", 10), lpos=0.35, dashed=True)
    f.text(T(o), "o", dx=6, dy=-8, anchor="start"); f.text(T(b), "b", dx=-8, anchor="end")
    f.set_scalebar(2.5, "1 cm = 2.5 m/s²")
    return true_size(f.svg())


def m5():
    f = Fig(48, "Memo Q5: n along the line of centres (30 degrees), t perpendicular; before and after velocities")
    out = []
    n, t = U(30), U(120)
    for x0, title, vA, vB in ((0, "before", V(4, 0), V(0, 2)), (9.5, "after", V(1.899, -1.213), V(1.313, 2.758))):
        P = V(x0, 0)
        f.line(T(P - 3 * n), T(P + 4 * n), "cons"); f.line(T(P - 2.5 * t), T(P + 3 * t), "cons")
        f.text(T(P + 4 * n), "+n", "n", dx=6, anchor="start"); f.text(T(P + 3 * t), "+t", "t", dy=-8)
        f.arrow(T(P), T(P + vA), "abs" if title == "before" else "ans", f"v_{{A}} {'= 4' if title == 'before' else '= 2.25'}", at=("S", 12), lpos=1.0)
        f.arrow(T(P), T(P + vB), "abs" if title == "before" else "ans", f"v_{{B}} {'= 2' if title == 'before' else '= 3.05'}", at=("W", 6), lpos=1.0)
        f.text(T(P + V(0, -3.4)), title, "muted")
    return f.svg()


def m6():
    f = Fig(150, "Memo Q6: positions 1, 2, 3 along the incline, with the block's FBD while sliding down")
    u, nrm = U(30), U(120)
    base = V(0, 0)
    f.line(T(base - 0.3 * u), T(base + 2.9 * u), "ink")
    f.line(T(base), T(base + 0.5 * nrm), "ink")
    P3, P2 = base + 0.6 * u - 0.141 * 2 * u, base + 0.6 * u
    P1 = P2 + 1.2 * u
    for P, lab in ((P1, "1: rest"), (P2, "2: touches spring"), (P3, "3: max squash")):
        f.dot(T(P + 0.02 * nrm)); f.text(T(P), lab, "muted", dx=6, dy=14, anchor="start")
    f.dim(T(P2), T(P1), "1.2 m", off=30, side="l")
    f.dim(T(P3), T(P2), "x", off=30, side="l")
    G = P1 + 0.9 * u + 0.6 * nrm
    f.path_world([T(G - 0.15 * u - 0.12 * nrm), T(G + 0.15 * u - 0.12 * nrm), T(G + 0.15 * u + 0.12 * nrm), T(G - 0.15 * u + 0.12 * nrm), T(G - 0.15 * u - 0.12 * nrm)], "block")
    f.arrow(T(G), T(G + V(0, -0.5)), "ans", "W = 39.24 N", at=("E", 6), lpos=0.9)
    f.arrow(T(G - 0.12 * nrm - 0.45 * nrm), T(G - 0.12 * nrm), "ans", "N", at=("W", 6), lpos=0.3)
    f.arrow(T(G - 0.12 * nrm), T(G - 0.12 * nrm + 0.42 * u), "ans", "F = μ_k N (up the slope)", at=("N", 10), lpos=1.0)
    f.arrow(T(G + 0.35 * nrm + 0.1 * u), T(G + 0.35 * nrm - 0.3 * u), "abs", "motion", at=("N", 8), lpos=0.6)
    return f.svg()


def m7fbd():
    f = Fig(110, "Memo Q7 FBD just after the cable is cut")
    A, G = V(0, 0), V(1.4, 0)
    f.link(T(A), T(V(2, 0)), w=8); f.circle(T(V(2, 0)), 0.2, "outline")
    f.arrow(T(A + V(0, -0.8)), T(A), "ans", "A_{y}", at=("W", 6), lpos=0.3)
    f.arrow(T(A + V(-0.8, 0)), T(A), "ans", "A_{x} (= 0)", at=("N", 10), lpos=0.3)
    f.arrow(T(V(1, 0)), T(V(1, -0.8)), "ans", "58.86 N", at=("W", 6), lpos=0.8)
    f.arrow(T(V(2, 0)), T(V(2, -0.8)), "ans", "39.24 N", at=("E", 6), lpos=0.8)
    f.dot(T(G), cls="dotans"); f.text(T(G), "G (1.4 m)", "ans", dy=-14)
    f.text(T(A), "A", dx=-10, dy=-10, anchor="end")
    return f.svg()


def m7kd():
    f = Fig(110, "Memo Q7 KD: m a_G down at G (omega = 0), I_G alpha clockwise")
    A, G = V(0, 0), V(1.4, 0)
    f.link(T(A), T(V(2, 0)), w=8); f.circle(T(V(2, 0)), 0.2, "outline")
    f.arrow(T(G), T(G + V(0, -0.8)), "abs", "m a_{G} = 10(1.4α)", at=("E", 6), lpos=0.8)
    curl(f, G, "I_{G}α", cw=True, r=16)
    f.text(T(A), "A", dx=-10, dy=-10, anchor="end")
    f.text(T(V(0.6, -0.6)), "(m a_G)_n = m r̄ ω² = 0", "muted")
    return f.svg()


def m8():
    f = Fig(240, "Memo Q8 FBD and KD of the cylinder")
    for x0, kind in ((0, "fbd"), (1.25, "kd")):
        G = V(x0, 0.25); Cc = V(x0, 0)
        f.circle(T(G), 0.25, "outline")
        f.line(T(V(x0 - 0.4, 0)), T(V(x0 + 0.4, 0)), "muted")
        if kind == "fbd":
            f.arrow(T(G + V(-0.42, 0)), T(G), "ans", "P", at=("N", 10), lpos=0.4)
            f.arrow(T(G), T(G + V(0, -0.36)), "ans", "mg", at=("E", 6), lpos=0.5)
            f.arrow(T(Cc + V(0, -0.2)), T(Cc), "ans", "N", at=("E", 6), lpos=0.3)
            f.arrow(T(Cc), T(Cc + V(-0.3, 0)), "ans", "F", at=("S", 12), lpos=0.8)
            f.text(T(G + V(0, 0.36)), "FBD", "muted")
        else:
            f.arrow(T(G), T(G + V(0.35, 0)), "abs", "m a", at=("N", 10), lpos=0.7)
            curl(f, G, "I_{G}α", cw=True, r=18)
            f.text(T(G + V(0, 0.36)), "KD", "muted")
    return f.svg()


def build_all():
    names = ("e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8", "m1", "m1a", "m2", "m3", "m4geom", "m4v", "m4a", "m5", "m6",
             "m7fbd", "m7kd", "m8")
    return {n: globals()[n]() for n in names}


if __name__ == "__main__":
    for k_, v_ in build_all().items():
        print(k_, len(v_))
