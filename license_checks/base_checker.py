# -*- coding: utf-8 -*-
import abc

import argparse
from builtins import dict
from json import load, dumps
from os.path import abspath, exists
from pathlib import Path
from typing import List


class BaseLicenseChecker(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def prepare_directory(self, directory: str):
        """Prepare the directory for the license check, e.g. by installing all needed tools."""

    @abc.abstractmethod
    def extract_installed_licenses(self, directory: str, configuration: dict) -> List[str]:
        """"""

    def remove_duplicates(self, values: List[str]) -> List[str]:
        return list(dict.fromkeys(values))

    def get_pipenv_directories(self, filenames) -> List[str]:
        directories = []
        for filename in filenames:
            directories.append(abspath(Path(filename).parent.absolute()))
        return self.remove_duplicates(directories)

    def get_config_file_path(self, directory: str) -> str:
        return str(Path(directory, self.CONFIG_FILE_NAME).absolute())

    def load_configuration(self, directory) -> dict:
        config_file_path = self.get_config_file_path(directory)
        if not exists(config_file_path):
            return {}

        with open(config_file_path) as list_file:
            return load(list_file)

    def find_forbidden_licenses(self, used_licenses: List[str], configuration) -> List[str]:
        license_list = []
        if 'allowed_licenses' in configuration:
            license_list = configuration['allowed_licenses']
        return list(set(used_licenses) - set(license_list))

    def print_license_warning(self, directory: str, forbidden_licenses: List[str]):
        forbidden_licenses.sort()
        demo_configuration = {
            'allowed_licenses': forbidden_licenses
        }

        print('**************************************************************')
        print(f'Not all licenses used by pipenv in directory {directory} are allowed.')
        print()
        print('If you want to allow these licenses, please put the following lines into')
        print(f'the allow list file: {self.get_config_file_path(directory)}: ')
        print()
        print(dumps(demo_configuration, indent=2, sort_keys=True))
        print()
        print('**************************************************************')

    def run(self, argv=None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument('filenames', nargs='*', help='filenames to check')
        args = parser.parse_args(argv)

        return_code = 0

        directories = self.get_pipenv_directories(args.filenames)

        for directory in directories:
            print('**************************************************************')
            print(f'Starting scan in {directory}...')

            configuration = self.load_configuration(directory)
            self.prepare_directory(directory)
            used_licenses = self.extract_installed_licenses(directory, configuration)
            forbidden_licenses = self.find_forbidden_licenses(used_licenses, configuration)
            if len(forbidden_licenses) > 0:
                return_code = 1
                self.print_license_warning(directory, forbidden_licenses)

        return return_code
