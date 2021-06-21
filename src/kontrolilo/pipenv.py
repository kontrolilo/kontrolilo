# -*- coding: utf-8 -*-
from json import loads
from subprocess import run
from typing import List

from kontrolilo.base_checker import BaseLicenseChecker
from kontrolilo.shared_main import shared_main
from kontrolilo.configuration import Configuration
from kontrolilo.configuration.package import Package


# TODO: ignore pip-licenses
class PipenvLicenseChecker(BaseLicenseChecker):
    def prepare_directory(self, directory: str):
        run('pipenv install -d', capture_output=True, check=True, cwd=directory, shell=True)
        run("pipenv run pip install 'pip-licenses==3.3.1'", capture_output=True, check=True, cwd=directory,
            shell=True)

    def get_license_checker_command(self, directory: str) -> str:
        return 'pipenv run pip-licenses --format=json'

    def parse_packages(self, output: str, configuration: Configuration, directory: str) -> List[Package]:
        values = loads(output)
        packages = []

        for license_structure in values:
            if not license_structure['Name'] in configuration.excluded_packages:
                packages.append(
                    Package(license_structure['Name'], license_structure['Version'], license_structure['License']))

        return packages


def main():
    shared_main(PipenvLicenseChecker())


if __name__ == '__main__':
    main()
