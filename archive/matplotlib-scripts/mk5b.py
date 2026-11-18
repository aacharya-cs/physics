import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # style.py sits beside this script
import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle, Arc
from style import *

OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'figs'))  # repo-root figs/
BLK = '#93C5C6'          # block fill used across the volume


def blk(ax, cx, cy, w, h, ang=0.0, fc=BLK):
    """block centred at (cx, cy), rotated by ang degrees"""
    t = np.deg2rad(ang)
    R = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
    pts = np.array([[-w/2, -h/2], [w/2, -h/2], [w/2, h/2], [-w/2, h/2]]) @ R.T + [cx, cy]
    ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=STEEL, lw=0.9, zorder=4))


# ------------------------------------------------------------- normal_force
def normal_force():
    fig, ax = newax(6.3, 3.35)
    title(ax, r'The normal force adjusts: it is not always $mg$')
    xs = [0.0, 3.1, 6.2]
    heads = ['Flat surface', 'Incline', 'Pushed down']
    th = 28
    for x, hd in zip(xs, heads):
        lab(ax, x + 1.0, 3.62, hd, fs=8.0, style='italic')
        ax.plot([x - 0.15, x + 2.15], [1.86, 1.86], color=GREY, lw=0.7, ls=(0, (3, 3)))
        lab(ax, x + 2.12, 1.98, 'isolate', c=STEEL, fs=6.6, ha='right')

    # --- scenes (top row)
    ground(ax, xs[0] - 0.1, xs[0] + 2.1, 2.2, n=14, d=0.09)
    blk(ax, xs[0] + 1.0, 2.38, 0.66, 0.36)

    x0 = xs[1]
    ax.add_patch(Polygon([(x0 - 0.1, 2.05), (x0 + 2.0, 2.05), (x0 + 2.0, 2.05 + 2.1*np.tan(np.deg2rad(th)))],
                         closed=True, fc='#E1E7EF', ec=INK, lw=1.1, zorder=2))
    t = np.deg2rad(th)
    px = x0 + 0.95; py = 2.05 + 1.05*np.tan(t)
    blk(ax, px - 0.17*np.sin(t), py + 0.17*np.cos(t), 0.40, 0.26, ang=th)

    ground(ax, xs[2] - 0.1, xs[2] + 2.1, 2.2, n=14, d=0.09)
    blk(ax, xs[2] + 1.0, 2.38, 0.66, 0.36)
    arr(ax, xs[2] + 1.85, 3.02, xs[2] + 1.40, 2.62, c=ACC, lw=1.4)
    lab(ax, xs[2] + 1.92, 3.08, r'$F$', c=ACC, fs=8.0, ha='left')

    # --- free-body diagrams (bottom row)
    # flat
    cx, cy = xs[0] + 1.0, 0.50
    blk(ax, cx, cy, 0.62, 0.34)
    arr(ax, cx - 0.12, cy + 0.17, cx - 0.12, cy + 0.95, c=FOR, lw=1.5)
    lab(ax, cx - 0.24, cy + 0.80, r'$N$', c=FOR, fs=8.0, ha='right')
    arr(ax, cx + 0.12, cy, cx + 0.12, cy - 0.85, c=CRIM, lw=1.5)
    lab(ax, cx + 0.24, cy - 0.62, r'$mg$', c=CRIM, fs=8.0, ha='left')
    lab(ax, cx, -0.62, r'$N=mg$', fs=8.4)

    # incline
    cx, cy = xs[1] + 1.0, 0.50
    blk(ax, cx, cy, 0.56, 0.32, ang=th)
    nvec = np.array([-np.sin(t), np.cos(t)])
    arr(ax, cx, cy, cx + 0.95*nvec[0], cy + 0.95*nvec[1], c=FOR, lw=1.5)
    lab(ax, cx + 1.05*nvec[0] - 0.08, cy + 1.05*nvec[1] + 0.06, r'$N$', c=FOR, fs=8.0, ha='right')
    arr(ax, cx + 0.08, cy, cx + 0.08, cy - 0.88, c=CRIM, lw=1.5)
    lab(ax, cx + 0.20, cy - 0.65, r'$mg$', c=CRIM, fs=8.0, ha='left')
    lab(ax, cx, -0.62, r'$N=mg\cos\theta$', fs=8.4)

    # pushed down
    cx, cy = xs[2] + 1.0, 0.50
    blk(ax, cx, cy, 0.62, 0.34)
    arr(ax, cx - 0.16, cy + 0.17, cx - 0.16, cy + 0.95, c=FOR, lw=1.5)
    lab(ax, cx - 0.28, cy + 0.80, r'$N$', c=FOR, fs=8.0, ha='right')
    arr(ax, cx + 0.62, cy + 0.80, cx + 0.22, cy + 0.27, c=ACC, lw=1.4)
    lab(ax, cx + 0.66, cy + 0.84, r'$F$', c=ACC, fs=8.0, ha='left')
    arr(ax, cx + 0.10, cy, cx + 0.10, cy - 0.85, c=CRIM, lw=1.5)
    lab(ax, cx + 0.22, cy - 0.62, r'$mg$', c=CRIM, fs=8.0, ha='left')
    lab(ax, cx, -0.62, r'$N=mg+F_{\perp}$', fs=8.4)

    ax.set_xlim(-0.35, 8.55); ax.set_ylim(-0.88, 3.85)
    save(fig, f'{OUT}/normal_force.pdf')


