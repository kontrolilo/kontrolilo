# -*- coding: utf-8 -*-
import argparse
import sys
from logging import basicConfig, DEBUG, INFO
from os import getenv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='print debug messages to stderr')
    parser.add_argument('filenames', nargs='*', help='filenames to check')
    args = parser.parse_args(sys.argv[1:])

    debug = args.debug or (getenv('DEBUG', 'false').lower() == 'true')

    basicConfig(level=DEBUG if debug else INFO)

    print(args.filenames)


if __name__ == '__main__':
    main()
