"""Builds every SVG figure in the book. Polygons are drawn to scale from mech.py."""
import math
import numpy as np

import mech
from svgkit import Fig

V = mech.V
unit = mech.unit


def tup(v):
    return (float(v[0]), float(v[1]))


def right_angle(f, p, d1, d2, s=9, step=None, cls="muted"):
    x, y = f.P(p)
    a = (x + d1[0] * s, y - d1[1] * s)
    c = (x + d2[0] * s, y - d2[1] * s)
    b = (x + (d1[0] + d2[0]) * s, y - (d1[1] + d2[1]) * s)
    f.add(f'<path class="ramark {cls}" d="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f} L{c[0]:.1f},{c[1]:.1f}"/>', step)


def through(f, p, d, X, ext, step=None, cls="cons"):
    """Construction line through p along unit d, long enough to pass X by ext."""
    p = np.asarray(p, float)
    d = np.asarray(d, float)
    tX = float(np.dot(np.asarray(X, float) - p, d))
    f.cline(tup(p), tup(d), min(0.0, tX) - ext, max(0.0, tX) + ext, cls=cls, step=step)


FIGS = {}


def reg(name):
    def deco(fn):
        FIGS[name] = fn
        return fn
    return deco


# ------------------------------------------------------------------ toolkit
@reg("tri_rules")
def tri_rules():
    f = Fig(52, "Triangle with sides a, b, c opposite angles A, B, C")
    A, B, C = (0, 0), (4.2, 0), (1.4, 2.5)
    f.path_world([A, B, C, A], "tri")
    f.text(A, "A", dx=-10, dy=6)
    f.text(B, "B", dx=10, dy=6)
    f.text(C, "C", dx=0, dy=-12)
    f.text(((B[0] + C[0]) / 2, (B[1] + C[1]) / 2), "a", "abs", dx=12, dy=-6)
    f.text(((A[0] + C[0]) / 2, (A[1] + C[1]) / 2), "b", "abs", dx=-12, dy=-6)
    f.text(((A[0] + B[0]) / 2, 0), "c", "abs", dy=12)
    angA = math.degrees(math.atan2(C[1], C[0]))
    f.arc(A, 22, 0, angA, "muted")
    angB = math.degrees(math.atan2(C[1] - B[1], C[0] - B[0]))
    f.arc(B, 22, angB, 180, "muted")
    angC1 = math.degrees(math.atan2(A[1] - C[1], A[0] - C[0]))
    angC2 = math.degrees(math.atan2(B[1] - C[1], B[0] - C[0]))
    f.arc(C, 20, angC1, angC2, "muted")
    return f.svg()


@reg("motion_graphs")
def motion_graphs():
    f = Fig(1, "Stacked s-t, v-t and a-t graphs for a start-cruise-stop trip")
    X = lambda t: t * 14.0

    def s_of(t):
        if t <= 5:
            return t * t
        if t <= 15:
            return 25 + 10 * (t - 5)
        return 125 + 10 * (t - 15) - (t - 15) ** 2

    def v_of(t):
        if t <= 5:
            return 2 * t
        if t <= 15:
            return 10
        return 10 - 2 * (t - 15)

    ts = [i * 0.25 for i in range(81)]
    # panel offsets (world y up)
    S0, V0, A0 = 250, 135, 40
    ks, kv, ka = 75 / 150, 7.0, 13.0
    for base, top, name in ((S0, S0 + 85, "s (m)"), (V0, V0 + 80, "v (m/s)"), (A0 - 30, A0 + 38, "a (m/s²)")):
        f.line((0, base), (0, top), "axis")
        f.text((0, top), name, "muted", dy=-10, anchor="start")
    for base in (S0, V0, A0):
        f.line((0, base), (X(21.5), base), "axis")
        f.text((X(21.5), base), "t (s)", "muted", dx=4, anchor="start")
    for t in (5, 15):
        f.line((X(t), A0 - 30), (X(t), S0 + 80), "grid", dash="3 4")
    for t in (0, 5, 15, 20):
        f.text((X(t), A0 - 30), str(t), "muted", dy=11)
    f.path_world([(X(t), S0 + s_of(t) * ks) for t in ts], "curve")
    f.path_world([(X(t), V0 + v_of(t) * kv) for t in ts], "curve")
    # area under v-t
    pts = [(X(0), V0)] + [(X(t), V0 + v_of(t) * kv) for t in ts] + [(X(20), V0)]
    d = " ".join(("M" if i == 0 else "L") + f"{f.P(p)[0]:.1f},{f.P(p)[1]:.1f}" for i, p in enumerate(pts)) + " Z"
    f.add(f'<path class="area" d="{d}"/>')
    f.path_world([(X(0), A0 + 2 * ka), (X(5), A0 + 2 * ka), (X(5), A0), (X(15), A0), (X(15), A0 - 2 * ka), (X(20), A0 - 2 * ka)], "curve")
    f.text((X(20), S0 + 150 * ks), "150", "muted", dx=8, anchor="start")
    f.text((X(5), S0 + 25 * ks), "25", "muted", dx=-6, dy=-8, anchor="end")
    f.text((X(15), S0 + 125 * ks), "125", "muted", dx=-6, dy=-8, anchor="end")
    f.text((X(10), V0 + 10 * kv), "10", "muted", dy=-9)
    f.text((X(2.5), A0 + 2 * ka), "+2", "muted", dy=-9)
    f.text((X(17.5), A0 - 2 * ka), "−2", "muted", dy=10)
    f.text((X(10), V0 + 4.2 * kv), "area = 150 m", "t")
    f.text((X(13), S0 + 30 * ks), "slope of s–t = v", "abs", anchor="start")
    f.text((X(2.6), V0 + 7.5 * kv), "slope = a", "n", dx=-10, dy=-6, anchor="end")
    return f.svg()


