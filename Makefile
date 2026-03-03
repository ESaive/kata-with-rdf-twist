.EXPORT_ALL_VARIABLES:

# Virtual Environment variables
SHELL = /bin/bash
PYTHON_VERSION = 3.13
PY = python3
VENV = .venv
BIN=$(VENV)/bin

export BASH_ENV=$(VENV)/bin/activate

$(VENV): pyproject.toml
	@uv self update || true
	@uv venv --python ${PYTHON_VERSION} --python-fetch automatic --python-preference only-managed --link-mode=copy -q
	@uv sync --all-groups --link-mode=copy

test: $(VENV) ## run all tests
	@echo "Running all tests..."
	@.venv/Scripts/pytest

test-python: $(VENV) ## run python tests
	pytest python/tests/
	
lint: $(VENV) ## Linting - only report issues, don't fix
	@echo "Running linter (ruff)..."
	@.venv/Scripts/python -m ensurepip --upgrade >/dev/null 2>&1 || true
	@.venv/Scripts/python -m pip install -q ruff
	@.venv/Scripts/python -m ruff check .

precommit: $(VENV) ## Install and set up pre-commit hooks
	@echo "Installing pre-commit and ruff for hooks..."
	@.venv/Scripts/python -m ensurepip --upgrade >/dev/null 2>&1 || true
	@.venv/Scripts/python -m pip install -q pre-commit ruff
	@.venv/Scripts/pre-commit install
