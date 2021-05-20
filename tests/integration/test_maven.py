# -*- coding: utf-8 -*-
from os import environ
from pathlib import Path
from shutil import unpack_archive
from subprocess import run
from tempfile import TemporaryDirectory, NamedTemporaryFile

import requests
from git import Repo

from license_checks.configuration import Configuration


class TestMavenCheck:

    def setup(self):
        self.directory = TemporaryDirectory()

        self.prepare_spring_boot_project()

        self.repo = Repo.init(self.directory.name)
        self.repo.index.add(self.repo.untracked_files)

    def test_run_fails_without_config(self):
        result = self.run_pre_commit()
        assert result.returncode == 1

    def test_success(self):
        Configuration(
            allowed_licenses=[
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
            ],
            excluded_packages=[],
            includes=[]).save(self.directory.name)
        result = self.run_pre_commit()
        print(result.stdout)
        assert result.returncode == 0

    def run_pre_commit(self):
        return run(
            f'pre-commit try-repo {Path(__file__).parent.parent.parent.absolute()} license-check-maven --all-files -v',
            capture_output=True, cwd=self.directory.name, env=dict(environ, PIPENV_IGNORE_VIRTUALENVS='1'),
            shell=True)

    def prepare_spring_boot_project(self):
        with NamedTemporaryFile() as temp_archive:
            response = requests.post('https://start.spring.io/starter.tgz', data={
                'dependencies': 'web,devtools',
                'bootVersion': '2.3.5.RELEASE'
            })
            response.raise_for_status()
            open(temp_archive.name, 'wb').write(response.content)

            unpack_archive(temp_archive.name, self.directory.name, format='gztar')
