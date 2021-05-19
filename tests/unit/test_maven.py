# -*- coding: utf-8 -*-
from tempfile import TemporaryDirectory

from license_checks.configuration import Configuration
from license_checks.configuration.package import Package
from license_checks.maven import MavenLicenseChecker


class TestMavenLicenseChecker:
    DEMO_LICENSE_OUTPUT = \
        '''"module name","license","repository"
"xtend@4.0.2","MIT","https://github.com/Raynos/xtend"
"y18n@4.0.0","ISC","https://github.com/yargs/y18n"
"y18n@5.0.5","ISC","https://github.com/yargs/y18n"'''

    def setup(self):
        self.directory = TemporaryDirectory()
        self.checker = MavenLicenseChecker()

    def test_prepare_directory(self):
        self.checker.prepare_directory(self.directory.name)

    def test_get_license_checker_command(self):
        assert self.checker.get_license_checker_command() == './mvnw org.codehaus.mojo:license-maven-plugin:2.0.0:download-licenses'

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