@reg("nt_path")
def nt_path():
    f = Fig(150, "Normal and tangential components on a curved path")
    xs = np.linspace(-1.0, 1.08, 60)
    f.path_world([(x, 0.9 * x * x) for x in xs], "curve")
    x0 = 0.5
    P = V(x0, 0.9 * x0 * x0)
    yp, ypp = 1.8 * x0, 1.8
    et = unit(V(1, yp))
    en = unit(V(-yp, 1))
    rho = (1 + yp * yp) ** 1.5 / ypp
    Cc = P + rho * en
    f.line(tup(P), tup(Cc), "cons")
    f.dot(tup(Cc), label="centre of curvature", ldx=-8, ldy=-12, anchor="end", lcls="muted")
    f.text(tup(P + 0.62 * rho * en), "ρ", "muted", dx=-12)
    f.arrow(tup(P), tup(P + 0.62 * et), "abs", "v", side="r", off=12, lpos=0.9)
    an = 0.42 * en
    at = 0.28 * et
    f.arrow(tup(P), tup(P + an), "n", "a_{n} = v²/ρ", side="l", off=12, lpos=0.62, ldx=-38, ldy=4)
    f.arrow(tup(P + an), tup(P + an + at), "t", "a_{t} = dv/dt", side="l", off=11, ldx=6, ldy=-6)
    f.arrow(tup(P), tup(P + an + at), "ans", "a", side="r", off=10, lpos=0.6)
    f.dot(tup(P), label="P", ldx=10, ldy=12, anchor="start")
    f.text((-0.95, 0.9 * 0.95 * 0.95), "path", "muted", dx=-14, anchor="end")
    return f.svg()


@reg("polar")
def polar():
    f = Fig(150, "Polar coordinates r and theta with unit vectors e_r and e_theta")
    O = V(0, 0)
    th = math.radians(35)
    r = 1.25
    P = r * V(math.cos(th), math.sin(th))
    f.line((0, 0), (1.7, 0), "axis")
    phis = np.linspace(0.12, 1.25, 50)
    f.path_world([tup((r + 0.45 * (p - th)) * V(math.cos(p), math.sin(p))) for p in phis], "curve", dash="5 5")
    f.line((0, 0), tup(P), "ink")
    f.text(tup(0.5 * P), "r", "ink", dx=-6, dy=-12)
    f.arc((0, 0), 34, 0, 35, "muted", "θ", lr=48)
    er = unit(P)
    eth = V(-er[1], er[0])
    f.arrow(tup(P), tup(P + 0.42 * er), "abs", "e_{r}", side="r", off=12, lpos=0.85)
    f.arrow(tup(P), tup(P + 0.42 * eth), "t", "e_{θ}", side="l", off=12, lpos=0.85)
    right_angle(f, tup(P), er, eth)
    f.dot((0, 0), label="O", ldx=-10, ldy=10, anchor="end")
    f.dot(tup(P), label="P", ldx=10, ldy=12, anchor="start")
    f.text(tup(1.55 * V(math.cos(1.2), math.sin(1.2))), "path", "muted")
    return f.svg()


# ------------------------------------------------------------------ particles
@reg("cars_map")
def cars_map():
    f = Fig(80, "Car A heading east at 20 m/s, car B heading north at 15 m/s")
    f.line((-2.2, 0.18), (1.0, 0.18), "road")
    f.line((-2.2, -0.18), (-0.18, -0.18), "road")
    f.line((0.18, -0.18), (1.0, -0.18), "road")
    f.line((-0.18, -1.8), (-0.18, -0.18), "road")
    f.line((0.18, -1.8), (0.18, -0.18), "road")
    f.line((-0.18, 0.18), (-0.18, 0.7), "road")
    f.line((0.18, 0.18), (0.18, 0.7), "road")
    f.dot((-1.6, 0), r=6, cls="car", label="A", ldx=-12, ldy=0, anchor="end")
    f.arrow((-1.6, 0), (-0.75, 0), "abs", "20 m/s", at=("N", 24), lpos=0.6)
    f.dot((0, -1.4), r=6, cls="car", label="B", ldx=0, ldy=16, anchor="middle")
    f.arrow((0, -1.4), (0, -0.7), "abs", "15 m/s", at=("E", 24))
    f.arrow((0.75, 0.45), (0.75, 0.75), "muted", None)
    f.text((0.75, 0.75), "N", "muted", dy=-9)
    return f.svg()


