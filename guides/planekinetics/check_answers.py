"""Independent checks (scalar AND vector form) for every number quoted in the plane-kinetics workthrough."""
import numpy as np
from math import *
g = 9.81
k = np.array([0, 0, 1.0])
def V(x, y): return np.array([x, y, 0.0])
def cz(a, b): return float(np.cross(a, b)[2])
def acc(aO, alpha, r, w=0.0): return aO + alpha * np.cross(k, r) - w**2 * r   # alpha>0 CCW

print("== T10 Q2 mast (fixed axis O)")
m, L = 300, 24; T = 1300 / 0.6; I_O = m * L**2 / 3
alpha = (2*T*16*sin(radians(30)) - m*g*12*cos(radians(30))) / I_O
rG = 12 * V(cos(radians(30)), sin(radians(30))); aG = acc(V(0, 0), alpha, rG)
O = m*aG - V(-2*T, 0) - V(0, -m*g)
print(f"T={T:.1f} I_O={I_O:.0f} alpha={alpha:.4f} a_t={12*alpha:.3f} aG={aG[:2]} O={O[:2]} |O|={np.linalg.norm(O):.0f}")

print("== T10 Q3 L-body (fixed axis O)")
m, Lb = 3.0, 0.25; m1, l1, m2, l2 = 0.75*m, 0.75*Lb, 0.25*m, 0.25*Lb
G1, G2 = V(l1/2, 0), V(l1, l2/2); G = (m1*G1 + m2*G2) / m
I_O = m1*l1**2/3 + (m2*l2**2/12 + m2*(G2[0]**2 + G2[1]**2))
alpha = cz(G, V(0, -m*g)) / I_O
print(f"G={G[:2]} xbar={G[0]:.4f}=15L/32 {15*Lb/32:.4f} ybar={G[1]:.5f}=L/32 {Lb/32:.5f} I_O={I_O:.6f} alpha={alpha:.2f}")
print(f"   check via two weights: {(cz(G1, V(0,-m1*g)) + cz(G2, V(0,-m2*g)))/I_O:.2f}")

print("== T10 Q1 pipe (curvilinear TRANSLATION, alpha_pipe = 0)")
m, r, mu, R = 80, 1.0, 0.3, 0.5
u = V(sin(radians(45)), cos(radians(45)))          # link direction from its ground pivot
alpha = mu*g / (r*(sin(radians(45)) - mu*cos(radians(45))))
a = acc(V(0, 0), alpha, r*u)                       # omega = 0 at the start
print(f"alpha_links={alpha:.3f} a={a[:2]} |a|={np.linalg.norm(a):.3f}")
xbar = 2*R/pi; A, B, Gp = V(-R, 0), V(R, 0), V(0, xbar)
d = cz(Gp - A, a/np.linalg.norm(a))
NB = (m*g*0.5 + m*cz(Gp - A, a)) / 1.0
Ntot = m*g + m*a[1]; NA = Ntot - NB; Ff = -m*a[0]
print(f"ybar={xbar:.4f} angle AG={degrees(atan2(xbar, R)):.1f} d={d:.4f} NB={NB:.1f} NA={NA:.1f} Ftot={Ff:.1f}=mu*N {mu*Ntot:.1f}")
print(f"   check sum M_G = 0: {cz(A-Gp, V(0,NA)) + cz(B-Gp, V(0,NB)) + cz(A-Gp, V(-Ff*NA/Ntot,0)) + cz(B-Gp, V(-Ff*NB/Ntot,0)):.2e}")

print("== T11 Q1 plate 2b x b pinned at corner (fixed axis O)")
m, b = 3, 0.2; rG = V(b, -b/2)
I_G = m*(b**2 + (2*b)**2)/12; I_O = I_G + m*(rG[0]**2 + rG[1]**2)
alpha = cz(rG, V(0, -m*g)) / I_O; aG = acc(V(0, 0), alpha, rG)
O = m*aG - V(0, -m*g); th = degrees(atan2(b/2, b))
print(f"I_G={I_G:.4f} d2={rG[0]**2+rG[1]**2:.4f} I_O={I_O:.4f} alpha={alpha:.3f} (3g/5b={3*g/5/b:.3f}) aG={aG[:2]} O={O[:2]} |O|={np.linalg.norm(O):.2f} theta={th:.1f}")
rr = np.linalg.norm(rG); print(f"   n-t: (F_O)_t={m*g*cos(radians(th)) - m*rr*abs(alpha):.2f} (F_O)_n={m*g*sin(radians(th)):.2f}")

