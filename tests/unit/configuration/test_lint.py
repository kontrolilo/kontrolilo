from pathlib import Path
from tempfile import TemporaryDirectory, NamedTemporaryFile
from unittest.mock import Mock

from kontrolilo.configuration import Configuration, ConfigurationInclude
from kontrolilo.configuration.configuration import CONFIG_FILE_NAME
from kontrolilo.configuration.lint import ConfigurationFileChecker


class TestConfigurationFileChecker:

    def setup_method(self):
        self.checker = ConfigurationFileChecker()
        self.directory = TemporaryDirectory()
        self.cache_file = NamedTemporaryFile()

    def test_run_returns_zero_on_valid_configuration(self):
        base_configuration = Configuration(
            allowed_licenses=['MIT', 'Apache 2.0'],
            includes=[
                ConfigurationInclude(url='https://examle.com/test.yaml'),
                ConfigurationInclude(url='https://examle.com/test2.yaml'),
            ],
            cache_name=self.cache_file.name
        )

        base_configuration.save_to_directory(self.directory.name)

        args = Mock()
        args.filenames = [Path(self.directory.name, CONFIG_FILE_NAME).absolute()]

        assert self.checker.run(args) == 0

        assert Configuration.load_from_directory(self.directory.name) == Configuration(
            allowed_licenses=['Apache 2.0', 'MIT'],
            includes=[
                ConfigurationInclude(url='https://examle.com/test.yaml'),
                ConfigurationInclude(url='https://examle.com/test2.yaml'),
            ],
            cache_name=self.cache_file.name
        )

    def test_run_returns_non_zero_on_invalid_configuration(self):
        path = Path(self.directory.name, CONFIG_FILE_NAME)
        with open(path.absolute(), 'w') as file:
            file.write('---')

        args = Mock()
        args.filenames = [path.absolute()]

        assert self.checker.run(args) != 0
