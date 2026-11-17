# CLAUDE.md: working notes for editing this book

This repository is a Class 11 mechanics textbook in LaTeX (JEE/NEET level). It was written for a
student, so every change should serve a reader learning the material for the first time: say why
before how, derive rather than quote, and be candid about where a model or method stops working.

## Build and check

```bash
latexmk -pdf main.tex                      # must finish with no errors
grep -c "undefined" main.log               # expect 0 undefined references
grep "Overfull" main.log                   # nothing over ~3pt is acceptable
```

Baseline after switching to the formal-textbook layout (2026-11-17): 230 pages, 0 errors,
0 undefined references, no overfull boxes, 100 figures (all native, all cited in the text).
Expected harmless warnings: about ten tcolorbox "Discard zero height first box part" (a box starting
at a page foot; checked, nothing visible is lost) and one font size substitution.

Layout (chosen by the owner from three test settings): Palatino 10.5pt via the `fontsize` package,
line spread 1.0, A4 margins inner 25 / outer 22 / top 22 / bottom 25 mm. Ruled boxes keep 13pt above
(their small-caps label needs it), other boxes 6-6.5pt; the label of a left-hairline box (Derivation, Example, Remark, Problem type, Challenge) is real text inside the box, never an overlay, because an overlay's clearance is dropped when a box starts a page and the body then overprints the label; sections 14pt above. Figure labels are \small
(9.6pt, subscripts 6.7pt), so they stay in proportion to the body; preview.tex matches. A clean build with an empty figures-cache takes about 10 minutes.
`python3 tools/census.py` prints the content census; `python3 tools/census.py OLD NEW` diffs two copies.
CI: `.github/workflows/build.yml` builds every push (latexmk with shell-escape), fails on errors or
undefined references, and deploys `main` to GitHub Pages. It was recreated on 2026-11-16 and has not
yet run on GitHub; check the first run.

## Structure

- `main.tex` only `\input`s files; do not put content in it.
- `preamble.tex` holds every package, environment and macro. Add new macros there, never in a chapter.
- Chapters are started with `\ncertchapter{n}{Title}` (sets the number explicitly, so Chapter 0
  works). Parts use `\partdivider{Letter}{Title}{thesis}{chapter list}`; the divider is the first
  thing in the first chapter file of its part (ch00, ch07, ch11, ch13, ch16).
- Every chapter ends in the same order: `\section{Summary}`, `\section{Problem Types}`, then
  `Practice Problems` (Ch 6, 10, 12, 14, 16, each with `\subsection*{Answers}`) and/or
  `Challenge Problems` (Ch 8, 10, 12, 15, 17). Each part closes with `\section*{Looking Back on Part X}`,
  and Ch 17 closes with `Looking Back on the Volume`.

## Style conventions (keep these consistent)

- **A formal book, not a slide deck.** Text is black. Colour lives in the figures, not the prose;
  boxes are hairline rules, never filled panels.
- **No em dashes.** Use a comma, colon, semicolon, parentheses or a new sentence. En dashes (`--`)
  only for ranges and named pairs (work--energy).
- **British spelling** (centre, metre, colour, behaviour, modelling).
- **Never hard-code a number** for a chapter, section, figure, example or equation. Use `\label` and
  `\ref` (labels look like `sec:shell`, `ex:slack`, `fig:...`). Hard-coded numbers broke repeatedly
  during earlier restructures. Every chapter carries a label (`ch:toolkit`, `ch:measurement`,
  `ch:straightline`, `ch:vectors`, `ch:projectiles`, `ch:relative`, `ch:circkin`, `ch:newton`,
  `ch:connected`, `ch:friction`, `ch:circdyn`, `ch:energy`, `ch:collisions`, `ch:com`, `ch:rotation`,
  `ch:rolling`, `ch:gravitation`, `ch:kepler`); write `\chref{ch:energy}` ("Chapter~11") or
  `\chsref{a}{b}`. There are currently no hard-coded chapter numbers anywhere; keep it that way.
