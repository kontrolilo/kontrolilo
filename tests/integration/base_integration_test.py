# -*- coding: utf-8 -*-
import os
from abc import abstractmethod, ABC
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
from typing import List

from git import Repo

from kontrolilo.configuration import Configuration


class IntegrationTestBase(ABC):

    def setup(self):
        self.directory = TemporaryDirectory()

        self.prepare_test_directory()

        self.repo = Repo.init(self.directory.name)
        self.repo.index.add(self.repo.untracked_files)

    @abstractmethod
    def prepare_test_directory(self):
        """Setup everything inside the target directory for the tests."""

    @abstractmethod
    def get_hook_id(self) -> str:
        """Return the hook id to test."""

    @abstractmethod
    def get_allowed_licenses(self) -> List[str]:
        """Return a list of licenses that should be allowed in the success case."""

    def test_run_fails_without_config(self):
        result = self.run_pre_commit()
        assert result.returncode == 1

    def test_success(self):
        Configuration(allowed_licenses=self.get_allowed_licenses(), excluded_packages=[], includes=[]).save_to_directory(
            self.directory.name)
        result = self.run_pre_commit()
        assert result.returncode == 0

    def run_pre_commit(self):
        result = run(
            f'pre-commit try-repo {Path(__file__).parent.parent.parent.absolute()} {self.get_hook_id()} --all-files -v',
            capture_output=True, cwd=self.directory.name,
            env=dict(os.environ, PIPENV_IGNORE_VIRTUALENVS='1', DEBUG='true'), shell=True)
        print(result.stdout.decode('utf-8').replace('\\n', '\n'))
        return result
