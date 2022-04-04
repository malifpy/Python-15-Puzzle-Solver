PROJ_NAME = 15_Puzzle_Solver

init:
	pip install -r requirements.txt

test:
	python $(PROJ_NAME)/$(FILE).py

.PHONY: test