- Terminology: "normal force" (not "normal reaction"), "pseudo-force", "centre of mass (CM)" spelled out
  at first use in each chapter, "that is," rather than "i.e.". Every Problem Types entry is an `\archq`
  MCQ (the old `\arch` is no longer used), with answer letters spread over A to D.
- Maths in a sectioning title needs `\texorpdfstring{...}{plain text}` for the PDF bookmarks.
- **`toward` is written `towards`**, and -ise spellings are used (memorise, rationalised).
- **One symbol per quantity**, used book-wide: `\theta_r` for the angle of repose, `\ell` for the
  length of a rod or string (never `L`), `L` for angular momentum, `T_{\text{per}}` for a period
  wherever `T` is a tension, `c` for the shape factor in `I=cMR^2`, `v_o` for orbital speed, `\vF`, `\va`, `\vv`, `\vr`, `\vL`, `\vtau` for vectors.
- **Physics must be checked, not trusted.** Earlier drafts contained a bicycle-stability myth
  (gyroscopic effect as the reason bikes stay up) and a Newton's-cannon figure whose "too slow"
  paths went into orbit. Both were fixed; do not reintroduce either.

## Box semantics

All boxes share one counter (`bxcount`, numbered chapter.N). Use the box whose meaning fits:

| Environment / macro | Look | Use for |
|---|---|---|
| `defbox{Title}` | rules above and below | Definition |
| `keybox{Title}` | rules above and below | Result (a formula or law to carry forward) |
| `methodbox{Title}` | rules above and below | Method (a procedure) |
| `tablebox{Title}` | rules above and below | Table of results |
| `derivbox{Title}` | left hairline | Derivation |
| `exbox{Title}` (or `\wex`) | left hairline, ends with a square | Worked example |
| `\archq{Title}{Tell}{Method}{Trap}{Question}{A}{B}{C}{D}` (builds an `archbox`) | left hairline | Problem type with an exam-style MCQ; put `\archans{Letter}{reason}` at the end of the (D) argument, which stores the answer and prints it below the options |
| `challengebox{Title}` | left hairline | Challenge problem (`\challengeans` for answers) |
| `remarkbox{Title}` | left hairline | Remark, aside, history |
| `trapbox{Title}` | small italic lead | Caution (common error) |
| `motivbox{Lead}`, `\why{}`, `\inwords{}`, `\scopebox{}` | small italic lead | Motivation, why it matters, plain-words restatement, syllabus scope |

`\ans{...}` right-aligns a short answer at the end of a practice problem.

## Figures

- Figures are floats: `\begin{figure}[htbp]\centering\includegraphics[width=..]{name.pdf}\figcaption{fig:label}{Caption.}\end{figure}`.
  `\figcaption` numbers and labels the figure; the caption should say what to notice, not just
  what is drawn.
- **Minimum printed text size is 6.5pt** (measure at the width used in the book, not at the
  native size). Thirteen figures failed this once and were redrawn.
- After any figure change, render the page and look at it. Check for overlapping labels, clipped
  arrows, and that the physics drawn matches the text.
- **All 93 figures are native TikZ/PGFPlots** (see the next section). `figs/*.pdf`, `figures-src/python/`
  and `make figures` are the superseded matplotlib/recovered versions, kept only for reference; nothing
  in the book uses them, and they can be deleted once the owner is satisfied with the new figures.

## Native-LaTeX figures

The owner wants the book as close to native LaTeX as practical. Status and rules:

- **Shared style:** `figures-src/tikz/bookstyle.tex` (loaded by `preamble.tex`) holds the palette as
  `cInk cPrim cTeal cAcc cCrim cFor cSteel cPlum cAmber cGrey` plus fills (`cEarth cMoon cBlock cSlope
  cRock cSun`), and the named styles every figure must use: `force applied velocity accel momentum`
  (arrows), `dim dimtick leader guide orbitpath`, `body planet moon point mass ground`, `curve thin line`,
  and the PGFPlots style `bookplot`. Colours carry the same meaning in every chapter (see the file's
  header). No raw HTML colours or hand-set line widths in figure files. (The prefix `c` avoids the text
  greys in `preamble.tex`, where `ink` is pure black.)
