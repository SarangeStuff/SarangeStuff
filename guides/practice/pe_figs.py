"""Figures for the guided practice exam and its memo."""
import math
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
for sub in ("textbook", "guides/planekinetics", "guides/hwmemo", "guides/constrained", "guides/polar"):
    sys.path.insert(0, str(ROOT / sub))
from svgkit import Fig  # noqa: E402
from pk_figs import true_size, ppu_for, right_mark  # noqa: E402
import pk_figs  # noqa: E402
import hw_figs  # noqa: E402
import cm_figs  # noqa: E402

V = lambda x, y: np.array([float(x), float(y)])
T = lambda v: (float(v[0]), float(v[1]))
U = lambda d: V(math.cos(math.radians(d)), math.sin(math.radians(d)))


# ------------------------------------------------------------------ theory: four situations
def situations():
    f = Fig(48, "Relative velocity in four situations: same body, separate bodies, shared pin, bodies touching")
    # 1 same body
    A, B = V(0, 0), 2.6 * U(30)
    f.link(T(A), T(B), w=7); f.pin(T(A)); f.pin(T(B))
    f.text(T(A), "A", dx=-8, dy=8, anchor="end"); f.text(T(B), "B", dx=8, anchor="start")
    f.line(T(B - 1.2 * U(120)), T(B + 1.2 * U(120)), "cons")
    f.arrow(T(B), T(B + 1.1 * U(120)), "ans", "v_{B/A} ⊥ AB", at=("W", 6), lpos=1.0)
    f.text((1.3, -1.6), "1 · same rigid body", "muted")
    # 2 separate bodies
    o = V(6.2, 0)
    vA, vB = V(2.4, 0), V(0, 1.6)
    f.arrow(T(o), T(o + vA), "abs", "v_{A}", at=("S", 12), lpos=0.5)
    f.arrow(T(o), T(o + vB), "abs", "v_{B}", at=("W", 6), lpos=0.6)
    f.arrow(T(o + vA), T(o + vB), "ans", "v_{B/A} = v_{B} − v_{A}", at=("NE", 4), lpos=0.4)
    f.text((7.4, -1.6), "2 · separate bodies: join the tips", "muted")
    # 3 shared pin
    O1, Bp, C1 = V(11.3, 0), V(12.6, 1.6), V(14.6, 0.3)
    f.link(T(O1), T(Bp), w=7); f.link(T(Bp), T(C1), w=7)
    f.pin(T(O1)); f.pin(T(Bp)); f.pin(T(C1))
    f.text(T(Bp), "pin B: one velocity", "ans", dy=-14)
    f.text((12.9, -1.6), "3 · two links, one shared pin", "muted")
    # 4 touching
    g1, g2 = V(17.6, 0.4), V(19.6, 0.4)
    f.circle(T(g1), 1.2, "outline"); f.circle(T(g2), 0.8, "outline")
    Cc = V(18.8, 0.4)
    f.arrow(T(Cc), T(Cc + V(0, 1.2)), "ans", "shared v (no slip)", at=("E", 6), lpos=1.0)
    f.text((18.7, -1.6), "4 · touching: contact points", "muted")
    return f.svg()


# ------------------------------------------------------------------ exam figures
def q1a():
    f = Fig(300, "Q1(a) link AB at 30 degrees, omega 4 rad/s clockwise")
    A, B = V(0, 0), 0.25 * U(30)
    f.link(T(A), T(B), w=8); f.pin(T(A)); f.pin(T(B))
    f.line(T(A), T(V(0.3, 0)), "muted", dash="4 4")
    f.arc(T(A), 40, 0, 30, "muted", "30°", lr=56)
    f.text(T(A), "A", dx=-8, dy=8, anchor="end"); f.text(T(B), "B", dx=8, dy=-6, anchor="start")
    f.text(T((A + B) / 2), "250 mm", "muted", dx=-8, dy=-12, anchor="end")
    f.arc(T((A + B) / 2), 26, 150, 30, "abs", "ω = 4 rad/s CW", arrow=True, ccw=False, lr=42, la=90)
    return f.svg()


def q1b():
    f = Fig(9, "Q1(b) car A heading east at 24 m/s, car B heading north at 10 m/s")
    f.line((-14, 0), (16, 0), "muted"); f.line((0, -12), (0, 12), "muted")
    A, B = V(-9, -0.8), V(1.2, -8)
    f.path_world([(A[0] - 1.4, A[1] - 0.7), (A[0] + 1.4, A[1] - 0.7), (A[0] + 1.4, A[1] + 0.7), (A[0] - 1.4, A[1] + 0.7), (A[0] - 1.4, A[1] - 0.7)], "block")
    f.path_world([(B[0] - 0.7, B[1] - 1.4), (B[0] + 0.7, B[1] - 1.4), (B[0] + 0.7, B[1] + 1.4), (B[0] - 0.7, B[1] + 1.4), (B[0] - 0.7, B[1] - 1.4)], "block")
    f.text(T(A), "A"); f.text(T(B), "B")
    f.arrow(T(A + V(1.6, 0)), T(A + V(7, 0)), "abs", "24 m/s", at=("N", 10), lpos=0.6)
    f.arrow(T(B + V(0, 1.6)), T(B + V(0, 6.5)), "abs", "10 m/s", at=("E", 6), lpos=0.6)
    f.text((16, 0), "E", "muted", dx=6, anchor="start"); f.text((0, 12), "N", "muted", dy=-8)
    return f.svg()


