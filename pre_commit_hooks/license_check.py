# -*- coding: utf-8 -*-
import argparse
import sys
from builtins import dict
from json import loads, load, dumps
from os.path import abspath, exists
from pathlib import Path
from subprocess import run
from typing import List


def remove_duplicates(values: List[str]) -> List[str]:
    return list(dict.fromkeys(values))


def get_pipenv_directories(filenames) -> List[str]:
    directories = []
    for filename in filenames:
        directories.append(abspath(Path(filename).parent.absolute()))
    return remove_duplicates(directories)


def parse_licenses(output) -> List[str]:
    values = loads(output)
    licenses = []

    for license_structure in values:
        licenses.append(license_structure['License'])

    return remove_duplicates(licenses)


def extract_installed_licenses(directory) -> List[str]:
    run("pipenv run pip install 'pip-licenses==3.3.1'", check=True, cwd=directory, shell=True)
    result = run('pipenv run pip-licenses --format=json', capture_output=True, check=True, cwd=directory, shell=True,
                 text=True)
    return parse_licenses(result.stdout)


CONFIG_FILE_NAME = '.license-check-pipenv.json'


def get_config_file_path(directory: str) -> str:
    return str(Path(directory, CONFIG_FILE_NAME).absolute())


def load_configuration(directory):
    config_file_path = get_config_file_path(directory)
    if not exists(config_file_path):
        print('2')
        return {}

    with open(config_file_path) as list_file:
        return load(list_file)


def find_forbidden_licenses(used_licenses: List[str], configuration) -> List[str]:
    license_list = []
    if 'allowed_licenses' in configuration:
        license_list = configuration['allowed_licenses']
    return list(set(used_licenses) - set(license_list))


def print_license_warning(directory: str, forbidden_licenses: List[str]):
    forbidden_licenses.sort()
    demo_configuration = {
        'allowed_licenses': forbidden_licenses
    }

    print('**************************************************************')
    print(f'Not all licenses used by pipenv in directory {directory} are allowed.')
    print()
    print('If you want to allow these licenses, please put the following lines into')
    print(f'the allow list file: {get_config_file_path(directory)}: ')
    print()
    print(dumps(demo_configuration, indent=2, sort_keys=True))
    print()
    print('**************************************************************')


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='filenames to check')
    args = parser.parse_args(argv)

    return_code = 0

    directories = get_pipenv_directories(args.filenames)

    for directory in directories:
        print('**************************************************************')
        print(f'Starting scan in {directory}...')

        configuration = load_configuration(directory)
        used_licenses = extract_installed_licenses(directory)

        forbidden_licenses = find_forbidden_licenses(used_licenses, configuration)
        if len(forbidden_licenses) > 0:
            return_code = 1
            print_license_warning(directory, forbidden_licenses)

    return return_code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
