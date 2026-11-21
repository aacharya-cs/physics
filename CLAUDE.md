# CLAUDE.md: working notes for editing this book

This repository is a physics textbook in LaTeX (JEE/NEET level), published as one PDF in volumes:
Foundations (the shared mathematical toolkit), Volume I Mechanics, Volume II Properties of Matter and
Thermal Physics, Volume III Nuclei and Radioactivity. It was written for a student, so every change should serve a reader learning the material for the first time: say why
before how, derive rather than quote, and be candid about where a model or method stops working.

## Build and check

```bash
latexmk -pdf main.tex                      # must finish with no errors
grep -c "undefined" main.log               # expect 0 undefined references
grep "Overfull" main.log                   # nothing over ~3pt is acceptable
```

Baseline after adding Volumes II and III (2026-11-17): 478 pages (Foundations, Vol I to p. 232,
Vol II pp. 233-368, Vol III pp. 369-476), 0 errors, 0 undefined references, no overfull boxes, 171
figures (all native, all cited in the text), about 180,000 words. Every source label should appear in
`main.aux` (a label at the very start of a box can be lost when the box starts at a page foot).
Expected harmless warnings: about 25 tcolorbox "Discard zero height first box part" (a box starting
at a page foot; checked, nothing visible is lost), font size substitutions for the sans-serif `\mathsf` dimension letters, and two hyperref
"bookmark levels" notes (a volume bookmark is followed directly by its unnumbered opening).

Layout (chosen by the owner from three test settings): Palatino 10.5pt via the `fontsize` package,
line spread 1.0, A4 margins inner 25 / outer 22 / top 22 / bottom 25 mm. Ruled boxes keep 13pt above
(their small-caps label needs it), other boxes 6-6.5pt; the label of a left-hairline box (Derivation, Example, Remark, Problem type, Challenge) is real text inside the box, never an overlay, because an overlay's clearance is dropped when a box starts a page and the body then overprints the label; sections 14pt above. Figure labels are \small
(9.6pt, subscripts 6.7pt), so they stay in proportion to the body; preview.tex matches. A clean build with an empty figures-cache takes about 10 minutes.
`python3 tools/census.py` prints the content census; `python3 tools/census.py OLD NEW` diffs two copies.
CI: `.github/workflows/build.yml` builds every push (latexmk with shell-escape), fails on errors or
undefined references, attaches `Physics.pdf` as the run's artifact, and on `main` replaces the PDF on the
"Latest build" release (tag `latest-build`; link `releases/latest/download/Physics.pdf`). Deploying `main` to GitHub
Pages is off until the repository variable `DEPLOY_PAGES` is `true`. The first run passed (2026-11-16).
`python3 tools/stylecheck.py [path]` checks the house style (em dashes, spelling, hard-coded numbers,
duplicate labels); it should report 0 issues. Mark a deliberate exception with `% stylecheck: ok`.

## Structure

- `main.tex` only `\input`s files; do not put content in it.
- `preamble.tex` holds every package, environment and macro. Add new macros there, never in a chapter.
- Layout: `main.tex` and `preamble.tex` in the root; `chapters/` (front matter, Foundations, `vol1`-`vol3`);
  `figures/` (`bookstyle.tex`, `preview.tex`, one folder per part); `tools/`; `archive/` (superseded,
  unused); `build/` (single-chapter PDFs and logs, ignored by git).
