import os
from pathlib import Path
from shutil import copy
from subprocess import run
from typing import List

from tests.integration.base_integration_test import IntegrationTestBase


class TestPipenvCheck(IntegrationTestBase):

    def prepare_test_directory(self):
        copy(Path(Path(__file__).parent, 'Pipfile').absolute(),
             Path(self.directory.name, 'Pipfile').absolute())
        run('pipenv lock', capture_output=True, check=True, cwd=self.directory.name,
            env=dict(os.environ, PIPENV_IGNORE_VIRTUALENVS='1'), shell=True)

    def get_hook_id(self) -> str:
        return 'license-check-pipenv'

    def get_allowed_licenses(self) -> List[str]:
        return [
            'MIT License'
        ]
