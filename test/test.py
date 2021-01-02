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

from jsonformatter import JsonFormatter, basicConfig


class JsonFormatterTest(unittest.TestCase):

    def test_default_config(self):
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        datefmt = None
        sh = logging.StreamHandler()
        formatter = JsonFormatter()
        sh.setFormatter(formatter)

        sh.setLevel(logging.INFO)

        root.addHandler(sh)

        root.info("test %s config", 'default')

    def test_string_format(self):
        STRING_FORMAT = '''{
            "Name":            "name",
            "Levelno":         "levelno",
            "Levelname":       "levelname",
            "Pathname":        "pathname",
            "Filename":        "filename",
            "Module":          "module",
            "Lineno":          "lineno",
            "FuncName":        "funcName",
            "Created":         "created",
            "Asctime":         "asctime",
            "Msecs":           "msecs",
            "RelativeCreated": "relativeCreated",
            "Thread":          "thread",
            "ThreadName":      "threadName",
            "Process":         "process",
            "Message":         "message"
        }'''
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        datefmt = None
        sh = logging.StreamHandler()
        formatter = JsonFormatter(STRING_FORMAT, datefmt)
        sh.setFormatter(formatter)

        sh.setLevel(logging.INFO)

        root.addHandler(sh)

        root.info("test %s format", 'string')

    def test_format_style(self):
        FORMT_STYLE = {
            "name": "name",
            "levelno": "levelno",
            "levelname": "levelname",
            "pathname": "pathname",
            "filename": "filename",
            "module": "module",
            "lineno": "lineno",
            "funcName": "funcName",
            "created": "created",
            "asctime": "asctime",
            "msecs": "msecs",
            "relativeCreated": "relativeCreated",
            "thread": "thread",
            "threadName": "threadName",
            "process": "process",
            "message": "{message}"
        }

        root = logging.getLogger()
        root.setLevel(logging.INFO)

        datefmt = None
        sh = logging.StreamHandler()
        formatter = JsonFormatter(FORMT_STYLE, datefmt, '{')
        sh.setFormatter(formatter)

        sh.setLevel(logging.INFO)

        root.addHandler(sh)

        root.info("test %s style", 'format')

    def test_template_style(self):
        TEMPLATE_STYLE = {
            "name": "name",
            "levelno": "levelno",
            "levelname": "levelname",
            "pathname": "pathname",
            "filename": "filename",
            "module": "module",
            "lineno": "lineno",
            "funcName": "funcName",
            "created": "created",
            "asctime": "asctime",
            "msecs": "msecs",
            "relativeCreated": "relativeCreated",
            "thread": "thread",
            "threadName": "threadName",
            "process": "process",
            "message": "${message}"
        }
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        datefmt = None
        sh = logging.StreamHandler()
        formatter = JsonFormatter(TEMPLATE_STYLE, datefmt, '$')
        sh.setFormatter(formatter)

        sh.setLevel(logging.INFO)

        root.addHandler(sh)

        root.info("test %s style", 'template')

    def test_percent_style_unicode(self):
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        formatter = JsonFormatter(
            """{"log":"%(message)s"}""", style="%", ensure_ascii=False)

        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        sh.setLevel(logging.INFO)

        root.addHandler(sh)
        root.info('test percent style unicode: %s', '中文')

    def test_format_style_unicode(self):
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        formatter = JsonFormatter(
            """{"log":"{message}"}""", style="{", ensure_ascii=False)

        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        sh.setLevel(logging.INFO)

        root.addHandler(sh)
        root.info('test format style unicode: %s', '中文')

    def test_template_style_unicode(self):
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        formatter = JsonFormatter(
            """{"log":"${message}"}""", style="$", ensure_ascii=False)

        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        sh.setLevel(logging.INFO)

        root.addHandler(sh)
        root.info('test template style unicode: %s', '中文')

    def test_dict_format(self):
        DICT_FORMAT = {
            "name": "name",
            "levelno": "levelno",
            "levelname": "levelname",
            "pathname": "pathname",
            "filename": "filename",
            "module": "module",
            "lineno": "lineno",
            "funcName": "funcName",
            "created": "created",
            "asctime": "asctime",
            "msecs": "msecs",
            "relativeCreated": "relativeCreated",
            "thread": "thread",
            "threadName": "threadName",
            "process": "process",
            "message": "message"
        }
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        datefmt = None
        sh = logging.StreamHandler()
        formatter = JsonFormatter(DICT_FORMAT, datefmt)
        sh.setFormatter(formatter)

        sh.setLevel(logging.INFO)

        root.addHandler(sh)

        root.info("test %s format", 'dict')

    def test_ordered_dict_format(self):
        ORDERED_DICT_FORMAT = OrderedDict([
            ("name", "name"),
            ("levelno", "levelno"),
            ("levelname", "levelname"),
            ("pathname", "pathname"),
            ("filename", "filename"),
            ("module", "module"),
            ("lineno", "lineno"),
            ("funcName", "funcName"),
            ("created", "created"),
            ("asctime", "asctime"),
            ("msecs", "msecs"),
            ("relativeCreated", "relativeCreated"),
            ("thread", "thread"),
            ("threadName", "threadName"),
            ("process", "process"),
            ("message", "message")
        ])
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        datefmt = None
        sh = logging.StreamHandler()
        formatter = JsonFormatter(ORDERED_DICT_FORMAT, datefmt)
        sh.setFormatter(formatter)

        sh.setLevel(logging.INFO)

        root.addHandler(sh)

        root.info("test %s format", 'ordered dict')

    def test_log_exception(self):
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        sh = logging.StreamHandler()
        formatter = JsonFormatter()
        sh.setFormatter(formatter)

        sh.setLevel(logging.INFO)

        root.addHandler(sh)
        try:
            1 / 0
        except Exception as e:
            root.exception('test log exception')

    def test_record_custom_attrs(self):
        RECORD_CUSTOM_ATTRS = {
            'asctime': lambda: datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f'),
            'user id': lambda: str(random.random())[2:10]
        }
        RECORD_CUSTOM_FORMAT = OrderedDict([
            ("user id", "user id"),  # new custom attrs
            ("name", "name"),
            ("levelno", "levelno"),
            ("levelname", "levelname"),
            ("pathname", "pathname"),
            ("filename", "filename"),
            ("module", "module"),
            ("lineno", "lineno"),
            ("funcName", "funcName"),
            ("created", "created"),
            ("asctime", "asctime"),  # use custom format replace default.
            ("msecs", "msecs"),
            ("relativeCreated", "relativeCreated"),
            ("thread", "thread"),
            ("threadName", "threadName"),
            ("process", "process"),
            ("message", "message")
        ])
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        datefmt = None
        sh = logging.StreamHandler()
        formatter = JsonFormatter(
            RECORD_CUSTOM_FORMAT, datefmt, record_custom_attrs=RECORD_CUSTOM_ATTRS)
        sh.setFormatter(formatter)

        sh.setLevel(logging.INFO)

        root.addHandler(sh)
        root.info('test record custom attrs')

    def test_multi_value_in_one_key(self):
        MULTI_VALUE_FORMAT = {
            "multi value": "%(name)s - %(levelno)s - %(levelname)s - %(pathname)s - %(filename)s - %(module)s - %(lineno)d - %(funcName)s - %(created)f - %(asctime)s - %(msecs)d - %(relativeCreated)d - %(thread)d - %(threadName)s - %(process)d - %(message)s"
        }
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        datefmt = None
        sh = logging.StreamHandler()
        formatter = JsonFormatter(
            MULTI_VALUE_FORMAT, datefmt)
        sh.setFormatter(formatter)

        sh.setLevel(logging.INFO)

        root.addHandler(sh)
        root.info('test multi value in one key')

    def test_json_dumps_parameter_indent(self):
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        datefmt = None
        sh = logging.StreamHandler()
        formatter = JsonFormatter(indent=4)
        sh.setFormatter(formatter)

        sh.setLevel(logging.INFO)

        root.addHandler(sh)

        root.info('test json dumps parameter `index`: 4')

    def test_json_dumps_parameter_ensure_ascii_false(self):
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        sh = logging.StreamHandler()
        formatter = JsonFormatter(ensure_ascii=False)
        sh.setFormatter(formatter)

        sh.setLevel(logging.INFO)

        root.addHandler(sh)

        root.info('test json dumps parameter `ensure_ascii` False: 中文')

    def test_file_config(self):
        fileConfig(os.path.join(os.path.dirname(
            __file__), 'logger_config.ini'))
        root = logging.getLogger('root')
        root.info('test file config')

    def test_multi_handlers(self):
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        sh = logging.StreamHandler()
        formatter = JsonFormatter(ensure_ascii=False)
        sh.setFormatter(formatter)
        sh.setLevel(logging.INFO)
        root.addHandler(sh)

        sh = logging.StreamHandler()
        formatter = JsonFormatter(ensure_ascii=False)
        sh.setFormatter(formatter)
        sh.setLevel(logging.INFO)
        root.addHandler(sh)

        sh = logging.StreamHandler()
        formatter = logging.Formatter('%(message)s')
        sh.setFormatter(formatter)
        sh.setLevel(logging.INFO)
        root.addHandler(sh)

        root.info('test multi handlers')

    def test_mix_extra(self):
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        sh = logging.StreamHandler()
        formatter = JsonFormatter(
            ensure_ascii=False, mix_extra=True, indent=4)
        sh.setFormatter(formatter)
        sh.setLevel(logging.INFO)
        root.addHandler(sh)
        root.info('test mix extra in fmt', extra={'extra': 'extra content'})

    def test_mix_extra_position_is_head(self):
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        sh = logging.StreamHandler()
        formatter = JsonFormatter(
            ensure_ascii=False, mix_extra=True, mix_extra_position='head', indent=4)
        sh.setFormatter(formatter)
        sh.setLevel(logging.INFO)
        root.addHandler(sh)
        root.info('test mix extra position is head',
                  extra={'extra': 'extra content'})

    def test_mix_extra_multi_formatter(self):
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        fh = logging.FileHandler('jsonformatter.log')
        formatter = JsonFormatter(
            ensure_ascii=False, mix_extra=True, indent=4)
        fh.setFormatter(formatter)
        fh.setLevel(logging.INFO)
        root.addHandler(fh)

        sh = logging.StreamHandler()
        formatter = JsonFormatter(
            ensure_ascii=False, mix_extra=True, indent=4)
        sh.setFormatter(formatter)
        sh.setLevel(logging.INFO)
        root.addHandler(sh)

        root.info('test mix extra multi formatter',
                  extra={'extra': 'extra content'})

    def test_mix_extra_position_is_mix(self):
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        sh = logging.StreamHandler()
        formatter = JsonFormatter(
            ensure_ascii=False, mix_extra=True, mix_extra_position='mix', indent=4)
        sh.setFormatter(formatter)
        sh.setLevel(logging.INFO)
        root.addHandler(sh)
        root.info('test mix extra position is mix',
                  extra={'extra': 'extra content'})

    def test_record_custom_attrs_with_kwargs(self):
        def _new_custom_attribute_status(**record_attrs):
            if record_attrs['levelname'] in ['ERROR', 'CRITICAL']:
                return 'failed'
            else:
                return 'success'

        RECORD_CUSTOM_ATTRS = {
            'status': _new_custom_attribute_status,
        }

        RECORD_CUSTOM_FORMAT = OrderedDict([
            ("status", "status"),  # new custom attribute
            ("log", "message")
        ])
        root = logging.getLogger()
        root.setLevel(logging.INFO)

        datefmt = None
        sh = logging.StreamHandler()
        formatter = JsonFormatter(
            RECORD_CUSTOM_FORMAT,
            record_custom_attrs=RECORD_CUSTOM_ATTRS
        )
        sh.setFormatter(formatter)

        sh.setLevel(logging.INFO)

        root.addHandler(sh)
        root.info('test record custom attrs with kwargs')
        root.error('test record custom attrs with kwargs')

    def test_basic_config_level(self):
        basicConfig(level=logging.INFO)
        logging.info('basic config level')

    def test_basic_config_format(self):
        basicConfig(
            level=logging.INFO,
            format="""{
            "levelname": "levelname",
            "name": "name",
            "log": "message"
            }"""
        )
        logging.info('basic config format')

    def tearDown(self):
        root = logging.getLogger()
        # remove handlers
        root.handlers = []


if __name__ == '__main__':
    unittest.main()
