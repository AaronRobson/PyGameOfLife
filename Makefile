ifneq (, $(shell which python3))
	PYTHON := python3
else
	PYTHON := python
endif

.DEFAULT_GOAL := all

.PHONY: all
all: check test

.PHONY: install-packages
install-packages:
	$(PYTHON) -m pip install --upgrade --user \
	  -r dev-requirements.txt \
	  -r requirements.txt \
	  -r tests/requirements.txt

.PHONY: check
check: lint typecheck

.PHONY: lint
lint:
	$(PYTHON) -m flake8 .

.PHONY: typecheck
typecheck:
	$(PYTHON) -m mypy .

.PHONY: test
test: unittest

.PHONY: unittest
unittest:
	$(PYTHON) -m unittest

.PHONY: run
run:
	$(PYTHON) gameoflifegui.py
