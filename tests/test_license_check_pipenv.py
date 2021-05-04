# -*- coding: utf-8 -*-
from pathlib import Path

from pre_commit_hooks.license_check_pipenv import get_pipenv_directories, remove_duplicates, parse_licenses, \
    find_forbidden_licenses


def test_remove_duplicates():
    list = ['a', 'b', 'c', 'a', 'c']
    consolidated_list = remove_duplicates(list)
    assert consolidated_list == ['a', 'b', 'c']


def test_get_pipenv_directories():
    filenames = ['Pipfile.lock', 'Pipfile',
                 'deployment/Pipfile', 'deployment/Pipfile.lock']
    directories = get_pipenv_directories(filenames)
    assert len(directories) == 2
    assert directories == [str(Path('.').absolute()),
                           str(Path('.', 'deployment').absolute())]


def test_parse_licenses():
    stdout = '''[
      {
        "License": "BSD License",
        "Name": "starlette",
        "Version": "0.14.1"
      },
      {
        "License": "MIT License",
        "Name": "urllib3",
        "Version": "1.26.4"
      },
      {
        "License": "BSD License",
        "Name": "uvicorn",
        "Version": "0.13.3"
      },
      {
        "License": "MIT License",
        "Name": "zipp",
        "Version": "3.4.1"
      }
    ]
    '''
    configuration = {}
    licenses = parse_licenses(stdout, configuration)
    assert licenses == ['BSD License', 'MIT License']


def test_parse_licenses_with_excluded_packages():
    stdout = '''[
      {
        "License": "BSD License",
        "Name": "starlette",
        "Version": "0.14.1"
      },
      {
        "License": "GPL",
        "Name": "demo1234",
        "Version": "0.14.1"
      },
      {
        "License": "MIT License",
        "Name": "urllib3",
        "Version": "1.26.4"
      },
      {
        "License": "BSD License",
        "Name": "uvicorn",
        "Version": "0.13.3"
      },
      {
        "License": "MIT License",
        "Name": "zipp",
        "Version": "3.4.1"
      }
    ]
    '''
    configuration = {
        'excluded_packages': [
            'demo1234'
        ]
    }
    licenses = parse_licenses(stdout, configuration)
    assert licenses == ['BSD License', 'MIT License']


def test_find_forbidden_licenses():
    configuration = {
        'allowed_licenses': ['BSD License', 'MIT License']
    }
    used_licenses = ['BSD License', 'GPL', 'MIT License']

    forbidden_licenses = find_forbidden_licenses(used_licenses, configuration)
    assert forbidden_licenses == ['GPL']
