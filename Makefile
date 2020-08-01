.PHONY: install
install:
	pip install poetry
	poetry install

.PHONY: lint
lint:
	poetry run flake8 dymy

.PHONY: mypy
mypy:
	poetry run mypy