@reg("cars_tri")
def cars_tri():
    f = Fig(9, "Velocity triangle v_B = v_A + v_B/A")
    o, a, b = V(0, 0), V(20, 0), V(0, 15)
    f.dot(tup(o), label="o", ldx=-8, ldy=8, anchor="end", step=1)
    f.arrow(tup(o), tup(a), "abs", "v_{A} = 20", side="r", off=13, step=1)
    f.arrow(tup(o), tup(b), "abs", "v_{B} = 15", side="l", off=14, ldx=-16, step=2)
    f.arrow(tup(a), tup(b), "ans", "v_{B/A} = 25 m/s", side="r", off=14, ldx=26, ldy=-8, step=3)
    f.arc(tup(a), 30, 143.13, 180, "ans", "36.9°", lr=46, step=3)
    right_angle(f, (0, 0), (1, 0), (0, 1), step=2)
    f.set_scalebar(5, "5 m/s")
    return f.svg()


@reg("cars_acc")
def cars_acc():
    f = Fig(42, "Acceleration triangle a_B = a_A + a_B/A")
    o = V(0, 0)
    aA = V(2, 0)
    aBn = V(-2.25, 0)
    aBt = V(0, -1)
    aB = aBn + aBt
    f.ppu = 70
    f.dot(tup(o), label="o", ldx=0, ldy=-12, anchor="middle", step=1)
    f.arrow(tup(o), tup(aA), "abs", "a_{A} = 2", at=("N", 10), step=1)
    f.arrow(tup(o), tup(aBn), "n", "(a_{B})_{n} = 2.25", at=("N", 10), step=2)
    f.arrow(tup(aBn), tup(aB), "abs", "(a_{B})_{t} = 1", at=("W", 8), step=2)
    f.arrow(tup(aA), tup(aB), "ans", "a_{B/A} = 4.37 m/s²", at=("S", 14), lpos=0.4, step=3)
    f.set_scalebar(1, "1 m/s²")
    return f.svg()


@reg("pulley_line")
def pulley_line():
    f = Fig(130, "Pulley velocity line: fixed side zero, pulled side v, centre v/2")
    R = 0.5
    f.circle((0, 0), R, "outline")
    f.line((-0.75, 0), (0.75, 0), "muted", dash="3 4")
    f.line((-R, 0), (-R, 1.15), "rope")
    f.line((R, 0), (R, 1.15), "rope")
    x1, y1 = f.P((-R - 0.2, 1.15))
    x2, y2 = f.P((-R + 0.2, 1.15))
    f.hatch(x2, y2, x1, y1, side=1)
    f.line((0, 0), (0, -0.85), "rope")
    f.add(f'<rect class="block" x="{-0.22 * 130:.1f}" y="{0.85 * 130:.1f}" width="{0.44 * 130:.1f}" height="{0.3 * 130:.1f}" rx="3"/>')
    f.bb(0, 1.15 * 130, 30, 0)
    f.text((0, -1.0), "load", "muted")
    f.pin((0, 0))
    v = 0.6
    f.arrow((R, 0), (R, v), "abs", "v", side="r", off=12, lpos=0.6)
    f.line((-R, 0), (R + 0.12, v * (2 * R + 0.12) / (2 * R)), "cons")
    f.arrow((0, 0), (0, v / 2), "ans", "v/2", side="l", off=14, lpos=0.75)
    f.dot((-R, 0), label="rope fixed: v = 0", ldx=-10, ldy=14, anchor="end", lcls="muted")
    f.text((R, v), "pulled up at v", "muted", dx=14, dy=-4, anchor="start")
    return f.svg()


# ------------------------------------------------------------------ rigid bodies
@reg("rot_point")
def rot_point():
    f = Fig(120, "Point P on a body rotating about fixed axis O")
    f.circle((0, 0), 1.0, "outline")
    th = math.radians(40)
    P = 0.8 * V(math.cos(th), math.sin(th))
    f.line((0, 0), tup(P), "ink")
    f.text(tup(0.3 * P), "r", dx=8, dy=10)
    er = unit(P)
    eth = V(-er[1], er[0])
    f.arrow(tup(P), tup(P + 0.62 * eth), "abs", "v = ωr", at=("W", 8), lpos=0.85)
    f.arrow(tup(P), tup(P - 0.42 * er), "n", "a_{n} = ω²r (toward O)", at=("NW", 10), lpos=0.75)
    f.arrow(tup(P), tup(P - 0.34 * eth), "t", "a_{t} = αr", at=("E", 8), lpos=0.9)
    f.pivot((0, 0))
    f.arc((0, 0), 34, 200, 330, "ink", "ω", lr=48, arrow=True, la=265)
    f.dot(tup(P), label="P", ldx=10, ldy=-10)
    f.text((0, 0), "O", dx=-14, dy=-8)
    return f.svg()


