# -*- coding: utf-8 -*-
import os
from os.path import join
from pathlib import Path
from shutil import copy
from subprocess import run
from tempfile import TemporaryDirectory

from git import Repo

from license_checks.configuration import Configuration


class TestNpmCheck:

    def setup(self):
        self.directory = TemporaryDirectory()
        copy(join(Path(__file__).parent, 'package.json'), join(self.directory.name, 'package.json'))

        self.repo = Repo.init(self.directory.name)
        self.repo.index.add(self.repo.untracked_files)

    def test_run_fails_without_config(self):
        result = self.run_pre_commit()
        assert result.returncode == 1

    def test_success(self):
        # TODO: maybe this should be
        Configuration(allowed_licenses=['ISC', 'MIT'], excluded_packages=[], includes=[]).save(self.directory.name)
        self.repo.index.add(self.repo.untracked_files)
        self.repo.index.commit('dummy commit')

        result = self.run_pre_commit()
        print(result.stdout)
        assert result.returncode == 0

    def run_pre_commit(self):
        return run(
            f'pre-commit try-repo {Path(__file__).parent.parent.parent.absolute()} license-check-npm --all-files --show-diff-on-failure',
            capture_output=True, cwd=self.directory.name,
            env=dict(os.environ, PIPENV_IGNORE_VIRTUALENVS='1'), shell=True)
