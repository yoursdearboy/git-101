.PHONY: all test practice build dev

all: build

test:
	python3 -m unittest discover -s tests -v
	python3 bin/check_course.py

practice:
	quarto render practice/workshop_notebook.qmd --execute-dir practice/assets

build:
	R -e 'bookdown::render_book(output_dir="docs")'

dev:
	R -e 'bookdown::serve_book(output_dir="docs")'
