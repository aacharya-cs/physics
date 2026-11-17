import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, Polygon, Rectangle, Wedge, Arc

INK   = '#102A43'
PRIM  = '#1F6FEB'
TEAL  = '#0E7C7B'
ACC   = '#E85D04'
CRIM  = '#C1121F'
FOR   = '#2D6A4F'
STEEL = '#486581'
PLUM  = '#7B2CBF'
AMBER = '#F4A261'
GREY  = '#9FB3C8'

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['DejaVu Serif'],
    'mathtext.fontset': 'dejavuserif',
    'savefig.transparent': True,
    'savefig.pad_inches': 0.02,
})


def newax(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax


def title(ax, t, y=1.0):
    ax.set_title(t, fontsize=7.4, color=INK, style='italic', pad=5, y=y)


def arr(ax, x0, y0, x1, y1, c=INK, lw=1.3, ms=7, ls='-', z=3, alpha=1.0):
    a = FancyArrowPatch((x0, y0), (x1, y1), arrowstyle='-|>',
                        mutation_scale=ms, color=c, lw=lw, linestyle=ls,
                        shrinkA=0, shrinkB=0, zorder=z, alpha=alpha)
    ax.add_patch(a)
    return a


def darr(ax, x0, y0, x1, y1, c=STEEL, lw=0.9, ms=6, z=2):
    a = FancyArrowPatch((x0, y0), (x1, y1), arrowstyle='<|-|>',
                        mutation_scale=ms, color=c, lw=lw,
                        shrinkA=0, shrinkB=0, zorder=z)
    ax.add_patch(a)
    return a


def lab(ax, x, y, s, c=INK, fs=7.2, ha='center', va='center', box=False,
        style='normal', weight='normal', z=6, rot=0):
    bb = dict(boxstyle='round,pad=0.18', fc='white', ec='#DDE3EA', lw=0.5) if box else None
    return ax.text(x, y, s, color=c, fontsize=fs, ha=ha, va=va, bbox=bb,
                   style=style, weight=weight, zorder=z, rotation=rot)


def block(ax, x, y, w, h, fc='#D9E2EC', ec=INK, lw=1.1, z=3, alpha=1.0):
    r = Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, zorder=z, alpha=alpha)
    ax.add_patch(r)
    return r


def ground(ax, x0, x1, y, n=22, d=0.09, c=INK, lw=1.1):
    ax.plot([x0, x1], [y, y], color=c, lw=lw, zorder=2)
    step = (x1 - x0) / n
    for i in range(n):
        xx = x0 + i * step
        ax.plot([xx, xx - d], [y, y - d], color=c, lw=0.7, zorder=2)


def halo(ax, x, y, r, c=AMBER, alpha=0.22, z=1):
    ax.add_patch(Circle((x, y), r, fc=c, ec='none', alpha=alpha, zorder=z))


def save(fig, path):
    fig.savefig(path, bbox_inches='tight', pad_inches=0.03)
    plt.close(fig)
