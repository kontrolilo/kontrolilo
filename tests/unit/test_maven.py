# -*- coding: utf-8 -*-
from os import mkdir
from os.path import join
from tempfile import TemporaryDirectory

from license_checks.configuration import Configuration
from license_checks.configuration.package import Package
from license_checks.maven import MavenLicenseChecker


class TestMavenLicenseChecker:
    LICENSES_XML = \
        '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<licenseSummary>
  <dependencies>
    <dependency>
      <groupId>ch.qos.logback</groupId>
      <artifactId>logback-classic</artifactId>
      <version>1.2.3</version>
      <licenses>
        <license>
          <name>Eclipse Public License - v 1.0</name>
          <url>http://www.eclipse.org/legal/epl-v10.html</url>
          <file>eclipse public license - v 1.0 - epl-v10.html</file>
        </license>
        <license>
          <name>GNU Lesser General Public License</name>
          <url>http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html</url>
          <file>gnu lesser general public license - lgpl-2.1.html</file>
        </license>
      </licenses>
    </dependency>
    <dependency>
      <groupId>ch.qos.logback</groupId>
      <artifactId>logback-core</artifactId>
      <version>1.2.3</version>
      <licenses>
        <license>
          <name>Eclipse Public License - v 1.0</name>
          <url>http://www.eclipse.org/legal/epl-v10.html</url>
          <file>eclipse public license - v 1.0 - epl-v10.html</file>
        </license>
        <license>
          <name>GNU Lesser General Public License</name>
          <url>http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html</url>
          <file>gnu lesser general public license - lgpl-2.1.html</file>
        </license>
      </licenses>
    </dependency>
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-annotations</artifactId>
      <version>2.11.4</version>
      <licenses>
        <license>
          <name>The Apache Software License, Version 2.0</name>
          <url>http://www.apache.org/licenses/LICENSE-2.0.txt</url>
          <distribution>repo</distribution>
          <file>the apache software license, version 2.0 - license-2.0.txt</file>
        </license>
      </licenses>
    </dependency>
  </dependencies>
</licenseSummary>
'''

    def setup(self):
        self.directory = TemporaryDirectory()
        self.checker = MavenLicenseChecker()

    def test_prepare_directory(self):
        self.checker.prepare_directory(self.directory.name)

    def test_get_license_checker_command(self):
        assert self.checker.get_license_checker_command() == './mvnw org.codehaus.mojo:license-maven-plugin:2.0.0:download-licenses'

    def test_parse_packages(self):
        target_directory = join(self.directory.name, 'target')
        mkdir(target_directory)

        with open(join(target_directory, 'licenses.xml'), 'w') as licenses_file:
            licenses_file.write(self.LICENSES_XML)

        packages = self.checker.parse_packages('', Configuration(
            allowed_licenses=[],
            excluded_packages=[]
        ),
                                               self.directory.name)
        assert packages == [
            Package('ch.qos.logback:logback-classic', '1.2.3',
                    'Eclipse Public License - v 1.0;GNU Lesser General Public License'),
            Package('ch.qos.logback:logback-core', '1.2.3',
                    'Eclipse Public License - v 1.0;GNU Lesser General Public License'),
            Package('com.fasterxml.jackson.core:jackson-annotations', '2.11.4',
                    'The Apache Software License, Version 2.0')
        ]
