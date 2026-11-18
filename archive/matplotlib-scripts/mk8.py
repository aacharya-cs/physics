import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # style.py sits beside this script
import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle, Arc, Wedge
import matplotlib.pyplot as plt
from style import *

OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'figs'))  # repo-root figs/
BLK = '#93C5C6'


def blk(ax, cx, cy, w, h, ang=0.0, fc=BLK, z=4):
    t = np.deg2rad(ang)
    R = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
    pts = np.array([[-w/2, -h/2], [w/2, -h/2], [w/2, h/2], [-w/2, h/2]]) @ R.T + [cx, cy]
    ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=STEEL, lw=0.9, zorder=z))


# ---------------------------------------------------- kin_projectile_height
def kin_projectile_height():
    fig, ax = newax(5.4, 3.0)
    title(ax, 'Projectile launched from a height')
    g, v0, th, H0 = 9.8, 14.0, np.deg2rad(50), 6.0
    vx, vy = v0*np.cos(th), v0*np.sin(th)
    T = (vy + np.sqrt(vy**2 + 2*g*H0))/g
    t = np.linspace(0, T, 300)
    X = vx*t; Y = H0 + vy*t - 0.5*g*t**2
    s = 0.17                                    # metres -> plot units
    X, Y = X*s, Y*s
    ta = vy/g; xa, ya = vx*ta*s, (H0 + vy**2/(2*g))*s
    tl = 2*vy/g; xl = vx*tl*s                   # back at launch level

    # cliff and ground
    ax.add_patch(Rectangle((-0.62, 0), 0.62, H0*s, fc='#E1E7EF', ec=INK, lw=1.1, zorder=2))
    ground(ax, -0.85, X[-1] + 0.5, 0.0, n=30, d=0.10)
    ax.plot([0, xl + 0.3], [H0*s, H0*s], color=GREY, lw=0.8, ls=(0, (4, 3)), zorder=1)
    lab(ax, xl + 0.34, H0*s - 0.14, 'launch level', c=STEEL, fs=7.0, ha='left')

    # ascent and descent coloured differently
    up = t <= ta
    ax.plot(X[up], Y[up], color=ACC, lw=2.0, zorder=4)
    ax.plot(X[~up], Y[~up], color=PRIM, lw=2.0, zorder=4)
    ax.add_patch(Circle((xa, ya), 0.06, fc=CRIM, ec='none', zorder=6))
    lab(ax, xa, ya + 0.24, 'apex', c=CRIM, fs=7.6)
    ax.add_patch(Circle((xl, H0*s), 0.05, fc=STEEL, ec='none', zorder=6))
    ax.add_patch(Circle((X[-1], 0), 0.06, fc=PRIM, ec='none', zorder=6))

    arr(ax, 0, H0*s, 0.62*np.cos(th), H0*s + 0.62*np.sin(th), c=PLUM, lw=1.6, z=7)
    lab(ax, 0.06, H0*s + 0.40, r'$v_0$', c=PLUM, fs=8.4, ha='right')
    darr(ax, -0.82, 0, -0.82, H0*s)
    lab(ax, -0.92, H0*s/2, r'$H_0$', c=STEEL, fs=8.4, ha='right')

    lab(ax, xa*0.42, ya*0.98, 'ascent', c=ACC, fs=7.4, ha='right')
    lab(ax, X[-1]*0.80 + 0.30, ya*0.80, 'descent: longer, and\nit falls PAST the launch level',
        c=PRIM, fs=7.2, ha='left')
    ax.set_xlim(-1.35, X[-1] + 2.6); ax.set_ylim(-0.25, ya + 0.55)
    save(fig, f'{OUT}/kin_projectile_height.pdf')