@reg("ic_ladder")
def ic_ladder():
    L = mech.ladder()
    f = Fig(165, "Instantaneous centre of the sliding bar")
    A, B = tup(L["A"]), tup(L["B"])
    IC = (A[0], B[1])
    wall = B[0]
    x1, y1 = f.P((wall, 0))
    x2, y2 = f.P((wall, 1.1))
    f.hatch(x2, y2, x1, y1, side=1)
    x1, y1 = f.P((wall, 0))
    x2, y2 = f.P((0.55, 0))
    f.hatch(x1, y1, x2, y2, side=1)
    f.line(A, (A[0], 1.05), "cons")
    f.line(B, (0.45, B[1]), "cons")
    f.link(A, B)
    f.pin(A)
    f.pin(B)
    f.arrow(A, (A[0] + 0.45, 0), "abs", "v_{A} = 3 m/s", side="r", off=14, ldx=10)
    f.arrow(B, (B[0], B[1] - 0.48), "ans", "v_{B}", side="l", off=-14)
    right_angle(f, IC, (0, -1), (-1, 0))
    f.dot(IC, r=4.5, cls="dotans", label="IC", ldx=10, ldy=-10)
    f.text(((A[0] + IC[0]) / 2, (A[1] + IC[1]) / 2), "0.75 m", "muted", dx=10, anchor="start")
    f.text(((B[0] + IC[0]) / 2, IC[1]), "1.30 m", "muted", dy=-11)
    f.text(A, "A", dx=-4, dy=16)
    f.text(B, "B", dx=-14, dy=10)
    return f.svg()


@reg("rel_concept")
def rel_concept():
    f = Fig(150, "Seen from A, point B can only move on a circle, so v_B/A is perpendicular to AB")
    A = V(0, 0)
    B = V(1.3, 0.65)
    r = mech.mag(B)
    phis = np.linspace(math.radians(-8), math.radians(72), 50)
    f.path_world([tup(r * V(math.cos(p), math.sin(p))) for p in phis], "cons")
    f.link(tup(A), tup(B))
    f.pin(tup(A))
    f.pin(tup(B))
    d = unit(V(-B[1], B[0]))
    f.arrow(tup(B), tup(B + 0.55 * d), "t", "v_{B/A} = ωr", at=("W", 10), lpos=0.75)
    right_angle(f, tup(B), unit(-B), d)
    f.arc(tup(A), 30, 200, 320, "ink", "ω", lr=44, arrow=True, la=260)
    f.text(tup(A), "A", dx=-14, dy=8)
    f.text(tup(B), "B", dx=14, dy=8)
    f.text(tup(0.5 * B), "r", "ink", dx=6, dy=14)
    f.text(tup(r * V(math.cos(1.2), math.sin(1.2))), "circle of radius r about A", "muted", dx=-10, anchor="end")
    return f.svg()


@reg("acc_concept")
def acc_concept():
    f = Fig(150, "Relative acceleration components: normal toward A, tangential perpendicular to AB")
    A = V(0, 0)
    B = V(1.3, 0.65)
    r = mech.mag(B)
    phis = np.linspace(math.radians(-8), math.radians(72), 50)
    f.path_world([tup(r * V(math.cos(p), math.sin(p))) for p in phis], "cons")
    f.link(tup(A), tup(B))
    f.pin(tup(A))
    f.pin(tup(B))
    d = unit(V(-B[1], B[0]))
    f.arrow(tup(B), tup(B - 0.55 * unit(B)), "n", "(a_{B/A})_{n} = ω²r", at=("S", 16), lpos=0.55)
    f.arrow(tup(B), tup(B + 0.5 * d), "t", "(a_{B/A})_{t} = αr", at=("W", 10), lpos=0.75)
    right_angle(f, tup(B), unit(-B), d)
    f.arc(tup(A), 30, 200, 320, "ink", "ω, α", lr=46, arrow=True, la=260)
    f.text(tup(A), "A", dx=-14, dy=8)
    f.text(tup(B), "B", dx=14, dy=8)
    return f.svg()


# ------------------------------------------------------------------ ladder
@reg("ladder_mech")
def ladder_mech():
    L = mech.ladder()
    f = Fig(165, "Bar AB sliding: A on the floor at 3 m/s, B on the wall")
    A, B = tup(L["A"]), tup(L["B"])
    wall = B[0]
    x1, y1 = f.P((wall, 0))
    x2, y2 = f.P((wall, 1.05))
    f.hatch(x2, y2, x1, y1, side=1)
    x2, y2 = f.P((0.6, 0))
    f.hatch(x1, y1, x2, y2, side=1)
    f.link(A, B)
    f.pin(A)
    f.pin(B)
    f.arrow(A, (0.48, 0), "abs", "v_{A} = 3 m/s", side="l", off=14)
    f.arrow(B, (B[0], B[1] - 0.42), "ans", "v_{B} = ?", at=("E", 10), lpos=0.7)
    f.arc(A, 40, 150, 180, "muted", "30°", lr=56)
    f.dim(B, A, "1.5 m", off=16, side="l")
    f.text(A, "A", dx=2, dy=17)
    f.text(B, "B", dx=-14, dy=-8)
    return f.svg()


