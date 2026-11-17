BOOK = Physics.pdf

.PHONY: pdf figures fig release clean

pdf:
	latexmk -pdf main.tex

# Regenerate the 39 scripted figures. Order matters: mk_grav must run after mk9.
figures:
	cd figures-src/python && for s in mk5 mk4 mk9 mk5b mk8 mk_grav; do python3 $$s.py || exit 1; done

# Draw one native figure on its own at printed size: make fig F=grav_shell
fig:
	cd figures-src/tikz && pdflatex -interaction=nonstopmode -jobname=preview-$(F) "\\def\\figname{$(F)}\\input{preview}" >/dev/null && echo figures-src/tikz/preview-$(F).pdf

release: pdf
	python3 tools/compress_pdf.py main.pdf $(BOOK)

clean:
	latexmk -C main.tex
	rm -f $(BOOK)
	rm -rf figures-cache figures-src/tikz/preview-*
