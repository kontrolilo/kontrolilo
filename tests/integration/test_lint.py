# -*- coding: utf-8 -*-
from typing import List

from license_checks.configuration import Configuration
from tests.integration.base_integration_test import IntegrationTestBase


class TestLintCheck(IntegrationTestBase):

    def prepare_test_directory(self):
        base_configuration = Configuration(
            allowed_licenses=['MIT', 'Apache 2.0'],
        )

        base_configuration.save_to_directory(self.directory.name)

    def get_hook_id(self) -> str:
        return 'license-check-configuration-lint'

    def get_allowed_licenses(self) -> List[str]:
        return [
            'Apache 2',
            'Apache License 2.0',
            'Apache License, Version 2.0',
            'BSD',
            'BSD License 3',
            'EDL 1.0',
            'EPL 2.0;GPL2 w/ CPE',
            'Eclipse Distribution License - v 1.0',
            'Eclipse Public License - v 1.0;GNU Lesser General Public License',
            'Eclipse Public License v2.0',
            'MIT License',
            'The Apache License, Version 2.0',
            'The Apache Software License, Version 2.0',
            'The MIT License'
        ]
