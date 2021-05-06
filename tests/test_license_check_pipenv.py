# -*- coding: utf-8 -*-
from json import dump
from os.path import join
from pathlib import Path
from shutil import copy2
from tempfile import TemporaryDirectory
from unittest.mock import patch, Mock, call

from pre_commit_hooks.license_check_pipenv import get_pipenv_directories, remove_duplicates, parse_licenses, \
    find_forbidden_licenses, load_configuration, CONFIG_FILE_NAME, print_license_warning, install_tools, \
    extract_installed_licenses, PipenvLicenseChecker


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
        run_mock.assert_has_calls([
            call('pipenv install -d', check=True, cwd=directory, shell=True),
            call("pipenv run pip install 'pip-licenses==3.3.1'", check=True, cwd=directory, shell=True),
        ])


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


class TestPipenvLicenseChecker:
    checker: PipenvLicenseChecker

    def setup(self):
        self.checker = PipenvLicenseChecker()

    def test_main_returns_failure_on_no_config(self):
        with TemporaryDirectory() as directory:
            copy2('Pipfile', directory)
            copy2('Pipfile.lock', directory)

            result = self.checker.run([join(directory, 'Pipfile')])
            assert result == 1

    def test_main_returns_success(self):
        with TemporaryDirectory() as directory:
            copy2('Pipfile', directory)
            copy2('Pipfile.lock', directory)

            with open(join(directory, CONFIG_FILE_NAME), 'w+') as config_file:
                dump(
                    {'allowed_licenses': [
                        'Apache Software License',
                        'Apache Software License, BSD License',
                        'BSD License',
                        'GNU Lesser General Public License v3 (LGPLv3)',
                        'GNU Library or Lesser General Public License (LGPL)',
                        'MIT',
                        'MIT License',
                        'MIT License, Mozilla Public License 2.0 (MPL 2.0)',
                        'Mozilla Public License 2.0 (MPL 2.0)',
                        'Public Domain',
                        'Public Domain, Python Software Foundation License, BSD License, GNU General Public License (GPL)',
                        'Python Software Foundation License',
                        'Python Software Foundation License, MIT License'
                    ]}, config_file)

            result = self.checker.run([join(directory, 'Pipfile')])
            assert result == 0
