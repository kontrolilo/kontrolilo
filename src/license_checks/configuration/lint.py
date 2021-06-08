# -*- coding: utf-8 -*-

from license_checks.shared_main import BaseChecker, shared_main


class ConfigurationFileChecker(BaseChecker):
    def run(self, args) -> int:
        return 0


def main():
    shared_main(ConfigurationFileChecker())


if __name__ == '__main__':
    main()
