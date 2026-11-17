#!/usr/bin/env python3
"""Swap \\includegraphics{NAME.pdf} for \\tikzfig{NAME} wherever a native figure
figures-src/tikz/NAME.tex exists.  Usage: python3 tools/swapfigs.py [chNN ...]
(with no arguments, all chapters).  Prints what it changed."""
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
skip = {'bookstyle', 'preview', 'angle_repose_demo'}
native = {p.stem for p in (root / 'figures-src' / 'tikz').glob('*.tex')
          if p.stem not in skip and not p.stem.startswith('preview-')}
want = sys.argv[1:]
for f in sorted((root / 'chapters').glob('ch*.tex')):
    if want and not any(f.name.startswith(w) for w in want):
        continue
    s = f.read_text()
    def repl(m):
        name = m.group(1)
        if name in native:
            print(f'{f.name}: {name}')
            return r'\tikzfig{%s}' % name
        return m.group(0)
    s2 = re.sub(r'\\includegraphics\[[^\]]*\]\{([A-Za-z0-9_]+)\.pdf\}', repl, s)
    if s2 != s:
        f.write_text(s2)
