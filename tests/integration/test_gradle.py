# -*- coding: utf-8 -*-
from shutil import unpack_archive
from tempfile import NamedTemporaryFile
from typing import List

import requests

from tests.integration.base_integration_test import IntegrationTestBase


class TestGradleCheck(IntegrationTestBase):

    def prepare_test_directory(self):
        with NamedTemporaryFile() as temp_archive:
            response = requests.post('https://start.spring.io/starter.tgz', data={
                'dependencies': 'web,devtools',
                'bootVersion': '2.3.5.RELEASE',
                'type': 'gradle-project'
            })
            response.raise_for_status()
            open(temp_archive.name, 'wb').write(response.content)

            unpack_archive(temp_archive.name, self.directory.name, format='gztar')

    def get_hook_id(self) -> str:
        return 'license-check-gradle'

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
