# -*- coding: utf-8 -*-
from json import dump

from license_checks.configuration import Configuration


def write_config_file(directory: str, allowed_licenses: []):
    with open(Configuration.get_config_file_path(directory), 'w+') as config_file:
        dump(
            {'allowedLicenses': allowed_licenses}, config_file)
