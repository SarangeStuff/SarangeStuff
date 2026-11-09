"""Figures for the polar / cylindrical / spherical study guide (SVG via textbook/svgkit.py)."""
import math
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "textbook"))
from svgkit import Fig  # noqa: E402

V = lambda x, y: np.array([float(x), float(y)])
T = lambda v: (float(v[0]), float(v[1]))


def U(deg):
    return V(math.cos(math.radians(deg)), math.sin(math.radians(deg)))


def right_angle(f, p, d1, d2, s=9):
    x, y = f.P(p)
    a = (x + d1[0] * s, y - d1[1] * s)
    c = (x + d2[0] * s, y - d2[1] * s)
    b = (x + (d1[0] + d2[0]) * s, y - (d1[1] + d2[1]) * s)
    f.add(f'<path class="ramark muted" d="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f} L{c[0]:.1f},{c[1]:.1f}"/>')


FIGS = {}


def reg(fn):
    FIGS[fn.__name__] = fn
    return fn


@reg
def pu_unitvec():
    f = Fig(210, "Unit vectors e_r and e_theta at P, with their x and y components")
    th = 35
    P = 1.3 * U(th)
    f.line((0, 0), (1.9, 0), "axis")
    f.text((1.9, 0), "x", "muted", dx=10, anchor="start")
    f.line((0, 0), (0, 1.55), "axis")
    f.text((0, 1.55), "y", "muted", dy=-10)
    f.line((0, 0), T(P), "ink")
    f.line(T(P), T(2.25 * U(th)), "muted", dash="4 4")
    f.text(T(2.25 * U(th)), "radial line", "muted", dx=6, anchor="start")
    f.text(T(0.55 * U(th)), "r", dx=-4, dy=-12)
    f.arc((0, 0), 34, 0, th, "muted", "θ", lr=48)
    L = 0.6
    er, et = U(th), U(th + 90)
    # component triangles
    f.line(T(P), T(P + V(L * er[0], 0)), "cons")
    f.line(T(P + V(L * er[0], 0)), T(P + L * er), "cons")
    f.text(T(P + V(L * er[0] / 2, 0)), "cos θ", "abs", dy=12)
    f.text(T(P + V(L * er[0], L * er[1] / 2)), "sin θ", "abs", dx=8, anchor="start")
    f.line(T(P), T(P + V(0, L * et[1])), "cons")
    f.line(T(P + V(0, L * et[1])), T(P + L * et), "cons")
    f.text(T(P + V(L * et[0] / 2, L * et[1])), "−sin θ", "t", dy=-12)
    f.text(T(P + V(0, L * et[1] * 0.45)), "cos θ", "t", dx=8, anchor="start")
    f.arrow(T(P), T(P + L * er), "abs", "e_{r}", at=("NW", 6), lpos=1.0)
    f.arrow(T(P), T(P + L * et), "t", "e_{θ}", at=("N", 10), lpos=1.0)
    right_angle(f, T(P), er, et)
    f.arc(T(P), 38, 90, 90 + th, "t", "θ", lr=50, la=105)
    f.dot((0, 0), label="O", ldx=-10, ldy=10, anchor="end")
    f.dot(T(P), label="P", ldx=-10, ldy=14, anchor="end")
    return f.svg()


@reg
def pu_rotating():
    f = Fig(110, "As P moves, e_r and e_theta turn with it")
    f.line((0, 0), (2.4, 0), "axis")
    phis = np.linspace(0.15, 2.2, 60)
    rr = lambda p: 1.0 + 0.45 * p
    f.path_world([T(rr(p) * U(math.degrees(p))) for p in phis], "curve", dash="5 5")
    for k, p in enumerate((0.35, 1.15, 1.95)):
        P = rr(p) * U(math.degrees(p))
        f.line((0, 0), T(P), "muted", dash="3 4")
        er, et = U(math.degrees(p)), U(math.degrees(p) + 90)
        f.arrow(T(P), T(P + 0.45 * er), "abs", "e_{r}" if k == 0 else None, at=("E", 6), lpos=1.0)
        f.arrow(T(P), T(P + 0.45 * et), "t", "e_{θ}" if k == 0 else None, at=("N", 8), lpos=1.0)
        f.dot(T(P), r=3)
    f.dot((0, 0), label="O", ldx=-10, ldy=10, anchor="end")
    f.text(T(rr(2.2) * U(math.degrees(2.2))), "path", "muted", dx=-8, anchor="end")
    return f.svg()


