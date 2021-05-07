# -*- coding: utf-8 -*-
from sys import argv
from typing import List

from license_checks.base_checker import BaseLicenseChecker
from license_checks.configuration import Configuration


class PipenvLicenseChecker(BaseLicenseChecker):
    def __init__(self) -> None:
        super().__init__()

    def prepare_directory(self, directory: str):
        pass

    def get_license_checker_command(self) -> str:
        return 'npx license-checker'

    def parse_licenses(self, output: str, configuration: Configuration) -> List[str]:
        return []


if __name__ == '__main__':
    exit(PipenvLicenseChecker().run(argv[1:]))
