# -*- coding: utf-8 -*-
import csv
from sys import argv
from typing import List

from license_checks.base_checker import BaseLicenseChecker
from license_checks.configuration import Configuration


class NpmLicenseChecker(BaseLicenseChecker):
    def __init__(self) -> None:
        super().__init__()

    def prepare_directory(self, directory: str):
        pass

    def get_license_checker_command(self) -> str:
        # yes, we are using csv here. license-checker's json output does not build an array of licenses, which is
        # pretty hard to parse.
        return 'npx license-checker --csv'

    def parse_licenses(self, output: str, configuration: Configuration) -> List[str]:
        licenses = []
        license_reader = csv.DictReader(output.splitlines())
        for row in license_reader:
            licenses.append(row['license'])
        return self.remove_duplicates(licenses)


if __name__ == '__main__':
    exit(NpmLicenseChecker().run(argv[1:]))
