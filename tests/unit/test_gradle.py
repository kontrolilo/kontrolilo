# -*- coding: utf-8 -*-
from os.path import join
from pathlib import Path
from tempfile import TemporaryDirectory

from kontrolilo.configuration import Configuration
from kontrolilo.configuration.package import Package
from kontrolilo.gradle import GradleLicenseChecker


class TestGradleLicenseChecker:
    LICENSE_REPORT_JSON = '''[
      {
        "project": "Apache Log4j API",
        "description": "The Apache Log4j API",
        "version": "2.13.3",
        "developers": [],
        "url": null,
        "year": null,
        "licenses": [
          {
            "license": "Apache License, Version 2.0",
            "license_url": "https://www.apache.org/licenses/LICENSE-2.0.txt"
          }
        ],
        "dependency": "org.apache.logging.log4j:log4j-api:2.13.3"
      },
      {
        "project": "Apache Log4j to SLF4J Adapter",
        "description": "The Apache Log4j binding between Log4j 2 API and SLF4J.",
        "version": "2.13.3",
        "developers": [],
        "url": null,
        "year": null,
        "licenses": [
          {
            "license": "Apache License, Version 2.0",
            "license_url": "https://www.apache.org/licenses/LICENSE-2.0.txt"
          }
        ],
        "dependency": "org.apache.logging.log4j:log4j-to-slf4j:2.13.3"
      },
      {
        "project": "Jackson datatype: jdk8",
        "description": "Add-on module for Jackson (http://jackson.codehaus.org) to support\\nJDK 8 data types.",
        "version": "2.11.4",
        "developers": [],
        "url": null,
        "year": null,
        "licenses": [
          {
            "license": "The Apache Software License, Version 2.0",
            "license_url": "http://www.apache.org/licenses/LICENSE-2.0.txt"
          }
        ],
        "dependency": "com.fasterxml.jackson.datatype:jackson-datatype-jdk8:2.11.4"
      }
    ]'''

    def setup(self):
        self.directory = TemporaryDirectory()
        self.checker = GradleLicenseChecker()

    def test_prepare_directory(self):
        self.checker.prepare_directory(self.directory.name)

    def test_get_license_checker_command(self):
        assert self.checker.get_license_checker_command(
            self.directory.name) == f'gradlew -I {self.checker.init_script.name} licenseReport'

    def test_get_license_checker_command_with_wrapper_present(self):
        Path(join(self.directory.name, 'gradlew')).touch()
        assert self.checker.get_license_checker_command(
            self.directory.name) == f"{join(self.directory.name, 'gradlew')} -I {self.checker.init_script.name} licenseReport"

    def test_parse_packages(self):
        target_directory = Path(self.directory.name, 'build', 'reports', 'licenses')
        target_directory.mkdir(parents=True)

        with open(join(target_directory.absolute(), 'licenseReport.json'), 'w') as licenses_file:
            licenses_file.write(self.LICENSE_REPORT_JSON)

        packages = self.checker.parse_packages('', Configuration(
            allowed_licenses=[],
            excluded_packages=[]
        ),
                                               self.directory.name)
        assert packages == [
            Package('org.apache.logging.log4j:log4j-api', '2.13.3',
                    'Apache License, Version 2.0'),
            Package('org.apache.logging.log4j:log4j-to-slf4j', '2.13.3',
                    'Apache License, Version 2.0'),
            Package('com.fasterxml.jackson.datatype:jackson-datatype-jdk8', '2.11.4',
                    'The Apache Software License, Version 2.0'),
        ]