@reg("ladder_vpoly")
def ladder_vpoly():
    L = mech.ladder()
    f = Fig(38, "Velocity polygon for the sliding bar")
    o = V(0, 0)
    a = L["vA"]
    b = L["vB"]
    d = unit(L["vBA"])
    f.dot(tup(o), label="o", ldx=-10, ldy=-8, anchor="end", step=1)
    f.arrow(tup(o), tup(a), "abs", "v_{A} = 3", at=("N", 10), step=1)
    through(f, a, d, b, 1.2, step=2)
    through(f, o, V(0, 1), b, 1.2, step=3)
    f.arrow(tup(o), tup(b), "ans", "v_{B} = 5.20", at=("W", 10), step=4)
    f.arrow(tup(a), tup(b), "t", "v_{B/A} = 6.00", at=("E", 10), step=4)
    right_angle(f, tup(o), (1, 0), (0, -1), step=4)
    f.arc(tup(b), 34, 60, 90, "muted", "30°", lr=50, step=4)
    f.set_scalebar(1, "1 m/s")
    return f.svg()


@reg("ladder_apoly")
def ladder_apoly():
    L = mech.ladder()
    f = Fig(4.6, "Acceleration polygon for the sliding bar with a_A = 0")
    o = V(0, 0)
    n = L["aBAn"]
    b = L["aB"]
    d = unit(L["aBAt"])
    f.dot(tup(o), label="o  (a_{A} = 0)", ldx=10, ldy=-10, step=1)
    f.arrow(tup(o), tup(n), "n", "(a_{B/A})_{n} = 24", at=("NE", 8), step=2)
    through(f, n, d, b, 9, step=3)
    through(f, o, V(0, 1), b, 9, step=4)
    f.arrow(tup(o), tup(b), "ans", "a_{B} = 48.0", at=("W", 10), step=5)
    f.arrow(tup(n), tup(b), "t", "(a_{B/A})_{t} = 41.6", at=("E", 10), step=5)
    f.set_scalebar(10, "10 m/s²")
    return f.svg()


# ------------------------------------------------------------------ slider crank
@reg("sc_mech")
def sc_mech():
    S = mech.slider_crank()
    f = Fig(700, "Slider-crank: crank OB 125 mm, rod AB 350 mm, theta = 60 degrees")
    O, A, B = tup(S["O"]), tup(S["A"]), tup(S["B"])
    f.line((A[0] - 0.06, 0), (0.06, 0), "muted", dash="4 4")
    f.slider(A, 0, w=36, h=22, guide=38)
    f.link(A, B)
    f.link(O, B, w=8)
    f.pivot(O)
    f.pin(B)
    f.pin(A)
    f.arc(O, 30, 120, 180, "muted", "θ = 60°", lr=56, ldy=-4)
    f.arc(A, 46, 0, S["beta"], "muted", "β", lr=58, ldy=-6)
    f.arc(O, 18, 60, -40, "abs", "ω", lr=30, arrow=True, ccw=False, la=10, ldx=8)
    f.text(A, "A", dx=0, dy=24)
    f.text(B, "B", dx=0, dy=-14)
    f.text(O, "O", dx=14, dy=6)
    f.text(tup((V(*O) + V(*B)) / 2), "125 mm", "muted", dx=34, dy=0)
    f.text(tup((V(*A) + V(*B)) / 2), "350 mm", "muted", dx=-10, dy=-14)
    f.arrow(B, tup(V(*B) + 0.07 * unit(S["vB"])), "abs", "v_{B}", side="l", off=10, lpos=1.0, ldy=-4)
    return f.svg()


@reg("sc_vpoly")
def sc_vpoly():
    S = mech.slider_crank()
    f = Fig(11, "Velocity polygon for the slider-crank")
    o = V(0, 0)
    b, a = S["vB"], S["vA"]
    d = unit(S["vAB"])
    f.dot(tup(o), label="o", ldx=-10, ldy=6, anchor="end", step=1)
    f.arrow(tup(o), tup(b), "abs", "v_{B} = 19.6", at=("NW", 8), step=1)
    through(f, b, d, a, 4, step=2)
    through(f, o, V(1, 0), a, 4, step=3)
    f.arrow(tup(o), tup(a), "ans", "v_{A} = 20.2", at=("S", 12), step=4)
    f.arrow(tup(b), tup(a), "t", "v_{A/B} = 10.3", at=("E", 10), step=4)
    f.arc(tup(o), 40, 0, 30, "muted", "30°", lr=56, step=4)
    f.set_scalebar(5, "5 m/s")
    return f.svg()


