"""Planar kinematics helpers and the worked examples used in the textbook.

Every number quoted in the book's relative-velocity and relative-acceleration
chapters is computed here, so the text and the to-scale diagrams agree.
Run `python3 mech.py` to print a summary of all results.
"""
import math
import numpy as np

V = lambda x, y: np.array([float(x), float(y)])


def perp(w, r):
    """omega (scalar, CCW +) cross r  ->  w k x r."""
    return w * V(-r[1], r[0])


def unit(v):
    return v / np.linalg.norm(v)


def mag(v):
    return float(np.linalg.norm(v))


def ang(v):
    """Angle of a vector in degrees, CCW from +x, in (-180, 180]."""
    return math.degrees(math.atan2(v[1], v[0]))


def solve2(known, d1, d2):
    """Find m1, m2 with known = m1*d1 + m2*d2 (d1, d2 unit directions)."""
    M = np.column_stack([d1, d2])
    m1, m2 = np.linalg.solve(M, known)
    return float(m1), float(m2)


def rot_dir(w):
    return "CCW" if w > 0 else "CW"


# ---------------------------------------------------------------- examples

def ladder():
    """L14 Ex 1: bar AB, 1.5 m, A on floor moving right at 3 m/s (constant),
    B on the wall, bar at 30 deg to the floor."""
    L, th = 1.5, math.radians(30)
    A = V(0, 0)
    B = A + L * V(-math.cos(th), math.sin(th))
    vA = V(3, 0)
    rBA = B - A
    dBA_perp = unit(V(-rBA[1], rBA[0]))  # direction of w k x r for w>0
    # vB = vA + vB/A ; vB vertical (unknown m1 along +y), vB/A along dBA_perp
    m_vB, m_rel = solve2(-vA, V(0, 1), -dBA_perp)  # vB j - rel*d = vA  -> rearranged
    # cleaner: vB*j = vA + rel*d  -> vB*j - rel*d = vA
    m_vB, m_rel = solve2(vA, V(0, 1), -dBA_perp)
    vB = m_vB * V(0, 1)
    vBA = m_rel * dBA_perp
    w = m_rel / L  # since vBA = w k x r and |r| = L, signed along dBA_perp
    # acceleration with aA = 0
    aA = V(0, 0)
    aBAn = -w**2 * rBA
    # aB j = aA + aBAn + alpha k x r
    m_aB, m_t = solve2(aA + aBAn, V(0, 1), -dBA_perp)
    alpha = m_t / L
    aB = m_aB * V(0, 1)
    aBAt = m_t * dBA_perp
    return dict(A=A, B=B, vA=vA, vB=vB, vBA=vBA, w=w, aA=aA, aBAn=aBAn,
                aBAt=aBAt, aB=aB, alpha=alpha, L=L)


def slider_crank():
    """L15 Ex 2 / L16 Ex 2 (M&K): crank OB r = 125 mm, rod AB l = 350 mm,
    theta = 60 deg, crank 1500 rev/min clockwise and constant. Piston A is
    on the horizontal line through O, to the left."""
    r, l, th = 0.125, 0.350, math.radians(60)
    wOB = -1500 * 2 * math.pi / 60  # CW negative
    O = V(0, 0)
    B = O + r * V(-math.cos(th), math.sin(th))
    beta = math.asin(B[1] / l)
    A = V(B[0] - l * math.cos(beta), 0)
    rBO = B - O
    vB = perp(wOB, rBO)
    rAB = A - B
    d = unit(V(-rAB[1], rAB[0]))  # +w direction for A relative to B
    # vA i = vB + m d -> vA i - m d = vB
    m_vA, m_rel = solve2(vB, V(1, 0), -d)
    vA = m_vA * V(1, 0)
    vAB = m_rel * d
    wAB = m_rel / l
    # accelerations
    aB = -wOB**2 * rBO  # alpha_OB = 0
    aABn = -wAB**2 * rAB
    m_aA, m_t = solve2(aB + aABn, V(1, 0), -d)
    aA = m_aA * V(1, 0)
    aABt = m_t * d
    alphaAB = m_t / l
    return dict(O=O, A=A, B=B, beta=math.degrees(beta), wOB=wOB, vB=vB, vA=vA,
                vAB=vAB, wAB=wAB, aB=aB, aABn=aABn, aABt=aABt, aA=aA,
                alphaAB=alphaAB, r=r, l=l)


