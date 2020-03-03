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
import json
import logging
import sys
import warnings

# From python3.7, dict is in ordered,so do json package's load(s)/dump(s).
# https://docs.python.org/3.7/library/stdtypes.html#dict
# Changed in version 3.7: Dictionary order is guaranteed to be insertion order. This behavior was an implementation detail of CPython from 3.6.
if sys.version_info >= (3, 7):
    dictionary = dict
else:
    from collections import OrderedDict
    dictionary = OrderedDict


class JsonFormatter(logging.Formatter):
    """
    Formatter instances are used to convert a LogRecord to text.

    Formatters need to know how a LogRecord is constructed. They are
    responsible for converting a LogRecord to (usually) a string which can
    be interpreted by either a human or an external system. The base Formatter
    allows a formatting string to be specified. If none is supplied, the
    default value of "%s(message)" is used.

    The Formatter can be initialized with a format string which makes use of
    knowledge of the LogRecord attributes - e.g. the default value mentioned
    above makes use of the fact that the user's message and arguments are pre-
    formatted into a LogRecord's message attribute. Currently, the useful
    attributes in a LogRecord are described by:

    %(name)s            Name of the logger (logging channel)
    %(levelno)s         Numeric logging level for the message (DEBUG, INFO,
                        WARNING, ERROR, CRITICAL)
    %(levelname)s       Text logging level for the message ("DEBUG", "INFO",
                        "WARNING", "ERROR", "CRITICAL")
    %(pathname)s        Full pathname of the source file where the logging
                        call was issued (if available)
    %(filename)s        Filename portion of pathname
    %(module)s          Module (name portion of filename)
    %(lineno)d          Source line number where the logging call was issued
                        (if available)
    %(funcName)s        Function name
    %(created)f         Time when the LogRecord was created (time.time()
                        return value)
    %(asctime)s         Textual time when the LogRecord was created
    %(msecs)d           Millisecond portion of the creation time
    %(relativeCreated)d Time in milliseconds when the LogRecord was created,
                        relative to the time the logging module was loaded
                        (typically at application startup time)
    %(thread)d          Thread ID (if available)
    %(threadName)s      Thread name (if available)
    %(process)d         Process ID (if available)
    %(message)s         The result of record.getMessage(), computed just as
                        the record is emitted
    """

    def parseFmt(self, fmt):
        if isinstance(fmt, str):
            return json.loads(fmt, object_pairs_hook=dictionary)
        elif isinstance(fmt, dictionary):
            return fmt
        elif isinstance(fmt, dict):
            warnings.warn(
                "Current Python version is below 3.7.0, the key's order of dict may be different from the definition, Please Use `OrderedDict` replace.", UserWarning)
            return dictionary([(k, fmt[k]) for k in sorted(fmt.keys())])
        else:
            raise TypeError(
                'The type `%s` is not supported, fmt must be `string` with json format, `OrderedDcit` or `dict` type. ' % type(fmt))

    def checkRecordCustomAttrs(self, record_custom_attrs):
        if isinstance(record_custom_attrs, dict):
            for attr, value in record_custom_attrs.items():
                if not callable(value):
                    raise TypeError('%s is not callable.' % value)
        else:
            raise TypeError('record_custom_attrs must be dict type.')

    def __init__(self, fmt=None, datefmt=None, style='%', record_custom_attrs=None, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False, **kw):
        """
        If ``record_custom_attrs`` is not ``None``, it must be a ``dict`` type, the key of dict will be setted as LogRecord's attribute, the value of key must be a callable object and without parameters, it returned obj will be setted as attribute's value of LogRecord.

        If ``skipkeys`` is true then ``dict`` keys that are not basic types
        (``str``, ``int``, ``float``, ``bool``, ``None``) will be skipped
        instead of raising a ``TypeError``.

        If ``ensure_ascii`` is false, then the return value can contain non-ASCII
        characters if they appear in strings contained in ``obj``. Otherwise, all
        such characters are escaped in JSON strings.

        If ``check_circular`` is false, then the circular reference check
        for container types will be skipped and a circular reference will
        result in an ``OverflowError`` (or worse).

        If ``allow_nan`` is false, then it will be a ``ValueError`` to
        serialize out of range ``float`` values (``nan``, ``inf``, ``-inf``) in
        strict compliance of the JSON specification, instead of using the
        JavaScript equivalents (``NaN``, ``Infinity``, ``-Infinity``).

        If ``indent`` is a non-negative integer, then JSON array elements and
        object members will be pretty-printed with that indent level. An indent
        level of 0 will only insert newlines. ``None`` is the most compact
        representation.

        If specified, ``separators`` should be an ``(item_separator, key_separator)``
        tuple.  The default is ``(', ', ': ')`` if *indent* is ``None`` and
        ``(',', ': ')`` otherwise.  To get the most compact JSON representation,
        you should specify ``(',', ':')`` to eliminate whitespace.

        ``default(obj)`` is a function that should return a serializable version
        of obj or raise TypeError. The default simply raises TypeError.

        If *sort_keys* is true (default: ``False``), then the output of
        dictionaries will be sorted by key.

        To use a custom ``JSONEncoder`` subclass (e.g. one that overrides the
        ``.default()`` method to serialize additional types), specify it with
        the ``cls`` kwarg; otherwise ``JSONEncoder`` is used.

        """
        if record_custom_attrs:
            self.checkRecordCustomAttrs(record_custom_attrs)

        logging.Formatter.__init__(self, fmt='', datefmt=datefmt, style=style)

        self.record_custom_attrs = record_custom_attrs
        self._style._fmt = ''
        self.skipkeys = skipkeys
        self.ensure_ascii = ensure_ascii
        self.check_circular = check_circular
        self.allow_nan = allow_nan
        self.cls = cls
        self.indent = indent
        self.separators = separators
        self.default = default
        self.sort_keys = sort_keys
        self.kw = kw

        self.json_fmt = self.parseFmt(fmt)

    def setRecordMessage(self, record, msg, args):
        if not isinstance(msg, (str, int, float, bool, type(None))):
            record.message = str(msg)
        else:
            record.message = msg

        if args:
            record.message = str(record.message) % args

        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            record.message = str(record.message)
            if record.message[-1:] != "\n":
                record.message = record.message + "\n"
            record.message = record.message + record.exc_text
        if record.stack_info:
            record.message = str(record.message)
            if record.message[-1:] != "\n":
                record.message = record.message + "\n"
            record.message = record.message + self.formatStack(record.stack_info)

    def setRecordCustomAttrs(self, record):
        if self.record_custom_attrs:
            for k, v in self.record_custom_attrs.items():
                setattr(record, k, v())

    def formatMessage(self, record):
        return self._style.format(record)

    def format(self, record):
        result = dictionary()

        # store origin attributes
        _msg, _args = record.msg, record.args
        record.msg, record.args = '', tuple()

        self.setRecordMessage(record, _msg, _args)

        record.asctime = self.formatTime(record, self.datefmt)

        if self.record_custom_attrs:
            self.setRecordCustomAttrs(record)

        for k, v in self.json_fmt.items():
            self._style._fmt = v
            result[k] = getattr(record, v, None) if v in record.__dict__ else self.formatMessage(record)
        self._style._fmt = ''
        # apply origin attributes
        record.msg, record.args = _msg, _args

        return json.dumps(result, skipkeys=self.skipkeys, ensure_ascii=self.ensure_ascii, check_circular=self.check_circular, allow_nan=self.allow_nan, cls=self.cls, indent=self.indent, separators=self.separators, default=self.default, sort_keys=self.sort_keys, **self.kw)
