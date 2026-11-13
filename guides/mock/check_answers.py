"""Solutions for the mock exam, each checked by a second route."""
import numpy as np
from math import *
g = 9.81
k = np.array([0, 0, 1.0]); V = lambda x, y: np.array([x, y, 0.0]); cr = lambda w, r: w * np.cross(k, r)
ang = lambda v: degrees(atan2(v[1], v[0])) % 360

print("Q1 radar + drone: r=600, th=40, v=30 -> horizontal, a_t=2 (speeding up), rho=500, centre below")
r, th = 600.0, radians(40); er = np.array([cos(th), sin(th)]); et = np.array([-sin(th), cos(th)])
v = np.array([30.0, 0]); a = np.array([2.0, -30**2 / 500])
vr, vt = v @ er, v @ et; thd = vt / r
ar, at = a @ er, a @ et; rdd = ar + r * thd**2; thdd = (at - 2 * vr * thd) / r
print(f"  v_r={vr:.3f} v_th={vt:.3f} thetadot={thd:.5f} | a_n={30**2/500} a_r={ar:.4f} a_th={at:.4f} rdd={rdd:.4f} thdd={thdd:.6f}")
print(f"  |a| check: {np.linalg.norm(a):.4f} vs {hypot(ar, at):.4f}")

print("Q2 collar A on horizontal bar h=2 below pulley P; rope P->A and P->B (hanging); A moves right at 1.5 const; x=1.5")
h, x, xd = 2.0, 1.5, 1.5; S = hypot(x, h)
yBd = -x * xd / S; yBdd = -(xd**2 / S - x**2 * xd**2 / S**3)
print(f"  S={S} yB'={yBd} (neg = up) yB''={yBdd:.4f}")
dt = 1e-5; L = lambda xx: hypot(xx, h); yB = lambda t: 10 - L(x + xd * t)
print(f"  numeric v={(yB(dt) - yB(-dt)) / (2*dt):.4f} a={(yB(dt) - 2*yB(0) + yB(-dt)) / dt**2:.4f}")

print("Q3 crank OA=0.2 @30 deg, 6 rad/s CCW; AB=0.5; B in vertical guide x=0.45")
A = 0.2 * V(cos(radians(30)), sin(radians(30))); B = V(0.45, A[1] + sqrt(0.25 - (0.45 - A[0])**2))
C = V(B[1] / tan(radians(30)), B[1])
vA = cr(6, A); rA, rB = np.linalg.norm(A - C), np.linalg.norm(B - C)
wAB = -np.linalg.norm(vA) / rA; vB = cr(wAB, B - C)
print(f"  A={A[:2].round(4)} B={B[:2].round(4)} C={C[:2].round(4)} vA={vA[:2].round(4)} |{np.linalg.norm(vA):.3f}| rA/C={rA:.4f} rB/C={rB:.4f} wAB={wAB:.4f} vB={vB[:2].round(4)}")
M = np.column_stack([np.cross(k, B - A)[:2], [0, -1]]); sol = np.linalg.solve(M, -vA[:2]); print("  vector check wAB, vB:", sol.round(4))

print("Q4 four-bar: O=(0,0), OA=0.15 @60, C=(0.45,0), CB=0.25, AB=0.35; wOA=10 CCW, aOA=40 CCW")
O, Cp = V(0, 0), V(0.45, 0); A = 0.15 * V(cos(radians(60)), sin(radians(60)))
d = np.linalg.norm(Cp - A); aa = (0.35**2 - 0.25**2 + d**2) / (2 * d); hh = sqrt(0.35**2 - aa**2)
u = (Cp - A) / d; perp = V(-u[1], u[0])
B1, B2 = A + aa * u + hh * perp, A + aa * u - hh * perp
B = B1 if B1[1] > B2[1] else B2
print(f"  A={A[:2].round(4)} B={B[:2].round(4)} |AB|={np.linalg.norm(B-A):.4f} |CB|={np.linalg.norm(B-Cp):.4f} AB angle={ang(B-A):.2f} CB angle (C->B)={ang(B-Cp):.2f}")
vA = cr(10, A)
M = np.column_stack([np.cross(k, B - A)[:2], -np.cross(k, B - Cp)[:2]]); wAB, wCB = np.linalg.solve(M, -vA[:2])
vB = cr(wCB, B - Cp); vBA = cr(wAB, B - A)
print(f"  vA={vA[:2].round(4)} |{np.linalg.norm(vA):.3f}| @ {ang(vA):.1f}; wAB={wAB:.4f} wCB={wCB:.4f}; vB={np.linalg.norm(vB):.4f} @ {ang(vB):.1f}; vB/A={np.linalg.norm(vBA):.4f} @ {ang(vBA):.1f}")
aA = cr(40, A) - 100 * A
rhs = -aA[:2] + wAB**2 * (B - A)[:2] - wCB**2 * (B - Cp)[:2]
aAB, aCB = np.linalg.solve(M, rhs)
print(f"  (aA)n={100*0.15} (aA)t={40*0.15}; aA={aA[:2].round(4)}; (aB/A)n={wAB**2*0.35:.4f} (aB)n={wCB**2*0.25:.4f}")
print(f"  alphaAB={aAB:.4f} alphaCB={aCB:.4f}; (aB/A)t={abs(aAB)*0.35:.4f} @ {ang(cr(aAB, B-A)):.1f}; (aB)t={abs(aCB)*0.25:.4f} @ {ang(cr(aCB, B-Cp)):.1f}")
aB = cr(aCB, B - Cp) - wCB**2 * (B - Cp); print(f"  aB={aB[:2].round(4)} |{np.linalg.norm(aB):.3f}|")

