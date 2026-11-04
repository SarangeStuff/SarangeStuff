"""Checks every Part II (kinetics) worked example. Run: python3 kinetics.py"""
import math

g = 9.81
d = math.radians
out = []


def show(name, **kw):
    out.append(name + ": " + ", ".join(f"{k} = {v:.4g}" for k, v in kw.items()))


# ---- Ch12 Newton II, rectilinear
vi, vf = 320 / 3.6, 55 / 3.6
show("L19 Ex1 shuttle", s=1000 * math.log(vi / vf))
a = 2 * 6 / 3**2
N = 20 * g * math.cos(d(30))
show("L19 Ex2 crate", a=a, N=N, T=0.3 * N + 20 * g * math.sin(d(30)) + 20 * a)
# L20 Ex2: A 60 kg on 30 deg slope, B 20 kg on a movable pulley, a_A = 2 a_B
mA, mB, th, mus, muk = 60, 20, d(30), 0.25, 0.20
Tst = mB * g / 2
NA = mA * g * math.cos(th)
show("L20 Ex2 static", T_static=Tst, Ff_needed=mA * g * math.sin(th) - Tst, Ff_max=mus * NA)
# mB aB = 2T - mB g ; mA (2 aB) = mA g sin - T - muk N
aB = (mA * g * math.sin(th) - muk * NA - mB * g / 2) / (2 * mA + mB / 2)
T = (mB * aB + mB * g) / 2
show("L20 Ex2 moving", aB=aB, aA=2 * aB, T=T)
# 2023 exam Q6: block 25 kg, T = 40 N, horizontal pull 2T + T cos30, T sin30 up
m = 25
N = m * g - 40 * math.sin(d(30))
show("2023 Q6", N=N, Ff_needed=2 * 40 + 40 * math.cos(d(30)), Ff_max=0.2 * N,
     a=(2 * 40 + 40 * math.cos(d(30)) - 0.15 * N) / m)

# ---- Ch13 curves
t = 10
v = 0.0625 * t * t
show("L21 Ex1 boat", v=v, Ft=540 * 0.125 * t, Fn=540 * v * v / 40)
# hollow tube (lecture): m 0.2, w 4, wdot -2, r 0.8, rdot -2, rddot 4
m, w, wd, r, rd, rdd = 0.2, 4, -2, 0.8, -2, 4
show("L21 Ex2 tube", T=-m * (rdd - r * w * w), Ftheta=m * (r * wd + 2 * rd * w))
# Supp 2024 Q6: m 0.4, w 5, wdot -3, r 0.9, rdot -2.5, rddot +4
m, w, wd, r, rd, rdd = 0.4, 5, -3, 0.9, -2.5, 4
show("Supp2024 Q6 tube", T_correct=-m * (rdd - r * w * w), T_memo=-m * (rdd - r * wd * wd),
     Ftheta=m * (r * wd + 2 * rd * w))
show("bank example", theta_deg=math.degrees(math.atan(25**2 / (100 * g))))

# ---- Ch14 work-energy, power
show("L25 Ex1 collar", Ug=6 * g * 0.55, Us=-0.5 * 12000 * 0.05**2,
     v=math.sqrt(2 * (6 * g * 0.55 - 0.5 * 12000 * 0.05**2) / 6))
N = 360 * g * math.cos(d(30))
T = 0.5 * N + 360 * g * math.sin(d(30))
show("L27 Ex1 winch", N=N, T=T, Pout=T * 1.2, Pin=T * 1.2 / 0.8)
show("L27 Ex2 escalator", Pout=30 / 60 * 65 * g * 7, eff=30 / 60 * 65 * g * 7 / 3000)
show("M&K 3/133 elevator", Pin=1000 * g * 3 / 0.8)

# ---- Ch15 impulse-momentum
Rx = (0.06 * 21 * math.cos(d(15)) + 0.06 * 15) / 0.02
Ry = (0.06 * 21 * math.sin(d(15)) + 0.06 * g * 0.02) / 0.02
show("L28 Ex1 tennis", Rx=Rx, Ry=Ry, R=math.hypot(Rx, Ry), ang=math.degrees(math.atan2(Ry, Rx)))
v2 = 10 * 15 / 25
show("L28 Ex2 blocks", v2=v2, x=math.sqrt(25 * v2**2 / 10000))
show("L29 Ex1 spheres", impulse=0.25 * 16 + 0.8 * 4, v=(0.25 * 16 + 0.8 * 4) / (4 * 0.6 * 5))
show("L29 Ex2 clay", H1=0.012 * 2.5 * 0.05, w=0.012 * 2.5 * 0.05 / (0.012 * 0.05**2 + 0.08 * 0.1**2))

