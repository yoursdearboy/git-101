all: build

build:
	R -e 'bookdown::render_book(output_dir="docs")'

dev:
	R -e 'bookdown::serve_book(output_dir="docs")'
