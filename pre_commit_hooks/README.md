# pre-commit-license-check-python

This repo contains git hooks to integrate with [pre-commit](http://pre-commit.com). These are centered around license
compliance in the python ecosystem.


<!--TOC-->

- [pre-commit-license-check-python](#pre-commit-license-check-python)
  - [Installation](#installation)
  - [Available hooks](#available-hooks)
    - [`license-check-pipenv`](#license-check-pipenv)
  - [Contributing](#contributing)
  - [License](#license)

<!--TOC-->

## Installation

Please install pre-commit first according to the documentation.

Afterwards put the need hook into your `.pre-commit-config.yaml`:

```
---
repos:
  - repo: https://github.com/nbyl/pre-commit-license-check-python
    rev: main
    hooks:
      - id: license-check-pipenv
```

## Available hooks

### `license-check-pipenv`

**What it does**

* This hook checks the contents of a [pipenv](https://pypi.org/project/pipenv/) environment against a definied list of allowed open source licenses.

**Configuration**

To configure the list of allowed licenses, put a file called `.license-check-pipenv.json` alongside your `Pipfile`.

The file must be structured the following way:

```json
{
  "allowed_licenses": [
    "[a list of allowed licenses]",
  ],
  "excluded_packages": [
    "[any package listed here will be excluded from the check]]",
  ]
}
```

**More info**

* [pipenv](https://pypi.org/project/pipenv/)
* [pip-licenses](https://pypi.org/project/pip-licenses/)


## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

The code in this repo is licensed under the [MIT License](LICENSE).
