# -*- coding: utf-8 -*-
import argparse
import sys
from os.path import abspath
from pathlib import Path


def get_pipenv_directories(filenames):
    directories = []
    for filename in filenames:
        directories.append(abspath(Path(filename).parent.absolute()))
    return list(dict.fromkeys(directories))


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='filenames to check')
    args = parser.parse_args(argv)

    print(args.filenames)

    return_code = 0
    return return_code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
