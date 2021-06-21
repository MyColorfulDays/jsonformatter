import logging

from jsonformatter import JsonFormatter

# The `fmt/format` argument of `JsonFormatter` can be `json`, `OrderedDict`, `dict`.
# If the argument type is `dict` and python version < 3.7.0, the output order is sorted keys, otherwise consistent with defined order.
# key: string, whatever you like.
# value: string, `LogRecord` attribute name.
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

formatter = JsonFormatter(STRING_FORMAT)
sh = logging.StreamHandler()
sh.setFormatter(formatter)
sh.setLevel(logging.INFO)
root = logging.getLogger()
root.setLevel(logging.INFO)
root.addHandler(sh)

root.info("Hello, %s", 'jsonformatter')
import logging

from jsonformatter import JsonFormatter

# The `fmt/format` argument of `JsonFormatter` can be `json`, `OrderedDict`, `dict`.
# If the argument type is `dict` and python version < 3.7.0, the output order is sorted keys, otherwise consistent with defined order.
# key: string, whatever you like.
# value: string, `LogRecord` attribute name.
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

formatter = JsonFormatter(STRING_FORMAT)
sh = logging.StreamHandler()
sh.setFormatter(formatter)
sh.setLevel(logging.INFO)
root = logging.getLogger()
root.setLevel(logging.INFO)
root.addHandler(sh)

root.info("Hello, %s", 'jsonformatter')
