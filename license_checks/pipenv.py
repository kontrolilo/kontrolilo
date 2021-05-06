# -*- coding: utf-8 -*-
import sys
from builtins import dict
from json import loads
from subprocess import run
from typing import List

from license_checks.base_checker import BaseLicenseChecker


class PipenvLicenseChecker(BaseLicenseChecker):
    def __init__(self) -> None:
        super().__init__()

    def prepare_directory(self, directory: str):
        run('pipenv install -d', check=True, cwd=directory, shell=True)
        run("pipenv run pip install 'pip-licenses==3.3.1'", check=True, cwd=directory, shell=True)

    def get_license_checker_command(self) -> str:
        return 'pipenv run pip-licenses --format=json'

    def parse_licenses(self, output: str, configuration: dict) -> List[str]:
        values = loads(output)
        licenses = []
        excluded_packages = []
        if 'excluded_packages' in configuration:
            excluded_packages = configuration['excluded_packages']

        for license_structure in values:
            if not license_structure['Name'] in excluded_packages:
                licenses.append(license_structure['License'])

        return self.remove_duplicates(licenses)

if __name__ == '__main__':
    sys.exit(PipenvLicenseChecker().run(sys.argv[1:]))
