.PHONY: clean docs test
help:	## Show this help.
		@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean:
	rm -rf build

build:
	mkdir build

binary: build
	CGO_ENABLED=0 go build -o build/kontrolilo

test:
	go test ./...

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

docs:
	hugo -s docs

docs-server:
	hugo server -s docs