@reg
def pu_derivative():
    f = Fig(185, "When theta grows by d-theta, the tip of e_r moves along e_theta and the tip of e_theta moves along minus e_r")
    th, dth = 15, 38
    f.circle((0, 0), 1.0, "outline thin", dash="3 4")
    e1, e2 = U(th), U(th + dth)
    t1, t2 = U(th + 90), U(th + dth + 90)
    f.arrow((0, 0), T(e1), "abs", "e_{r}(θ)", at=("SE", 6), lpos=1.0)
    f.arrow((0, 0), T(e2), "abs", "e_{r}(θ + Δθ)", at=("N", 10), lpos=1.0)
    f.arrow(T(e1), T(e2), "ans", "Δe_{r} ≈ Δθ e_{θ}", at=("E", 10), lpos=0.5, w=3)
    f.arrow((0, 0), T(t1), "t", "e_{θ}(θ)", at=("N", 10), lpos=1.0)
    f.arrow((0, 0), T(t2), "t", "e_{θ}(θ + Δθ)", at=("SW", 8), lpos=1.0)
    f.arrow(T(t1), T(t2), "n", "Δe_{θ} ≈ −Δθ e_{r}", at=("NW", 10), lpos=0.35, w=3)
    f.arc((0, 0), 40, th, th + dth, "muted", "Δθ", lr=56)
    f.dot((0, 0), label="O", ldx=-8, ldy=12, anchor="end")
    return f.svg()


@reg
def pu_velocity():
    f = Fig(140, "Velocity at P split into v_r along e_r and v_theta along e_theta")
    th = 30
    phis = np.linspace(0.05, 1.25, 60)
    rr = lambda p: 1.0 + 0.6 * p
    f.path_world([T(rr(p) * U(math.degrees(p))) for p in phis], "curve", dash="5 5")
    p = math.radians(th)
    P = rr(p) * U(th)
    er, et = U(th), U(th + 90)
    vr, vt = 0.6 * 0.55, rr(p) * 0.55  # proportional to rdot and r*thetadot
    f.line((0, 0), (2.3, 0), "axis")
    f.line((0, 0), T(P), "ink")
    f.text(T(0.5 * P), "r", dx=-2, dy=-12)
    f.arc((0, 0), 34, 0, th, "muted", "θ", lr=48)
    tip = P + vr * er + vt * et
    f.line(T(P + vr * er), T(tip), "cons")
    f.line(T(P + vt * et), T(tip), "cons")
    f.arrow(T(P), T(P + vr * er), "abs", "v_{r} = ṙ", at=("SE", 6), lpos=0.9)
    f.arrow(T(P), T(P + vt * et), "t", "v_{θ} = rθ̇", at=("W", 8), lpos=0.8)
    f.arrow(T(P), T(tip), "ans", "v (tangent to path)", at=("NE", 6), lpos=0.95)
    f.dot((0, 0), label="O", ldx=-10, ldy=10, anchor="end")
    f.dot(T(P), label="P", ldx=10, ldy=12, anchor="start")
    return f.svg()


@reg
def pu_accel():
    f = Fig(140, "Acceleration at P: the radial part r-double-dot minus r theta-dot squared, and the transverse part")
    th = 30
    P = 1.4 * U(th)
    er, et = U(th), U(th + 90)
    f.line((0, 0), (2.2, 0), "axis")
    f.line((0, 0), T(P), "ink")
    f.arc((0, 0), 34, 0, th, "muted", "θ", lr=48)
    rdd, cent, at = 0.35, -0.75, 0.55
    f.arrow(T(P), T(P + rdd * er), "abs", "r̈ (speeding out)", at=("SE", 6), lpos=1.0)
    f.arrow(T(P - 0.07 * et), T(P - 0.07 * et + cent * er), "n", "−rθ̇² (towards O)", at=("SE", 8), lpos=0.75)
    f.arrow(T(P), T(P + at * et), "t", "a_{θ} = rθ̈ + 2ṙθ̇", at=("N", 10), lpos=1.0)
    ar = rdd + cent
    tip = P + ar * er + at * et
    f.arrow(T(P), T(P + ar * er), "abs", "a_{r} = r̈ − rθ̇²", at=("NW", 6), lpos=1.0, dashed=True)
    f.line(T(P + ar * er), T(tip), "cons")
    f.line(T(P + at * et), T(tip), "cons")
    f.arrow(T(P), T(tip), "ans", "a", at=("W", 10), lpos=0.6)
    f.dot((0, 0), label="O", ldx=-10, ldy=10, anchor="end")
    f.dot(T(P), label="P", ldx=12, ldy=8, anchor="start")
    return f.svg()


