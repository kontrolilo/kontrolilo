# -*- coding: utf-8 -*-
import abc

import argparse
from builtins import dict
from os.path import abspath, exists
from pathlib import Path
from subprocess import run
from typing import List

from license_checks.configuration import Configuration


class BaseLicenseChecker(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def prepare_directory(self, directory: str):
        """Prepare the directory for the license check, e.g. by installing all needed tools."""

    @abc.abstractmethod
    def get_license_checker_command(self) -> str:
        """Return the command needed to run in the target directory"""

    @abc.abstractmethod
    def parse_licenses(self, output: str, configuration: dict) -> List[str]:
        """Parse the licenses from the output of the checker program."""

    def load_installed_licenses(self, directory: str, configuration: dict) -> List[str]:
        result = run(self.get_license_checker_command(), capture_output=True, check=True, cwd=directory,
                     shell=True, text=True)
        return self.parse_licenses(result.stdout, configuration)

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
            used_licenses = self.load_installed_licenses(directory, configuration)
            forbidden_licenses = self.find_forbidden_licenses(used_licenses, configuration)
            if len(forbidden_licenses) > 0:
                return_code = 1
                self.print_license_warning(directory, forbidden_licenses)

        return return_code

    @staticmethod
    def remove_duplicates(values: List[str]) -> List[str]:
        return list(dict.fromkeys(values))

    @staticmethod
    def print_license_warning(directory: str, forbidden_licenses: List[str]):
        forbidden_licenses.sort()
        demo_configuration = Configuration(allowedLicenses=forbidden_licenses)

        print('**************************************************************')
        print(f'Not all licenses used by pipenv in directory {directory} are allowed.')
        print()
        print('If you want to allow these licenses, please put the following lines into')
        print(f'the allow list file: {Configuration.get_config_file_path(directory)}: ')
        print()
        print(demo_configuration.dump())
        print()
        print('**************************************************************')

    @staticmethod
    def find_forbidden_licenses(used_licenses: List[str], configuration) -> List[str]:
        return list(set(used_licenses) - set(configuration.allowedLicenses))
