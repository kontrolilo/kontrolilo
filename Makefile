help:	## Show this help.
		@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

local-setup:
	pipenv install -d
	pipenv run pre-commit install
	pipenv run pre-commit install --hook-type commit-msg

test:
	pipenv run pytest --cov=pre_commit_hooks --cov-report term-missing tests/

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
