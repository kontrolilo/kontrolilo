# -*- coding: utf-8 -*-

import sys
from json import load
from logging import DEBUG, basicConfig, getLogger
from pathlib import Path
from typing import List

from license_checks.base_checker import BaseLicenseChecker, shared_main
from license_checks.configuration import Configuration
from license_checks.configuration.package import Package

logger = getLogger(__name__)


class GradleLicenseChecker(BaseLicenseChecker):

    def prepare_directory(self, directory: str):
        pass

    def get_license_checker_command(self, directory: str) -> str:
        wrapper_path = Path(directory, 'gradlew')

        binary = 'gradlew'
        if wrapper_path.exists():
            binary = wrapper_path.absolute()

        return f'{binary} -I {Path(Path(__file__).parent.absolute(), "init.gradle").absolute()} licenseReport'

    def parse_packages(self, output: str, configuration: Configuration, directory: str) -> List[Package]:
        packages = []

        licenses_file_path = Path(directory, 'build', 'reports', 'licenses', 'licenseReport.json')

        logger.debug('Loading license data from [%s]', licenses_file_path.absolute())

        with open(licenses_file_path.absolute()) as license_file:
            dependencies = load(license_file)
            for dependency in dependencies:
                artifact_name = dependency['dependency']

                version = ''
                index = artifact_name.rfind(':')
                if index > -1:
                    version = artifact_name[index + 1:]
                    artifact_name = artifact_name[:index]

                license_names = []
                for license_entry in dependency['licenses']:
                    license_names.append(license_entry['license'])
                license_names.sort()

                packages.append(Package(artifact_name, version, ';'.join(license_names)))

        logger.debug('Found %s packages in license file.', len(packages))

        return packages


def main():
    shared_main(GradleLicenseChecker())


if __name__ == '__main__':
    main()