- Files: `chapters/frontmatter.tex`, `chapters/foundations.tex`, then `chapters/volN/volume.tex` (the `\volumedivider`),
  `chapters/volN/opening.tex` (Volumes II and III: an unnumbered `\volumeopening{About This Volume}`
  with the volume's purpose, map and notation table; no numbered boxes or figures in it), then
  `chapters/volN/chNN-slug.tex`. `tools/chapter.sh volN/chNN-slug` builds one chapter on its own
  (jobname `test-...`, PDF in `build/`), so several chapters can be worked on at once.
- **Numbering.** Foundations is numbered F (`\foundationschapter`), so its sections, boxes and figures
  read F.1, F.2. Chapter and part numbers restart in every volume (`\volumedivider` resets them); the
  hyperlink anchors include the volume, so equal numbers in different volumes never collide.
- Chapters are started with `\ncertchapter{n}{Title}\chlabel{ch:slug}` (`\chlabel`, not `\label`:
  it records the volume). `\chref{ch:slug}` prints "Chapter~11" within a volume, "Volume~I,
  Chapter~11" from another volume, and "the Foundations" for `ch:toolkit`. Never type "Volume I,
  Chapter 11" by hand.
- Parts use `\partdivider{Letter}{Title}{thesis}{chapter list}`, the first thing in the first chapter
  file of its part. Volume I: Parts A to E (ch01, ch07, ch11, ch13, ch16). Volume II: A (ch01-ch02),
  B (ch03), C (ch04-ch05). Volume III: A (ch01-ch03), B (ch04-ch05).
- Every chapter ends in the same order: `\section{Summary}`, `\section{Problem Types}`, then
  `Practice Problems` (with `\subsection*{Answers}`) and/or `Challenge Problems`. Each part closes with
  `\section*{Looking Back on Part X}`, and the last chapter of each volume closes with
  `Looking Back on the Volume`. Volume I: Practice Problems in Ch 6, 10, 12, 14, 16; Challenge
  Problems in Ch 8, 10, 12, 15, 17.
- A table's `\label` goes after `\end{tabular}` inside its `tablebox` (directly after `\begin{tablebox}{...}` it was once not written to the aux file); cite it as `Table~\ref{tab:...}`.
- Labels must be unique across the whole book: use descriptive names (`fig:bernoulli-tube`,
  `sec:carnot`, `ex:dam-force`), never `fig:2`. Check with `grep -rn 'label{NAME}' chapters` first.

## Notation across volumes

Within a volume one symbol means one quantity. Across volumes a letter may be reused only when each
volume's notation table says so (e.g. `\lambda` is the mean free path in Volume II and the decay
constant in Volume III; `k` is the spring constant in Volume I and the neutron multiplication factor in
Volume III). When a quantity from an earlier volume reappears, it keeps its earlier symbol (kinetic
energy `K`, period `T_{\text{per}}` where `T` is taken, length `\ell`, spring constant `k`, CM).
Volume II: temperature `T` (kelvin), Celsius `t_C`; `\alpha_\ell, \alpha_A, \alpha_V` expansion
coefficients; `\gamma = C_p/C_v` only; specific heat `s`, molar heat capacity `C`; conductivity `K`;
Boltzmann `k_B`; stress `\sigma`, Stefan's constant `\sigma_{\!s}`; Young's modulus `Y`, bulk modulus `B`, shear modulus `G`, Poisson's ratio `\nu`; surface tension `S`; reservoirs `T_h, T_c`, heats `Q_h, Q_c` (magnitudes); polytropic index `x` (`PV^x`), so `n` is always moles; `C_v, C_p`; heat current `H`, cooling constant `\kappa`. Declared double use: `\eta` is viscosity in Ch 2 and efficiency in Ch 4 (never in one chapter).
Volume III: mass number `A`, atomic number `Z`, neutron number written `A-Z` (never `N`, which is
the number of undecayed nuclei `N(t)`); `\nuc{A}{Z}{X}`, `\iso{A}{X}`; decay constant `\lambda`,
half-life `\Thalf`, mean life `\tau`, activity `\Act`, production rate `\Prod`, binding energy
`\Eb`, `Q`-value `Q`, electron lepton number `L_e` (never plain `L`, which is angular momentum); units through siunitx (`\si{\MeV}`, `\si{\fm}`, `\si{\amu}`,
`\si{\becquerel}`, `\si{\curie}`, `\si{\gray}`, `\si{\sievert}`, `\si{\year}`).

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
- **All figures are native TikZ/PGFPlots** (see the next section). `archive/` holds the superseded
  matplotlib PDFs and scripts and one unused figure, kept only for reference; nothing
  in the book uses them, and they can be deleted once the owner is satisfied with the new figures.

