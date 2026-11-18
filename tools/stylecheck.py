#!/usr/bin/env python3
"""House-style checks for the book (see CLAUDE.md).

    python3 tools/stylecheck.py                 # every chapter file
    python3 tools/stylecheck.py chapters/vol2   # one folder or file

Reports, with file:line, anything the house style forbids in prose:
em dashes, "i.e."/"e.g.", hard-coded chapter/section/figure numbers,
colour or raw boxes in chapters, non-native figures, American spellings,
"toward", and labels defined more than once anywhere in the book.
Comments are ignored.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CHECKS = [
    ('em dash', re.compile(r'(?<!-)---(?!-)')),
    ('i.e./e.g.', re.compile(r'\b(i\.e\.|e\.g\.)')),
    ('hard-coded number', re.compile(
        r'(Ch\.~?\s?\d|\\S\s?\d|\bSection~?\s?\d|\bFigure~?\s?\d|\bFig\.~?\s?\d|'
        r'\bChapter~?\s?\d|\bExample~?\s?\d|\bEquation~?\s?\(?\d|'
        r'\bVolume~I+,?~?\s?Chapter)')),
    ('colour in prose', re.compile(r'\\textcolor')),
    ('raw box', re.compile(r'\\begin\{tcolorbox\}|\\begin\{multicols\}|\\begin\{(whybox|summarybox)\}')),
    ('non-native figure', re.compile(r'\\includegraphics|\\begin\{tikzpicture\}')),
    ('toward', re.compile(r'\btoward\b')),
    ('American spelling', re.compile(
        # "meter" (an instrument) and "gray" (the SI unit) are correct British usage
        r'(?<![\\{])\b(color|colors|colored|center|centers|centered|liter|liters|'
        r'behavior|behaviors|modeling|modeled|fiber|analyze|analyzed|realize|realized|'
        r'recognize|recognized|organize|organized|minimize|minimized|maximize|maximized|'
        r'ionize|ionized|ionization|polarize|polarized|vaporize|vaporization|crystallize|'
        r'normalize|normalized|summarize|summarized|emphasize|characterize|characterized|'
        r'neighbor|favor|favorable|labor|vapor|sulfur|aluminum|program)\b')),
]
LABEL = re.compile(r'\\(?:ch)?label\{([^}]+)\}|\\figcaption\{([^}]+)\}')


def strip_comment(line):
    return re.sub(r'(?<!\\)%.*', '', line)


def files(args):
    paths = [ROOT / a for a in args] or [ROOT / 'chapters']
    out = []
    for p in paths:
        out += sorted(p.rglob('*.tex')) if p.is_dir() else [p]
    return out


def main():
    targets = files(sys.argv[1:])
    n = 0
    for f in targets:
        for i, line in enumerate(f.read_text().splitlines(), 1):
            text = strip_comment(line)
            if 'stylecheck: ok' in line:      # deliberate, e.g. quoting a format
                continue
            for name, rx in CHECKS:
                for m in rx.finditer(text):
                    # \color inside a figure is fine; chapters should not have it
                    print(f'{f.relative_to(ROOT)}:{i}: {name}: ...{text[max(0, m.start()-30):m.end()+30].strip()}...')
                    n += 1
    # duplicate labels across the whole book
    seen = defaultdict(list)
    for f in files([]):
        for i, line in enumerate(f.read_text().splitlines(), 1):
            for m in LABEL.finditer(strip_comment(line)):
                seen[m.group(1) or m.group(2)].append(f'{f.relative_to(ROOT)}:{i}')
    for lab, where in sorted(seen.items()):
        if len(where) > 1:
            print(f'duplicate label {lab}: {", ".join(where)}')
            n += 1
    print(f'{n} issue(s) in {len(targets)} file(s)')
    return 1 if n else 0


if __name__ == '__main__':
    sys.exit(main())
