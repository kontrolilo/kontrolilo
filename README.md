# kontrolilo

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/kontrolilo/kontrolilo/release%20project?label=Release&style=for-the-badge)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/kontrolilo/kontrolilo/run%20all%20tests?label=PR%20tests&style=for-the-badge)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/kontrolilo/kontrolilo?style=for-the-badge)
![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/kontrolilo/kontrolilo?style=for-the-badge)
![Code Climate coverage](https://img.shields.io/codeclimate/coverage/kontrolilo/kontrolilo?style=for-the-badge)

This repo contains git hooks to integrate with [pre-commit](http://pre-commit.com). These are centered around license
compliance in the python ecosystem.


<!--TOC-->

- [kontrolilo](#kontrolilo)
  - [Installation](#installation)
  - [Configuration](#configuration)
    - [Include external configuration files](#include-external-configuration-files)
  - [Available hooks](#available-hooks)
    - [`license-check-configuration-lint`](#license-check-configuration-lint)
    - [`license-check-gradle`](#license-check-gradle)
    - [`license-check-maven`](#license-check-maven)
    - [`license-check-npm`](#license-check-npm)
    - [`license-check-pipenv`](#license-check-pipenv)
  - [Contributing](#contributing)
  - [License](#license)
  - [Docs](#docs)

<!--TOC-->

## Installation

Please install pre-commit first according to the documentation.

Afterwards put the needed hooks into your `.pre-commit-config.yaml`:

```
---
repos:
  - repo: https://github.com/kontrolilo/kontrolilo
    rev: main
    hooks:
      - id: license-check-configuration-lint
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
include: []
```

### Include external configuration files

Through the include keyword in the configuration file, you can load license lists from external HTTP(S) sources.

By using this feature, you can build a central list of allowed licenses to keep this configuration in sync for all your projects:

```yaml
allowedLicenses: []
excludedPackages: []
include:
- url: https://raw.githubusercontent.com/nbyl/license-check-config/main/commercial-use/license-check-python.yaml
- url: https://raw.githubusercontent.com/nbyl/license-check-config/main/open-source/license-check-python.yaml
```

An examples of such a central repository can be found under [nbyl/license-check-config](https://github.com/nbyl/license-check-config).

## Available hooks

### `license-check-configuration-lint`

**What it does**

* This hook lints configurations files as described above. It checks for correctness and sorts the licenses.

**More info**

* [gradle](https://gradle.org/)
* [gradle-license-plugin](https://github.com/jaredsburrows/gradle-license-plugin)


### `license-check-gradle`

**What it does**

* This hook checks the licenses of your gradle dependencies declared in a `build.gradle` against defined list of allowed open
  source licenses.

**More info**

* [gradle](https://gradle.org/)
* [gradle-license-plugin](https://github.com/jaredsburrows/gradle-license-plugin)

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


## Docs

git remote add theme https://github.com/matcornic/hugo-theme-learn.git
