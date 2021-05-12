# -*- coding: utf-8 -*-
from os.path import exists
from pathlib import Path

from yaml import dump, safe_load

CONFIG_FILE_NAME = '.license-check.yaml'


class ConfigurationInclude:
    url: str

    def __init__(self, url) -> None:
        self.url = url

    def __eq__(self, o: object) -> bool:
        return self.url == o.url

    def __repr__(self) -> str:
        return f'ConfigurationInclude(url={self.url})'


class Configuration:
    allowedLicenses = []
    excludedPackages = []
    includes = []

    def __init__(self,
                 allowedLicenses=None,
                 excludedPackages=None,
                 includes=None) -> None:
        if allowedLicenses:
            self.allowedLicenses = allowedLicenses
        if excludedPackages:
            self.excludedPackages = excludedPackages
        if includes:
            self.includes = includes

    def to_yaml(self) -> str:
        return dump({
            'allowedLicenses': self.allowedLicenses,
            'excludedPackages': self.excludedPackages,
            'include': [{'url': value.url} for value in self.includes]
        })

    def save(self, directory: str):
        with open(self.get_config_file_path(directory), 'w') as config_file:
            dump(self, config_file)

    @staticmethod
    def load(directory: str):
        config_file_path = Configuration.get_config_file_path(directory)
        if not exists(config_file_path):
            return Configuration([], [])

        with open(config_file_path) as list_file:
            content = safe_load(list_file)

            includes = []
            if 'include' in content:
                includes = [ConfigurationInclude(**value) for value in content['include']]

            return Configuration(
                allowedLicenses=content['allowedLicenses'] if 'allowedLicenses' in content else None,
                excludedPackages=content['excludedPackages'] if 'excludedPackages' in content else None,
                includes=includes
            )

    @staticmethod
    def get_config_file_path(directory: str) -> str:
        return str(Path(directory, CONFIG_FILE_NAME).absolute())

    @staticmethod
    def exists_in_directory(directory: str) -> bool:
        return exists(Configuration.get_config_file_path(directory))

    def __eq__(self, o: object) -> bool:
        return self.allowedLicenses == o.allowedLicenses and self.excludedPackages == o.excludedPackages and self.includes == o.includes

    def __repr__(self):
        return f'Configuration(allowedLicenses={self.allowedLicenses},excludedPackages{self.excludedPackages},includes={self.includes})'
