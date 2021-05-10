# -*- coding: utf-8 -*-
from os.path import exists
from pathlib import Path

from yaml import load, dump

CONFIG_FILE_NAME = '.license-check.yaml'


class Configuration:
    allowedLicenses = []
    excludedPackages = []

    def __init__(self, allowedLicenses=None, excludedPackages=None) -> None:
        if allowedLicenses:
            self.allowedLicenses = allowedLicenses
        if excludedPackages:
            self.excludedPackages = excludedPackages

    def load_configuration(directory: str):
        config_file_path = Configuration.get_config_file_path(directory)
        if not exists(config_file_path):
            return Configuration([], [])

        with open(config_file_path) as list_file:
            content = load(list_file)

            return Configuration(**content)

    def get_config_file_path(directory: str) -> str:
        return str(Path(directory, CONFIG_FILE_NAME).absolute())

    def __eq__(self, o: object) -> bool:
        return self.allowedLicenses == o.allowedLicenses and self.excludedPackages == o.excludedPackages

    def __str__(self) -> str:
        return f'Configuration(allowedLicenses={self.allowedLicenses},excludedPackages{self.excludedPackages})'

    def dump(self) -> str:
        return dump({
            'allowedLicenses': self.allowedLicenses,
            'excludedPackages': self.excludedPackages
        })
