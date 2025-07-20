# PyGameOfLife

[![Build Status](https://travis-ci.org/AaronRobson/PyGameOfLife.svg?branch=master)](https://travis-ci.org/AaronRobson/PyGameOfLife)
[![CircleCI](https://circleci.com/gh/AaronRobson/PyGameOfLife.svg?style=svg)](https://circleci.com/gh/AaronRobson/PyGameOfLife)
[![Coverage Status](https://coveralls.io/repos/github/AaronRobson/PyGameOfLife/badge.svg?branch=master)](https://coveralls.io/github/AaronRobson/PyGameOfLife?branch=master)

John Conway's Game Of Life implemented in the Python programming language.

![screenshot](screenshot.png)

# Install dependencies

## General

```sh
make install-packages
```

## Linux specific

```sh
sudo apt install -y python3-tk
```

(for Ubuntu and other Debian derived repositories)

## Windows

When installing python:
1. Select the _Add to Path_ option.
1. Include Tkinter bindings.

# Run linting and tests

```sh
make
```

## Run code checks

```sh
make check
```

### Run linting

Runs `flake8`.

```sh
make lint
```

### Run type checks

Runs `mypy`.

```sh
make typecheck
```

## Run tests

```sh
make test
```

Or:

```sh
make unittest
```

# Running

```sh
python3 gameoflifegui.py
```

(In Windows you may need to use `python` instead of `python3`)

aka:

```sh
make run
```
