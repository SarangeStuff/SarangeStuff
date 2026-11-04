"""Part II figures: free-body diagrams (FBD) and kinetic diagrams (KD).

Colour roles in Part II: abs = known forces (weight, given loads); ans = unknown
forces (reactions, tension, normal, friction); n = m*a terms; t = I*alpha terms.
Registered into figs.FIGS so build.py picks them up.
"""
import math

import numpy as np

from figs import reg, tup, right_angle
from svgkit import Fig

V = lambda x, y: np.array([float(x), float(y)])


def U(deg):
    return V(math.cos(math.radians(deg)), math.sin(math.radians(deg)))


def block(f, c, w, h, ang, cls="block"):
    s, n = U(ang), U(ang + 90)
    pts = [c + s * w / 2 + n * h / 2, c - s * w / 2 + n * h / 2, c - s * w / 2 - n * h / 2, c + s * w / 2 - n * h / 2]
    px = [f.P(p) for p in pts]
    for x, y in px:
        f.bb(x, y)
    f.add(f'<polygon class="{cls}" points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in px) + '"/>')


def disc(f, c, r, cls="body"):
    x, y = f.P(c)
    R = r * f.ppu
    f.bb(x, y, R, R)
    f.add(f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="{R:.1f}"/>')


def moment(f, c, rpx, ccw, cls, label, la=90):
    a1, a2 = (210, 330) if not ccw else (330, 210)
    if ccw:
        f.arc(tup(c), rpx, -30, 210, cls, label, lr=rpx + 14, arrow=True, ccw=True, la=la)
    else:
        f.arc(tup(c), rpx, 210, -30, cls, label, lr=rpx + 14, arrow=True, ccw=False, la=la)


def ghost_line(f, p, q):
    f.line(tup(p), tup(q), "muted", dash="4 5")


# ------------------------------------------------------------- crate on incline
def _crate(kd):
    f = Fig(150, "Crate on a 30 degree incline: " + ("kinetic diagram" if kd else "free-body diagram"))
    s, n = U(30), U(120)
    P0 = V(0, 0)
    w, h = 0.6, 0.4
    c = P0 + n * h / 2
    ghost_line(f, P0 - s * 0.75, P0 + s * 0.75)
    block(f, c, w, h, 30)
    if kd:
        f.arrow(tup(c), tup(c + s * 0.55), "n", "m a", at=("NW", 8), lpos=0.9)
    else:
        f.arrow(tup(c), tup(c + V(0, -0.6)), "abs", "W = mg", at=("S", 12), lpos=1.0)
        f.arrow(tup(P0 - n * 0.5), tup(P0), "ans", "N", at=("E", 8), lpos=0.25)
        f.arrow(tup(P0 + s * 0.05), tup(P0 - s * 0.45), "ans", "F_{f}", at=("NW", 6), lpos=0.95)
        tip = c + s * w / 2
        f.arrow(tup(tip), tup(tip + s * 0.55), "ans", "T", at=("NW", 8), lpos=0.8)
        f.arc(tup(P0 - s * 0.75), 40, 0, 30, "muted", "30°", lr=54)
        f.line(tup(P0 - s * 0.75), tup(P0 - s * 0.75 + V(0.35, 0)), "muted", dash="3 3")
    return f.svg()


reg("k_crate_fbd")(lambda: _crate(False))
reg("k_crate_kd")(lambda: _crate(True))


# ------------------------------------------------------------- banked track
def _bank(kd):
    f = Fig(150, "Car on a banked track seen end-on: " + ("kinetic diagram" if kd else "free-body diagram"))
    th = 25
    s, n = U(th), U(th + 90)
    P0 = V(0, 0)
    c = P0 + n * 0.17
    ghost_line(f, P0 - s * 0.8, P0 + s * 0.8)
    block(f, c, 0.5, 0.34, th)
    if kd:
        f.arrow(tup(c), tup(c + V(-0.6, 0)), "n", "m v²/ρ", at=("S", 12), lpos=0.6)
        f.text(tup(c + V(-0.62, 0)), "to centre of bend", "muted", dx=-8, anchor="end")
    else:
        f.arrow(tup(c), tup(c + V(0, -0.6)), "abs", "W = mg", at=("W", 8), lpos=0.9)
        f.arrow(tup(P0 - n * 0.55), tup(P0), "ans", "N", at=("E", 8), lpos=0.25)
        f.line(tup(P0), tup(P0 + V(0, 0.55)), "muted", dash="3 3")
        f.arc(tup(P0), 46, 90, 90 + th, "muted", "θ", lr=58)
        f.arc(tup(P0 - s * 0.8), 40, 0, th, "muted", "θ", lr=54)
        f.line(tup(P0 - s * 0.8), tup(P0 - s * 0.8 + V(0.4, 0)), "muted", dash="3 3")
    return f.svg()


reg("k_bank_fbd")(lambda: _bank(False))
reg("k_bank_kd")(lambda: _bank(True))


# ------------------------------------------------------------- rotating tube (top view)
def _tube(kd):
    f = Fig(150, "Slider in a rotating tube, top view: " + ("kinetic diagram" if kd else "free-body diagram"))
    O = V(0, 0)
    P = V(1.0, 0)
    f.line((0, 0.07), (1.5, 0.07), "guide")
    f.line((0, -0.07), (1.5, -0.07), "guide")
    f.pin((0, 0))
    f.text((0, 0), "axis O", "muted", dy=-18)
    block(f, P, 0.18, 0.12, 0)
    f.arc((0, 0), 26, 200, 330, "abs", "ω", lr=40, arrow=True, la=265)
    if kd:
        f.arrow(tup(P), tup(P + V(-0.55, 0)), "n", "m a_{r} = m(r̈ − rθ̇²)", at=("S", 22), lpos=0.5)
        f.arrow(tup(P), tup(P + V(0, 0.45)), "n", "m a_{θ} = m(rθ̈ + 2ṙθ̇)", at=("E", 8), lpos=0.9)
    else:
        f.arrow(tup(P), tup(P + V(-0.55, 0)), "ans", "T (string)", at=("S", 22), lpos=0.5)
        f.arrow(tup(P + V(0, -0.5)), tup(P + V(0, -0.07)), "ans", "F_{θ} (tube wall)", at=("E", 8), lpos=0.3)
        f.text(tup(P + V(0.25, 0)), "r →", "muted", anchor="start", dx=4)
    return f.svg()


reg("k_tube_fbd")(lambda: _tube(False))
reg("k_tube_kd")(lambda: _tube(True))


# ------------------------------------------------------------- energy bars (putty)
@reg("k_energy_bars")
def k_energy_bars():
    f = Fig(1, "Energy bookkeeping for the putty and block")
    k = 7.0  # px per joule
    states = [("Just after impact", [("T", 3.92, "abs"), ("V_{g}", 12.94, "n"), ("V_{e}", 6.50, "t")]),
              ("Maximum compression", [("T", 0.0, "abs"), ("V_{g}", 0.0, "n"), ("V_{e}", 23.36, "t")])]
    x0 = 0
    for i, (name, parts) in enumerate(states):
        x = x0 + i * 220
        y = 0
        for lab, val, cls in parts:
            hgt = val * k
            if hgt > 0.5:
                f.add(f'<rect class="bar {cls}" x="{x:.1f}" y="{-(y + hgt):.1f}" width="70" height="{hgt:.1f}"/>')
                f.bb(x, -(y + hgt))
                f.bb(x + 70, -y)
                f.text((x + 80, y + hgt / 2), f"{lab} = {val:.2f} J", cls, anchor="start")
            y += hgt
        f.text((x + 35, -18), name, "muted")
        f.text((x + 35, y + 14), f"total {sum(v for _, v, _ in parts):.1f} J", "ink")
    f.line((-10, 0), (420, 0), "axis")
    return f.svg()


# ------------------------------------------------------------- impulse triangle (tennis)
@reg("k_impulse_tri")
def k_impulse_tri():
    f = Fig(220, "Impulse-momentum triangle for the tennis ball")
    o = V(0, 0)
    mv1 = V(-0.9, 0)
    mv2 = 1.26 * U(15)
    f.dot(tup(o), label="o", ldx=0, ldy=16, anchor="middle")
    f.arrow(tup(o), tup(mv1), "abs", "m v_{1} = 0.90 N·s", at=("S", 14), lpos=0.6)
    f.arrow(tup(mv1), tup(mv2), "ans", "∫R dt ≈ 2.14 N·s", at=("N", 14), lpos=0.4)
    f.arrow(tup(o), tup(mv2), "abs", "m v_{2} = 1.26 N·s", at=("SE", 8), lpos=0.7)
    f.arc(tup(o), 40, 0, 15, "muted", "15°", lr=56)
    f.set_scalebar(0.5, "0.5 N·s")
    return f.svg()


# ------------------------------------------------------------- oblique impact
@reg("k_oblique")
def k_oblique():
    f = Fig(1500, "Oblique impact geometry: line of impact through the two centres")
    dn = V(math.sin(math.radians(55.15)), -math.cos(math.radians(55.15)))
    dt = V(-dn[1], dn[0])
    A = V(0, 0)
    B = A + dn * 0.105
    disc(f, A, 0.075)
    disc(f, B, 0.030)
    f.text(tup(A), "A (20 kg)")
    f.text(tup(B), "B")
    f.line(tup(A - dn * 0.1), tup(B + dn * 0.09), "cons")
    f.text(tup(B + dn * 0.09), "line of impact (n)", "muted", dx=8, dy=6, anchor="start")
    C = A + dn * 0.075
    f.line(tup(C - dt * 0.09), tup(C + dt * 0.09), "muted", dash="2 3")
    f.text(tup(C + dt * 0.09), "contact plane (t)", "muted", dx=8, anchor="start")
    f.arrow(tup(A + V(-0.05, 0.09)), tup(A + V(0.05, 0.09)), "abs", "v_{A} = 4 m/s", at=("N", 10))
    f.arrow(tup(B + V(0.07, -0.05)), tup(B + V(-0.07, -0.05)), "abs", "v_{B} = 15 m/s", at=("S", 12))
    f.line(tup(A), tup(A + V(0, -0.075)), "muted", dash="3 3")
    f.arc(tup(A), 60, -90, -90 + 55.15, "muted", "55.15°", lr=78, la=-62)
    return f.svg()


@reg("k_oblique_comp")
def k_oblique_comp():
    f = Fig(45, "Splitting v_A into components along and across the line of impact")
    dn = V(math.sin(math.radians(55.15)), -math.cos(math.radians(55.15)))
    dt = V(-dn[1], dn[0])
    o = V(0, 0)
    vn = dn * 3.283
    f.dot(tup(o), label="o", ldx=-8, ldy=-8, anchor="end")
    f.arrow(tup(o), (4, 0), "abs", "v_{A} = 4 m/s", at=("N", 10))
    f.arrow(tup(o), tup(vn), "n", "along n: 4 sin 55.15° = 3.28", at=("SW", 8), lpos=0.6)
    f.arrow(tup(vn), (4, 0), "t", "across: 4 cos 55.15° = 2.29", at=("E", 8), lpos=0.5)
    right_angle(f, tup(vn), tuple(-dn), tuple(dt))
    return f.svg()


# ------------------------------------------------------------- rod released from horizontal
def _rod(kd):
    f = Fig(200, "Slender rod pinned at O, released from rest: " + ("kinetic diagram" if kd else "free-body diagram"))
    O, G, E = V(0, 0), V(0.6, 0), V(1.2, 0)
    f.link(tup(O), tup(E), w=11)
    f.pin(tup(O))
    f.dot(tup(G), label="G", ldx=0, ldy=-14, anchor="middle")
    f.text(tup(O), "O", dx=-6, dy=-14)
    if kd:
        f.arrow(tup(G), tup(G + V(0, -0.45)), "n", "m(a_{G})_{t} = m α (L/2)", at=("E", 8), lpos=0.8)
        f.text(tup(G + V(-0.32, 0.0)), "m(a_{G})_{n} = 0", "muted", dy=22)
        moment(f, G, 22, False, "t", "I_{G}α", la=90)
    else:
        f.arrow(tup(G), tup(G + V(0, -0.45)), "abs", "W = mg", at=("E", 8), lpos=0.8)
        f.arrow(tup(O + V(0, -0.4)), tup(O), "ans", "O_{t}", at=("W", 8), lpos=0.4)
        f.arrow(tup(O + V(-0.35, 0)), tup(O), "ans", "O_{n}", at=("S", 12), lpos=0.4)
        f.dim(tup(O), tup(E), "L = 1.2 m", off=70, side="r")
    return f.svg()


reg("k_rod_fbd")(lambda: _rod(False))
reg("k_rod_kd")(lambda: _rod(True))


# ------------------------------------------------------------- rolling cylinder
def _roll(kd):
    f = Fig(220, "Cylinder rolling down a 30 degree ramp: " + ("kinetic diagram" if kd else "free-body diagram"))
    th = 30
    s, n = U(-th), U(90 - th)  # s points down the slope (to the right)
    r = 0.3
    Cpt = V(0, 0)
    G = Cpt + n * r
    ghost_line(f, Cpt - s * 0.6, Cpt + s * 0.6)
    disc(f, G, r)
    f.dot(tup(G), label="G", ldx=-10, ldy=-10, anchor="end")
    if kd:
        f.arrow(tup(G), tup(G + s * 0.5), "n", "m a_{G}", at=("NE", 8), lpos=0.9)
        moment(f, G, 30, False, "t", "I_{G}α", la=110)
    else:
        f.arrow(tup(G), tup(G + V(0, -0.55)), "abs", "W = mg", at=("W", 8), lpos=0.85)
        f.arrow(tup(Cpt - n * 0.4), tup(Cpt), "ans", "N", at=("W", 8), lpos=0.3)
        f.arrow(tup(Cpt + s * 0.02), tup(Cpt - s * 0.4), "ans", "F_{f}", at=("S", 12), lpos=0.75)
    return f.svg()


reg("k_roll_fbd")(lambda: _roll(False))
reg("k_roll_kd")(lambda: _roll(True))


# ------------------------------------------------------------- boom on a bakkie
def _boom(kd):
    f = Fig(70, "Boom pivoted at A on an accelerating bakkie: " + ("kinetic diagram" if kd else "free-body diagram"))
    A = V(0, 0)
    B = A + 4 * U(120)
    C = V(2, 0)
    G = (A + B) / 2
    f.link(tup(A), tup(B), w=9)
    f.pin(tup(A))
    f.dot(tup(G), label="G", ldx=10, ldy=-6)
    f.text(tup(A), "A", dx=12, dy=12)
    f.text(tup(B), "B", dx=-12, dy=-6)
    if kd:
        f.arrow(tup(G), tup(G + V(1.4, 0)), "n", "m a = 300 N", at=("N", 10), lpos=0.6)
        f.text(tup(G + V(0, -0.6)), "(no rotation: no Iα)", "muted", dx=10, anchor="start")
    else:
        f.line(tup(B), tup(C), "muted", dash="3 4")
        f.dot(tup(C), label="C", ldx=8, ldy=10)
        dBC = (C - B) / np.linalg.norm(C - B)
        f.arrow(tup(B), tup(B + dBC * 1.3), "ans", "T", at=("NE", 8), lpos=0.7)
        f.arrow(tup(G), tup(G + V(0, -1.3)), "abs", "W = 589 N", at=("W", 8), lpos=0.8)
        f.arrow(tup(A + V(1.2, 0)), tup(A), "ans", "A_{x}", at=("S", 12), lpos=0.4)
        f.arrow(tup(A + V(0, -1.1)), tup(A), "ans", "A_{y}", at=("E", 8), lpos=0.4)
        f.arc(tup(A), 30, 120, 180, "muted", "60°", lr=44)
        f.line(tup(A), tup(A + V(-1.0, 0)), "muted", dash="3 3")
    return f.svg()


reg("k_boom_fbd")(lambda: _boom(False))
reg("k_boom_kd")(lambda: _boom(True))


# ------------------------------------------------------------- parallel axis
@reg("k_paxis")
def k_paxis():
    f = Fig(120, "Parallel-axis theorem: I about O equals I_G plus m d squared")
    pts = [(-0.9, -0.3), (-0.4, -0.75), (0.5, -0.6), (1.0, 0.0), (0.6, 0.7), (-0.3, 0.75), (-1.0, 0.35)]
    px = [f.P(p) for p in pts]
    for x, y in px:
        f.bb(x, y)
    d = "M" + " ".join(f"{x:.1f},{y:.1f}" for x, y in px) + " Z"
    f.add(f'<path class="body" d="{d}"/>')
    G, O = V(0, 0), V(-0.55, -0.25)
    f.dot(tup(G), r=4.5, label="G (mass centre)", ldx=10, ldy=-10)
    f.dot(tup(O), r=4.5, cls="dotans", label="O (new axis)", ldx=-10, ldy=14, anchor="end", lcls="ans")
    f.line(tup(O), tup(G), "ink")
    f.text(tup((O + G) / 2), "d", dx=-4, dy=-12)
    return f.svg()