@reg("sc_apoly")
def sc_apoly():
    S = mech.slider_crank()
    f = Fig(0.072, "Acceleration polygon for the slider-crank")
    o = V(0, 0)
    aB = S["aB"]
    n = aB + S["aABn"]
    a = S["aA"]
    d = unit(S["aABt"])
    f.dot(tup(o), label="o", ldx=-10, ldy=-6, anchor="end", step=1)
    f.arrow(tup(o), tup(aB), "abs", "a_{B} = 3084", at=("W", 10), step=1)
    f.arrow(tup(aB), tup(n), "n", "(a_{A/B})_{n} = 305", at=("E", 12), lpos=1.0, ldy=6, step=2)
    through(f, n, d, a, 400, step=3)
    through(f, o, V(1, 0), a, 400, step=4)
    f.arrow(tup(o), tup(a), "ans", "a_{A} = 994", at=("N", 12), step=5)
    f.arrow(tup(n), tup(a), "t", "(a_{A/B})_{t} = 2710", at=("E", 10), step=5)
    f.set_scalebar(500, "500 m/s²")
    return f.svg()


# ------------------------------------------------------------------ 2016 exam
@reg("x16_mech")
def x16_mech():
    X = mech.exam2016()
    f = Fig(420, "2016 exam mechanism: bars AB, BD, DE")
    A, B, D, E = (tup(X[k]) for k in "ABDE")
    f.link(A, B, w=8)
    f.link(B, D)
    f.link(D, E, w=8)
    f.pivot(A, down=False)
    f.pivot(E)
    f.pin(B)
    f.pin(D)
    f.arc(A, 20, 300, 200, "abs", "10 rad/s", lr=38, arrow=True, ccw=False, la=180, ldx=-30)
    f.text(A, "A", dx=16, dy=0, anchor="start")
    f.text(B, "B", dx=12, dy=4, anchor="start")
    f.text(D, "D", dx=-12, dy=-8)
    f.text(E, "E", dx=14, dy=-10)
    f.dim((0.6, 0.45), (0.6, 0.25), "0.2 m", off=30, side="l")
    f.dim((0.6, 0.25), (0.6, 0.0), "0.25 m", off=30, side="l")
    f.dim((0, 0), (0.2, 0), "0.2 m", off=34, side="r")
    f.dim((0, 0), (0.6, 0), "0.6 m", off=58, side="r")
    return f.svg()


@reg("x16_vpoly")
def x16_vpoly():
    X = mech.exam2016()
    f = Fig(40, "2016 exam velocity polygon")
    o = V(0, 0)
    b, d_ = X["vB"], X["vD"]
    dirDB = unit(-X["vBD"])
    f.dot(tup(o), label="o", ldx=10, ldy=-8, step=1)
    f.arrow(tup(o), tup(b), "abs", "v_{B} = 2.0", at=("N", 10), step=1)
    through(f, b, dirDB, d_, 0.9, step=2)
    through(f, o, V(0, 1), d_, 0.9, step=3)
    f.arrow(tup(o), tup(d_), "ans", "v_{D} = 4.8", at=("E", 10), step=4)
    f.arrow(tup(b), tup(d_), "t", "v_{D/B} = 5.2", at=("W", 10), step=4)
    f.arc(tup(d_), 40, 90, 112.6, "muted", "22.6°", lr=58, step=4)
    f.set_scalebar(1, "1 m/s")
    return f.svg()


@reg("x16_apoly")
def x16_apoly():
    X = mech.exam2016()
    f = Fig(1.15, "2016 exam acceleration polygon")
    o = V(0, 0)
    aDn = X["aDn"]
    aB = X["aB"]
    aDBn = -X["aBDn"]  # (a_D/B)n = -(a_B/D)n
    p2 = aB + aDBn
    Xp = aDn + X["aDt"]
    dt = unit(-X["aBDt"])
    f.dot(tup(o), label="o", ldx=-8, ldy=12, anchor="end", step=1)
    f.arrow(tup(o), tup(aDn), "n", "(a_{D})_{n} = 115.2", at=("S", 12), lpos=0.62, step=1)
    through(f, aDn, V(0, 1), Xp, 25, step=2)
    f.arrow(tup(o), tup(aB), "abs", "a_{B} = 20", at=("W", 8), step=3)
    f.arrow(tup(aB), tup(p2), "n", "(a_{D/B})_{n} = 41.6", at=("NW", 8), lpos=0.4, step=4)
    through(f, p2, dt, Xp, 25, step=5)
    f.arrow(tup(aDn), tup(Xp), "t", "(a_{D})_{t} = 148", at=("E", 10), step=6)
    f.arrow(tup(p2), tup(Xp), "t", "(a_{D/B})_{t} = 200", at=("W", 10), lpos=0.6, step=6)
    f.set_scalebar(20, "20 m/s²")
    return f.svg()