# ------------------------------------------------------------ incline_pulley
def incline_pulley():
    fig, ax = newax(4.6, 3.0)
    title(ax, 'The incline version of the same machine')
    th = np.deg2rad(30)
    L = 3.0
    top = np.array([L, L*np.tan(th)])
    ax.add_patch(Polygon([(0, 0), (L, 0), tuple(top)], closed=True, fc='#E1E7EF', ec=INK, lw=1.2, zorder=1))
    ax.plot([-0.2, L + 0.2], [0, 0], color=INK, lw=1.2)
    ax.add_patch(Arc((0, 0), 1.1, 1.1, theta1=0, theta2=30, color=INK, lw=1.0))
    lab(ax, 0.72, 0.17, r'$\theta$', fs=8.6)

    # pulley at the top corner
    Rp = 0.17
    P = top + np.array([0.0, Rp])
    ax.add_patch(Circle(P, Rp, fc='white', ec=INK, lw=1.3, zorder=5))
    ax.add_patch(Circle(P, 0.03, fc=INK, ec='none', zorder=6))
    ax.plot([L, L], [top[1], P[1]], color=INK, lw=1.0, zorder=4)

    # block m1 on the slope
    d = np.array([np.cos(th), np.sin(th)]); n = np.array([-np.sin(th), np.cos(th)])
    s1 = 1.55
    C1 = s1*d + 0.19*n
    blk(ax, C1[0], C1[1], 0.52, 0.36, ang=30)
    lab(ax, C1[0] - 0.02, C1[1] + 0.03, r'$m_1$', fs=8.2, z=6)
    # string from block to pulley (parallel to slope), then down
    a0 = C1 + 0.26*d
    tp = P + Rp*np.array([-np.sin(th), np.cos(th)])
    ax.plot([a0[0], tp[0]], [a0[1], tp[1]], color=INK, lw=1.0, zorder=3)
    ax.plot([P[0] + Rp, P[0] + Rp], [P[1], 0.95], color=INK, lw=1.0, zorder=3)
    blk(ax, P[0] + Rp, 0.72, 0.42, 0.44, fc='#C7B2E3')
    lab(ax, P[0] + Rp, 0.72, r'$m_2$', fs=8.2, z=6)
    arr(ax, P[0] + Rp, 0.50, P[0] + Rp, 0.05, c=CRIM, lw=1.4)
    lab(ax, P[0] + Rp + 0.12, 0.18, r'$m_2g$', c=CRIM, fs=7.8, ha='left')
    # down-slope component on m1
    arr(ax, C1[0], C1[1], C1[0] - 0.62*d[0], C1[1] - 0.62*d[1], c=CRIM, lw=1.4, z=7)
    lab(ax, C1[0] - 0.80*d[0] - 0.02, C1[1] - 0.80*d[1] + 0.22, r'$m_1g\sin\theta$', c=CRIM, fs=7.6, ha='right')

    lab(ax, 1.55, -0.42, r'driving term: $m_2g-m_1g\sin\theta$', fs=8.2)
    lab(ax, 1.55, -0.72, r'set $\theta=0$ for the flat table, $\theta=90^\circ$ for the Atwood machine',
        c=STEEL, fs=7.2)
    ax.set_xlim(-0.3, L + 0.75); ax.set_ylim(-0.95, top[1] + 0.55)
    save(fig, f'{OUT}/incline_pulley.pdf')


# -------------------------------------------------------------------- hookes
def hookes():
    fig, ax = plt.subplots(figsize=(4.6, 2.9))
    ax.set_title("Hooke's law: the force always restores", fontsize=7.8, color=INK, style='italic', pad=6)
    x = np.linspace(-1, 1, 50)
    ax.plot(x, -x, color=CRIM, lw=2.0, zorder=3)
    ax.axhline(0, color=INK, lw=0.9); ax.axvline(0, color=INK, lw=0.9)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlim(-1.15, 1.15); ax.set_ylim(-1.15, 1.15)
    ax.annotate('', xy=(-0.62, 0.62), xytext=(-0.62, 0.0),
                arrowprops=dict(arrowstyle='-|>', color=FOR, lw=1.5))
    ax.annotate('', xy=(0.62, -0.62), xytext=(0.62, 0.0),
                arrowprops=dict(arrowstyle='-|>', color=FOR, lw=1.5))
    ax.text(-1.08, -0.24, 'compressed ($x<0$):', color=FOR, fontsize=7.4, ha='left')
    ax.text(-1.08, -0.38, 'force pushes outward', color=FOR, fontsize=7.4, ha='left')
    ax.text(0.68, -0.32, 'stretched ($x>0$):', color=FOR, fontsize=7.4, ha='left')
    ax.text(0.68, -0.46, 'force pulls back', color=FOR, fontsize=7.4, ha='left')
    ax.text(0.40, -0.98, r'$F=-kx$', color=CRIM, fontsize=9.0)
    ax.text(1.12, 0.05, r'$x$', color=INK, fontsize=8.6, ha='right')
    ax.text(0.04, 1.08, r'$F$', color=INK, fontsize=8.6)
    ax.text(0.20, 0.82, 'slope $=-k$', color=STEEL, fontsize=7.2)
    save(fig, f'{OUT}/hookes.pdf')


