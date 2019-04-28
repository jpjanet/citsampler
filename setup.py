#!/usr/bin/env python


from setuptools import setup, find_packages

# Package meta-data.
NAME = 'citsampler'
DESCRIPTION = 'simple rejection sampling MCMC'
URL = 'https://github.com/me/myproject'
EMAIL = 'jp@mit.edu'
AUTHOR = 'JP Janet'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.1.0'

REQUIRED = ['pyclustering', 'numpy']

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(),
    install_requires=REQUIRED,
    entry_points={'console_scripts': ['citsampler = citsampler.__main__:main']},
    package_data={'citsampler':['scripts/*.sh']},
    setup_requires=[''],
    include_package_data = True)