@reg
def pu_project():
    f = Fig(175, "Turning x-y components into r-theta components by projecting onto e_r and e_theta")
    th = 30
    P = V(0, 0)
    er, et = U(th), U(th + 90)
    v = V(0.9, 1.5)
    f.line((-0.3, 0), (1.6, 0), "muted", dash="3 3")
    f.text((1.6, 0), "x", "muted", dx=8, anchor="start")
    f.line((0, -0.2), (0, 1.8), "muted", dash="3 3")
    f.text((0, 1.8), "y", "muted", dy=-10)
    f.line(T(-0.3 * er), T(2.0 * er), "muted", dash="1 3")
    f.text(T(2.0 * er), "r direction", "abs", dx=6, anchor="start")
    f.line(T(-0.2 * et), T(1.5 * et), "muted", dash="1 3")
    f.text(T(1.5 * et), "θ direction", "t", dy=-10)
    vr, vt = float(v @ er), float(v @ et)
    f.line(T(v), T(vr * er), "cons")
    f.line(T(v), T(vt * et), "cons")
    f.arrow(T(P), T(v), "ans", "v", at=("E", 8), lpos=0.9)
    f.arrow(T(P), T(vr * er), "abs", "v_{r} = v_{x}cos θ + v_{y}sin θ", at=("SE", 6), lpos=1.0)
    f.arrow(T(P), T(vt * et), "t", "v_{θ} = −v_{x}sin θ + v_{y}cos θ", at=("W", 8), lpos=1.0)
    f.arc(T(P), 40, 0, th, "muted", "θ", lr=54)
    right_angle(f, T(vr * er), -er, et)
    return f.svg()


# ---------------------------------------------------------------- 3D sketches
def p3(x, y, z):
    """Oblique projection: x drawn down-left, y right, z up."""
    return (y - 0.55 * x, z - 0.32 * x)


@reg
def cyl_geom():
    f = Fig(120, "Cylindrical coordinates r, theta, z and the unit vectors e_r, e_theta, k")
    th = math.radians(55)
    r, z = 1.6, 1.3
    O = (0, 0, 0)
    f.arrow(p3(*O), p3(2.0, 0, 0), "muted", None)
    f.text(p3(2.0, 0, 0), "x", "muted", dx=-8, dy=8)
    f.arrow(p3(*O), p3(0, 2.2, 0), "muted", None)
    f.text(p3(0, 2.2, 0), "y", "muted", dx=10)
    f.arrow(p3(*O), p3(0, 0, 2.1), "muted", None)
    f.text(p3(0, 0, 2.1), "z", "muted", dy=-10)
    Pg = (r * math.cos(th), r * math.sin(th), 0)
    P = (Pg[0], Pg[1], z)
    f.line(p3(*O), p3(*Pg), "ink")
    f.text(p3(Pg[0] / 2, Pg[1] / 2, 0), "r", dx=6, dy=12)
    f.line(p3(*Pg), p3(*P), "muted", dash="4 4")
    f.text(p3(Pg[0], Pg[1], z / 2), "z", dx=8, anchor="start")
    f.line(p3(*O), p3(*P), "muted", dash="2 4")
    pts = [p3(0.55 * math.cos(a), 0.55 * math.sin(a), 0) for a in np.linspace(0, th, 20)]
    f.path_world(pts, "muted")
    f.text(p3(0.75 * math.cos(th / 2), 0.75 * math.sin(th / 2), 0), "θ", "muted")
    er = (math.cos(th), math.sin(th), 0)
    et = (-math.sin(th), math.cos(th), 0)
    L = 0.7
    f.arrow(p3(*P), p3(P[0] + L * er[0], P[1] + L * er[1], z), "abs", "e_{r}", at=("S", 12), lpos=1.0)
    f.arrow(p3(*P), p3(P[0] + L * et[0], P[1] + L * et[1], z), "t", "e_{θ}", at=("E", 8), lpos=1.0)
    f.arrow(p3(*P), p3(P[0], P[1], z + L), "n", "k", at=("E", 8), lpos=1.0)
    f.dot(p3(*O), label="O", ldx=-8, ldy=12, anchor="end")
    f.dot(p3(*P), label="P", ldx=-10, ldy=-8, anchor="end")
    return f.svg()


