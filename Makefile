.DEFAULT_GOAL := all

.PHONY: all
all: check test

.PHONY: install-packages
install-packages:
	python3 -m pip install --upgrade --user \
	  -r dev-requirements.txt \
	  -r requirements.txt \
	  -r tests/requirements.txt

.PHONY: check
check: lint typecheck

.PHONY: lint
lint:
	python3 -m flake8 .

.PHONY: typecheck
typecheck:
	python3 -m mypy .

.PHONY: test
test: unittest

.PHONY: unittest
unittest:
	python3 -m unittest

.PHONY: run
run:
	python3 gameoflifegui.py
