# Physics: A Reasoning-First Companion (JEE/NEET)

A LaTeX physics textbook for JEE and NEET preparation, published as one PDF in volumes:

- **Foundations**: the mathematical toolkit every volume uses (numbered F).
- **Volume I, Mechanics**: 17 chapters in five parts, from measurement and kinematics through
  Newton's laws, energy and collisions, rotation and rolling, to gravitation and Kepler's laws.
- **Volume II, Properties of Matter and Thermal Physics**: solids, fluids, thermal properties,
  thermodynamics and kinetic theory (5 chapters, three parts).
- **Volume III, Nuclei and Radioactivity**: the nucleus, radioactive decay, the decay law, nuclear
  reactions and applications (5 chapters, two parts), with a glossary.

Chapter numbers restart in each volume. All 171 figures are drawn natively in TikZ/PGFPlots; every
chapter ends with exam-style Problem Types (single-correct MCQs with the method and the trap).

**PDF:** every push is built by CI, and the PDF is attached to the workflow run as the artifact
`Physics`. Deployment to GitHub Pages is optional (see *Publishing* below).

## Building locally

You need a TeX Live installation (2023 or later) with `latexmk`.

```bash
latexmk -pdf main.tex        # or: make pdf
make release                 # also writes the compressed Physics.pdf
```

All figures are drawn in TikZ/PGFPlots from `figures-src/tikz/` with the shared style
`bookstyle.tex`; no Python is needed to build the book. To work on one figure at its printed size:

```bash
make fig F=grav_shell        # writes figures-src/tikz/preview-grav_shell.pdf
```

The release step (`make release`) needs Python 3.10+ with `pymupdf` for PDF compression.

## Repository layout

```
main.tex                  document skeleton: \input's the preamble, front matter and chapters
preamble.tex              packages, page layout, box environments, macros
frontmatter.tex           title page, preface, how to use the book, contents
chapters/foundations.tex  the mathematical toolkit (numbered F)
chapters/volN/            volume.tex (divider), opening.tex (Vols II, III), chNN-*.tex one per chapter;
                          a Part divider sits at the top of its first chapter
figs/*.pdf                superseded PDF versions of the figures (no longer used by the book)
figures-src/python/       superseded matplotlib scripts (no longer used)
figures-src/tikz/         native figures: bookstyle.tex (shared palette and styles), one .tex per
                          figure, preview.tex (make fig F=name); cached in figures-cache/
tools/compress_pdf.py     font subsetting and stream compression for the release PDF
tools/census.py           content census (boxes, figures, words per chapter) and diff of two copies
tools/chapter.sh          build one chapter on its own: tools/chapter.sh vol2/ch01-solids
tools/stylecheck.py       house-style checks (em dashes, spelling, hard-coded numbers, duplicate labels)
tools/index.html          landing page for the GitHub Pages site (redirects to the PDF)
.github/workflows/        CI: compile, compress, upload artifact, deploy to Pages
CLAUDE.md                 conventions and working notes for anyone (human or AI) editing the book
```

## Publishing

1. Create an empty repository on GitHub and push this folder to its `main` branch.
2. In the repository, open **Settings → Pages → Build and deployment** and set **Source** to
   **GitHub Actions**.
3. Under **Settings → Secrets and variables → Actions → Variables**, add `DEPLOY_PAGES` = `true`
   (deployment is off without it).
4. Push any commit (or run the workflow from the **Actions** tab). When it finishes, the PDF is at
   `https://<github-user>.github.io/<repo-name>/Physics.pdf`, and the site root
   redirects there. That link stays the same; it always serves the latest build.

Each workflow run also attaches the PDF as a downloadable artifact, and pull requests are built
(but not deployed) so a broken change is caught before it reaches the live link.

Pages from a private repository need a paid GitHub plan; on the free plan, make the repository public.
