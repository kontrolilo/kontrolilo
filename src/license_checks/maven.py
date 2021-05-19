# -*- coding: utf-8 -*-
import sys
from json import loads
from typing import List

from license_checks.base_checker import BaseLicenseChecker
from license_checks.configuration import Configuration
from license_checks.configuration.package import Package


class MavenLicenseChecker(BaseLicenseChecker):
    def prepare_directory(self, directory: str):
        pass

    def get_license_checker_command(self) -> str:
        # TODO: don't use wrapper when not present
        return './mvnw org.codehaus.mojo:license-maven-plugin:2.0.0:download-licenses'

    def parse_packages(self, output: str, configuration: Configuration, directory: str) -> List[Package]:
        values = loads(output)
        packages = []

        for license_structure in values:
            if not license_structure['Name'] in configuration.excluded_packages:
                packages.append(
                    Package(license_structure['Name'], license_structure['Version'], license_structure['License']))

        return packages


def main():
    sys.exit(MavenLicenseChecker().run(sys.argv[1:]))


if __name__ == '__main__':
    main()
