#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: jsonformatter.py
Author: Me
Email: yourname@email.com
Github: https://github.com/yourname
Description: jsonformatter.py
"""
import datetime
import logging
import os
import random
import unittest
from collections import OrderedDict
from logging.config import fileConfig


if __file__ == 'test.py':
    import sys
    sys.path.insert(0, '..')

from jsonformatter import JsonFormatter

STRING_FORMAT = '''{
    "name":            "name",
    "levelno":         "levelno",
    "levelname":       "levelname",
    "pathname":        "pathname",
    "filename":        "filename",
    "module":          "module",
    "lineno":          "lineno",
    "funcName":        "funcName",
    "created":         "created",
    "asctime":         "asctime",
    "msecs":           "msecs",
    "relativeCreated": "relativeCreated",
    "thread":          "thread",
    "threadName":      "threadName",
    "process":         "process",
    "message":         "message"
}'''


DICT_FORMAT = {
    "name":            "name",
    "levelno":         "levelno",
    "levelname":       "levelname",
    "pathname":        "pathname",
    "filename":        "filename",
    "module":          "module",
    "lineno":          "lineno",
    "funcName":        "funcName",
    "created":         "created",
    "asctime":         "asctime",
    "msecs":           "msecs",
    "relativeCreated": "relativeCreated",
    "thread":          "thread",
    "threadName":      "threadName",
    "process":         "process",
    "message":         "message"
}

ORDERED_DICT_FORMAT = OrderedDict([
    ("name",            "name"),
    ("levelno",         "levelno"),
    ("levelname",       "levelname"),
    ("pathname",        "pathname"),
    ("filename",        "filename"),
    ("module",          "module"),
    ("lineno",          "lineno"),
    ("funcName",        "funcName"),
    ("created",         "created"),
    ("asctime",         "asctime"),
    ("msecs",           "msecs"),
    ("relativeCreated", "relativeCreated"),
    ("thread",          "thread"),
    ("threadName",      "threadName"),
    ("process",         "process"),
    ("message",         "message")
])


RECORD_CUSTOM_ATTRS = {
    'asctime': lambda: datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f'),
    'user id': lambda: str(random.random())[2:10]
}


RECORD_CUSTOM_FORMAT = OrderedDict([
    ("user id",         "user id"),  # new custom attrs
    ("name",            "name"),
    ("levelno",         "levelno"),
    ("levelname",       "levelname"),
    ("pathname",        "pathname"),
    ("filename",        "filename"),
    ("module",          "module"),
    ("lineno",          "lineno"),
    ("funcName",        "funcName"),
    ("created",         "created"),
    ("asctime",         "asctime"),  # use custom format replace default.
    ("msecs",           "msecs"),
    ("relativeCreated", "relativeCreated"),
    ("thread",          "thread"),
    ("threadName",      "threadName"),
    ("process",         "process"),
    ("message",         "message")
])


MULTI_VALUE_FORMAT = OrderedDict([
    ("multi value", "%(name)s - %(levelno)s - %(levelname)s - %(pathname)s - %(filename)s - %(module)s - %(lineno)d - %(funcName)s - %(created)f - %(asctime)s - %(msecs)d - %(relativeCreated)d - %(thread)d - %(threadName)s - %(process)d - %(message)s")
])


class JsonFormatterTest(unittest.TestCase):

    def test_string_config(self):
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        datefmt = None
        sh = logging.StreamHandler()
        formatter = JsonFormatter(STRING_FORMAT, datefmt)
        sh.setFormatter(formatter)

        sh.setLevel(logging.INFO)

        root.addHandler(sh)

        root.info("test %s format", 'string')

    def test_dict_config(self):
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        datefmt = None
        sh = logging.StreamHandler()
        formatter = JsonFormatter(DICT_FORMAT, datefmt)
        sh.setFormatter(formatter)

        sh.setLevel(logging.INFO)

        root.addHandler(sh)

        root.info("test dict format")

    def test_ordered_dict_config(self):
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        datefmt = None
        sh = logging.StreamHandler()
        formatter = JsonFormatter(ORDERED_DICT_FORMAT, datefmt)
        sh.setFormatter(formatter)

        sh.setLevel(logging.INFO)

        root.addHandler(sh)

        root.info("test dict format")

    def test_log_exception(self):
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        datefmt = '%Y-%m-%d %H:%M:%S'
        sh = logging.StreamHandler()
        formatter = JsonFormatter(ORDERED_DICT_FORMAT, datefmt)
        sh.setFormatter(formatter)

        sh.setLevel(logging.INFO)

        root.addHandler(sh)
        try:
            1 / 0
        except Exception as e:
            root.exception('test log exception')

    def test_record_custom_attrs(self):

        root = logging.getLogger()
        root.setLevel(logging.INFO)

        datefmt = None
        sh = logging.StreamHandler()
        formatter = JsonFormatter(RECORD_CUSTOM_FORMAT, datefmt, record_custom_attrs=RECORD_CUSTOM_ATTRS)
        sh.setFormatter(formatter)

        sh.setLevel(logging.INFO)

        root.addHandler(sh)
        root.info('test record custom attrs')

    def test_multi_value_in_one_key(self):

        root = logging.getLogger()
        root.setLevel(logging.INFO)

        datefmt = None
        sh = logging.StreamHandler()
        formatter = JsonFormatter(MULTI_VALUE_FORMAT, datefmt, record_custom_attrs=RECORD_CUSTOM_ATTRS)
        sh.setFormatter(formatter)

        sh.setLevel(logging.INFO)

        root.addHandler(sh)
        root.info('test multi value in one key')

    def test_indent(self):
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        datefmt = None
        sh = logging.StreamHandler()
        formatter = JsonFormatter(ORDERED_DICT_FORMAT, datefmt, indent=4)
        sh.setFormatter(formatter)

        sh.setLevel(logging.INFO)

        root.addHandler(sh)

        root.info('test indent')

    def test_ensure_ascii_false(self):
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        datefmt = None
        sh = logging.StreamHandler()
        formatter = JsonFormatter(ORDERED_DICT_FORMAT, datefmt, ensure_ascii=False)
        sh.setFormatter(formatter)

        sh.setLevel(logging.INFO)

        root.addHandler(sh)

        root.info('test ensure ascii false: 中文')

    def test_file_config(self):
        fileConfig(os.path.join(os.path.dirname(__file__), 'logger_config.ini'))
        root = logging.getLogger('root')
        root.info('test file config')

    def tearDown(self):
        root = logging.getLogger()
        # remove handlers
        root.handlers = []


if __name__ == '__main__':
    unittest.main()

