#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: jsonformatter.py
Author: Me
Email: yourname@email.com
Github: https://github.com/yourname
Description: jsonformatter.py
"""
import inspect
import json
import logging
import sys
import warnings
from functools import wraps, partial
from string import Template

# From python3.7, dict is in ordered,so do json package's load(s)/dump(s).
# https://docs.python.org/3.7/library/stdtypes.html#dict
# Changed in version 3.7: Dictionary order is guaranteed to be insertion order. This behavior was an implementation detail of CPython from 3.6.
if sys.version_info >= (3, 7):
    dictionary = dict
else:
    from collections import OrderedDict
    dictionary = OrderedDict

# compatible python2, python 3  no long type, start
if sys.version_info >= (3, 0):
    long = int
# compatible python2, python 3  no long type, end


class PercentStyle(object):

    asctime_format = '%(asctime)s'
    asctime_search = '%(asctime)'

    def __init__(self, fmt):
        self._fmt = ''

    def usesTime(self):
        return self._fmt.find(self.asctime_search) >= 0

    def format(self, record):
        return self._fmt % record.__dict__


class StrFormatStyle(PercentStyle):

    asctime_format = '{asctime}'
    asctime_search = '{asctime'

    def format(self, record):
        return self._fmt.format(**record.__dict__)


class StringTemplateStyle(PercentStyle):

    asctime_format = '${asctime}'
    asctime_search = '${asctime}'

    def __init__(self, fmt):
        PercentStyle.__init__(self, fmt)
        self._tpl = {}
        for _, v in fmt.items():
            self._tpl[v] = Template(v)

    def usesTime(self):
        fmt = self._fmt
        return fmt.find('$asctime') >= 0 or fmt.find(self.asctime_format) >= 0

    def format(self, record):
        return self._tpl[self._fmt].substitute(**record.__dict__)


BASIC_FORMAT = dictionary([
    ('levelname', 'levelname'),
    ('name', 'name'),
    ('message', 'message')
])

_STYLES = {
    '%': PercentStyle,
    '{': StrFormatStyle,
    '$': StringTemplateStyle,
}

_LogRecordDefaultAttributes = {
    'name',
    'msg',
    'args',
    'levelname',
    'levelno',
    'pathname',
    'filename',
    'module',
    'exc_info',
    'exc_text',
    'stack_info',
    'lineno',
    'funcName',
    'created',
    'msecs',
    'relativeCreated',
    'thread',
    'threadName',
    'processName',
    'process',
    'message',
    'asctime'
}

_MIX_EXTRA_ORDER = {
    'head',
    'tail',
    'mix'
}


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
                "Current python version is lower than 3.7.0, the key's order of dict may be different with definition, please use `OrderedDict` replace.", UserWarning)
            return dictionary((k, fmt[k]) for k in sorted(fmt.keys()))
        else:
            raise TypeError(
                '`%s` type is not supported, `fmt` must be `json`, `OrderedDcit` or `dict` type. ' % type(fmt))

    def checkRecordCustomAttrs(self, record_custom_attrs):
        def _patch_no_params_func_accept_kwargs(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args)
            return wrapper

        if record_custom_attrs:
            if isinstance(record_custom_attrs, dict):
                for attr, func in record_custom_attrs.items():
                    if not callable(func):
                        raise TypeError('`%s` is not callable.' % func)

                    if inspect.isfunction(func):
                        argspec = getattr(inspect, 'getfullargspec',
                                          inspect.getargspec)(func)
                        if argspec.args:
                            raise TypeError(
                                "`%s` must no Positional Parameters." % func.__name__
                            )
                        else:
                            if not (
                                getattr(argspec, 'keywords', False) or
                                    getattr(argspec, 'varkw', False)
                            ):
                                record_custom_attrs[attr] = _patch_no_params_func_accept_kwargs(
                                    func
                                )
                    else:
                        if isinstance(func, partial):
                            warnings.warn(
                                "`%s` is a partial function, please make sure no positional parameters in function signature." % (func), UserWarning)
                        elif hasattr(func, '__call__'):
                            warnings.warn(
                                "`%s` is a callable instance, please make sure no positional parameters in method signature." % (func), UserWarning)
                        else:
                            warnings.warn(
                                "`%s` is a unknown callable type, please make sure no positional parameters in function/method signature." % (func), UserWarning)
            else:
                raise TypeError('`record_custom_attrs` must be `dict` type.')
        else:
            return

    def __init__(self, fmt=BASIC_FORMAT, datefmt=None, style='%', record_custom_attrs=None, mix_extra=False, mix_extra_position='tail', skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, encoding='utf-8', default=None, sort_keys=False, **kw):
        """
        If ``style`` not in ``['%', '{', '$']``, a ``ValueError`` will be raised.

        If ``record_custom_attrs`` is not ``None``, it must be a ``dict``
        type, the key of dict will be setted as ``LogRecord``'s attribute, the
        value of key must be a callable object and no positional
        parameters(e.g. ``lambda: None``, ``lambda **log_reocrd_attrs: None``), it 
        returned will be setted as attribute's value of ``LogRecord``.

        If ``mix_extra`` is ``True``, the keys of ``extra`` different with ``fmt``
        will be added to log, the keys' value of ``extra`` same with ``fmt`` 
        will overwrite ``fmt``.

        If ``mix_extra_position`` not in ``['head', 'tail' or 'mix']``, a
        ``ValueError`` will be raised.

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

        ``encoding`` is the character encoding for str instances, only
        supported by python 2.7, default is UTF-8.

        ``default(obj)`` is a function that should return a serializable version
        of obj or raise TypeError. The default simply raises TypeError.

        If *sort_keys* is true (default: ``False``), then the output of
        dictionaries will be sorted by key.

        To use a custom ``JSONEncoder`` subclass (e.g. one that overrides the
        ``.default()`` method to serialize additional types), specify it with
        the ``cls`` kwarg; otherwise ``JSONEncoder`` is used.

        """
        if style not in _STYLES:
            raise ValueError('`style` must be one of: %s' % ','.join(
                             _STYLES.keys()))
        if mix_extra_position not in _MIX_EXTRA_ORDER:
            raise ValueError('`mix_extra_position` must be one of: %s' % ','.join(
                             _MIX_EXTRA_ORDER))
        # compatible python2 start
        if sys.version_info < (3, 0):
            kw.update(encoding=encoding)
            logging.Formatter.__init__(
                self, fmt='', datefmt=datefmt)
        else:
            logging.Formatter.__init__(
                self, fmt='', datefmt=datefmt, style=style)
        # compatible python2 end

        self.json_fmt = self.parseFmt(fmt)
        self.record_custom_attrs = record_custom_attrs
        self._style = _STYLES[style](self.json_fmt)
        self._style._fmt = ''
        self.mix_extra = mix_extra
        self.mix_extra_position = mix_extra_position

        self.checkRecordCustomAttrs(self.record_custom_attrs)

        # support `json.dumps` parameters start
        self.skipkeys = skipkeys
        self.ensure_ascii = ensure_ascii
        self.check_circular = check_circular
        self.allow_nan = allow_nan
        self.cls = cls
        self.indent = indent
        self.separators = separators
        self.encoding = encoding
        self.default = default
        self.sort_keys = sort_keys
        self.kw = kw
        # support `json.dumps` parameters end

    def setRecordMessage(self, record):
        if isinstance(record.msg, (int, long, float, bool, type(None))):
            # keep these types without quote when output
            record.message = record.msg
        else:
            record.message = str(record.msg)

        if record.args:
            record.message = str(record.message) % record.args

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
        # compatible python2, record no stack_info attribute in python2, start
        if getattr(record, 'stack_info', None):
            record.message = str(record.message)
            if record.message[-1:] != "\n":
                record.message = record.message + "\n"
            record.message = record.message + \
                self.formatStack(record.stack_info)
        # compatible python2, record no stack_info attribute in python2, end

    def getRecordExtraAttrs(self, record):
        extras = {
            k: record.__dict__[k]
            for k in record.__dict__
            if k not in _LogRecordDefaultAttributes
        }
        if sys.version_info >= (3, 7):
            return extras
        else:
            return dictionary((k, extras[k]) for k in sorted(extras.keys()))

    def setRecordCustomAttrs(self, record):
        for k, v in self.record_custom_attrs.items():
            setattr(record, k, v(**record.__dict__))

    def formatMessage(self, record):
        return self._style.format(record)

    def format(self, record):
        def _set_extra_to_result():
            for k, v in extra.items():
                if k not in self.json_fmt:
                    result[k] = v

        def _set_fmt_to_result():
            # this is for keeping `record` attribute `type`
            if v in record.__dict__:
                result[k] = getattr(record, v, None)
            # this is for convert to string
            else:
                self._style._fmt = v
                result[k] = self.formatMessage(record)

        result = dictionary()

        self.setRecordMessage(record)

        record.asctime = self.formatTime(record, self.datefmt)

        # pop stored __extra start
        extra = record.__dict__.pop('__extra', None) or record.__dict__.pop('_JsonFormatter__extra', None)
        if extra is None:
            # extra is dictionary
            extra = self.getRecordExtraAttrs(record)
        # pop stored __extra end

        if self.record_custom_attrs:
            self.setRecordCustomAttrs(record)

        # compatible python2 start
        if sys.version_info < (3, 0):
            for k, v in record.__dict__.items():
                if isinstance(v, str):
                    record.__dict__.update({k: v.decode(self.encoding)})
        # compatible python2 end

        if not self.mix_extra:
            for k, v in self.json_fmt.items():
                _set_fmt_to_result()
        else:
            if self.mix_extra_position == 'head':
                _set_extra_to_result()
            for k, v in self.json_fmt.items():
                if k in extra:
                    result[k] = extra[k]
                else:
                    _set_fmt_to_result()
            if self.mix_extra_position == 'tail':
                _set_extra_to_result()
            if self.mix_extra_position == 'mix':
                _set_extra_to_result()
                result = dictionary(
                    (k, result[k])
                    for k in sorted(result.keys())
                )

        self._style._fmt = ''

        # store __extra start
        record.__extra = extra
        # store __extra end

        return json.dumps(
            result,
            skipkeys=self.skipkeys,
            ensure_ascii=self.ensure_ascii,
            check_circular=self.check_circular,
            allow_nan=self.allow_nan,
            cls=self.cls,
            indent=self.indent,
            separators=self.separators,
            default=self.default,
            sort_keys=self.sort_keys,
            **self.kw
        )


def basicConfig(**kwargs):
    """
    Do basic configuration for the logging system.

    This function does nothing if the root logger already has handlers
    configured. It is a convenience method intended for use by simple scripts
    to do one-shot configuration of the logging package.

    The default behaviour is to create a StreamHandler which writes to
    sys.stderr, set a formatter using the BASIC_FORMAT format string, and
    add the handler to the root logger.

    A number of optional keyword arguments may be specified, which can alter
    the default behaviour.

    filename  Specifies that a FileHandler be created, using the specified
              filename, rather than a StreamHandler.
    filemode  Specifies the mode to open the file, if filename is specified
              (if filemode is unspecified, it defaults to 'a').
    format    Use the specified format string for the handler.
    datefmt   Use the specified date/time format.
    style     If a format string is specified, use this to specify the
              type of format string (possible values '%', '{', '$', for
              %-formatting, :meth:`str.format` and :class:`string.Template`
              - defaults to '%').
    level     Set the root logger level to the specified level.
    stream    Use the specified stream to initialize the StreamHandler. Note
              that this argument is incompatible with 'filename' - if both
              are present, 'stream' is ignored.
    handlers  If specified, this should be an iterable of already created
              handlers, which will be added to the root handler. Any handler
              in the list which does not have a formatter assigned will be
              assigned the formatter created in this function.

    Note that you could specify a stream created using open(filename, mode)
    rather than passing the filename and mode in. However, it should be
    remembered that StreamHandler does not close its stream (since it may be
    using sys.stdout or sys.stderr), whereas FileHandler closes its stream
    when the handler is closed.

    .. versionchanged:: 3.2
       Added the ``style`` parameter.

    .. versionchanged:: 3.3
       Added the ``handlers`` parameter. A ``ValueError`` is now thrown for
       incompatible arguments (e.g. ``handlers`` specified together with
       ``filename``/``filemode``, or ``filename``/``filemode`` specified
       together with ``stream``, or ``handlers`` specified together with
       ``stream``.
    """
    # Add thread safety in case someone mistakenly calls
    # basicConfig() from multiple threads
    logging._acquireLock()
    try:
        if len(logging.root.handlers) == 0:
            handlers = kwargs.pop("handlers", None)
            if handlers is None:
                if "stream" in kwargs and "filename" in kwargs:
                    raise ValueError("'stream' and 'filename' should not be "
                                     "specified together")
            else:
                if "stream" in kwargs or "filename" in kwargs:
                    raise ValueError("'stream' or 'filename' should not be "
                                     "specified together with 'handlers'")
            if handlers is None:
                filename = kwargs.pop("filename", None)
                mode = kwargs.pop("filemode", 'a')
                if filename:
                    h = logging.FileHandler(filename, mode)
                else:
                    stream = kwargs.pop("stream", None)
                    h = logging.StreamHandler(stream)
                handlers = [h]
            dfs = kwargs.pop("datefmt", None)
            style = kwargs.pop("style", '%')
            if style not in _STYLES:
                raise ValueError('Style must be one of: %s' % ','.join(
                                 _STYLES.keys()))
            fs = kwargs.pop("format", BASIC_FORMAT)
            fmt = JsonFormatter(fs, dfs, style)
            for h in handlers:
                if h.formatter is None:
                    h.setFormatter(fmt)
                logging.root.addHandler(h)
            level = kwargs.pop("level", None)
            if level is not None:
                logging.root.setLevel(level)
            if kwargs:
                keys = ', '.join(kwargs.keys())
                raise ValueError('Unrecognised argument(s): %s' % keys)
    finally:
        logging._releaseLock()
