.DEFAULT_GOAL := all

.PHONY: all
all: lint test build

test: ## Runs all tests
	poetry run pytest --cov-report=html --cov-report=term --cov ./gitgus ./tests

lint: ## Runs all linters
	poetry run flakeheaven lint
	poetry run black -l120 --check ./gitgus ./tests

lint/fix: ## Runs the black linter in fix mode (changes files)
	poetry run black -l120 ./gitgus ./tests

gui: ## Runs the GUI
	poetry run python -m gitgus gus mgf

deps: ## Installs dependencies
	poetry install

build: deps ## Builds the project
	poetry build

.PHONY: clean
clean: ## Cleans the project
	rm -rf build dist .pytest_cache .coverage .mypy_cache .flakeheaven .tox .eggs .venv

.PHONY: build/gui
build/gui: build ## Builds the GUI
	poetry run pyinstaller --log-level INFO -p "$(shell poetry env info -p)/lib/python3.11/site-packages" --windowed --noconfirm --name gitgus gitgus/gui.py

install: build ## Installs the CLI app with pipx
	pipx uninstall gitgus
	pipx install dist/gitgus-0.1.0-py3-none-any.whl

DEMOS = $(shell ls demos/*.tape | sed 's/demos\///' | sed 's/.tape//')
demos: install ## Creates the demos
	for file in $(DEMOS); do \
		@echo "Running demo: $$file"; \
		vhs -o demos/$$file.gif < demos/$$file.tape; \
		open demos/$$file.gif; \
	done

generate-sobjects: ## Generates the SObject classes
	poetry run python -m gitgus dev generate-sobjects ADM_Build__c FeedItem ADM_Epic__c ADM_Product_Tag__c ADM_Planned_Release__c ADM_Release__c User ADM_Scrum_Team__c ADM_Work__c

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-30s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