# -------------------------------------------------------------- angle_repose
def angle_repose():
    fig, ax = newax(4.6, 2.75)
    title(ax, 'Angle of repose = angle of friction')
    th = np.deg2rad(30); L = 3.2
    ax.add_patch(Polygon([(0, 0), (L, 0), (L, L*np.tan(th))], closed=True, fc='#E1E7EF', ec=INK, lw=1.2, zorder=1))
    ax.plot([-0.2, L + 0.2], [0, 0], color=INK, lw=1.2)
    ax.add_patch(Arc((0, 0), 1.0, 1.0, theta1=0, theta2=30, color=INK, lw=1.0))
    lab(ax, 0.70, 0.16, r'$\theta_r$', fs=8.4)
    d = np.array([np.cos(th), np.sin(th)]); n = np.array([-np.sin(th), np.cos(th)])
    s1 = 1.85
    C = s1*d + 0.21*n; base = s1*d
    blk(ax, C[0], C[1], 0.56, 0.42, ang=30)
    # forces from the contact point / centre
    arr(ax, base[0], base[1], base[0] + 0.85*n[0], base[1] + 0.85*n[1], c=FOR, lw=1.5, z=7)
    lab(ax, base[0] + 0.95*n[0] - 0.06, base[1] + 0.95*n[1] + 0.06, r'$N$', c=FOR, fs=8.4, ha='right')
    arr(ax, base[0] + 0.30*d[0], base[1] + 0.30*d[1], base[0] + 1.05*d[0], base[1] + 1.05*d[1], c=ACC, lw=1.5, z=7)
    lab(ax, base[0] + 1.10*d[0] + 0.04, base[1] + 1.10*d[1] + 0.10, r'$\mu_sN$', c=ACC, fs=8.2, ha='left')
    arr(ax, C[0], C[1], C[0], C[1] - 0.95, c=CRIM, lw=1.5, z=7)
    lab(ax, C[0] + 0.10, C[1] - 0.78, r'$mg$', c=CRIM, fs=8.2, ha='left')
    lab(ax, 1.65, -0.40, r'$mg\sin\theta_r=\mu_s\,mg\cos\theta_r\;\Rightarrow\;\tan\theta_r=\mu_s$', fs=8.2)
    lab(ax, 1.65, -0.70, 'the mass cancels: heavy and light blocks slip at the same angle', c=STEEL, fs=7.2)
    ax.set_xlim(-0.3, L + 0.45); ax.set_ylim(-0.92, L*np.tan(th) + 0.25)
    save(fig, f'{OUT}/angle_repose.pdf')