print("Q5 oblique: A 0.5 kg 4 m/s ->; B 0.8 kg 2 m/s up; line of centres A->B at 30 deg; e=0.6")
n = np.array([cos(radians(30)), sin(radians(30))]); t = np.array([-sin(radians(30)), cos(radians(30))])
mA, mB, e = 0.5, 0.8, 0.6; vA, vB = np.array([4.0, 0]), np.array([0, 2.0])
An, At, Bn, Bt = vA @ n, vA @ t, vB @ n, vB @ t
Mm = np.array([[mA, mB], [-1, 1]]); rr = np.array([mA*An + mB*Bn, e * (An - Bn)])
An2, Bn2 = np.linalg.solve(Mm, rr)
vA2, vB2 = An2 * n + At * t, Bn2 * n + Bt * t
print(f"  before A n={An:.4f} t={At:.4f} | B n={Bn:.4f} t={Bt:.4f}")
print(f"  after  A n={An2:.4f} -> {np.linalg.norm(vA2):.4f} @ {ang(vA2):.1f} {vA2.round(4)} | B n={Bn2:.4f} -> {np.linalg.norm(vB2):.4f} @ {ang(vB2):.1f} {vB2.round(4)}")
print(f"  momentum x: {mA*4:.3f} -> {mA*vA2[0] + mB*vB2[0]:.4f}; y: {mB*2:.3f} -> {mA*vA2[1] + mB*vB2[1]:.4f}; KE {0.5*mA*16 + 0.5*mB*4:.3f} -> {0.5*mA*vA2@vA2 + 0.5*mB*vB2@vB2:.4f}")

print("Q6 (particle work-energy) block 4 kg on 30 deg incline, mu_k 0.25, mu_s 0.30, 1.2 m above a spring k 1500")
m, th, mk, ms, d, kk = 4.0, radians(30), 0.25, 0.30, 1.2, 1500.0
W_along, N = m * g * sin(th), m * g * cos(th); Fk = mk * N
v2 = sqrt(2 * (W_along - Fk) * d / m)
a_, b_, c_ = 0.5 * kk, -(W_along - Fk), -(W_along - Fk) * d
x = (-b_ + sqrt(b_**2 - 4 * a_ * c_)) / (2 * a_)
print(f"  mg sin30={W_along:.3f} N={N:.3f} F_k={Fk:.4f} net={W_along - Fk:.4f}")
print(f"  (a) Vg drop={W_along*d:.4f} U_f={-Fk*d:.4f} v={v2:.4f}")
print(f"  (b) 750x^2 - {W_along - Fk:.4f}x - {(W_along - Fk)*d:.4f} = 0 -> x = {x:.5f} m; check energy: {(W_along - Fk)*(d + x):.4f} vs {0.5*kk*x*x:.4f}")
print(f"  (c) spring force {kk*x:.2f} vs mg sin30 {W_along:.2f} + mu_s N {ms*N:.3f} = {W_along + ms*N:.2f} -> moves back up")

print("Q7 bar AB 6 kg 2 m + disk 4 kg r 0.2 welded centred at B; pin A, cable at B; cable cut (horizontal)")
mb, Lb, md, rd = 6.0, 2.0, 4.0, 0.2; mt = mb + md
xbar = (mb * 1 + md * 2) / mt
IA = mb * Lb**2 / 3 + (0.5 * md * rd**2 + md * Lb**2)
alpha = (mb * g * 1 + md * g * 2) / IA; aG = xbar * alpha; Ay = mt * g - mt * aG
print(f"  xbar={xbar} IA={IA} alpha={alpha:.4f} aG={aG:.4f} Ay={Ay:.4f} Ax=0")
IG = mb * Lb**2 / 12 + mb * (xbar - 1)**2 + 0.5 * md * rd**2 + md * (2 - xbar)**2
print(f"  check via G: IG={IG:.4f}, IG + m xbar^2 = {IG + mt*xbar**2:.4f}; sum M_G with Ay: {Ay*xbar:.4f} vs IG alpha {IG*alpha:.4f}")

print("Q8 solid cylinder 30 kg r 0.25 on floor mu_s 0.2 mu_k 0.15, horizontal P at centre")
m, r, ms, mk = 30.0, 0.25, 0.2, 0.15; N = m * g
for P in (120.0, 200.0):
    a = P / (1.5 * m); F = 0.5 * m * a
    if F <= ms * N:
        print(f"  P={P}: no slip a={a:.4f} alpha={a/r:.4f} F={F:.3f} <= {ms*N:.3f}")
    else:
        Fk = mk * N; a2 = (P - Fk) / m; al2 = Fk * r / (0.5 * m * r**2)
        print(f"  P={P}: needs F={F:.3f} > {ms*N:.3f} -> slips: F={Fk:.3f} a={a2:.4f} alpha={al2:.4f} (v_contact grows: a - r alpha = {a2 - r*al2:.3f} > 0)")
