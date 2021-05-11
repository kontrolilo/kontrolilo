# -*- coding: utf-8 -*-

from os.path import join
from shutil import copy2
from subprocess import run
from tempfile import TemporaryDirectory
from unittest.mock import patch, call

from license_checks.configuration import Configuration
from license_checks.package import Package
from license_checks.pipenv import PipenvLicenseChecker
from tests.util import write_config_file


class TestPipenvLicenseChecker:
    DEMO_LICENSE_OUTPUT = '''[
          {
            "License": "BSD License",
            "Name": "starlette",
            "Version": "0.14.1"
          },
          {
            "License": "GPL",
            "Name": "demo1234",
            "Version": "0.14.1"
          },
          {
            "License": "MIT License",
            "Name": "urllib3",
            "Version": "1.26.4"
          },
          {
            "License": "BSD License",
            "Name": "uvicorn",
            "Version": "0.13.3"
          },
          {
            "License": "MIT License",
            "Name": "zipp",
            "Version": "3.4.1"
          }
        ]
        '''

    checker: PipenvLicenseChecker

    def setup(self):
        self.checker = PipenvLicenseChecker()

    def test_parse_packages(self):
        packages = self.checker.parse_packages(self.DEMO_LICENSE_OUTPUT, Configuration())
        assert packages == [
            Package('starlette', '0.14.1', 'BSD License'),
            Package('demo1234', '0.14.1', 'GPL'),
            Package('urllib3', '1.26.4', 'MIT License'),
            Package('uvicorn', '0.13.3', 'BSD License'),
            Package('zipp', '3.4.1', 'MIT License')]

    @patch('license_checks.pipenv.run')
    def prepare_directory(self, run_mock):
        run_mock.return_value = {}

        with TemporaryDirectory() as directory:
            self.checker.prepare_directory(directory)
            run_mock.assert_has_calls([
                call('pipenv install -d', capture_output=False, check=True, cwd=directory, shell=True),
                call("pipenv run pip install 'pip-licenses==3.3.1'", capture_output=False, check=True, cwd=directory,
                     shell=True),
            ])

    def test_main_returns_failure_on_no_config(self):
        with TemporaryDirectory() as directory:
            copy2('Pipfile', directory)
            copy2('Pipfile.lock', directory)

            result = self.checker.run([join(directory, 'Pipfile')])
            assert result == 1

    def test_main_returns_success(self):
        with TemporaryDirectory() as directory:
            self.prepare_integration_test_directory(directory)

            write_config_file(directory, [
                'Apache License 2.0',
                'Apache Software License',
                'Apache Software License, BSD License',
                'BSD License',
                'BSD License, Apache Software License',
                'Freely Distributable',
                'GNU Lesser General Public License v3 (LGPLv3)',
                'GNU Library or Lesser General Public License (LGPL)',
                'ISC License (ISCL)',
                'MIT',
                'MIT License',
                'MIT License, Mozilla Public License 2.0 (MPL 2.0)',
                'Mozilla Public License 2.0 (MPL 2.0)',
                'Public Domain',
                'Public Domain, Python Software Foundation License, BSD License, GNU General Public License (GPL)',
                'Python Software Foundation License',
                'Python Software Foundation License, MIT License'
            ])

            result = self.checker.run([join(directory, 'Pipfile')])
            assert result == 0

    @staticmethod
    def prepare_integration_test_directory(directory: str):
        with open(join(directory, 'Pipfile'), 'w') as pipfile:
            pipfile.write('''[[source]]
        url = "https://pypi.python.org/simple"
        verify_ssl = true
        name = "pypi"

        [packages]
        texttable = "*"

        [dev-packages]

        [requires]
        python_version = "3.8"''')
            run('pipenv lock', check=True, cwd=directory, shell=True)
