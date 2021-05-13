# -*- coding: utf-8 -*-
from tempfile import TemporaryDirectory

from httptest import Handler, Server
from yaml import dump

from license_checks.configuration import Configuration, ConfigurationInclude


def test_load_without_file():
    with TemporaryDirectory() as directory:
        configuration = Configuration.load_from_directory(directory)
        assert configuration == Configuration([], [])


def test_load_with_partial_values():
    demo_configuration = {
        'allowedLicenses': [
            'MIT',
            'GPL'
        ],
    }

    with TemporaryDirectory() as directory:
        with open(Configuration.get_config_file_path(directory), 'w') as config_file:
            dump(demo_configuration, config_file)

        configuration = Configuration.load_from_directory(directory)
        assert configuration == Configuration(['MIT', 'GPL'])


def test_load_with_file():
    demo_configuration = {
        'allowedLicenses': [
            'MIT',
            'GPL'
        ],
        'excludedPackages': [
            'demo1234'
        ],
        'include': [
            {
                'url': 'http://localhost:8000/license-check-node.yaml'
            }
        ]
    }

    with TemporaryDirectory() as directory:
        with open(Configuration.get_config_file_path(directory), 'w') as config_file:
            dump(demo_configuration, config_file)

        configuration = Configuration.load_from_directory(directory)
        assert configuration == Configuration(['MIT', 'GPL'], ['demo1234'],
                                              [ConfigurationInclude('http://localhost:8000/license-check-node.yaml')])


def test_to_yaml():
    demo_configuration = Configuration(
        allowed_licenses=[
            'MIT',
            'GPL'
        ],
        excluded_packages=[
            'demo1234'
        ],
        includes=[
            ConfigurationInclude(url='http://localhost:8000/license-check-node.yaml')
        ]
    )
    expected = '''allowedLicenses:
- MIT
- GPL
excludedPackages:
- demo1234
include:
- url: http://localhost:8000/license-check-node.yaml
'''

    assert demo_configuration.to_yaml() == expected


class ConfigurationTestServer(Handler):

    def do_GET(self) -> None:
        demo_configuration = Configuration(
            allowed_licenses=['MIT', 'GPL'],
            excluded_packages=['demo1234'],
        )

        contents = demo_configuration.to_yaml().encode()
        self.send_response(200)
        self.send_header('Content-type', 'text/yaml')
        self.send_header('Content-length', len(contents))
        self.end_headers()
        self.wfile.write(contents)


def test_merge_includes():
    with Server(ConfigurationTestServer) as ts:
        base_configuration = Configuration(
            allowed_licenses=['Apache 2.0'],
            includes=[ConfigurationInclude(url=ts.url())]
        )
        merged_configuration = base_configuration.merge_includes()

        assert merged_configuration == Configuration(
            allowed_licenses=['Apache 2.0', 'MIT', 'GPL'],
            excluded_packages=['demo1234']
        )
