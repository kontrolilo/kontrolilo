help:	## Show this help.
		@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

local-setup:
	pipenv --python $(shell which python)
	pipenv install -d
	pipenv run pre-commit install
	pipenv run pre-commit install --hook-type commit-msg

unit-test:
	COVERAGE_FILE=.coverage_unit pipenv run pytest -n auto --cov=license_checks src tests/unit

integration-test:
	COVERAGE_FILE=.coverage_integration pipenv run pytest -n auto --cov=license_checks src tests/integration

test: unit-test integration-test
	pipenv run coverage combine .coverage_unit .coverage_integration
	pipenv run coverage xml

ci-setup-environment:
	pip install pipenv

sync:
	pipenv run pipenv-setup sync

lint:
	pipenv run pre-commit run --all-files
	pipenv run pipenv-setup check

release:
	pipenv run semantic-release publish

print-release:
	pipenv run semantic-release print-version

run-sample-webserver:
	(cd examples && pipenv run python -m http.server)