## Native-LaTeX figures

The owner wants the book as close to native LaTeX as practical. Status and rules:

- **Shared style:** `figures/bookstyle.tex` (loaded by `preamble.tex`) holds the palette as
  `cInk cPrim cTeal cAcc cCrim cFor cSteel cPlum cAmber cGrey` plus fills (`cEarth cMoon cBlock cSlope
  cRock cSun`), and the named styles every figure must use: `force applied velocity accel momentum`
  (arrows), `dim dimtick leader guide orbitpath`, `body planet moon point mass ground`, `curve thin line`,
  and the PGFPlots style `bookplot`. Colours carry the same meaning in every chapter (see the file's
  header). No raw HTML colours or hand-set line widths in figure files. (The prefix `c` avoids the text
  greys in `preamble.tex`, where `ink` is pure black.)
- **One file per figure** in `figures/<part>/NAME.tex` (part = `foundations`, `vol1`, `vol2`, `vol3`:
  the part whose chapter uses it), containing only the `tikzpicture`. `\tikzfig{NAME}` finds the folder. Include it
  with `\tikzfig{NAME}` inside the usual `figure` float, keeping the existing `\figcaption` label.
- **Draw at printed size.** Never scale with `width=`/`scale=` afterwards. Figure text is `\small`
  (subscripts 7pt); `\footnotesize` is the floor and only for plain words.
- **Compute, don't import.** Curves come from closed forms in pgfmath (conics for orbits, Newton's
  method for Kepler's equation), with the physics written in the file's header comment.
- **Preview one figure:** `make fig F=NAME` writes `figures/preview-NAME.pdf` at printed size.
- **Caching:** `.latexmkrc` enables shell-escape, and `\tikzfig` pictures are cached in
  `figures-cache/` (other TikZ, such as tcolorbox frames, is never externalised). Without shell-escape
  the figures are drawn inline, so the book still builds. The cache keys on the picture's own code
  only: **after editing `bookstyle.tex`, run `rm -rf figures-cache`**.
- **Status:** Volume I's 93 original figures converted and 7 added (2026-11-16); Volumes II and III
  added about 70 more (2026-11-17), all native, about 171 in the book. Audited for the colour legend and
  shared styles, and checked in their pages. Many old figures had physics errors that are now fixed (cone angle,
  rolling friction direction, vertical-circle slack points, movable pulley, cross product drawn in the
  plane, door torque, collinear vs parallel vectors, and others).
- **Colour legend** is in the header of `bookstyle.tex`: crimson every force; accent friction/applied
  pushes and kinetic energy; forest velocity and omega; primary acceleration and alpha; teal momentum
  and L; plum U, E and potentials; steel dimensions; grey guides. Documented exceptions: generic
  vectors in Ch 3, third-law pairs, Lami's three forces, cross product, paths coloured by category.
  Volume II: heat Q and heat current accent, work W plum; isotherms primary (hot/cold isotherms of a
  cycle crimson/primary), adiabats teal, isobars forest, isochores accent (they exchange only heat);
  hot reservoir `cAmber!55` fill, cold `cEarth`. Volume III: proton pale accent disc, neutron `cMoon`
  disc, alpha plum, electron and beta-minus primary, positron and beta-plus crimson, neutrino teal
  dashed, gamma and photon accent and always wavy (so never confused with a proton disc).
- **Shared pieces** (use them, never re-implement): `component resultant parallelogram rotation axis
  hidden slice ghost stable point unstable point U bar K bar ground strip rotation right angle contact
  point construction dot angle arc strip area fill mid arrow proton neutron photon`, pics
  `cm particle out of page into page`, and `\persp` for horizontal circles in perspective. Wished-for
  but not yet shared: pulley, spring, bracket.
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