# ----------------------------------------------------------------- cd_groove
def cd_groove():
    fig, ax = newax(3.6, 3.1)
    title(ax, 'Block in a circular groove')
    R = 1.25
    ph = np.linspace(0, 2*np.pi, 300)
    ax.plot(R*np.cos(ph)*1.04, R*np.sin(ph)*1.04, color='#B8C2CC', lw=5.0, zorder=1)
    ax.plot(R*np.cos(ph)*0.96, R*np.sin(ph)*0.96, color='#B8C2CC', lw=5.0, zorder=1)
    ax.plot(R*np.cos(ph), R*np.sin(ph), color=PRIM, lw=1.0, ls=(0, (4, 3)), zorder=2)
    ax.add_patch(Circle((0, 0), 0.04, fc=INK, ec='none', zorder=5))
    blk(ax, R, 0, 0.22, 0.28, z=6)
    arr(ax, R - 0.12, 0, R - 0.75, 0, c=CRIM, lw=1.7, z=7)
    lab(ax, R - 0.46, 0.20, r'$N$', c=CRIM, fs=8.8)
    arr(ax, R, 0.16, R, 0.82, c=STEEL, lw=1.4, z=7)
    lab(ax, R + 0.12, 0.70, r'$v$', c=STEEL, fs=8.4, ha='left')
    darr(ax, 0.04, -0.20, R - 0.12, -0.20, c=PRIM)
    lab(ax, R/2, -0.40, r'$r=25$ cm', c=PRIM, fs=7.8)
    lab(ax, 0, -1.68, 'the side wall is the ONLY horizontal force,', fs=7.6)
    lab(ax, 0, -1.94, r'so $N=mv^{2}/r$', fs=7.8)
    ax.set_xlim(-1.6, 1.85); ax.set_ylim(-2.12, 1.55)
    save(fig, f'{OUT}/cd_groove.pdf')


# -------------------------------------------------------------------- cm_boat
def cm_boat():
    fig, ax = newax(5.0, 3.0)
    title(ax, 'No external force: the centre of mass cannot move')
    xcm = 2.55
    for row, (y, lbl, boat_x, person_x) in enumerate(((1.55, 'before', 1.2, 1.55),
                                                      (0.0, 'after', 0.55, 3.25))):
        lab(ax, -0.25, y + 0.15, lbl, c=STEEL, fs=8.4, ha='left')
        ax.add_patch(Rectangle((boat_x, y), 3.0, 0.26, fc='#AFD3D3', ec=STEEL, lw=0.9, zorder=2))
        ax.plot([person_x, person_x], [y + 0.26, y + 0.78], color=INK, lw=2.0, zorder=3)
        ax.add_patch(Circle((person_x, y + 0.88), 0.11, fc=PLUM, ec=INK, lw=0.9, zorder=4))
        # boat's own centre marker
        ax.add_patch(Polygon([(boat_x + 1.5 - 0.08, y - 0.06), (boat_x + 1.5 + 0.08, y - 0.06), (boat_x + 1.5, y - 0.22)],
                             closed=True, fc=STEEL, ec='none', zorder=3))
    ax.plot([xcm, xcm], [-0.35, 2.85], color=CRIM, lw=1.2, ls=(0, (4, 3)), zorder=1)
    lab(ax, xcm + 0.08, 2.92, 'CM of person + boat stays here', c=CRIM, fs=7.6, ha='left')
    arr(ax, 1.85, 2.62, 3.15, 2.62, c=FOR, lw=1.5)
    lab(ax, 1.70, 2.62, 'person walks', c=FOR, fs=7.6, ha='right')
    arr(ax, 3.85, -0.32, 3.20, -0.32, c=PRIM, lw=1.5)
    lab(ax, 3.95, -0.32, 'boat slides back', c=PRIM, fs=7.6, ha='left')
    lab(ax, 2.4, -0.78, r'$m\,\Delta x_{\mathrm{person}}+M\,\Delta x_{\mathrm{boat}}=0$', fs=8.2)
    ax.set_xlim(-0.4, 5.6); ax.set_ylim(-1.0, 3.12)
    save(fig, f'{OUT}/cm_boat.pdf')


