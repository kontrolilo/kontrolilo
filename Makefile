.PHONY: docs
help:	## Show this help.
		@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

pyenv-setup:
	pyenv install
	pip install pipenv

local-setup:
	pip3 install -r requirements.txt
	pip3 install -r requirements-dev.txt
	pre-commit install
	pre-commit install --hook-type commit-msg

unit-test:
	COVERAGE_FILE=.coverage_unit  pytest -n auto --cov=kontrolilo src tests/unit

integration-test:
	COVERAGE_FILE=.coverage_integration  pytest -n auto --cov=kontrolilo src tests/integration

test: unit-test #integration-test
#coverage combine .coverage_unit .coverage_integration
	cp .coverage_unit .coverage
	coverage xml

ci-setup-environment:
	pip install pre-commit pyenv

lint:
	pre-commit run --all-files

release:
	semantic-release publish

print-release:
	semantic-release print-version

run-sample-webserver:
	(cd examples &&  python -m http.server)

docs:
	hugo -s docs

docs-server:
	hugo server -s docs
