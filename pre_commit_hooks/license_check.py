# -*- coding: utf-8 -*-
import argparse
import sys
from builtins import dict
from json import loads
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


ALLOW_LIST_FILE = '.licenses-allowed-pipenv'


def get_allow_list_path(directory: str) -> str:
    return str(Path(directory, ALLOW_LIST_FILE).absolute())


def load_allow_list(directory) -> List[str]:
    list_path = get_allow_list_path(directory)
    if not exists(list_path):
        return []

    with open(list_path) as list_file:
        lines = list_file.readlines()
        return [line.strip() for line in lines]


def find_unallowed_licenses(used_licenses: List[str], allow_list: List[str]) -> List[str]:
    return list(set(used_licenses) - set(allow_list))


def print_license_warning(directory: str, unallowed_licenses: List[str]):
    unallowed_licenses.sort()
    print('**************************************************************')
    print(f'Not all license used by pipenv in directory {directory} are using allowed licenses.')
    print()
    print('If you want to allow these licenses, please put the following lines into')
    print(f'the allow list file: {get_allow_list_path(directory)}: ')
    print('---')
    for unallowed_license in unallowed_licenses:
        print(unallowed_license)
    print('---')
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
        used_licenses = extract_installed_licenses(directory)
        allow_list = load_allow_list(directory)
        unallowed_licenses = find_unallowed_licenses(used_licenses, allow_list)
        if len(unallowed_licenses) > 0:
            return_code = 1
            print_license_warning(directory, unallowed_licenses)

    return return_code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
