# -*- coding: utf-8 -*-
from logging import getLogger

from license_checks.configuration import Configuration
from license_checks.shared_main import BaseChecker, shared_main

logger = getLogger(__name__)


class ConfigurationFileChecker(BaseChecker):
    def run(self, args) -> int:
        result = 0
        for filename in args.filenames:
            try:
                configuration = Configuration.load_from_file(filename, return_empty_if_not_present=False)
                configuration.save_to_file(filename)
            except Exception as ex:
                logger.info('Linting fails with error: %s', ex)
                result += 1
        return result


def main():
    shared_main(ConfigurationFileChecker())


if __name__ == '__main__':
    main()