# --------------------------------------------------------------- nif_groove
def nif_groove():
    fig, ax = newax(6.1, 3.15)
    title(ax, 'Same bead, two frames: the rotating frame is far easier here')
    R = 1.25
    for k, (cx, head, hc) in enumerate(((0.0, 'GROUND frame (inertial)', FOR),
                                       (3.25, 'ROTATING frame (non-inertial)', CRIM))):
        lab(ax, cx, 1.92, head, c=hc, fs=8.0, style='italic')
        ax.add_patch(Circle((cx, 0), R, fc='#EEF2F7', ec=INK, lw=1.3, zorder=1))
        ax.add_patch(Arc((cx, 0), 2*R*0.84, 2*R*0.84, theta1=40, theta2=140, color=PLUM, lw=1.3, zorder=3))
        arr(ax, cx - 0.66, 0.85, cx - 0.78, 0.74, c=PLUM, lw=1.2, ms=7)
        lab(ax, cx - 0.86, 0.98, r'$\omega$', c=PLUM, fs=8.4)
        # the radial groove
        ax.plot([cx, cx + R*0.95], [0, 0], color='#A0AEBB', lw=4.2, solid_capstyle='butt', zorder=2)
        ax.add_patch(Circle((cx, 0), 0.045, fc=INK, ec='none', zorder=6))
        bx = cx + 0.62
        ax.add_patch(Circle((bx, 0), 0.09, fc=TEAL, ec=INK, lw=0.9, zorder=7))
        lab(ax, bx - 0.02, -0.26, r'$x$', c=STEEL, fs=7.6)
        # normal force from the groove wall (sideways, perpendicular to the groove)
        arr(ax, bx, 0.09, bx, 0.68, c=PRIM, lw=1.4, z=8)
        lab(ax, bx + 0.12, 0.56, r'$N$', c=PRIM, fs=8.0, ha='left')
        if k == 1:
            arr(ax, bx + 0.09, 0.0, bx + 0.72, 0.0, c=CRIM, lw=1.6, z=8)
            lab(ax, bx + 0.48, -0.24, r'$m\omega^{2}x$', c=CRIM, fs=7.6)
    lab(ax, 0.0, -1.58, 'only a REAL sideways push;', fs=7.4)
    lab(ax, 0.0, -1.84, 'the path is a spiral', fs=7.4)
    lab(ax, 3.25, -1.58, 'add the CENTRIFUGAL pseudo-force;', c=CRIM, fs=7.4)
    lab(ax, 3.25, -1.84, r'then the bead simply slides out along $x$', c=CRIM, fs=7.4)
    ax.set_xlim(-1.75, 5.0); ax.set_ylim(-2.05, 2.15)
    save(fig, f'{OUT}/nif_groove.pdf')


# --------------------------------------------------------------- work_angle
def work_angle():
    fig, ax = newax(6.1, 2.2)
    title(ax, r'$W=Fd\cos\theta$: the angle sets the sign')
    cases = [(35, FOR, r'$\theta<90^\circ$: speeds up'),
             (90, STEEL, r'$\theta=90^\circ$: no work'),
             (148, CRIM, r'$\theta>90^\circ$: slows down')]
    for k, (ang, col, txt) in enumerate(cases):
        x = k*2.9
        lab(ax, x + 1.0, 1.70, txt, c=col, fs=7.8, style='italic')
        ground(ax, x - 0.05, x + 2.15, 0.0, n=15, d=0.09)
        blk(ax, x + 0.62, 0.17, 0.56, 0.34)
        t = np.deg2rad(ang)
        ox, oy = x + 0.62, 0.17
        arr(ax, ox, oy, ox + 0.92*np.cos(t), oy + 0.92*np.sin(t), c=col, lw=1.6, z=6)
        lab(ax, ox + 1.04*np.cos(t) + (0.06 if ang < 90 else -0.06), oy + 1.04*np.sin(t) + 0.06,
            r'$\vec{F}$', c=col, fs=8.4)
        ax.add_patch(Arc((ox, oy), 0.48, 0.48, theta1=0, theta2=ang, color=INK, lw=0.9, zorder=5))
        lab(ax, ox + 0.36*np.cos(t/2) + 0.04, oy + 0.36*np.sin(t/2) + 0.02, r'$\theta$', fs=7.4)
        arr(ax, x + 0.30, -0.40, x + 1.55, -0.40, c=PRIM, lw=1.4)
        lab(ax, x + 0.92, -0.62, r'$\vec{d}$', c=PRIM, fs=8.4)
    ax.set_xlim(-0.2, 8.15); ax.set_ylim(-0.85, 1.92)
    save(fig, f'{OUT}/work_angle.pdf')


