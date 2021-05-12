# -*- coding: utf-8 -*-
import csv
from subprocess import run
from sys import argv
from typing import List

from license_checks.base_checker import BaseLicenseChecker
from license_checks.package import Package


class NpmLicenseChecker(BaseLicenseChecker):
    def prepare_directory(self, directory: str):
        run('npm install --no-audit --no-fund', capture_output=not self.debug, check=True, cwd=directory, shell=True)

    def get_license_checker_command(self) -> str:
        # yes, we are using csv here. license-checker's json output does not build an array of licenses, which is
        # pretty hard to parse.
        return 'npx license-checker --csv'

    def parse_packages(self, output: str, configuration: dict) -> List[Package]:
        packages = []
        package_reader = csv.DictReader(output.splitlines())
        for row in package_reader:
            module = row['module name']
            name = module
            version = module
            index = module.find('@')
            if index > 0:
                name = module[:index]
                version = module[index + 1:]

            packages.append(Package(name, version, row['license']))

        return packages


def main():
    exit(NpmLicenseChecker().run(argv[1:]))


if __name__ == '__main__':
    main()
