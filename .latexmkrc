# Shell-escape lets TikZ cache each native figure in figures-cache/ (see preamble.tex).
$pdflatex = 'pdflatex -shell-escape -interaction=nonstopmode %O %S';
$pdf_mode = 1;
system('mkdir -p figures-cache');
