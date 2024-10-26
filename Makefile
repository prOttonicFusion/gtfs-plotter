.PHONY: dep test lint lint-fix typecheck check-pip

dep: ## Install client depedencies locally
	@pip install -r requirements.txt

test: ## Run tests
	python3 -m unittest discover -s .

lint: ## Check code formatting
	@python3 -m black . --check --diff

lint-fix: ## Format code
	@python3 -m black .

typecheck: ## Check validity of type hints
	@python3 -m pyright

check-pip:
ifeq ($(shell pip --version 2>/dev/null),)
	$(error "pip not found. Make sure it is installed before running this.")
endif