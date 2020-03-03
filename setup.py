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
    version='0.1.4',
    description=(
        'Python log in json format.'
    ),
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    platforms=["all"],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities',
    ],
    python_requires='>=3',
    author='MyColorfulDays',
    author_email='my_colorful_days@163.com',
    url='https://github.com/MyColorfulDays/jsonformatter.git',
    license='BSD License',
    packages=['jsonformatter']
)