def q1c():
    f = Fig(60, "Q1(c) gear B (radius 2 m) meshing with gear C (radius 1 m) at A")
    Bc, Cc = V(0, 0), V(3, 0)
    f.circle(T(Bc), 2, "outline"); f.circle(T(Cc), 1, "outline")
    f.pin(T(Bc)); f.pin(T(Cc))
    f.text(T(Bc), "B (r = 2 m)", dy=16); f.text(T(Cc), "C (r = 1 m)", dy=16)
    P = V(2, 0)
    f.dot(T(P)); f.text(T(P), "A / A′", dx=-8, dy=-10, anchor="end")
    f.arrow(T(P), T(P + V(0, -1.4)), "ans", "(a_{A})_{t} = 100 m/s²", at=("E", 6), lpos=1.0)
    return f.svg()


def q2():
    return cm_figs.b_cars_geom()


# ------------------------------------------------------------------ memo figures
def m1a():
    f = Fig(300, "Memo Q1(a): v_B/A perpendicular to AB, (a_B/A)_n from B towards A")
    A, B = V(0, 0), 0.25 * U(30)
    f.link(T(A), T(B), w=8); f.pin(T(A)); f.pin(T(B))
    f.text(T(A), "A", dx=-8, dy=8, anchor="end"); f.text(T(B), "B", dx=8, dy=-6, anchor="start")
    f.line(T(B - 0.14 * U(120)), T(B + 0.14 * U(120)), "cons")
    f.arrow(T(B), T(B + 0.18 * U(300)), "ans", "v_{B/A} = 1 m/s @ 300°", at=("E", 6), lpos=1.0)
    f.arrow(T(A), T(A + 0.18 * U(120)), "t", "v_{A/B} = 1 m/s @ 120°", at=("W", 6), lpos=1.0)
    f.arrow(T(B), T(B + 0.12 * U(210)), "n", "(a_{B/A})_{n} = 4 m/s² → A", at=("NW", 4), lpos=1.0)
    right_mark(f, B, U(210), U(300))
    return f.svg()


def m1b():
    f = Fig(ppu_for(5), "Memo Q1(b): v_B/A joins the tip of v_A to the tip of v_B (1 cm = 5 m/s)")
    o = V(0, 0); vA, vB = V(24, 0), V(0, 10)
    f.arrow(T(o), T(vA), "abs", "v_{A} = 24", at=("S", 12), lpos=0.5)
    f.arrow(T(o), T(vB), "abs", "v_{B} = 10", at=("W", 6), lpos=0.5)
    f.arrow(T(vA), T(vB), "ans", "v_{B/A} = 26 m/s", at=("NE", 4), lpos=0.45)
    f.arc(T(vA), 34, 157.4, 180, "muted", "22.6°", lr=52, la=170)
    f.set_scalebar(5, "1 cm = 5 m/s")
    return true_size(f.svg())


def m2v():
    f = Fig(ppu_for(5), "Memo Q2: velocity diagram, 1 cm = 5 m/s")
    o = V(0, 0); vA = 25 * U(115); vB = V(0, 20)
    f.arrow(T(o), T(vB), "abs", "v_{B} = 20", at=("E", 6), lpos=0.5)
    f.arrow(T(o), T(vA), "abs", "v_{A} = 25", at=("W", 6), lpos=0.5)
    f.arrow(T(vB), T(vA), "ans", "v_{A/B} = 10.9 m/s", at=("N", 10), lpos=0.5)
    f.arc(T(o), 30, 90, 115, "muted", "25°", lr=44)
    f.set_scalebar(5, "1 cm = 5 m/s")
    return true_size(f.svg())


def m2a():
    f = Fig(ppu_for(0.25), "Memo Q2: acceleration diagram, 1 cm = 0.25 m/s^2")
    o = V(0, 0); aBn = V(-1.1111, 0); aB = V(-1.1111, 0.8); aA = 1.6667 * U(205)
    f.arrow(T(o), T(aBn), "n", "(a_{B})_{n} = 1.111", at=("N", 10), lpos=0.5)
    f.arrow(T(aBn), T(aB), "t", "(a_{B})_{t} = 0.8", at=("W", 6), lpos=0.6)
    f.arrow(T(o), T(aA), "n", "a_{A} = 1.667 (→ O)", at=("S", 12), lpos=0.6)
    f.arrow(T(aB), T(aA), "ans", "a_{A/B} = 1.56", at=("W", 8), lpos=0.5)
    f.set_scalebar(0.25, "1 cm = 0.25 m/s²")
    return true_size(f.svg())


def build_all():
    out = {n: globals()[n]() for n in ("situations", "q1a", "q1b", "q1c", "q2", "m1a", "m1b", "m2v", "m2a")}
    hw = hw_figs.build_all()
    for k in ("i119", "i108", "i120", "r17_geom", "r17_vec", "m44"):
        out[k] = hw[k]
    pk = pk_figs.build_all()
    for k in ("w8_acc", "w8_fbd", "w8_kd"):
        out[k] = pk[k]
    return out


if __name__ == "__main__":
    for k_, v_ in build_all().items():
        print(k_, len(v_))
