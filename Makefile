FILE=main

LATEX=latexmk
LATEX_OPTS=-interaction=nonstopmode -halt-on-error -lualatex

all: document

dist:
	./helpers/dist.sh

serve:
	python3 -m http.server -d gh-pages/ 5000

ebooks:
	./helpers/ebooks.sh

document:
	$(LATEX) $(LATEX_OPTS) $(FILE).tex

%.pdf: %.tex
	$(LATEX) $(LATEX_OPTS) $<

part-1:
	$(LATEX) $(LATEX_OPTS) $(FILE)-part-1.tex

part-2:
	$(LATEX) $(LATEX_OPTS) $(FILE)-part-2.tex

part-covers:
	./helpers/generate_part_covers.sh

sass:
	sass --no-source-map ./assets/sass:./assets/stylesheets

sass-watch:
	sass --watch --no-source-map ./assets/sass:./assets/stylesheets