# ------------------------------------------------------------------ 2022 exam
@reg("x22_mech")
def x22_mech():
    Z = mech.exam2022()
    f = Fig(1800, "2022 exam mechanism: bar AB pivoted at A, bar BC, slider C on a 3-4-5 slope")
    A, B, C = tup(Z["A"]), tup(Z["B"]), tup(Z["C"])
    f.slider(C, 36.87, w=30, h=16, guide=46)
    f.link(B, C)
    f.link(A, B, w=8)
    f.pivot(A)
    f.pin(B)
    f.arc(A, 22, 200, 340, "abs", "ω = 3, α = 2", lr=0, arrow=True, ccw=True, la=270, ldy=34, ldx=34)
    f.text(A, "A", dx=14, dy=-4, anchor="start")
    f.text(B, "B", dx=12, dy=-6, anchor="start")
    f.text(C, "C", dx=-16, dy=-10)
    f.dim((0, 0.07), (0, 0), "70 mm", off=40, side="r")
    f.dim((0, 0), (0, -0.05), "50 mm", off=40, side="r")
    f.dim((-0.05, -0.05), (0, -0.05), "50 mm", off=30, side="r")
    # 3-4-5 slope triangle
    t0 = V(-0.085, -0.088)
    f.path_world([tup(t0), tup(t0 + V(0.016, 0)), tup(t0 + V(0.016, 0.012)), tup(t0)], "muted")
    f.text(tup(t0 + V(0.008, 0)), "4", "muted", dy=8, size=10)
    f.text(tup(t0 + V(0.016, 0.006)), "3", "muted", dx=7, size=10)
    return f.svg()


@reg("x22_vpoly")
def x22_vpoly():
    Z = mech.exam2022()
    f = Fig(1250, "2022 exam velocity polygon")
    o = V(0, 0)
    b, c = Z["vB"], Z["vC"]
    dCB = unit(-Z["vBC"])
    s = unit(V(4, 3))
    f.dot(tup(o), label="o", ldx=10, ldy=-8, step=1)
    f.arrow(tup(o), tup(b), "abs", "v_{B} = 0.21", at=("N", 10), step=1)
    through(f, b, dCB, c, 0.03, step=2)
    through(f, o, s, c, 0.04, step=3)
    f.arrow(tup(o), tup(c), "ans", "v_{C} = 0.094", at=("SE", 8), lpos=0.45, step=4)
    f.arrow(tup(b), tup(c), "t", "v_{C/B} = 0.146", at=("SW", 8), lpos=0.55, step=4)
    f.set_scalebar(0.05, "0.05 m/s")
    return f.svg()


@reg("x22_apoly")
def x22_apoly():
    Z = mech.exam2022()
    f = Fig(420, "2022 exam acceleration polygon")
    o = V(0, 0)
    p1 = Z["aBn"]
    p2 = p1 + Z["aBt"]
    p3 = p2 - Z["aBCn"]  # (a_C/B)n
    c = Z["aC"]
    dt = unit(-Z["aBCt"])
    s = unit(V(4, 3))
    f.dot(tup(o), label="o", ldx=10, ldy=-8, step=1)
    f.arrow(tup(o), tup(p1), "n", "(a_{B})_{n} = 0.63", at=("E", 10), step=1)
    f.arrow(tup(p1), tup(p2), "abs", "(a_{B})_{t} = 0.14", at=("S", 12), step=2)
    f.arrow(tup(p2), tup(p3), "n", "(a_{C/B})_{n} = 0.165", at=("E", 8), lpos=0.55, step=3)
    through(f, p3, dt, c, 0.08, step=4)
    through(f, o, s, c, 0.08, step=5)
    f.arrow(tup(o), tup(c), "ans", "a_{C} = 0.547", at=("NW", 8), step=6)
    f.arrow(tup(p3), tup(c), "t", "(a_{C/B})_{t} = 0.39", at=("SW", 8), lpos=0.6, step=6)
    f.set_scalebar(0.1, "0.1 m/s²")
    return f.svg()


# ------------------------------------------------------------------ 2021 exam
@reg("x21_mech")
def x21_mech():
    Y = mech.exam2021()
    f = Fig(600, "2021 exam mechanism: arms AB and CD, bar BDE")
    A, B, C, D, E = (tup(Y[k]) for k in "ABCDE")
    f.link(A, B, w=8)
    f.link(C, D, w=8)
    f.link(B, E)
    f.pivot(A)
    f.pivot(C)
    f.pin(B)
    f.pin(D)
    f.pin(E)
    f.arc(A, 20, 160, 20, "abs", "6 rad/s", lr=34, arrow=True, ccw=False, la=200, ldx=-28)
    for k, dx, dy in (("A", -16, -2), ("B", -14, -6), ("C", -16, -2), ("D", 4, 16), ("E", 12, -8)):
        f.text(tup(Y[k]), k, dx=dx, dy=dy)
    f.dim((0, 0), (0.225, 0), "225 mm", off=30, side="r")
    f.dim((0.225, 0), (0.45, 0), "225 mm", off=30, side="r")
    f.dim((0.45, 0.27), (0.45, 0.18), "90", off=26, side="l")
    f.dim((0.45, 0.18), (0.45, 0.09), "90", off=26, side="l")
    f.dim((0.45, 0.09), (0.45, 0.0), "90", off=26, side="l")
    return f.svg()


