.DEFAULT_GOAL := all

.PHONY: all
all: check test

.PHONY: check
check:
	flake8 .

.PHONY: test
test:
	python3 -m unittest
