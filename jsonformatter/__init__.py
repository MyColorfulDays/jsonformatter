#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: jsonformatter.py
Author: MyColorfulDays
Email: my_colorful_days@163.com
Github: https://github.com/MyColorfulDays
Description: jsonformatter.py
"""

from .jsonformatter import JsonFormatter, basicConfig, fileConfig

__all__ = ['JsonFormatter', 'basicConfig', 'fileConfig']

version_info = (0, 4, 0)
version = '.'.join(str(i) for i in version_info)
