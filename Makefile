.PHONY: install run-program

install:
	pip install --user --requirement requirements.txt

run-program:
	python GUI.py
