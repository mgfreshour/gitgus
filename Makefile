.DEFAULT_GOAL := all

.PHONY: all
all: lint test build

test:
	poetry run pytest --cov-report=html --cov-report=term --cov ./gitgus ./tests

lint:
	poetry run flakeheaven lint
	poetry run black -l120 --check ./gitgus ./tests

lint/fix:
	poetry run black -l120 ./gitgus ./tests

run:
	poetry run python -m gitgus gus mgf

deps:
	poetry install

build: deps
	poetry build

install: build
	pipx uninstall gitgus
	pipx install dist/gitgus-0.1.0-py3-none-any.whl

DEMOS = $(shell ls demos/*.tape | sed 's/demos\///' | sed 's/.tape//')
demos: install
	for file in $(DEMOS); do \
		@echo "Running demo: $$file"; \
		vhs -o demos/$$file.gif < demos/$$file.tape; \
		open demos/$$file.gif; \
	done

generate-sobjects:
	poetry run python -m gitgus dev generate-sobjects ADM_Build__c FeedItem ADM_Epic__c ADM_Product_Tag__c ADM_Planned_Release__c ADM_Release__c User ADM_Scrum_Team__c ADM_Work__c

