# -*- coding: utf-8 -*-
from os.path import join
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List
from unittest.mock import patch, Mock

from kontrolilo.base_checker import BaseLicenseChecker
from kontrolilo.configuration import Configuration
from kontrolilo.configuration.package import Package


class SimpleLicenseChecker(BaseLicenseChecker):

    def prepare_directory(self, directory: str):
        pass

    def get_license_checker_command(self, directory: str) -> str:
        return "echo 'Hello World!'"

    def parse_packages(self, output: str, configuration: dict, directory: str = None) -> List[Package]:
        return [
            Package('starlette', '0.14.1', 'BSD License'),
            Package('demo1234', '0.14.1', 'GPL'),
            Package('urllib3', '1.26.4', 'MIT License'),
        ]


class TestBaseLicenseChecker:

    def setup(self):
        self.directory = TemporaryDirectory()
        self.checker = SimpleLicenseChecker()

    def test_remove_duplicates(self):
        values = ['a', 'b', 'c', 'a', 'c']
        consolidated_list = self.checker.remove_duplicates(values)
        assert consolidated_list == ['a', 'b', 'c']

    def test_consolidate_directories(self):
        filenames = ['Pipfile.lock', 'Pipfile',
                     'deployment/Pipfile', 'deployment/Pipfile.lock']
        directories = self.checker.consolidate_directories(filenames)
        assert len(directories) == 2
        assert directories == [str(Path('.').absolute()),
                               str(Path('.', 'deployment').absolute())]

    def test_find_invalid_packages(self):
        packages = [
            Package('starlette', '0.14.1', 'BSD License'),
            Package('demo1234', '0.14.1', 'GPL'),
            Package('urllib3', '1.26.4', 'MIT License'),
        ]
        invalid_packages = self.checker.find_invalid_packages(packages, Configuration(
            allowed_licenses=['BSD License', 'MIT License']))
        assert invalid_packages == [Package('demo1234', '0.14.1', 'GPL')]

    def test_print_license_warning(self):
        # this test is mainly run, to verify syntactic correctness
        self.checker.print_license_warning(self.directory.name, [])

    def test_render_demo_config_file_without_file(self):
        text = self.checker.render_demo_config_file(self.directory.name, [Package('demo1234', '0.14.1', 'GPL')])
        assert text != ''

    def test_render_demo_config_file_with_file(self):
        Configuration().save_to_directory(self.directory.name)

        text = self.checker.render_demo_config_file(self.directory.name, [Package('demo1234', '0.14.1', 'GPL')])
        assert text == ''

    def test_remove_excluded_packages(self):
        packages = [
            Package('starlette', '0.14.1', 'BSD License'),
            Package('demo1234', '0.14.1', 'GPL'),
            Package('urllib3', '1.26.4', 'MIT License'),
        ]
        filtered_packages = BaseLicenseChecker.remove_excluded_packages(packages,
                                                                        Configuration(excluded_packages=['demo1234']))
        assert filtered_packages == [
            Package('starlette', '0.14.1', 'BSD License'),
            Package('urllib3', '1.26.4', 'MIT License'),
        ]

    @patch('kontrolilo.base_checker.run')
    def test_load_installed_licenses(self, run_mock):
        result_mock = Mock()
        result_mock.configure_mock(**{'stdout': ''})
        run_mock.return_value = result_mock

        self.checker.load_installed_packages(self.directory, {})
        run_mock.assert_called_once_with('echo \'Hello World!\'', capture_output=True, cwd=self.directory, shell=True,
                                         text=True)

    class Object(object):
        pass

    def test_run_returns_failure_on_no_config(self):
        args = self.Object()
        args.filenames = [join(self.directory.name, 'package.json')]
        result = self.checker.run(args)
        assert result == 1

    def test_run_returns_success(self):
        Configuration(allowed_licenses=['BSD License', 'GPL', 'MIT License']).save_to_directory(self.directory.name)

        args = self.Object()
        args.filenames = [join(self.directory.name, 'package.json')]
        result = self.checker.run(args)
        assert result == 0
