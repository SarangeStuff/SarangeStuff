"""Checks for the L11-L13 homework memo (every answer by two routes)."""
import numpy as np
from math import *
k = np.array([0, 0, 1.0]); V = lambda x, y: np.array([x, y, 0.0]); cr = lambda w, r: w * np.cross(k, r)

print("5/2 plate (b=2,h=1,w=3 CCW, alpha=4 CW) vs book formula")
b, h, w, al = 2.0, 1.0, 3.0, -4.0; r = V(b, -h)
print("  v", cr(w, r)[:2], "book", w * h, w * b, "| a", (cr(al, r) - w * w * r)[:2], "book", -(b*w*w + h*4), h*w*w - b*4)

print("5/17 bent bar: w = 2 CCW, alpha = 5 CW")
B = 0.5 * V(sin(radians(15)), -cos(radians(15))); A = B + 0.3 * V(cos(radians(-15)), sin(radians(-15)))
vA = cr(2, A); aA = cr(-5, A) - 4 * A
print("  A =", A[:2].round(4), "|OA| =", round(np.linalg.norm(A), 4), "cos rule:", round(sqrt(0.25 + 0.09 - 2*0.5*0.3*cos(radians(120))), 4))
print("  vA =", vA[:2].round(4), round(np.linalg.norm(vA), 4), " aA =", aA[:2].round(4), round(np.linalg.norm(aA), 4), " angle OA:", round(degrees(atan2(A[1], A[0])), 2))

print("5/26 pulleys")
w = 1.5 / 0.075; al = 45 / 0.4; an = 0.36 * w**2; at = 0.36 * al
print(f"  w={w} alpha={al} a_n={an} a_t={at} a_C={hypot(an, at):.2f} angle from CO={degrees(atan(at/an)):.1f}")

print("5/42 bar on corner: theta = atan(h/x), xdot = -r w0 -> thetadot = r h w0/(x^2+h^2)")
x, hh, rr, w0, dt = 0.5, 0.3, 0.1, 4.0, 1e-6
th = lambda xx: atan(hh / xx); print("  numeric", (th(x - rr*w0*dt) - th(x)) / dt, "formula", rr*hh*w0/(x*x + hh*hh))
print("5/44 lever on disk: theta = asin(r/x), xdot = -v -> w = v/(x sqrt((x/r)^2-1))")
x, rr, v = 0.5, 0.2, 1.5
th = lambda xx: asin(rr / xx); print("  numeric", (th(x - v*dt) - th(x)) / dt, "formula", v / (x * sqrt((x/rr)**2 - 1)))

print("5/56 Geneva")
rP, d = 0.2 / sqrt(2), 0.2
f = lambda t: rP * (d*cos(t) - rP) / (d*d + rP*rP - 2*d*rP*cos(t))
for t in (45, 20, 0):
    print(f"  theta={t}: w2/w1 = {f(radians(t)):.4f} -> w2 = {2*f(radians(t)):.4f}")
t = radians(20); beta = lambda tt: atan2(rP*sin(tt), d - rP*cos(tt))
print("  numeric:", 2 * (beta(t) - beta(t - 1e-7)) / 1e-7, " O2P =", sqrt(d*d + rP*rP - 2*d*rP*cos(t)), " beta =", degrees(beta(t)))

print("5/119 IC")
B = 0.8 * V(cos(radians(-30)), sin(radians(-30))); D = 1.2 * V(cos(radians(-30)), sin(radians(-30)))
vDmag = 0.6 / sin(radians(60)); wOD = vDmag / 1.2
A = V(B[0] + sqrt(0.49 - B[1]**2), 0)
C = V(A[0], -A[0] * tan(radians(30)))
rB, rA = np.linalg.norm(B - C), np.linalg.norm(A - C)
vB = wOD * 0.8; wAB = vB / rB; vAm = wAB * rA
vBv = cr(-wOD, B); M = np.column_stack([np.cross(k, A - B)[:2], [-1, 0]]); sol = np.linalg.solve(M, -vBv[:2])
print(f"  vD={vDmag:.4f} wOD={wOD:.4f} B={B[:2].round(4)} A={A[:2].round(4)} C={C[:2].round(4)} rB/C={rB:.4f} rA/C={rA:.4f}")
print(f"  vB={vB:.4f} wAB={wAB:.4f} vA={vAm:.4f} | vector: wAB={sol[0]:.4f} vA_x={sol[1]:.4f}")

print("5/108 IC (roller A on the plunger plate: only v_Ax = 2 fixed)")
A = V(0, 0); B = 0.1 * V(cos(radians(-30)), sin(radians(-30))); D = 0.3 * V(cos(radians(-30)), sin(radians(-30)))
C = V(B[0], D[1]); w = 2 / (A[1] - C[1]); vD = w * (D[0] - C[0])
print(f"  C={C[:2].round(4)} arm of A (vertical) = {A[1]-C[1]:.4f} arm of D = {D[0]-C[0]:.4f} w = {w:.3f} vD = {vD:.3f}")
vAvec = cr(-w, A - C); print("  v_A =", vAvec[:2].round(3), " v_B =", cr(-w, B - C)[:2].round(3), " v_D =", cr(-w, D - C)[:2].round(3))

print("5/117 IC (roller F on plunger cup: only v_Fy = 2 fixed)")
u = V(-sin(radians(45)), -cos(radians(45))); F = 0.32 * u; H = 0.24 * u
wDF = 2 / (-F[0]) ; wDF = -abs(wDF)                     # need v_Fy = +2: v_Fy = w * F_x
vH = cr(wDF, H); yB = H[1] - sqrt(0.04 - H[0]**2); Bp = V(0, yB)
A = Bp + 0.16 * (Bp - H) / 0.2
C = V(yB, yB)                                           # line DH is y = x; horizontal through B
wAH = np.linalg.norm(vH) / np.linalg.norm(H - C); vA = wAH * np.linalg.norm(A - C)
print(f"  wDF={wDF:.4f} vF={cr(wDF, F)[:2].round(3)} vH={vH[:2].round(4)} |vH|={np.linalg.norm(vH):.4f}")
print(f"  H={H[:2].round(4)} B={Bp[:2].round(4)} A={A[:2].round(4)} C={C[:2].round(4)} rH/C={np.linalg.norm(H-C):.4f} rA/C={np.linalg.norm(A-C):.4f} wAH={wAH:.3f} vA={vA:.3f}")
print("  angle of AH from horizontal:", round(degrees(atan2(-(Bp-H)[1], (Bp-H)[0])), 2))

print("5/120 planetary: sun rs = a/2, planet rp = a/2, ring = 1.5a, arm a at 90 rpm CW")
for wD in (0, 80):
    vAx = -90                     # planet centre at x = a: CW arm -> down (units: rpm * a)
    vring = +wD * 1.5             # ring contact at x = 1.5a, CCW -> up
    slope = (vring - vAx) / 0.5   # per a
    vsun = vAx - slope * 0.5      # at x = 0.5a
    zero = 1.0 + (0 - vAx) / slope
    print(f"  ring {wD} rpm CCW: sun-contact speed {vsun} a·rpm -> w_B = {vsun / 0.5:.0f} rpm (neg = CW); planet IC at x = {zero:.3f}a; w_planet = {slope:.0f} rpm")
