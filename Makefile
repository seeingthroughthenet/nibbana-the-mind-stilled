FILE=main

LATEX=latexmk
LATEX_OPTS=-interaction=nonstopmode -halt-on-error -lualatex

all: document

document:
	$(LATEX) $(LATEX_OPTS) $(FILE).tex

%.pdf: %.tex
	$(LATEX) $(LATEX_OPTS) $<

ebooks:
	./helpers/ebooks.sh

sass:
	sass --no-source-map ./assets/sass:./assets/stylesheets

sass-watch:
	sass --watch --no-source-map ./assets/sass:./assets/stylesheets
