# -*- coding: utf-8 -*-
import os
from json import loads
from subprocess import run
from typing import List

from kontrolilo.base_checker import BaseLicenseChecker
from kontrolilo.configuration import Configuration
from kontrolilo.configuration.package import Package
from kontrolilo.shared_main import shared_main


class PipenvLicenseChecker(BaseLicenseChecker):
    def prepare_directory(self, directory: str):
        run('pipenv install -d', capture_output=True, check=True, cwd=directory, env=self.get_license_checker_env(),
            shell=True)
        run("pipenv run pip install 'pip-licenses==*'", capture_output=True, check=True, cwd=directory,
            env=self.get_license_checker_env(), shell=True)

    def get_license_checker_command(self, directory: str) -> str:
        return 'pipenv run pip-licenses --format=json'

    def get_license_checker_env(self):
        return dict(os.environ, PIPENV_IGNORE_VIRTUALENVS='1')

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
