# -*- coding: utf-8 -*-
from tempfile import TemporaryDirectory

from yaml import dump

from license_checks.configuration import Configuration


class TestConfiguration:
    def test_load_configuration_without_file(self):
        with TemporaryDirectory() as directory:
            configuration = Configuration.load_configuration(directory)
            assert configuration == Configuration([], [])

    def test_load_configuration_with_partial_values(self):
        demo_configuration = {
            'allowedLicenses': [
                'MIT',
                'GPL'
            ],
        }

        with TemporaryDirectory() as directory:
            with open(Configuration.get_config_file_path(directory), 'w') as config_file:
                dump(demo_configuration, config_file)

            configuration = Configuration.load_configuration(directory)
            assert configuration == Configuration(['MIT', 'GPL'])

    def test_load_configuration_with_file(self):
        demo_configuration = {
            'allowedLicenses': [
                'MIT',
                'GPL'
            ],
            'excludedPackages': [
                'demo1234'
            ]
        }

        with TemporaryDirectory() as directory:
            with open(Configuration.get_config_file_path(directory), 'w') as config_file:
                dump(demo_configuration, config_file)

            configuration = Configuration.load_configuration(directory)
            assert configuration == Configuration(['MIT', 'GPL'], ['demo1234'])

    def test_dump(self):
        demo_configuration = Configuration(
            allowedLicenses=[
                'MIT',
                'GPL'
            ],
            excludedPackages=[
                'demo1234'
            ]
        )
        expected = '''allowedLicenses:
- MIT
- GPL
excludedPackages:
- demo1234
'''

        assert demo_configuration.dump() == expected
