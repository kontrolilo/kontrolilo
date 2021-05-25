# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

__version__ = '1.6.0'

setup(
    install_requires=[
        'certifi==2020.12.5',
        "chardet==4.0.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "idna==2.10; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        'ignore==0.1.4',
        "itsdangerous==2.0.1; python_version >= '3.6'",
        'pyyaml==5.4.1',
        'requests==2.25.1',
        'requests-cache==0.6.3',
        "six==1.16.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        'texttable==1.6.3',
        'typing-extensions==3.10.0.0',
        "url-normalize==1.4.3; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4, 3.5'",
        "urllib3==1.26.4; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_version < '4'",
    ],
    name='pre-commit-license-check',
    description='Check your repositories against a license allow list',
    url='https://github.com/nbyl/pre-commit-license-check',
    version=__version__,
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    entry_points={
        'console_scripts': [
            'license-check-gradle = license_checks.gradle:main',
            'license-check-maven = license_checks.maven:main',
            'license-check-npm = license_checks.npm:main',
            'license-check-pipenv = license_checks.pipenv:main',
        ],
    },
    dependency_links=[],
)