print("== T10 Q4 / T11 Q2 square plate, free on frictionless table (GENERAL PLANE MOTION)")
m, b, P = 6, 0.2, 120; A, B = V(b/2, -b/2), V(b/2, b/2)
aG = V(0, P/m); I_G = m*(b**2 + b**2)/12; alpha = cz(A, V(0, P)) / I_G
aB = acc(aG, alpha, B); aBG = alpha*np.cross(k, B)
print(f"aG={aG[:2]} I_G={I_G:.4f} alpha={alpha:.1f} aB/G={aBG[:2]} |aB/G|={np.linalg.norm(aBG):.2f} aB={aB[:2]} |aB|={np.linalg.norm(aB):.2f} dir={degrees(atan2(aB[1],aB[0])):.1f}")
print(f"   cos rule: {sqrt(20**2 + np.linalg.norm(aBG)**2 - 2*20*np.linalg.norm(aBG)*cos(radians(135))):.2f}")

print("== T10 Q5 bowling ball (slipping, then rolling)")
m, r, kG, mu, v0 = 6.4, 0.12, 0.083, 0.2, 6.0
a = mu*g; alpha = mu*m*g*r/(m*kG**2); t = v0/(a + alpha*r); v = v0 - a*t; s = v0*t - a*t**2/2
print(f"a={a:.3f} I_G={m*kG**2:.5f} (2/5mr^2 would be {0.4*m*r*r:.5f}) alpha={alpha:.2f} t={t:.4f} v={v:.3f} (v0/(1+k2/r2)={v0/(1+kG**2/r**2):.3f}) s={s:.3f}")
print(f"   formula s={v0**2/(2*mu*g)*kG**2*(kG**2+2*r**2)/(kG**2+r**2)**2:.3f}")

print("== T11 Q3 rod on massless hoop (rolls without slip)")
m, l = 0.5, 0.25; I_G = m*l**2/12
alpha_cw = 3*g/(8*l); al = -alpha_cw
aO = V(-al*l, 0); aG = acc(aO, al, V(l/2, 0))
Ff = m*aG[0]; N = m*g + m*aG[1]
C, G = V(0, -l), V(l/2, 0)
print(f"alpha={alpha_cw:.3f} CW aO={aO[:2]} aG={aG[:2]} Ff={Ff:.3f} N={N:.3f} mu_min={Ff/N:.3f}")
print(f"   sum M_G = {cz(C-G, V(Ff, N)):.5f} vs I_G*alpha = {I_G*al:.5f}")
print(f"   sum M_C: W term {cz(G-C, V(0,-m*g)):.5f} vs I_G a + (r_GC x m aG) = {I_G*al + cz(G-C, m*aG):.5f}")

print("== T11 Q4 bar AB, crank OA, link CB")
m, l = 0.8, 0.3; O, A, B, C = V(0, 0), V(0, -0.1), V(0.3, -0.1), V(0.3, 0.1)
wOA, aOA = 2.0, 4.0                                    # both CCW (A moves right)
vA = wOA*np.cross(k, A - O)
M = np.column_stack([np.cross(k, B - A)[:2], -np.cross(k, B - C)[:2]])
wAB, wCB = np.linalg.solve(M, -vA[:2])
aA = acc(V(0,0), aOA, A - O, wOA)
rhs = -aA[:2] + wAB**2*(B - A)[:2] - wCB**2*(B - C)[:2]
aAB, aCB = np.linalg.solve(M, rhs)
aG = acc(aA, aAB, (B - A)/2, wAB); I_G = m*l**2/12
Ax = m*aG[0]; Bf = (I_G*aAB + cz((B-A)/2, m*aG) + m*g*0.15) / 0.3; Ay = m*g + m*aG[1] - Bf
print(f"vA={vA[:2]} wAB={wAB:.3f} wCB={wCB:.3f} aA={aA[:2]} alphaAB={aAB:.4f} alphaCB={aCB:.3f} aG={aG[:2]}")
print(f"   I_G={I_G:.4f} I_G*alpha={I_G*aAB:.5f} B(CB)={Bf:.4f} Ax={Ax:.3f} Ay={Ay:.4f}")
print(f"   memo route: B - Ay = {2*I_G*aAB/l:.5f}, B + Ay = {m*g + m*aG[1]:.4f}")
