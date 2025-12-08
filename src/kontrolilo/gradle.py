from json import load
from logging import getLogger
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List

from kontrolilo.base_checker import BaseLicenseChecker
from kontrolilo.shared_main import shared_main
from kontrolilo.configuration import Configuration
from kontrolilo.configuration.package import Package

logger = getLogger(__name__)


class GradleLicenseChecker(BaseLicenseChecker):
    INIT_SCRIPT = '''
initscript {
    repositories {
        repositories {
            jcenter()
            google()
        }
        dependencies {
            classpath 'com.jaredsburrows:gradle-license-plugin:0.8.90'
        }
    }
}
allprojects {
    apply plugin: com.jaredsburrows.license.LicensePlugin

    licenseReport {
        generateCsvReport = false
        generateHtmlReport = false
        generateJsonReport = true
    }
}
'''

    def __init__(self) -> None:
        super().__init__()

        self.init_script = NamedTemporaryFile(prefix='init.gradle')

        with open(self.init_script.name, 'w') as init_script_file:
            init_script_file.write(self.INIT_SCRIPT)

    def prepare_directory(self, directory: str):
        pass

    def get_license_checker_command(self, directory: str) -> str:
        wrapper_path = Path(directory, 'gradlew')

        binary = 'gradlew'
        if wrapper_path.exists():
            binary = wrapper_path.absolute()

        return f'{binary} -I {self.init_script.name} licenseReport'

    def parse_packages(self, output: str, configuration: Configuration, directory: str) -> List[Package]:
        packages = []

        licenses_file_path = Path(directory, 'build', 'reports', 'licenses', 'licenseReport.json')

        logger.debug('Loading license data from [%s]', licenses_file_path.absolute())

        with open(licenses_file_path.absolute()) as license_file:
            dependencies = load(license_file)
            for dependency in dependencies:
                artifact_name = dependency['dependency']

                version = ''
                index = artifact_name.rfind(':')
                if index > -1:
                    version = artifact_name[index + 1:]
                    artifact_name = artifact_name[:index]

                license_names = []
                for license_entry in dependency['licenses']:
                    license_names.append(license_entry['license'])
                license_names.sort()

                packages.append(Package(artifact_name, version, ';'.join(license_names)))

        logger.debug('Found %s packages in license file.', len(packages))

        return packages


def main():
    shared_main(GradleLicenseChecker())


if __name__ == '__main__':
    main()
