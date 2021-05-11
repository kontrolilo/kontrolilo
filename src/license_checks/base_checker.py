# -*- coding: utf-8 -*-
import abc

import argparse
from builtins import dict
from os.path import abspath, exists
from pathlib import Path
from subprocess import run
from typing import List

from license_checks.configuration import Configuration
from license_checks.package import Package


class BaseLicenseChecker(metaclass=abc.ABCMeta):

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
        parser.add_argument('filenames', nargs='*', help='filenames to check')
        args = parser.parse_args(argv)

        return_code = 0

        directories = self.consolidate_directories(args.filenames)

        for directory in directories:
            print('**************************************************************')
            print(f'Starting scan in {directory}...')

            configuration = Configuration.load_configuration(directory)
            self.prepare_directory(directory)
            installed_packages = self.load_installed_packages(directory, configuration)
            # TODO: add exclude here
            invalid_packages = self.find_invalid_packages(installed_packages, configuration)
            if len(invalid_packages) > 0:
                return_code = 1
                self.print_license_warning(directory, invalid_packages)

        return return_code

    @staticmethod
    def remove_duplicates(values: List[str]) -> List[str]:
        return list(dict.fromkeys(values))

    @staticmethod
    def print_license_warning(directory: str, invalid_packages: List[str]):
        invalid_packages.sort(key=lambda package: package.name)
        # demo_configuration = Configuration(allowedLicenses=forbidden_licenses)

        test = f'''
        **************************************************************
        Not all licenses used in directory {directory} are allowed.
        **************************************************************
        '''
        # TODO: print list of packages
        # TODO: print file contents only if it does not exist

        # print('**************************************************************')
        # print(f'Not all licenses used by pipenv in directory {directory} are allowed.')
        # print()
        # print('If you want to allow these licenses, please put the following lines into')
        # print(f'the allow list file: {Configuration.get_config_file_path(directory)}: ')
        # print()
        # print(demo_configuration.dump())
        # print()
        # print('**************************************************************')

    @staticmethod
    def find_invalid_packages(installed_packages: List[Package], configuration) -> List[Package]:
        return list(filter(lambda package: package.license not in configuration.allowedLicenses, installed_packages))
