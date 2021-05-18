# -*- coding: utf-8 -*-
from json import dump
from os.path import join
from tempfile import TemporaryDirectory
from unittest.mock import patch, call

import pytest

from license_checks.configuration import Configuration
from license_checks.npm import NpmLicenseChecker
from license_checks.package import Package


class TestNpmLicenseChecker:
    DEMO_LICENSE_OUTPUT = \
        '''"module name","license","repository"
"xtend@4.0.2","MIT","https://github.com/Raynos/xtend"
"y18n@4.0.0","ISC","https://github.com/yargs/y18n"
"y18n@5.0.5","ISC","https://github.com/yargs/y18n"'''

    def setup(self):
        self.directory = TemporaryDirectory()
        self.checker = NpmLicenseChecker()

    @patch('license_checks.npm.run')
    def test_prepare_directory(self, run_mock):
        run_mock.return_value = {}

        with TemporaryDirectory() as directory:
            self.checker.prepare_directory(directory)
            run_mock.assert_has_calls([
                call('npm install --no-audit --no-fund', capture_output=True, check=True, cwd=directory, shell=True),
            ])

    def test_get_license_checker_command(self):
        assert self.checker.get_license_checker_command() == 'npx license-checker --csv'

    def test_parse_packages(self):
        packages = self.checker.parse_packages(self.DEMO_LICENSE_OUTPUT, Configuration(
            allowed_licenses=[],
            excluded_packages=[]
        ))
        assert packages == [
            Package('xtend', '4.0.2', 'MIT'),
            Package('y18n', '4.0.0', 'ISC'),
            Package('y18n', '5.0.5', 'ISC'),

        ]

    @pytest.mark.skip
    def test_main_returns_failure_on_no_config(self):
        self.prepare_integration_test_directory(self.directory.name)

        result = self.checker.run([join(self.directory.name, 'package.json')])
        assert result == 1

    @pytest.mark.skip
    def test_main_returns_success(self):
        self.prepare_integration_test_directory(self.directory.name)
        write_config_file(self.directory.name, ['ISC', 'MIT'])

        result = self.checker.run([join(self.directory.name, 'package.json')])
        assert result == 0

    @staticmethod
    def prepare_integration_test_directory(directory: str):
        package = {
            'name': 'pre-commit-integration-test',
            'version': '1.0.0',
            'description': 'No big deal.',
            'main': 'index.js',
            'scripts': {
                'test': "echo \"Error: no test specified\" && exit 1"
            },
            'author': '',
            'license': 'ISC',
            'dependencies': {
                'lodash': '^4.17.21'
            }
        }

        with open(join(directory, 'package.json'), 'w+')as package_file:
            dump(package, package_file)
