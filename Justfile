set shell := ["bash", "-c"]

alias chk := check
alias fmt := format

default: pre-commit

pre-commit: check format

check:
    ruff check

format:
    ruff format