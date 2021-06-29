---
title: "Configuration"

weight: 10
---

kontrolilo is configured by using a configuration file. To configure the list of allowed licenses, put a file
called `.license-check.yaml` alongside the file containing the declaration of your dependencies (e.g. `package.json`
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

By using this feature, you can build a central list of allowed licenses to keep this configuration in sync for all your
projects:

```yaml
allowedLicenses: []
excludedPackages: []
include:
  - url: https://raw.githubusercontent.com/nbyl/license-check-config/main/commercial-use/license-check-python.yaml
  - url: https://raw.githubusercontent.com/nbyl/license-check-config/main/open-source/license-check-python.yaml
```

An examples of such a central repository can be found
under [nbyl/license-check-config](https://github.com/nbyl/license-check-config).
