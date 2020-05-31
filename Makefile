target:
	@$(MAKE) test

dev:
	pip install --upgrade pip poetry
	poetry install

test:
	poetry run pytest -vvv