# --------------------------------------------------------------- cmd_triangle
def cmd_triangle():
    fig, ax = newax(3.6, 3.0)
    title(ax, 'Slicing the triangle into strips')
    b, h = 2.4, 2.2
    ax.add_patch(Polygon([(-b/2, 0), (b/2, 0), (0, h)], closed=True, fc='#CFE3E3', ec=INK, lw=1.2, zorder=1))
    ax.plot([0, 0], [-0.15, h + 0.15], color=STEEL, lw=0.8, ls=(0, (4, 3)), zorder=2)
    y = 1.22; dy = 0.13
    w = b*(1 - y/h)
    ax.add_patch(Rectangle((-w/2, y), w, dy, fc=CRIM, ec=CRIM, lw=0.8, alpha=0.75, zorder=3))
    ax.add_patch(Circle((0, y + dy/2), 0.04, fc=INK, ec='none', zorder=5))
    # y measured from the base
    arr(ax, -b/2 - 0.35, 0, -b/2 - 0.35, y, c=PRIM, lw=1.1, ms=6)
    ax.plot([-b/2 - 0.45, -w/2], [y, y], color=PRIM, lw=0.6, ls=(0, (2, 2)))
    lab(ax, -b/2 - 0.45, y/2, r'$y$', c=PRIM, fs=8.6, ha='right')
    # dy and width labels, placed outside the triangle
    ax.plot([w/2 + 0.04, w/2 + 0.45], [y + dy/2, y + 0.45], color=CRIM, lw=0.6)
    lab(ax, w/2 + 0.50, y + 0.52, r'$dy$', c=CRIM, fs=8.2, ha='left')
    darr(ax, -w/2, y + dy + 0.14, w/2, y + dy + 0.14, c=CRIM)
    lab(ax, -w/2 - 0.08, y + dy + 0.32, r'width $=b\,(1-y/h)$', c=CRIM, fs=7.4, ha='right')
    # centroid
    ax.add_patch(Circle((0, h/3), 0.05, fc=FOR, ec='none', zorder=6))
    ax.plot([0.06, 0.70], [h/3, h/3 - 0.30], color=FOR, lw=0.6)
    lab(ax, 0.74, h/3 - 0.34, r'$\bar y=h/3$', c=FOR, fs=8.2, ha='left')
    lab(ax, 0, -0.42, 'each strip\'s centre is on the axis; only its height $y$ matters', c=STEEL, fs=7.0)
    ax.set_xlim(-1.95, 1.95); ax.set_ylim(-0.65, h + 0.3)
    save(fig, f'{OUT}/cmd_triangle.pdf')


