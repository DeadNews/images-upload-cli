.PHONY: all clean default install lock update checks pc test docs run

default: checks

install:
	pre-commit install
	poetry install --sync

lock:
	poetry lock --no-update

update:
	poetry up --latest

checks: pc install lint test

pc:
	pre-commit run -a

lint:
	poetry run poe lint

test:
	poetry run poe test

docs:
	poetry run mkdocs serve
