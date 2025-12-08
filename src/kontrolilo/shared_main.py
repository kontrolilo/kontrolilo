import abc
import argparse
import sys
from logging import basicConfig, DEBUG, INFO
from os import getenv


class BaseChecker(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self, args) -> int:
        """Check the condition and return zero or non-zero."""


def shared_main(checker: BaseChecker):
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='print debug messages to stderr')
    parser.add_argument('filenames', nargs='*', help='filenames to check')
    args = parser.parse_args(sys.argv[1:])

    debug = args.debug or (getenv('DEBUG', 'false').lower() == 'true')

    basicConfig(level=DEBUG if debug else INFO)
    sys.exit(checker.run(args))
