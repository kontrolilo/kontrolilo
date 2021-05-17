# -*- coding: utf-8 -*-

from tempfile import TemporaryDirectory
from unittest.mock import patch, call

from license_checks.configuration import Configuration
from license_checks.package import Package
from license_checks.pipenv import PipenvLicenseChecker


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
        configuration = Configuration()
        packages = self.checker.parse_packages(self.DEMO_LICENSE_OUTPUT, configuration)
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
