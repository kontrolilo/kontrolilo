# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

__version__ = '1.1.1'

setup(
    install_requires=['ignore==0.1.4', 'pyyaml==5.4.1', 'texttable==1.6.3'],
    name='pre-commit-license-check',
    description='Check your repositories against a license allow list',
    url='https://github.com/nbyl/pre-commit-license-check',
    version=__version__,
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    entry_points={
        'console_scripts': [
            'license-check-npm = license_checks.npm:main',
            'license-check-pipenv = license_checks.pipenv:main'
        ],
    },
    dependency_links=[],
)
