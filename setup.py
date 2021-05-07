#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: setup.py
Author: MyColorfulDays
Email: my_colorful_days@163.com
Github: https://github.com/MyColorfulDays
Description: setup.py
"""
import sys
from setuptools import setup

import jsonformatter

long_description = ''

if 'win' in sys.platform and sys.version_info >= (3, 0):
    with open('README.md', encoding='utf-8') as r:
        long_description = r.read()
else:
    with open('README.md') as r:
        long_description = r.read()

setup(
    name='jsonformatter',
    version=jsonformatter.version,
    description=(
        'Python log json format.'
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
