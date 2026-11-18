#!/usr/bin/env python3
"""Content census for the book (CLAUDE.md, verification protocol step 1).

Counts boxes, figures and words per chapter so a restructure can be checked
for silent losses.  Usage:

    python3 tools/census.py            # table for the working tree
    python3 tools/census.py DIR        # table for another copy of the repo
    python3 tools/census.py A B        # compare two copies, print differences
"""
import re
import sys
from pathlib import Path

KINDS = ['defbox', 'keybox', 'methodbox', 'tablebox', 'derivbox', 'exbox',
         'archq', 'challengebox', 'remarkbox', 'trapbox', 'motivbox']


def strip_comments(s):
    return re.sub(r'(?<!\\)%.*', '', s)


def census(root):
    root = Path(root)
    rows = {}
    for f in sorted((root / 'chapters').rglob('*.tex')):
        if f.name == 'volume.tex':
            continue
        s = strip_comments(f.read_text())
        r = {}
        for k in KINDS:
            if k == 'archq':
                r[k] = len(re.findall(r'\\archq\b', s))
            else:
                r[k] = len(re.findall(r'\\begin\{%s\}' % k, s))
        r['wex'] = len(re.findall(r'\\wex\b', s))
        r['figure'] = len(re.findall(r'\\begin\{figure\*?\}', s))
        r['incgfx'] = len(re.findall(r'\\includegraphics', s))
        r['tikz'] = len(re.findall(r'\\(?:input|figinput)\{figures/|\\tikzfig\{', s))
        r['equation'] = len(re.findall(r'\\begin\{(?:equation|align|gather)\*?\}', s))
        words = re.sub(r'\\[A-Za-z@]+', ' ', s)
        words = re.sub(r'[{}\[\]$&^_\\]', ' ', words)
        r['words'] = len(re.findall(r'[A-Za-z]{2,}', words))
        rows[str(f.relative_to(root / 'chapters'))[:-4]] = r
    return rows


def table(rows):
    cols = list(next(iter(rows.values())).keys())
    head = 'ch   ' + ' '.join('%7s' % c[:7] for c in cols)
    print(head)
    tot = {c: 0 for c in cols}
    for ch, r in rows.items():
        print('%-4s ' % ch + ' '.join('%7d' % r[c] for c in cols))
        for c in cols:
            tot[c] += r[c]
    print('tot  ' + ' '.join('%7d' % tot[c] for c in cols))
    return tot


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 2:
        table(census(args[0] if args else '.'))
    else:
        a, b = census(args[0]), census(args[1])
        changed = False
        for ch in a:
            for c in a[ch]:
                if a[ch][c] != b.get(ch, {}).get(c):
                    changed = True
                    print('%s %-12s %6s -> %s' % (ch, c, a[ch][c], b.get(ch, {}).get(c)))
        if not changed:
            print('no differences')
