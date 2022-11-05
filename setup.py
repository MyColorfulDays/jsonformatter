#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: setup.py
Author: Me
Email: yourname@email.com
Github: https://github.com/yourname
Description: setup.py
"""
import sys
from setuptools import setup

from jsonformatter import version

long_description = ''

try:
    if 'win' in sys.platform and sys.version_info >= (3, 0):
        with open('README.md', encoding='utf-8') as r:
            long_description = r.read()
    else:
        with open('README.md') as r:
            long_description = r.read()
except Exception as e:
    pass

setup(
    name='jsonformatter',
    version=version,
    description=(
        'Python log in json format.'
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    platforms=["all"],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities',
    ],
    python_requires='>=2.7',
    author='MyColorfulDays',
    author_email='my_colorful_days@163.com',
    url='https://github.com/MyColorfulDays/jsonformatter.git',
    license='BSD License',
    packages=['jsonformatter']
)