@reg("x21_vpoly")
def x21_vpoly():
    Y = mech.exam2021()
    f = Fig(330, "2021 exam velocity polygon: the two direction lines meet at the tip of v_B")
    o = V(0, 0)
    b = Y["vB"]
    rDB = Y["D"] - Y["B"]
    d = unit(V(-rDB[1], rDB[0]))
    f.dot(tup(o), label="o", ldx=-8, ldy=-8, anchor="end", step=1)
    f.arrow(tup(o), tup(b), "abs", "v_{B} = 0.54", side="r", off=14, step=1)
    through(f, b, d, b, 0.2, step=2)
    through(f, o, V(1, 0), b, 0.12, step=3)
    f.dot(tup(b), r=4.5, cls="dotans", label="d lands on b", ldx=12, ldy=-14, step=4, lcls="ans")
    f.set_scalebar(0.1, "0.1 m/s")
    return f.svg()


@reg("x21_apoly")
def x21_apoly():
    Y = mech.exam2021()
    f = Fig(62, "2021 exam acceleration polygon")
    o = V(0, 0)
    aB = Y["aB"]
    aDn = Y["aDn"]
    Xp = aDn + Y["aDt"]
    dt = unit(Y["aDBt"])
    f.dot(tup(o), label="o", ldx=10, ldy=-8, step=1)
    f.arrow(tup(o), tup(aB), "n", "(a_{B})_{n} = 3.24", at=("E", 10), step=1, lpos=0.8)
    through(f, aB, dt, Xp, 0.5, step=2)
    f.arrow(tup(o), tup(aDn), "abs", "(a_{D})_{n} = 1.62", at=("W", 10), step=3, w=3.6, lpos=0.4)
    through(f, aDn, V(1, 0), Xp, 0.4, step=4)
    f.arrow(tup(aDn), tup(Xp), "t", "(a_{D})_{t} = 0.648", at=("NW", 6), lpos=1.0, step=5)
    f.arrow(tup(aB), tup(Xp), "t", "(a_{D/B})_{t} = 1.75", at=("W", 10), step=5)
    f.set_scalebar(0.5, "0.5 m/s²")
    return f.svg()


# ------------------------------------------------------------------ rolling gear
@reg("gear_mech")
def gear_mech():
    f = Fig(300, "Gear of radius 0.3 m rolling on a fixed rack")
    O = (0, 0.3)
    x1, y1 = f.P((-0.45, 0))
    x2, y2 = f.P((0.45, 0))
    f.hatch(x1, y1, x2, y2, side=1)
    f.circle(O, 0.3, "outline")
    f.circle(O, 0.27, "outline thin", dash="2 3")
    f.pin(O)
    f.dot((0, 0.6), label="A", ldx=0, ldy=-14, anchor="middle")
    f.dot((0, 0), label="C (contact)", ldx=8, ldy=18, anchor="start")
    f.arc(O, 28, 150, 30, "abs", "ω = 12 rad/s, α = 6 rad/s²", lr=0, arrow=True, ccw=False, la=90, ldy=-40, ldx=130)
    f.arrow(O, (0.18, 0.3), "abs", "a_{O} = αr", side="r", off=12, lpos=0.9, ldx=12)
    f.text((0, 0.45), "0.3 m", "muted", dx=-24)
    f.line(O, (0, 0.6), "muted", dash="3 3")
    return f.svg()


@reg("gear_apoly")
def gear_apoly():
    G = mech.rolling_gear()
    f = Fig(5.0, "Acceleration polygon for point A on the rolling gear")
    o = V(0, 0)
    p1 = G["aO"]
    p2 = p1 + G["aAOt"]
    p3 = p2 + G["aAOn"]
    f.dot(tup(o), label="o", ldx=0, ldy=-30, anchor="middle", step=1)
    f.arrow(tup(o), tup(p1), "abs", "a_{O} = 1.8", at=("W", 10), lpos=0.0, ldy=-14, step=1)
    f.arrow(tup(p1), tup(p2), "t", "(a_{A/O})_{t} = 1.8", at=("E", 10), lpos=1.0, ldy=-14, step=2)
    f.arrow(tup(p2), tup(p3), "n", "(a_{A/O})_{n} = 43.2", at=("E", 10), step=3)
    f.arrow(tup(o), tup(p3), "ans", "a_{A} = 43.3", at=("W", 10), step=4)
    f.set_scalebar(10, "10 m/s²")
    return f.svg()


def build_all():
    return {k: fn() for k, fn in FIGS.items()}


if __name__ == "__main__":
    out = build_all()
    for k, v in out.items():
        print(k, len(v))
