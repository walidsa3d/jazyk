.PHONY: help clean install lint format test build docs publish

help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo "  clean     to remove build artifacts"
	@echo "  install   to install dependencies"
	@echo "  lint      to run linting checks"
	@echo "  test      to run tests"
	@echo "  build     to build the project"
	@echo "  docs      to build the documentation"
	@echo "  publish   to publish the package to PyPI"

clean:
	rm -rf dist
	rm -rf build
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .tox
	rm -rf .coverage
	rm -rf _build
	find . -type d -name "__pycache__" -exec rm -r {} +

install:
	pip install --upgrade pip
	pip install --upgrade poetry
	poetry install

lint:
	poetry run pre-commit run --all-files

format:
	poetry run ruff check --fix .
	poetry run black .

test:
	poetry run pytest

build:
	poetry build

docs:
	cd docs && poetry run make html

publish:
	poetry publish