# ---------------------------------------------------------------- moid_ring
def moid_ring():
    fig, ax = newax(5.6, 3.0)
    title(ax, 'The ring two ways: the second needs no integral either')
    R = 1.0
    ph = np.linspace(0, 2*np.pi, 300)
    # left: central axis (out of the page)
    cx = 0.0
    lab(ax, cx, 1.95, 'About the central axis', fs=8.0, style='italic')
    lab(ax, cx, 1.55, r'$I_z=MR^{2}$', fs=9.0)
    ax.plot(cx + R*np.cos(ph), R*np.sin(ph), color=PRIM, lw=2.6, zorder=3)
    for a in (25, 112, 205, 290):
        t = np.deg2rad(a)
        ax.plot([cx, cx + R*np.cos(t)], [0, R*np.sin(t)], color='#A0AEBB', lw=0.9, ls=(0, (3, 2)), zorder=2)
        ax.add_patch(Circle((cx + R*np.cos(t), R*np.sin(t)), 0.055, fc=TEAL, ec='none', zorder=5))
    ax.add_patch(Circle((cx, 0), 0.09, fc='white', ec=CRIM, lw=1.3, zorder=6))
    ax.add_patch(Circle((cx, 0), 0.03, fc=CRIM, ec='none', zorder=7))
    lab(ax, cx + 0.45, 0.42, r'$R$', fs=8.0)
    lab(ax, cx, -1.38, r'every element at the same $R$', c=STEEL, fs=7.6)
    # right: diameter axes in the plane
    cx = 3.1
    lab(ax, cx, 1.95, 'About a diameter', fs=8.0, style='italic')
    lab(ax, cx, 1.55, r'$I_d=\frac{1}{2}MR^{2}$', fs=9.0)
    ax.plot(cx + R*np.cos(ph), R*np.sin(ph), color=PRIM, lw=2.6, zorder=3)
    ax.plot([cx - 1.45, cx + 1.45], [0, 0], color=CRIM, lw=1.4, ls=(0, (5, 3)), zorder=4)
    ax.plot([cx, cx], [-1.25, 1.25], color=FOR, lw=1.4, ls=(0, (5, 3)), zorder=4)
    lab(ax, cx + 1.40, 0.16, r'$x$', c=CRIM, fs=8.0)
    lab(ax, cx + 0.14, 1.18, r'$y$', c=FOR, fs=8.0)
    ax.add_patch(Circle((cx, 0), 0.09, fc='white', ec=PLUM, lw=1.3, zorder=6))
    ax.add_patch(Circle((cx, 0), 0.03, fc=PLUM, ec='none', zorder=7))
    lab(ax, cx, -1.38, r'$I_z=I_x+I_y=2I_d$', c=STEEL, fs=7.6)
    ax.set_xlim(-1.7, 4.8); ax.set_ylim(-1.6, 2.15)
    save(fig, f'{OUT}/moid_ring.pdf')


# ----------------------------------------------------------- movable_pulley
def movable_pulley():
    fig, ax = newax(2.9, 3.4)
    title(ax, 'Movable pulley')
    Rp = 0.36
    # ceiling
    ax.plot([-1.05, 1.05], [2.4, 2.4], color=INK, lw=1.6)
    for i in range(12):
        xx = -1.05 + i*0.19
        ax.plot([xx, xx + 0.09], [2.4, 2.49], color=INK, lw=0.7)
    # string segments
    for sx in (-Rp, Rp):
        ax.plot([sx, sx], [0.9, 2.4], color=INK, lw=1.1, zorder=2)
        arr(ax, sx, 1.45, sx, 2.02, c=FOR, lw=1.5, z=5)
    lab(ax, -Rp - 0.16, 1.80, r'$T$', c=FOR, fs=8.4, ha='right')
    lab(ax, Rp + 0.16, 1.80, r'$T$', c=FOR, fs=8.4, ha='left')
    # pulley
    ax.add_patch(Circle((0, 0.9), Rp, fc='white', ec=INK, lw=1.6, zorder=4))
    ax.add_patch(Circle((0, 0.9), 0.04, fc=INK, ec='none', zorder=5))
    lab(ax, 0.62, 0.92, r'up: $2T$', c=FOR, fs=8.0, ha='left')
    # hanger + load
    ax.plot([0, 0], [0.9 - Rp, 0.18], color=INK, lw=1.1, zorder=2)
    blk(ax, 0, -0.04, 0.62, 0.44)
    lab(ax, 0, -0.04, 'load', fs=7.6)
    arr(ax, 0, -0.26, 0, -0.80, c=CRIM, lw=1.5)
    lab(ax, 0.12, -0.66, r'$W$', c=CRIM, fs=8.4, ha='left')
    lab(ax, 0, -1.08, r'$2T=W$: half the force, twice the distance', c=STEEL, fs=7.0)
    ax.set_xlim(-1.35, 1.35); ax.set_ylim(-1.3, 2.62)
    save(fig, f'{OUT}/movable_pulley.pdf')


if __name__ == '__main__':
    normal_force(); nif_groove(); work_angle(); moid_ring(); movable_pulley()
    print('redrew 5')
