# Makefile

.PHONY: help install install-dev test lint format type-check clean build publish examples

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install package for users
	pip install -r requirements.txt
	pip install -e .

install-dev:  ## Install package for development
	pip install -r requirements.txt
	pip install -e .[dev]
	pre-commit install

test:  ## Run tests
	pytest tests/ -v --cov=plot_scaler --cov-report=html --cov-report=term

test-fast:  ## Run tests without coverage
	pytest tests/ -v

lint:  ## Run linting
	flake8 . --max-line-length=88 --extend-ignore=E203,W503
	black --check --diff .

format:  ## Format code
	black .
	isort .

type-check:  ## Run type checking
	mypy plot_scaler.py --ignore-missing-imports

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build:  ## Build package
	python -m build

publish-test:  ## Publish to test PyPI
	twine upload --repository testpypi dist/*

publish:  ## Publish to PyPI
	twine upload dist/*

examples:  ## Run example scripts
	python examples/aaa_growth_example.py
	python plot_scaler.py --demo

config-examples:  ## Create configuration examples
	python plot_scaler.py --create-examples

docs:  ## Generate documentation (if using sphinx)
	cd docs && make html

all: clean lint type-check test build  ## Run all checks and build

---