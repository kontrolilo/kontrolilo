# -*- coding: utf-8 -*-
from pathlib import Path

from pre_commit_hooks.license_check import get_pipenv_directories


def test_get_pipenv_directories():
    filenames = ['Pipfile.lock', 'Pipfile',
                 'deployment/Pipfile', 'deployment/Pipfile.lock']
    directories = get_pipenv_directories(filenames)
    assert len(directories) == 2
    assert directories == [str(Path('.').absolute()),
                           str(Path('.', 'deployment').absolute())]
