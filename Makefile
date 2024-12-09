all:
	@echo "Make what?"

ebooks:
	./helpers/ebooks.sh

sass:
	sass --no-source-map ./assets/sass:./assets/stylesheets

sass-watch:
	sass --watch --no-source-map ./assets/sass:./assets/stylesheets
