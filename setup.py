# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

__version__ = '0.4.0'

setup(
    install_requires=['pyyaml==5.4.1'],
    name='pre-commit-license-check',
    description='Check against license whitelist',
    url='https://github.com/nbyl/pre-commit-license-check',
    version='0.0.0',
    packages=find_packages('.'),
    entry_points={
        'console_scripts': ['license_checks = license_checks.license_checks:main',],
    },
    dependency_links=[],
)
