# -*- coding: utf-8 -*-
from datetime import timedelta
from os.path import exists
from pathlib import Path

from requests_cache import CachedSession
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
    def __init__(self,
                 allowed_licenses=None,
                 excluded_packages=None,
                 includes=None) -> None:

        self.allowed_licenses = allowed_licenses if allowed_licenses else []
        self.excluded_packages = excluded_packages if excluded_packages else []
        self.includes = includes if includes else []

    def to_yaml(self) -> str:
        return dump({
            'allowedLicenses': self.allowed_licenses,
            'excludedPackages': self.excluded_packages,
            'include': [{'url': value.url} for value in self.includes]
        })

    def save(self, directory: str):
        with open(self.get_config_file_path(directory), 'w') as config_file:
            config_file.write(self.to_yaml())

    def merge_includes(self):
        merged_configuration = Configuration(
            allowed_licenses=self.allowed_licenses.copy(),
            excluded_packages=self.excluded_packages.copy(),
        )

        for include in self.includes:
            other_configuration = self.load_external_configuration(include)
            merged_configuration.allowed_licenses += other_configuration.allowed_licenses
            merged_configuration.excluded_packages += other_configuration.excluded_packages

        return merged_configuration

    @staticmethod
    def load_external_configuration(include: ConfigurationInclude):
        session = CachedSession('~/.cache/pre-commit-license-check.sqlite', expire_after=timedelta(days=1))
        response = session.get(include.url)
        response.raise_for_status()

        return Configuration.load_from_string(response.text)

    @staticmethod
    def load_from_string(text):
        content = safe_load(text)

        includes = []
        if 'include' in content:
            includes = [ConfigurationInclude(**value) for value in content['include']]

        return Configuration(
            allowed_licenses=content['allowedLicenses'] if 'allowedLicenses' in content else None,
            excluded_packages=content['excludedPackages'] if 'excludedPackages' in content else None,
            includes=includes
        )

    @staticmethod
    def load_from_directory(directory: str):
        config_file_path = Configuration.get_config_file_path(directory)
        if not exists(config_file_path):
            return Configuration([], [])

        with open(config_file_path) as list_file:
            content = list_file.read()
            return Configuration.load_from_string(content)

    @staticmethod
    def get_config_file_path(directory: str) -> str:
        return str(Path(directory, CONFIG_FILE_NAME).absolute())

    @staticmethod
    def exists_in_directory(directory: str) -> bool:
        return exists(Configuration.get_config_file_path(directory))

    def __eq__(self, o: object) -> bool:
        return self.allowed_licenses == o.allowed_licenses and self.excluded_packages == o.excluded_packages and self.includes == o.includes

    def __repr__(self):
        return f'Configuration(allowedLicenses={self.allowed_licenses},excludedPackages{self.excluded_packages},includes={self.includes})'
