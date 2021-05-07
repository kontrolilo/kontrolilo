# -*- coding: utf-8 -*-
from json import dump
from os.path import join
from tempfile import TemporaryDirectory

from license_checks.configuration import Configuration
from license_checks.npm import NpmLicenseChecker
from tests.util import write_config_file


class TestNpmLicenseChecker:
    checker: NpmLicenseChecker

    DEMO_LICENSE_OUTPUT = \
        '''"module name","license","repository"
"xtend@4.0.2","MIT","https://github.com/Raynos/xtend"
"y18n@4.0.0","ISC","https://github.com/yargs/y18n"
"y18n@5.0.5","ISC","https://github.com/yargs/y18n"
"yallist@3.1.1","ISC","https://github.com/isaacs/yallist"
"yallist@4.0.0","ISC","https://github.com/isaacs/yallist"
"yaml@1.10.0","ISC","https://github.com/eemeli/yaml"
"yargs-parser@13.1.2","ISC","https://github.com/yargs/yargs-parser"
"yargs-parser@18.1.3","ISC","https://github.com/yargs/yargs-parser"
"yargs-parser@20.2.4","ISC","https://github.com/yargs/yargs-parser"
"yargs@13.3.2","MIT","https://github.com/yargs/yargs"
"yargs@15.4.1","MIT","https://github.com/yargs/yargs"
"yargs@16.1.1","MIT","https://github.com/yargs/yargs"
"yauzl@2.10.0","MIT","https://github.com/thejoshwolfe/yauzl"
"yn@3.1.1","MIT","https://github.com/sindresorhus/yn"
"yocto-queue@0.1.0","MIT","https://github.com/sindresorhus/yocto-queue"'''

    def setup(self):
        self.checker = NpmLicenseChecker()

    def test_parse_licenses(self):
        licenses = self.checker.parse_licenses(self.DEMO_LICENSE_OUTPUT, Configuration())
        assert licenses == ['MIT', 'ISC']

    def test_main_returns_failure_on_no_config(self):
        with TemporaryDirectory() as directory:
            self.prepare_integration_test_directory(directory)

            result = self.checker.run([join(directory, 'package.json')])
            assert result == 1

    def test_main_returns_success(self):
        with TemporaryDirectory() as directory:
            self.prepare_integration_test_directory(directory)
            write_config_file(directory, ['ISC', 'MIT'])

            result = self.checker.run([join(directory, 'package.json')])
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