- **One file per figure** in `figures-src/tikz/NAME.tex`, containing only the `tikzpicture`. Include it
  with `\tikzfig{NAME}` inside the usual `figure` float, keeping the existing `\figcaption` label.
- **Draw at printed size.** Never scale with `width=`/`scale=` afterwards. Figure text is `\small`
  (subscripts 7pt); `\footnotesize` is the floor and only for plain words.
- **Compute, don't import.** Curves come from closed forms in pgfmath (conics for orbits, Newton's
  method for Kepler's equation), with the physics written in the file's header comment.
- **Preview one figure:** `make fig F=NAME` writes `figures-src/tikz/preview-NAME.pdf` at printed size.
- **Caching:** `.latexmkrc` enables shell-escape, and `\tikzfig` pictures are cached in
  `figures-cache/` (other TikZ, such as tcolorbox frames, is never externalised). Without shell-escape
  the figures are drawn inline, so the book still builds. The cache keys on the picture's own code
  only: **after editing `bookstyle.tex`, run `rm -rf figures-cache`**.
- **Status:** all 93 original figures converted, and 7 new ones added since (100 in all) (2026-11-16), audited for the colour legend and shared styles,
  and checked in their pages. Many old figures had physics errors that are now fixed (cone angle,
  rolling friction direction, vertical-circle slack points, movable pulley, cross product drawn in the
  plane, door torque, collinear vs parallel vectors, and others).
- **Colour legend** is in the header of `bookstyle.tex`: crimson every force; accent friction/applied
  pushes and kinetic energy; forest velocity and omega; primary acceleration and alpha; teal momentum
  and L; plum U, E and potentials; steel dimensions; grey guides. Documented exceptions: generic
  vectors in Ch 3, third-law pairs, Lami's three forces, cross product, paths coloured by category.
- **Shared pieces** (use them, never re-implement): `component resultant parallelogram rotation axis
  hidden slice ghost stable point unstable point U bar K bar ground strip rotation right angle contact
  point construction dot angle arc strip area fill`, pics `cm particle out of page into page`, and
  `\persp` for horizontal circles in perspective. Wished-for but not yet shared: pulley, spring, bracket.
- `tikzphysics`, `physketch` and `memoize` are not in the installed TeX Live 2023; do not depend on them.

## Quality bar for every pass

- Every concept has its need, definition, intuition, derivation (or an explicit "quoted, because"),
  a worked use, its standard misconception, its limits, and links back and forward.
- Flow: every section and box says why it comes next. Notation: every symbol is introduced (meaning,
  units, vector or scalar) at or before its first use, and recalled when it reappears from an earlier
  chapter. Every figure is cited in the text where it is meant to be looked at.

- Build clean (0 errors, 0 undefined references, no overfull box, no new warnings).
- Every number in a changed passage recomputed (python3; numpy is not installed, so standard library).
- Every result the book uses is derived, or explicitly flagged as stated without proof, with the
  reason. Every model states where it stops working (uniform Earth, no air resistance, rigid bodies).
- MCQ answer letters spread over A to D; explanations refer to options as (A) to (D).
- Content census shows no loss unless intended; changed pages rendered and looked at.

## Verification protocol for substantive edits

1. **Content census** before and after any restructure: count `defbox`, `keybox`, `derivbox`,
   `exbox`, `archbox`, `challengebox`, `trapbox`, figures and words. Nothing should disappear
   unless that was the intent.
2. **Check new formulas** symbolically or numerically (e.g. a short sympy script) before committing.
3. **Check environment nesting** after any scripted edit (a regex once swallowed two
   `\ncertchapter` lines into an `enumerate`).
4. **Compile, then read the rendered pages** you changed, including figure placement and
   whitespace.
