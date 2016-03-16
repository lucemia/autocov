#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup for autocov."""

import ast
import io
import sys
import os
from setuptools import setup

reqs = []
with open('requirements.txt') as ifile:
    for i in ifile:
        if i.strip() and not i.strip()[0] == '#':
            reqs.append(i)

INSTALL_REQUIRES = (
    reqs +
    (['argparse'] if sys.version_info < (2, 7) else [])
)


def version():
    """Return version string."""
    from datetime import datetime
    __version__ = datetime.utcnow().strftime('%Y.%m.%d.%H')

    with io.open('autocov.py') as input_file:
        for line in input_file:
            return __version__


with io.open('README.rst') as readme:
    setup(
        name='autocov',
        version=version(),
        description="A tool that automatically generate coverage report",
        long_description=readme.read(),
        # license='Expat License',
        # author='Hideo Hattori',
        # author_email='hhatto.jp@gmail.com',
        # url='https://github.com/hhatto/autopep8',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Software Development :: Quality Assurance',
        ],
        keywords='automation, coverage, github',
        install_requires=INSTALL_REQUIRES,
        # test_suite='test.test_autopep8',
        py_modules=['autocov'],
        zip_safe=False,
        entry_points={'console_scripts': ['autocov = autocov:main']},
    )
