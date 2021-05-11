# -*- coding: utf-8 -*-
import sys
from builtins import dict
from json import loads
from subprocess import run
from typing import List

from license_checks.base_checker import BaseLicenseChecker
from license_checks.configuration import Configuration
from license_checks.package import Package


# TODO: ignore pip-licenses
class PipenvLicenseChecker(BaseLicenseChecker):
    def __init__(self) -> None:
        super().__init__()

    def prepare_directory(self, directory: str):
        run('pipenv install -d', check=True, cwd=directory, shell=True)
        run("pipenv run pip install 'pip-licenses==3.3.1'", check=True, cwd=directory, shell=True)
        # TODO: output only in debug mode

    def get_license_checker_command(self) -> str:
        return 'pipenv run pip-licenses --format=json'

    def parse_packages(self, output: str, configuration: Configuration) -> List[Package]:
        values = loads(output)
        packages = []

        for license_structure in values:
            if not license_structure['Name'] in configuration.excludedPackages:
                packages.append(
                    Package(license_structure['Name'], license_structure['Version'], license_structure['License']))

        return packages


if __name__ == '__main__':
    sys.exit(PipenvLicenseChecker().run(sys.argv[1:]))
