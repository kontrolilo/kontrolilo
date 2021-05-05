# -*- coding: utf-8 -*-
from json import dump
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch, Mock

from pre_commit_hooks.license_check_pipenv import get_pipenv_directories, remove_duplicates, parse_licenses, \
    find_forbidden_licenses, load_configuration, CONFIG_FILE_NAME, print_license_warning, install_tools, \
    extract_installed_licenses


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


DEMO_LICENSE_OUTPUT = '''[
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


def test_parse_licenses_with_excluded_packages():
    configuration = {
        'excluded_packages': [
            'demo1234'
        ]
    }
    licenses = parse_licenses(DEMO_LICENSE_OUTPUT, configuration)
    assert licenses == ['BSD License', 'MIT License']


def test_find_forbidden_licenses():
    configuration = {
        'allowed_licenses': ['BSD License', 'MIT License']
    }
    used_licenses = ['BSD License', 'GPL', 'MIT License']

    forbidden_licenses = find_forbidden_licenses(used_licenses, configuration)
    assert forbidden_licenses == ['GPL']


def test_load_configuration_without_file():
    with TemporaryDirectory() as directory:
        configuration = load_configuration(directory)
        assert configuration == {}


def test_load_configuration_with_file():
    demo_configuration = {
        'excluded_packages': [
            'demo1234'
        ]
    }

    with TemporaryDirectory() as directory:
        with open(str(Path(directory, CONFIG_FILE_NAME).absolute()), 'w') as config_file:
            dump(demo_configuration, config_file)

        configuration = load_configuration(directory)
        assert configuration == demo_configuration


def test_print_license_warning():
    # this test is mainly run, to verify syntactic correctness
    with TemporaryDirectory() as directory:
        print_license_warning(directory, [])


@patch('pre_commit_hooks.license_check_pipenv.run')
def test_install_tools(run_mock):
    run_mock.return_value = {}

    with TemporaryDirectory() as directory:
        install_tools(directory)
        run_mock.assert_called_once_with("pipenv run pip install 'pip-licenses==3.3.1'", check=True, cwd=directory,
                                         shell=True)


@patch('pre_commit_hooks.license_check_pipenv.run')
def test_extract_installed_licenses(run_mock):
    result_mock = Mock()
    result_mock.configure_mock(**{'stdout': DEMO_LICENSE_OUTPUT})
    run_mock.return_value = result_mock
    # run_mock.return_value.stdout = DEMO_LICENSE_OUTPUT

    with TemporaryDirectory() as directory:
        extract_installed_licenses(directory, {})
        run_mock.assert_called_once_with('pipenv run pip-licenses --format=json', capture_output=True, check=True,
                                         cwd=directory, shell=True, text=True)
