BOOK = Physics.pdf

.PHONY: pdf fig release clean

pdf:
	latexmk -pdf main.tex

# Draw one native figure on its own at printed size: make fig F=grav_shell
# (finds figures/*/grav_shell.tex; writes figures/preview-grav_shell.pdf)
fig:
	@cd figures && P=$$(ls */$(F).tex 2>/dev/null | head -1) && [ -n "$$P" ] || { echo "no figures/*/$(F).tex"; exit 1; }; \
	pdflatex -interaction=nonstopmode -jobname=preview-$(F) "\\def\\figname{$${P%.tex}}\\input{preview}" >/dev/null && echo figures/preview-$(F).pdf

release: pdf
	python3 tools/compress_pdf.py main.pdf $(BOOK)

clean:
	latexmk -C main.tex
	rm -f $(BOOK)
	rm -rf figures-cache figures/preview-*