@reg
def sph_geom():
    f = Fig(165, "Spherical coordinates R, theta, phi and the unit vectors e_R, e_theta, e_phi")
    th, ph = math.radians(50), math.radians(35)
    R = 2.0
    rh = R * math.cos(ph)
    O = (0, 0, 0)
    f.arrow(p3(*O), p3(2.2, 0, 0), "muted", None)
    f.text(p3(2.2, 0, 0), "x", "muted", dx=-8, dy=8)
    f.arrow(p3(*O), p3(0, 2.4, 0), "muted", None)
    f.text(p3(0, 2.4, 0), "y", "muted", dx=10)
    f.arrow(p3(*O), p3(0, 0, 1.9), "muted", None)
    f.text(p3(0, 0, 1.9), "z", "muted", dy=-10)
    A = (rh * math.cos(th), rh * math.sin(th), R * math.sin(ph))
    Ag = (A[0], A[1], 0)
    f.line(p3(*O), p3(*A), "ink")
    f.text(p3(A[0] * 0.55, A[1] * 0.55, A[2] * 0.55), "R", dx=-8, dy=-10)
    f.line(p3(*O), p3(*Ag), "muted", dash="4 4")
    f.text(p3(Ag[0] * 0.5, Ag[1] * 0.5, 0), "R cos φ", "muted", dx=8, dy=14, anchor="start")
    f.line(p3(*Ag), p3(*A), "muted", dash="4 4")
    f.text(p3(A[0], A[1], A[2] / 2), "R sin φ", "muted", dx=8, anchor="start")
    pts = [p3(0.5 * math.cos(a), 0.5 * math.sin(a), 0) for a in np.linspace(0, th, 20)]
    f.path_world(pts, "muted")
    f.text(p3(0.72 * math.cos(th / 2), 0.72 * math.sin(th / 2), 0), "θ", "muted")
    pts = [p3(0.75 * math.cos(b) * math.cos(th), 0.75 * math.cos(b) * math.sin(th), 0.75 * math.sin(b)) for b in np.linspace(0, ph, 20)]
    f.path_world(pts, "muted")
    f.text(p3(0.95 * math.cos(ph / 2) * math.cos(th), 0.95 * math.cos(ph / 2) * math.sin(th), 0.95 * math.sin(ph / 2)), "φ", "muted", dx=6)
    # horizontal circle through A (radius R cos phi) to explain cos phi
    circ = [p3(rh * math.cos(a), rh * math.sin(a), A[2]) for a in np.linspace(th - 0.9, th + 0.7, 40)]
    f.path_world(circ, "cons")
    f.text(circ[0], "circle of radius R cos φ", "muted", dx=-6, dy=-10, anchor="end")
    eR = (math.cos(ph) * math.cos(th), math.cos(ph) * math.sin(th), math.sin(ph))
    et = (-math.sin(th), math.cos(th), 0)
    ep = (-math.sin(ph) * math.cos(th), -math.sin(ph) * math.sin(th), math.cos(ph))
    L = 0.7
    f.arrow(p3(*A), p3(*(A[i] + L * eR[i] for i in range(3))), "abs", "e_{R}", at=("E", 8), lpos=1.0)
    f.arrow(p3(*A), p3(*(A[i] + L * et[i] for i in range(3))), "t", "e_{θ}", at=("S", 12), lpos=1.0)
    f.arrow(p3(*A), p3(*(A[i] + L * ep[i] for i in range(3))), "n", "e_{φ}", at=("N", 10), lpos=1.0)
    f.dot(p3(*O), label="O", ldx=-8, ldy=12, anchor="end")
    f.dot(p3(*A), label="A", ldx=-10, ldy=-6, anchor="end")
    return f.svg()


def build_all():
    return {k: fn() for k, fn in FIGS.items()}


if __name__ == "__main__":
    for k, v in build_all().items():
        print(k, len(v))
