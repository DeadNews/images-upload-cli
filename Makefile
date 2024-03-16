.PHONY: all clean install update checks pc test docs run

install:
	pre-commit install
	poetry install --sync

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
