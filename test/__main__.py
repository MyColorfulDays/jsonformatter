#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: jsonformatter.py
Author: MyColorfulDays
Email: my_colorful_days@163.com
Github: https://github.com/MyColorfulDays
Description: jsonformatter.py
"""
import unittest

if __name__ == '__main__':
    discover = unittest.defaultTestLoader.discover('./', pattern="test*.py")
    runner = unittest.TextTestRunner()
    runner.run(discover)
