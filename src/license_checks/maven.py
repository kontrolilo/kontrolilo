# -*- coding: utf-8 -*-
import sys
from os.path import join, exists
from typing import List
from xml.etree import ElementTree

from license_checks.base_checker import BaseLicenseChecker
from license_checks.configuration import Configuration
from license_checks.configuration.package import Package


class MavenLicenseChecker(BaseLicenseChecker):

    def prepare_directory(self, directory: str):
        pass

    def get_license_checker_command(self, directory: str) -> str:
        wrapper_path = join(directory, 'mvnw')

        binary = 'mvn'
        if exists(wrapper_path):
            binary = wrapper_path

        return f'{binary} org.codehaus.mojo:license-maven-plugin:2.0.0:download-licenses'

    def parse_packages(self, output: str, configuration: Configuration, directory: str) -> List[Package]:
        packages = []

        licenses_file_path = join(directory, 'target', 'generated-resources', 'licenses.xml')
        tree = ElementTree.parse(licenses_file_path)
        root = tree.getroot()
        for dependency in root.findall('./dependencies/dependency'):
            group_id = dependency.find('groupId')
            artifact_id = dependency.find('artifactId')
            version = dependency.find('version')

            license_names = []
            for license_element in dependency.findall('./licenses/license'):
                license_names.append(license_element.find('name').text)
            license_names.sort()

            packages.append(Package(
                f'{group_id.text}:{artifact_id.text}',
                version.text,
                ';'.join(license_names)
            ))

        return packages


def main():
    sys.exit(MavenLicenseChecker().run(sys.argv[1:]))


if __name__ == '__main__':
    main()