# --------------------------------------------------------------- nif_artgrav
def nif_artgrav():
    fig = plt.figure(figsize=(4.95, 2.35))
    fig.suptitle('Artificial gravity: the rotor of Section 10.2.3, scaled up to a spacecraft',
                 fontsize=7.8, color=INK, style='italic', y=0.99)
    # ---- left: the habitat
    ax = fig.add_axes([0.0, 0.02, 0.44, 0.86]); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('A rotating habitat', fontsize=7.6, color=INK, style='italic', pad=2)
    R, Ri = 1.0, 0.82
    ph = np.linspace(0, 2*np.pi, 300)
    ax.fill_between(R*np.cos(ph), R*np.sin(ph), color='#E3E8EE', zorder=1)
    ax.add_patch(Circle((0, 0), R, fc='#E3E8EE', ec=INK, lw=1.3, zorder=1))
    ax.add_patch(Circle((0, 0), Ri, fc='white', ec=INK, lw=1.0, zorder=2))
    for a in range(0, 360, 45):
        t = np.deg2rad(a)
        ax.plot([0.14*np.cos(t), Ri*np.cos(t)], [0.14*np.sin(t), Ri*np.sin(t)], color=GREY, lw=0.8, zorder=2)
    ax.add_patch(Circle((0, 0), 0.14, fc='#D0D9E3', ec=INK, lw=0.9, zorder=3))
    lab(ax, 0, 0, 'hub', fs=6.2, z=4)
    ax.add_patch(Arc((0, 0), 2.45, 2.45, theta1=60, theta2=120, color=PLUM, lw=1.3))
    arr(ax, -0.58, 1.08, -0.66, 1.02, c=PLUM, lw=1.2, ms=7)
    lab(ax, 0, 1.33, r'$\omega$', c=PLUM, fs=8.4)
    # astronaut standing on the rim floor at the bottom, head toward the hub
    ax.plot([0, 0], [-Ri, -Ri + 0.22], color=INK, lw=1.8, zorder=5)
    ax.add_patch(Circle((0, -Ri + 0.28), 0.055, fc=TEAL, ec=INK, lw=0.8, zorder=6))
    arr(ax, -0.12, -Ri, -0.12, -Ri + 0.42, c=FOR, lw=1.4, z=7)
    lab(ax, -0.18, -Ri + 0.36, r'$N$', c=FOR, fs=7.6, ha='right')
    # floater near the hub
    ax.add_patch(Circle((0.30, 0.28), 0.05, fc=PLUM, ec='none', zorder=5))
    # labels outside the wheel with leaders
    ax.plot([-0.14, -1.05], [-Ri + 0.20, -0.30], color=FOR, lw=0.6)
    lab(ax, -1.08, -0.18, 'floor pushes', c=FOR, fs=6.6, ha='right')
    lab(ax, -1.08, -0.34, 'INWARD: the only', c=FOR, fs=6.6, ha='right')
    lab(ax, -1.08, -0.50, 'real force', c=FOR, fs=6.6, ha='right')
    ax.plot([0.35, 1.05], [0.30, 0.62], color=PLUM, lw=0.6)
    lab(ax, 1.08, 0.66, 'floats here', c=PLUM, fs=6.6, ha='left')
    lab(ax, 1.08, 0.50, r'($r\approx0$)', c=PLUM, fs=6.6, ha='left')
    lab(ax, 0, -1.30, r'$g_{\mathrm{eff}}=\omega^{2}r$', fs=8.0)
    ax.set_xlim(-1.9, 1.9); ax.set_ylim(-1.5, 1.5)

    # ---- right: design penalty
    bx = fig.add_axes([0.55, 0.16, 0.42, 0.66])
    bx.set_title('Why real designs must be large', fontsize=7.6, color=INK, style='italic', pad=4)
    rpm = np.linspace(1, 7, 200)
    w = 2*np.pi*rpm/60
    r = 9.8/w**2
    bx.axvspan(1, 2, color=FOR, alpha=0.10); bx.axvspan(2, 6, color=AMBER, alpha=0.18); bx.axvspan(6, 7, color=CRIM, alpha=0.12)
    bx.semilogy(rpm, r, color=PRIM, lw=1.8)
    for rp, txt in ((2, '224 m'), (3, '99 m')):
        rr = 9.8/(2*np.pi*rp/60)**2
        bx.plot(rp, rr, 'o', color=PRIM, ms=3.5)
        bx.text(rp + 0.12, rr*1.25, txt, color=PRIM, fontsize=6.4)
    bx.plot(5.5, 32, 'o', color=CRIM, ms=4.5)
    bx.annotate('Endurance\n32 m, 5.5 rpm', xy=(5.5, 32), xytext=(3.7, 12), fontsize=6.4, color=CRIM,
                arrowprops=dict(arrowstyle='-', color=CRIM, lw=0.7))
    bx.text(1.5, 1600, 'comfortable', ha='center', fontsize=6.0, color=FOR)
    bx.text(4.0, 1600, 'tolerable with adaptation', ha='center', fontsize=6.0, color='#9A6A2E')
    bx.text(6.5, 1600, 'too fast', ha='center', fontsize=6.0, color=CRIM)
    bx.set_xlim(1, 7); bx.set_ylim(8, 3000)
    bx.set_xlabel('spin rate (rpm)', fontsize=7.0, color=INK)
    bx.set_ylabel(r'radius for $1\,g$ (m)', fontsize=7.0, color=INK)
    bx.tick_params(labelsize=6.4, colors=INK)
    for sp in ('top', 'right'): bx.spines[sp].set_visible(False)
    save(fig, f'{OUT}/nif_artgrav.pdf')


if __name__ == '__main__':
    kin_projectile_height(); incline_pulley(); hookes(); angle_repose()
    cd_groove(); cm_boat(); cmd_triangle(); nif_artgrav()
    print('redrew 8')
