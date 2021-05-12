# -*- coding: utf-8 -*-
import sys
from tempfile import TemporaryDirectory

from yaml import dump

from license_checks.configuration import Configuration, ConfigurationInclude


class TestConfiguration:
    def test_load_without_file(self):
        with TemporaryDirectory() as directory:
            configuration = Configuration.load(directory)
            assert configuration == Configuration([], [])

    def test_load_with_partial_values(self):
        demo_configuration = {
            'allowedLicenses': [
                'MIT',
                'GPL'
            ],
        }

        with TemporaryDirectory() as directory:
            with open(Configuration.get_config_file_path(directory), 'w') as config_file:
                dump(demo_configuration, config_file)

            configuration = Configuration.load(directory)
            assert configuration == Configuration(['MIT', 'GPL'])

    def test_load_with_file(self):
        demo_configuration = {
            'allowedLicenses': [
                'MIT',
                'GPL'
            ],
            'excludedPackages': [
                'demo1234'
            ],
            'include': [
                {
                    'url': 'http://localhost:8000/license-check-node.yaml'
                }
            ]
        }

        with TemporaryDirectory() as directory:
            with open(Configuration.get_config_file_path(directory), 'w') as config_file:
                dump(demo_configuration, config_file)

            configuration = Configuration.load(directory)
            assert configuration == Configuration(['MIT', 'GPL'], ['demo1234'],
                                                  [ConfigurationInclude('http://localhost:8000/license-check-node.yaml')])

    def test_to_yaml(self):
        demo_configuration = Configuration(
            allowedLicenses=[
                'MIT',
                'GPL'
            ],
            excludedPackages=[
                'demo1234'
            ],
            includes=[
                ConfigurationInclude(url='http://localhost:8000/license-check-node.yaml')
            ]
        )
        expected = '''allowedLicenses:
- MIT
- GPL
excludedPackages:
- demo1234
include:
- url: http://localhost:8000/license-check-node.yaml
'''

        assert demo_configuration.to_yaml() == expected