# ---- Ch16 impact
show("L30 TPS1", vB2=(1 * 10 - 3 * 4) / 1, e=(4 - (1 * 10 - 3 * 4)) / 10)
vy = math.sqrt(2 * g * 0.9)
show("L30 Ex1 ball", vy_in=vy, vy_out=0.8 * vy, v=math.hypot(2.4, 0.8 * vy), h=(0.8 * vy)**2 / (2 * g))
mom = 6 - 10 * math.cos(d(30))
sep = 0.75 * (6 + 10 * math.cos(d(30)))
vBx = (mom + sep) / 2
vAx = mom - vBx
show("L30 Ex2 pucks", vAx=vAx, vBx=vBx, vB=math.hypot(vBx, 5), thB=math.degrees(math.atan2(5, vBx)))
# Supp exam spheres: A 20 kg at 4 m/s ->, B 5 kg at 15 m/s <-, e 0.6, line 55.15 deg from vertical
s, c = math.sin(d(55.15)), math.cos(d(55.15))
uA, uB = 4 * s, -15 * s
mA, mB, e = 20, 5, 0.6
vA_par = (mA * uA + mB * uB - mB * e * (uA - uB)) / (mA + mB)
vB_par = vA_par + e * (uA - uB)
vA_perp = 4 * c
show("Supp spheres", uA=uA, uB=uB, vA_par=vA_par, vB_par=vB_par, vA_perp=vA_perp,
     vA=math.hypot(vA_par, vA_perp), ang_to_line=math.degrees(math.atan2(vA_perp, abs(vA_par))))
# Supp 2025 Q5 putty
vP = math.sqrt(2 * g * 2)
v3 = 2 * vP / 20
x0 = 18 * g / (2 * 1200)
T3 = 0.5 * 20 * v3**2
Ve3 = 0.5 * 2400 * x0**2
# T3 + 20 g delta + Ve3 = 0.5*2400*(delta + x0)^2
A, B, C = 1200, 2400 * x0 - 20 * g, 1200 * x0**2 - T3 - Ve3
delta = (-B + math.sqrt(B * B - 4 * A * C)) / (2 * A)
show("Supp2025 putty", vP=vP, v3=v3, x0=x0, T3=T3, Ve3=Ve3, delta=delta,
     energy_lost=0.5 * 2 * vP**2 - T3)

# ---- Ch17 MoI
I_O = 3 * 0.8**2 / 3 + 0.5 * 5 * 0.1**2 + 5 * 0.8**2
xG = (3 * 0.4 + 5 * 0.8) / 8
show("pendulum MoI", I_O=I_O, xG=xG, I_G=I_O - 8 * xG**2)

# ---- Ch18 translation
th = math.atan2(4 * math.sin(d(60)), 4 * math.cos(d(60)) + 2)
T = (60 * 5 * 2 * math.sin(d(60)) + 60 * g * 1) / (2 * math.sin(th))
Ax = T * math.cos(th) - 60 * 5
Ay = 60 * g + T * math.sin(th)
show("Boom on bakkie", theta=math.degrees(th), T=T, Ax=Ax, Ay=Ay, A=math.hypot(Ax, Ay))
show("Wheelie TPS", F=295 * 5)

# ---- Ch19 fixed axis
m, L = 4, 1.2
al = 3 * g / (2 * L)
show("Rod released", I_O=m * L * L / 3, alpha=al, aG=al * L / 2, O=m * g - m * al * L / 2)
m, k = 300, 2.32
I_O = k * k * m
al = m * g * 1.8 / I_O
rG = math.hypot(1.8, 0.9)
beta = math.atan2(0.9, 1.8)
Ft = m * g * math.cos(beta) - m * al * rG
Fn = m * g * math.sin(beta)
show("I-beam", I_O=I_O, alpha=al, rG=rG, beta=math.degrees(beta), Ft=Ft, Fn=Fn, F=math.hypot(Ft, Fn))

# ---- Ch20 general plane motion
m, r, th = 3.6, 0.15, d(30)
aG = 2 / 3 * g * math.sin(th)
show("Rolling cylinder", aG=aG, alpha=aG / r, Ff=m * g * math.sin(th) / 3,
     Ffmax=0.3 * m * g * math.cos(th))
m, k, r, th = 10, 0.18, 0.2, d(60)
a_roll = g * math.sin(th) / (1 + k * k / (r * r))
show("Wheel 60 deg: rolling check", a_roll=a_roll, F_needed=m * k * k * a_roll / (r * r),
     F_max=0.35 * m * g * math.cos(th))
N = m * g * math.cos(th)
show("Wheel 60 deg: slipping", N=N, alpha=0.3 * N * r / (m * k * k), aO=g * math.sin(th) - 0.3 * g * math.cos(th))
show("Rod+hoop", alpha=3 * g / (8 * 0.25))
mtot = 1.2
IG = 1 / 12 * 0.6 * 0.5**2 + 0.6 * 0.175**2 + 0.5 * 0.6 * 0.1**2 + 0.6 * 0.175**2
show("Pushed body", IG=IG, aG=6 / 1.2, alpha=6 * 0.425 / IG, aA=6 / 1.2 + 0.425 * 6 * 0.425 / IG)

print("\n".join(out))
