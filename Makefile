local-setup:
	pipenv install -d
	pipenv run pre-commit install
	pipenv run pre-commit install --hook-type commit-msg
