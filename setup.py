# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

__version__ = '0.1.0'

setup(
    name='pre-commit-license-check',
    description='Check against license whitelist',
    url='https://github.com/nbyl/pre-commit-license-check',
    version='0.0.0',

    packages=find_packages('.'),
    entry_points={
        'console_scripts': [
            'license_check = pre_commit_hooks.license_check:main',
        ],
    },
)
