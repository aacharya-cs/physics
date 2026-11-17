# Mechanics, Volume 1 (Class 11, JEE/NEET)

A LaTeX textbook on Class 11 mechanics, written for JEE and NEET preparation: 18 chapters (a
mathematical toolkit and Chapters 1 to 17) in five parts, from measurement and kinematics through
Newton's laws, energy and collisions, rotation and rolling, to gravitation and Kepler's laws.
About 230 A4 pages, 100 figures (all drawn natively in TikZ/PGFPlots), 71 worked examples, 78
derivations and 97 exam problem types.

**Live PDF:** `https://<github-user>.github.io/<repo-name>/Mechanics_Vol1_Class11.pdf`
(rebuilt automatically on every push to `main`; see *Publishing* below).

## Building locally

You need a TeX Live installation (2023 or later) with `latexmk`.

```bash
latexmk -pdf main.tex        # or: make pdf
make release                 # also writes the compressed Mechanics_Vol1_Class11.pdf
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
chapters/chNN-*.tex       one file per chapter; a Part divider sits at the top of its first chapter
figs/*.pdf                superseded PDF versions of the figures (no longer used by the book)
figures-src/python/       superseded matplotlib scripts (no longer used)
figures-src/tikz/         native figures: bookstyle.tex (shared palette and styles), one .tex per
                          figure, preview.tex (make fig F=name); cached in figures-cache/
tools/compress_pdf.py     font subsetting and stream compression for the release PDF
tools/census.py           content census (boxes, figures, words per chapter) and diff of two copies
tools/index.html          landing page for the GitHub Pages site (redirects to the PDF)
.github/workflows/        CI: compile, compress, upload artifact, deploy to Pages
CLAUDE.md                 conventions and working notes for anyone (human or AI) editing the book
```

## Publishing

1. Create an empty repository on GitHub and push this folder to its `main` branch.
2. In the repository, open **Settings → Pages → Build and deployment** and set **Source** to
   **GitHub Actions**.
3. Push any commit (or run the workflow from the **Actions** tab). When it finishes, the PDF is at
   `https://<github-user>.github.io/<repo-name>/Mechanics_Vol1_Class11.pdf`, and the site root
   redirects there. That link stays the same; it always serves the latest build.

Each workflow run also attaches the PDF as a downloadable artifact, and pull requests are built
(but not deployed) so a broken change is caught before it reaches the live link.

Pages from a private repository need a paid GitHub plan; on the free plan, make the repository public.
