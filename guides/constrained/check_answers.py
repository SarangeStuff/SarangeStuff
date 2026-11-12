"""Checks for the constrained-motion + coordinate-vectors pack (length method AND velocity line; scalar AND vector)."""
import numpy as np
from math import sqrt, sin, cos, radians, degrees, atan2, atan, pi

def vline(vl, vr):            # pulley centre velocity from its two strand velocities (up +)
    return (vl + vr) / 2

print("EA1 movable pulley: end pulled up at v=1.2 -> centre", vline(0, 1.2), "up (length: L = 2sP - sE -> vP = vE/2)")
print("EA2 two ropes, A down 2 m/s: length vC =", -2 / 2, "vB =", -2 / 4, "| line vC =", vline(2, 0), "vB =", vline(vline(2, 0), 0))
vP = (2 - 4) / 2; print("EA3 A down 4, C down 2: length vP =", vP, "(up 1) | line", vline(4, -2), "| accel aA=1 down, aC=0 ->", (0 - 1) / 2)
for name, rate in (("EA4 CT1 Q1 motor 100 mm/s", 100), ("EA4b F25 Q2 drum 180 mm/s", 180)):
    vB = rate / 3; vL = vB / 2                    # 3 segments on B; load pulley hangs in loop of cable 2
    x = rate / 3                                  # line: x = (rate + (-x))/2
    assert abs(x - vline(rate, -x)) < 1e-12
    print(f"{name}: vB = {vB:.2f} up, vL = {vL:.2f} up, vB/L = {vB - vL:.2f} up; over 10 s h = {vL * 10:.0f} mm")
xa, va = 4.0, 2.5; S = sqrt(xa**2 + 9)
vc = -xa * va / S; ac = -(va**2 / S - xa**2 * va**2 / S**3)
print(f"EA5 S25 Q2: xA = {sqrt(25 - 9)}, xC' = {vc} (up 2), xC'' = {ac:.3f} (negative = UP, x_C measured down)")
print("   crate speed vs xA:", [round(x * va / sqrt(x * x + 9), 3) for x in (3.5, 4, 4.5)], "increasing -> accelerating up")

print("B2 S25 Q1b (n-t vectors)")
et = np.array([cos(radians(-15)), sin(radians(-15))]); en = np.array([et[1], -et[0]])   # en = et turned 90 deg CW (centre below)
an = 75**2 / 600; at = (-9.81 - an * en[0]) / et[0]; a = at * et + an * en
print(f"   e_t={et.round(4)} e_n={en.round(4)} a_n={an} a_t={at:.3f} a={a.round(3)} |a|={np.linalg.norm(a):.3f} sqrt(at2+an2)={sqrt(at*at+an*an):.3f}")
print(f"   memo a_y=-11.03 -> |a| would be {sqrt(9.81**2 + 11.03**2):.2f} (inconsistent)")
print("B3 S25 Q1a (polar by dot products)")
v = 75 * np.array([cos(radians(-15)), sin(radians(-15))]); er = np.array([cos(radians(45)), sin(radians(45))]); eth = np.array([-er[1], er[0]])
print(f"   v_r={v @ er:.2f} v_th={v @ eth:.2f} thetadot={(v @ eth) / 800:.4f}")
print("B4 CT1 Q2 cars")
vA = 96 / 3.6; vB = vA
VA = vA * np.array([cos(radians(115)), sin(radians(115))]); VB = np.array([0, vB])
AA = vA**2 / 375 * np.array([cos(radians(205)), sin(radians(205))]); AB = np.array([-vB**2 / 360, 0.762])
vr = VA - VB; ar = AA - AB
print(f"   v={vA:.3f} vA={VA.round(3)} vA/B={vr.round(3)} |vA/B|={np.linalg.norm(vr):.3f} (2v sin12.5={2*vA*sin(radians(12.5)):.3f})")
print(f"   aA={AA.round(4)} |aA|={np.linalg.norm(AA):.4f} aB={AB.round(4)} aA/B={ar.round(4)} |aA/B|={np.linalg.norm(ar):.4f} angle={degrees(atan2(ar[1], ar[0])):.1f}")
print("B5 CT1 Q3 helix")
r = 7.2; c = 3 / pi; v = 25 / 3.6; vd = -3 / 3.6
g = atan(c / r); thd = v * cos(g) / r; zd = v * sin(g)
aR = -r * thd**2; ath = vd * cos(g); az = vd * sin(g); rho = r / cos(g)**2
print(f"   gamma={degrees(g):.3f} deg, v={v:.4f}, vtheta={v*cos(g):.4f}, thetadot={thd:.4f}, zdot={zd:.4f}")
print(f"   a_R={aR:.3f} a_theta={ath:.4f} a_z={az:.4f} |a|={sqrt(aR**2+ath**2+az**2):.4f} | n-t: rho={rho:.3f} v2/rho={v*v/rho:.3f} |a|={sqrt((v*v/rho)**2+vd**2):.4f}")
print("B6 spherical example: v = 250 i, R=4000, theta=30, phi=20")
th, ph, R = radians(30), radians(20), 4000
eR = np.array([cos(ph)*cos(th), cos(ph)*sin(th), sin(ph)]); eT = np.array([-sin(th), cos(th), 0]); eP = np.array([-sin(ph)*cos(th), -sin(ph)*sin(th), cos(ph)])
V = np.array([250.0, 0, 0])
print(f"   e_R={eR.round(4)} e_th={eT.round(4)} e_ph={eP.round(4)} dots: {eR@eT:.1e} {eR@eP:.1e} {eT@eP:.1e}")
print(f"   Rdot={V@eR:.2f} thetadot={(V@eT)/(R*cos(ph)):.5f} phidot={(V@eP)/R:.5f} |v| check={sqrt((V@eR)**2+(V@eT)**2+(V@eP)**2):.2f}")
