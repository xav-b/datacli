#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
    Packaging
    ---------

    :copyright (c) 2016 Xavier Bruhiere
    :license: MIT, see LICENSE.txt for more details.
"""

from setuptools import setup, find_packages
from datacli import __version__, __author__, __project__, __licence__

REQUIREMENTS = [
    'prompt-toolkit',
    'click',
    'Pygments',
    'pydrill',
    'pandas'
]


def long_description():
    """Insert readme.md into the package."""
    try:
        with open('readme.md') as fd:
            return fd.read()
    except IOError:
        return 'failed to read readme.md'


setup(
    name=__project__,
    version=__version__,
    licence=__licence__,
    description='Productive no-sql data sources exploration with SQL, Pandas and shortcuts',
    author=__author__,
    author_email='xavier.bruhiere@gmail.com',
    url='https://github.com/hackliff/datacli',
    packages=find_packages(),
    long_description=long_description(),
    install_requires=REQUIREMENTS,
    entry_points='''
        [console_scripts]
        datacli=datacli.__main__.cli
    ''',
    keywords=['data', 'database', 'analysis', 'cli', 'tool'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: SQL',
        'Topic :: Database',
        'Topic :: Database :: Front-Ends',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
