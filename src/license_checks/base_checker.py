# -*- coding: utf-8 -*-
import abc
import argparse
from builtins import dict
from os.path import abspath
from pathlib import Path
from subprocess import run
from typing import List

from texttable import Texttable

from license_checks.configuration import Configuration
from license_checks.package import Package


class BaseLicenseChecker(metaclass=abc.ABCMeta):
    debug = False

    @abc.abstractmethod
    def prepare_directory(self, directory: str):
        """Prepare the directory for the license check, e.g. by installing all needed tools."""

    @abc.abstractmethod
    def get_license_checker_command(self) -> str:
        """Return the command needed to run in the target directory"""

    @abc.abstractmethod
    def parse_packages(self, output: str, configuration: dict) -> List[Package]:
        """Parse the licenses from the output of the checker program."""

    def load_installed_packages(self, directory: str, configuration: dict) -> List[Package]:
        result = run(self.get_license_checker_command(), capture_output=True, check=True, cwd=directory,
                     shell=True, text=True)
        return self.parse_packages(result.stdout, configuration)

    def consolidate_directories(self, filenames) -> List[str]:
        directories = []
        for filename in filenames:
            directories.append(abspath(Path(filename).parent.absolute()))
        return self.remove_duplicates(directories)

    def run(self, argv=None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument('--debug', action='store_true', help='print debug messages to stderr')
        parser.add_argument('filenames', nargs='*', help='filenames to check')
        args = parser.parse_args(argv)

        self.debug = args.debug

        return_code = 0

        directories = self.consolidate_directories(args.filenames)

        for directory in directories:
            print('**************************************************************')
            print(f'Starting scan in {directory}...')

            configuration = Configuration.load_from_directory(directory).merge_includes()
            self.prepare_directory(directory)
            installed_packages = self.load_installed_packages(directory, configuration)
            filtered_packages = self.remove_excluded_packages(installed_packages, configuration)
            invalid_packages = self.find_invalid_packages(filtered_packages, configuration)
            if len(invalid_packages) > 0:
                return_code = 1
                self.print_license_warning(directory, invalid_packages)

        return return_code

    @staticmethod
    def remove_excluded_packages(installed_packages: List[Package], configuration: Configuration) -> List[Package]:
        return list(filter(lambda package: package.name not in configuration.excluded_packages, installed_packages))

    @staticmethod
    def remove_duplicates(values: List[str]) -> List[str]:
        return list(dict.fromkeys(values))

    @staticmethod
    def print_license_warning(directory: str, invalid_packages: List[Package]):
        invalid_packages.sort(key=lambda package: package.name)

        license_table = Texttable()
        license_table.header(['Name', 'Version', 'License'])
        for package in invalid_packages:
            license_table.add_row([package.name, package.version, package.license])

        text = f'''
Not all licenses used in directory {directory} are allowed:

{license_table.draw()}
{BaseLicenseChecker.render_demo_config_file(directory, invalid_packages)}
'''
        print(text)

    @staticmethod
    def render_demo_config_file(directory: str, invalid_packages: List[Package]) -> str:
        if Configuration.exists_in_directory(directory):
            return ''

        licenses = BaseLicenseChecker.remove_duplicates(list(map(lambda package: package.license, invalid_packages)))
        licenses.sort()
        demo_configuration = Configuration(allowed_licenses=licenses)

        return f'''

To allow all licenses, create a file called {Configuration.get_config_file_path(directory)}:
---
{demo_configuration.to_yaml()}'''

    @staticmethod
    def find_invalid_packages(installed_packages: List[Package], configuration) -> List[Package]:
        return list(filter(lambda package: package.license not in configuration.allowed_licenses, installed_packages))
