PROJ_NAME = 15_Puzzle_Solver

init:
	pip install -r requirements.txt

test:
	python $(PROJ_NAME)/$(FILE).py

run:
	python $(PROJ_NAME)/GUI.py

doc:
	pandoc  doc/Tucil3_13520135.md -o doc/Tucil3_13520135.pdf \
		--include-in-header doc/header.tex \
		--highlight-style tango \
		--pdf-engine=xelatex

.PHONY: test run doc
