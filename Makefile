PROJECT_NAME:=onto_to_kg_dynamic
EXECUTER:=uv run

all: format lint test

clean:
	rm -rf .mypy_cache .pytest_cache .coverage htmlcov

test:
	$(EXECUTER) pytest --cov-report term-missing --cov-report html --cov $(PROJECT_NAME)/

format:
	$(EXECUTER) ruff format .

lint:
	$(EXECUTER) ruff check . --fix
	$(EXECUTER) mypy .