def exam2016():
    """2016 exam: AB vertical (A fixed above B), AB = 0.2 m, 10 rad/s CW constant.
    DE horizontal, pivot E, DE = 0.2 m. B is 0.25 m above D and 0.6 m right."""
    D = V(0, 0)
    E = V(0.2, 0)
    B = V(0.6, 0.25)
    A = V(0.6, 0.45)
    wAB = -10.0
    rBA = B - A
    vB = perp(wAB, rBA)
    aB = -wAB**2 * rBA
    rDE = D - E
    dD = unit(V(-rDE[1], rDE[0]))  # +w direction for D about E
    rBD = B - D
    dBD = unit(V(-rBD[1], rBD[0]))  # +w direction for B relative to D
    # vB = vD + vB/D, vD = mD*dD, vB/D = mBD*dBD
    mD, mBD = solve2(vB, dD, dBD)
    vD, vBD = mD * dD, mBD * dBD
    wDE = mD / mag(rDE)
    wBD = mBD / mag(rBD)
    aDn = -wDE**2 * rDE
    aBDn = -wBD**2 * rBD
    # aB = aDn + aDt + aBDn + aBDt
    mDt, mBDt = solve2(aB - aDn - aBDn, dD, dBD)
    aDt, aBDt = mDt * dD, mBDt * dBD
    alphaDE = mDt / mag(rDE)
    alphaBD = mBDt / mag(rBD)
    return dict(A=A, B=B, D=D, E=E, vB=vB, vD=vD, vBD=vBD, wDE=wDE, wBD=wBD,
                aB=aB, aDn=aDn, aDt=aDt, aBDn=aBDn, aBDt=aBDt,
                alphaDE=alphaDE, alphaBD=alphaBD, rBD=mag(rBD))


def exam2021():
    """2021 exam: A(0,0) pivot, AB = 90 mm up; C(225,0) pivot, CD = 180 mm up;
    bar BDE straight, E at (450, 270) mm. AB 6 rad/s CW constant."""
    A, B = V(0, 0), V(0, 0.09)
    C, D = V(0.225, 0), V(0.225, 0.18)
    E = V(0.45, 0.27)
    wAB = -6.0
    rBA = B - A
    vB = perp(wAB, rBA)
    aB = -wAB**2 * rBA
    rDC = D - C
    dD = unit(V(-rDC[1], rDC[0]))
    rDB = D - B
    dDB = unit(V(-rDB[1], rDB[0]))
    # vD = vB + vD/B -> mD*dD - mDB*dDB = vB
    mD, mDB = solve2(vB, dD, -dDB)
    vD = mD * dD
    wDC = mD / mag(rDC)
    wBD = mDB / mag(rDB)
    aDn = -wDC**2 * rDC
    aDBn = -wBD**2 * rDB
    # aDn + mDt dD = aB + aDBn + mDBt dDB
    mDt, mDBt = solve2(aB + aDBn - aDn, dD, -dDB)
    aDt, aDBt = mDt * dD, mDBt * dDB
    alphaDC = mDt / mag(rDC)
    alphaBD = mDBt / mag(rDB)
    rEB = E - B
    aE = aB - wBD**2 * rEB + perp(alphaBD, rEB)
    return dict(A=A, B=B, C=C, D=D, E=E, vB=vB, vD=vD, wDC=wDC, wBD=wBD,
                aB=aB, aDn=aDn, aDt=aDt, aDBn=aDBn, aDBt=aDBt,
                alphaDC=alphaDC, alphaBD=alphaBD, aE=aE, rDB=mag(rDB))


def exam2022():
    """2022 exam: A(0,0) pivot, AB = 70 mm up, wAB = 3 CCW, alphaAB = 2 CCW.
    C at (-50, -50) mm slides along a 3-4-5 slope (36.87 deg)."""
    A, B, C = V(0, 0), V(0, 0.07), V(-0.05, -0.05)
    wAB, alAB = 3.0, 2.0
    rBA = B - A
    vB = perp(wAB, rBA)
    aBn = -wAB**2 * rBA
    aBt = perp(alAB, rBA)
    aB = aBn + aBt
    s = unit(V(4, 3))  # slope direction (up-right)
    rBC = B - C
    dBC = unit(V(-rBC[1], rBC[0]))
    # vB = vC + vB/C -> mC*s + mBC*dBC = vB
    mC, mBC = solve2(vB, s, dBC)
    vC, vBC = mC * s, mBC * dBC
    wBC = mBC / mag(rBC)
    aBCn = -wBC**2 * rBC
    mCa, mBCt = solve2(aB - aBCn, s, dBC)
    aC, aBCt = mCa * s, mBCt * dBC
    alphaBC = mBCt / mag(rBC)
    return dict(A=A, B=B, C=C, vB=vB, vC=vC, vBC=vBC, wBC=wBC, aBn=aBn,
                aBt=aBt, aB=aB, aBCn=aBCn, aBCt=aBCt, aC=aC, alphaBC=alphaBC,
                rBC=mag(rBC), theta=math.degrees(math.atan2(0.05, 0.12)))


def falling_rod():
    """L16 Ex 1: rod AB 5 m, A on wall at (0,4) moving down 6 m/s and
    speeding up at 5 m/s^2; B on floor at (3,0)."""
    A, B = V(0, 4), V(3, 0)
    vA, aA = V(0, -6), V(0, -5)
    rBA = B - A
    d = unit(V(-rBA[1], rBA[0]))
    mB, mrel = solve2(vA, V(1, 0), -d)
    w = mrel / mag(rBA)
    aBAn = -w**2 * rBA
    maB, mt = solve2(aA + aBAn, V(1, 0), -d)
    alpha = mt / mag(rBA)
    return dict(A=A, B=B, w=w, vB=mB * V(1, 0), aB=maB * V(1, 0),
                aBAn=aBAn, aBAt=mt * d, alpha=alpha)


