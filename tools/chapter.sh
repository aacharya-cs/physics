#!/bin/bash
# Build one chapter on its own, so several people (or agents) can work at once.
#   tools/chapter.sh vol2/ch03-fluids          -> build/test-vol2-ch03-fluids.pdf
#   tools/chapter.sh foundations
# The job runs in the repo root with its own jobname, so it never touches
# main.aux/main.pdf.  References to other chapters show as ?? here; that is
# expected.  Figures are cached in figures-cache/ exactly as in the full book.
set -e
cd "$(dirname "$0")/.."
ch="$1"; [ -f "chapters/$ch.tex" ] || { echo "no chapters/$ch.tex"; exit 1; }
job="test-$(echo "$ch" | tr '/' '-')"
vol=F
case "$ch" in vol1/*) vol=I;; vol2/*) vol=II;; vol3/*) vol=III;; esac
mkdir -p build figures-cache
# The driver must sit in the repo root as $job.tex: TikZ externalisation
# re-runs the job as \input{$job}, so any other location breaks figure caching.
cat > "$job.tex" <<TEX
\\documentclass[11pt,a4paper,twoside,openany]{book}
\\input{preamble}
\\begin{document}\\mainmatter
\\def\\currvol{$vol}
\\input{chapters/$ch}
\\end{document}
TEX
for i in 1 2; do
  pdflatex -shell-escape -interaction=nonstopmode "$job.tex" > /dev/null 2>&1 || true
done
mv -f "$job.pdf" "$job.log" build/ 2>/dev/null || true
rm -f "$job".{tex,aux,auxlock,out,toc}   # keep the root clean; the log is in build/
log="build/$job.log"
echo "errors:    $(grep -c '^!' "$log")"
grep -A3 '^!' "$log" | head -20
echo "overfull:  $(grep -c 'Overfull' "$log")"; grep 'Overfull' "$log" | head
echo "undefined (other chapters' refs are expected): $(grep -c 'undefined' "$log")"
echo "pages:     $(grep -o 'Output written.*' "$log")"
echo "pdf:       build/$job.pdf   log: $log"
