# pre-commit-license-checks

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/nbyl/pre-commit-license-checks/release%20project?label=Release&style=for-the-badge)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/nbyl/pre-commit-license-checks/run%20all%20tests?label=PR%20tests&style=for-the-badge)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/nbyl/pre-commit-license-checks?style=for-the-badge)
![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/nbyl/pre-commit-license-checks?style=for-the-badge)
![Code Climate coverage](https://img.shields.io/codeclimate/coverage/nbyl/pre-commit-license-checks?style=for-the-badge)

This repo contains git hooks to integrate with [pre-commit](http://pre-commit.com). These are centered around license
compliance in the python ecosystem.


<!--TOC-->

- [pre-commit-license-checks](#pre-commit-license-checks)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Available hooks](#available-hooks)
    - [`license-check-maven`](#license-check-maven)
    - [`license-check-npm`](#license-check-npm)
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
  - repo: https://github.com/nbyl/pre-commit-license-checks
    rev: main
    hooks:
      - id: license-check-npm
      - id: license-check-pipenv
```

## Configuration

All hooks in this repository share a common configuration file format. To configure the list of allowed licenses, put a
file called `.license-check.yaml` alongside the file containing the declaration of you dependencies (e.g. `package.json`
. `pom.xml`, ...).

The file must be structured the following way:

```yaml
---
allowedLicenses:
  - a
  - list
  - of
  - allowed
  - licenses
  - ...
excludedPackages:
  - any
  - package
  - listed
  - here
  - will
  - be
  - excluded
  - from
  - the
  - check
  - ...
```

## Available hooks

### `license-check-maven`

**What it does**

* This hook checks the licenses of your maven dependencies declared in a `pom.xml` against defined list of allowed open
  source licenses.

**More info**

* [maven](https://maven.apache.org/)
* [license-maven-plugin](https://www.mojohaus.org/license-maven-plugin/)

### `license-check-npm`

**What it does**

* This hook checks the licenses of your dependencies declared in a `package.json` against defined list of allowed open
  source licenses.

**More info**

* [npm](https://www.npmjs.com/)
* [license-checker](https://www.npmjs.com/package/license-checker)

### `license-check-pipenv`

**What it does**

* This hook checks the contents of a [pipenv](https://pypi.org/project/pipenv/) environment against a defined list of
  allowed open source licenses.

**More info**

* [pipenv](https://pypi.org/project/pipenv/)
* [pip-licenses](https://pypi.org/project/pip-licenses/)

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

The code in this repo is licensed under the [MIT License](LICENSE).