def rolling_gear():
    """L17 Ex 1: gear r = 0.3 m rolls right on a fixed rack, w = 12 rad/s CW,
    alpha = 6 rad/s^2 CW. Point A at the top."""
    r, w, al = 0.3, -12.0, -6.0
    aO = V(-al * r, 0)  # rolling: aO = alpha r, to the right for CW alpha
    rAO = V(0, r)
    aAOn = -w**2 * rAO
    aAOt = perp(al, rAO)
    aA = aO + aAOn + aAOt
    contact = aO - w**2 * V(0, -r) + perp(al, V(0, -r))
    return dict(aO=aO, aAOn=aAOn, aAOt=aAOt, aA=aA, contact=contact)


def fmt(v, unit=""):
    return f"{mag(v):.4g}{unit} at {ang(v):.1f} deg"


if __name__ == "__main__":
    L = ladder()
    print("LADDER  w =", round(L["w"], 4), rot_dir(L["w"]), " vB =", fmt(L["vB"]),
          " vB/A =", fmt(L["vBA"]))
    print("        aB/A n =", fmt(L["aBAn"]), " aB/A t =", fmt(L["aBAt"]),
          " aB =", fmt(L["aB"]), " alpha =", round(L["alpha"], 3), rot_dir(L["alpha"]))
    S = slider_crank()
    print("SLIDER  beta =", round(S["beta"], 2), " vB =", fmt(S["vB"]), " vA =", fmt(S["vA"]),
          " vA/B =", fmt(S["vAB"]), " wAB =", round(S["wAB"], 3), rot_dir(S["wAB"]))
    print("        aB =", fmt(S["aB"]), " aA/B n =", fmt(S["aABn"]), " aA/B t =", fmt(S["aABt"]),
          " aA =", fmt(S["aA"]), " alphaAB =", round(S["alphaAB"], 1), rot_dir(S["alphaAB"]))
    X = exam2016()
    print("EX2016  vB =", fmt(X["vB"]), " vD =", fmt(X["vD"]), " vB/D =", fmt(X["vBD"]),
          " wDE =", round(X["wDE"], 3), rot_dir(X["wDE"]), " wBD =", round(X["wBD"], 3), rot_dir(X["wBD"]))
    print("        aB =", fmt(X["aB"]), " aDn =", fmt(X["aDn"]), " aDt =", fmt(X["aDt"]),
          " aB/D n =", fmt(X["aBDn"]), " aB/D t =", fmt(X["aBDt"]))
    print("        alphaDE =", round(X["alphaDE"], 1), rot_dir(X["alphaDE"]),
          " alphaBD =", round(X["alphaBD"], 1), rot_dir(X["alphaBD"]), " rBD =", round(X["rBD"], 4))
    Y = exam2021()
    print("EX2021  vB =", fmt(Y["vB"]), " vD =", fmt(Y["vD"]), " wDC =", round(Y["wDC"], 3),
          rot_dir(Y["wDC"]), " wBD =", round(Y["wBD"], 6))
    print("        aB =", fmt(Y["aB"]), " aDn =", fmt(Y["aDn"]), " aDt =", fmt(Y["aDt"]),
          " aD/B t =", fmt(Y["aDBt"]), " alphaBD =", round(Y["alphaBD"], 3), rot_dir(Y["alphaBD"]),
          " alphaDC =", round(Y["alphaDC"], 3), rot_dir(Y["alphaDC"]), " aE =", fmt(Y["aE"]))
    Z = exam2022()
    print("EX2022  theta =", round(Z["theta"], 2), " vB =", fmt(Z["vB"]), " vC =", fmt(Z["vC"]),
          " vB/C =", fmt(Z["vBC"]), " wBC =", round(Z["wBC"], 4), rot_dir(Z["wBC"]))
    print("        aBn =", fmt(Z["aBn"]), " aBt =", fmt(Z["aBt"]), " aB/C n =", fmt(Z["aBCn"]),
          " aB/C t =", fmt(Z["aBCt"]), " aC =", fmt(Z["aC"]), " alphaBC =", round(Z["alphaBC"], 3),
          rot_dir(Z["alphaBC"]))
    F = falling_rod()
    print("ROD     w =", round(F["w"], 3), rot_dir(F["w"]), " vB =", fmt(F["vB"]), " aB =", fmt(F["aB"]),
          " aB/A t =", fmt(F["aBAt"]), " alpha =", round(F["alpha"], 3), rot_dir(F["alpha"]))
    G = rolling_gear()
    print("GEAR    aO =", fmt(G["aO"]), " aA =", fmt(G["aA"]), " contact pt a =", fmt(G["contact"]))
