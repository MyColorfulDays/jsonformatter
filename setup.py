#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: setup.py
Author: Me
Email: yourname@email.com
Github: https://github.com/yourname
Description: setup.py
"""

from setuptools import setup

setup(
    name='jsonformatter',
    version='0.2.2',
    description=(
        'Python log in json format.'
    ),
    long_description=open('README.md').read(),
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
