- [jsonformatter -- for python log json](#jsonformatter----for-python-log-json)
    - [Installation](#installation)
    - [Basic Usage](#basic-usage)
        - [Case 1. Initial root logger like `logging.basicConfig`](#case-1-initial-root-logger-like-loggingbasicconfig)
        - [Case 2. Complete config in python code](#case-2-complete-config-in-python-code)
        - [Case 3. Use config file](#case-3-use-config-file)
        - [Case 4. In `Flask` project, add `LogRecord` attribute for auto output](#case-4-in-flask-project-add-logrecord-attribute-for-auto-output)
        - [Case 5. In `Django` project, config `LOGGING`](#case-5-in-django-project-config-logging)
    - [More Usage](#more-usage)
        - [Case 1. Mix `extra` to output](#case-1-mix-extra-to-output)
        - [Case 2. Output multiple attributes in one key](#case-2-output-multiple-attributes-in-one-key)
        - [Case 3. Support `json.dumps` all optional parameters](#case-3-support-jsondumps-all-optional-parameters)
        - [Case 4. Solve cumtom `LogRecord` attribute is not `JSON serializable`](#case-4-solve-cumtom-logrecord-attribute-is-not-json-serializable)
    - [LogRecord Attributes](#logrecord-attributes)



# jsonformatter -- for python log json

**jsonformatter** is a formatter for python output json log, e.g. output **LogStash** needed log.

Easily **custom(add/replace)** `LogRecord` attribute, e.g. in `Flask` web project, add `username` attribute to `LogRecord`  for auto output username.



**Python 2.7** and **python 3** are supported from version 0.2.X,  if you are using a version lower than 0.2.X,  Only **python 3** is supported.



## Installation

jsonformatter is available on PyPI.
Use pip to install:

```shell
$ pip install jsonformatter
```
or:

```shell
$ git clone https://github.com/MyColorfulDays/jsonformatter.git
$ cd jsonformatter
$ python setup.py install
```



## Basic Usage

### Case 1. Initial root logger like `logging.basicConfig`
```python
import logging

from jsonformatter import basicConfig

# default keyword parameter `format`: """{"levelname": "levelname", "name": "name", "message": "message"}"""
basicConfig(level=logging.INFO)
logging.info('hello, jsonformatter')
```

output:

```shell
{"levelname": "INFO", "name": "root", "message": "hello, jsonformatter"}
```



### Case 2. Complete config in python code

```python
import logging

from jsonformatter import JsonFormatter

# `format` can be `json`, `OrderedDict`, `dict`.
# If `format` is `dict` and python version < 3.7.0, the output order is sorted keys, otherwise will same as defined order.
# key: string, can be whatever you like.
# value: `LogRecord` attribute name.
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

formatter = JsonFormatter(STRING_FORMAT)

sh = logging.StreamHandler()
sh.setFormatter(formatter)
sh.setLevel(logging.INFO)

root.addHandler(sh)

root.info("test %s format", 'string')
```

output:

```shell
{"Name": "root", "Levelno": 20, "Levelname": "INFO", "Pathname": "test.py", "Filename": "test.py", "Module": "test", "Lineno": 75, "FuncName": "test_string_format", "Created": 1588185267.3198836, "Asctime": "2020-04-30 02:34:27,319", "Msecs": 319.8835849761963, "RelativeCreated": 88.2880687713623, "Thread": 16468, "ThreadName": "MainThread", "Process": 16828, "Message": "test string format"}
```



### Case 3. Use config file

config file:
```shell
$ cat logger_config.ini
[loggers]
keys=root

[logger_root]
level=INFO
handlers=infohandler


###############################################

[handlers]
keys=infohandler

[handler_infohandler]
class=StreamHandler
level=INFO
formatter=form01
args=(sys.stdout,)

###############################################

[formatters]
keys=form01

[formatter_form01]
class=jsonformatter.JsonFormatter
format={"name": "name","levelno": "levelno","levelname": "levelname","pathname": "pathname","filename": "filename","module": "module","lineno": "lineno","funcName": "funcName","created": "created","asctime": "asctime","msecs": "msecs","relativeCreated": "relativeCreated","thread": "thread","threadName": "threadName","process": "process","message": "message"}
```
python code:
```python3
import logging
import os
from logging.config import fileConfig

fileConfig(os.path.join(os.path.dirname(__file__), 'logger_config.ini'))
root = logging.getLogger('root')
root.info('test file config')

```

output:

```shell
{"name": "root", "levelno": 20, "levelname": "INFO", "pathname": "test.py", "filename": "test.py", "module": "test", "lineno": 315, "funcName": "test_file_config", "created": 1588185267.3020294, "asctime": "2020-04-30 02:34:27", "msecs": 302.0293712615967, "relativeCreated": 70.4338550567627, "thread": 16468, "threadName": "MainThread", "process": 16828, "message": "test file config"}
```



### Case 4. In `Flask` project, add `LogRecord` attribute for auto output

flask_demo.py

```python
import datetime
import json
import logging
import random
from collections import OrderedDict

from jsonformatter import JsonFormatter
from flask import Flask, has_request_context, request, session
from flask.logging import default_handler

app = Flask(__name__)

# the key will add/replace `LogRecord` attribute.
# the value must be `callable` type and not support positional paramters, the returned value will be as the `LogRecord` attribute value.
RECORD_CUSTOM_ATTRS = {
    # no parameters
    'url': lambda: request.url if has_request_context() else None,
    'username': lambda: session['username'] if has_request_context() and ('username' in session) else None,
    # Arbitrary keywords parameters
    'status': lambda **record_attrs: 'failed' if record_attrs['levelname'] in ['ERROR', 'CRITICAL'] else 'success'
}

RECORD_CUSTOM_FORMAT = OrderedDict([
    # custom record attributes start
    ("Url", "url"),
    ("Username", "username"),
    ("Status", "status"),
    # custom record attributes end
    ("Name", "name"),
    ("Levelno", "levelno"),
    ("Levelname", "levelname"),
    ("Pathname", "pathname"),
    ("Filename", "filename"),
    ("Module", "module"),
    ("Lineno", "lineno"),
    ("FuncName", "funcName"),
    ("Created", "created"),
    ("Asctime", "asctime"),
    ("Msecs", "msecs"),
    ("RelativeCreated", "relativeCreated"),
    ("Thread", "thread"),
    ("ThreadName", "threadName"),
    ("Process", "process"),
    ("Message", "message")
])


formatter = JsonFormatter(
    RECORD_CUSTOM_FORMAT,
    record_custom_attrs=RECORD_CUSTOM_ATTRS
)

default_handler.setFormatter(formatter)
app.logger.warning('hello, jsonformatter')
```

output:

```shell
{"Url": null, "Username": null, "Status": "success", "Name": "flask_demo", "Levelno": 30, "Levelname": "WARNING", "Pathname": "flask_demo.py", "Filename": "flask_demo.py", "Module": "flask_demo", "Lineno": 54, "FuncName": "<module>", "Created": 1595781463.3557186, "Asctime": "2020-07-27 00:37:43,355", "Msecs": 355.71861267089844, "RelativeCreated": 858.7081432342529, "Thread": 15584, "ThreadName": "MainThread", "Process": 17560, "Message": "hello, jsonformatter"}
```



### Case 5. In `Django` project, config `LOGGING`

settings.py

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'class': 'jsonformatter.JsonFormatter',
            'format': OrderedDict([
                ("Name", "name"),
                ("Levelno", "levelno"),
                ("Levelname", "levelname"),
                ("Pathname", "pathname"),
                ("Filename", "filename"),
                ("Module", "module"),
                ("Lineno", "lineno"),
                ("FuncName", "funcName"),
                ("Created", "created"),
                ("Asctime", "asctime"),
                ("Msecs", "msecs"),
                ("RelativeCreated", "relativeCreated"),
                ("Thread", "thread"),
                ("ThreadName", "threadName"),
                ("Process", "process"),
                ("Message", "message")
            ])
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
    }
}
```



## More Usage

### Case 1. Mix `extra` to output

```python
import logging

from jsonformatter import JsonFormatter

root = logging.getLogger()
root.setLevel(logging.INFO)

sh = logging.StreamHandler()
formatter = JsonFormatter(
    ensure_ascii=False, 
    mix_extra=True,
    mix_extra_position='tail' # optional: head, mix
)
sh.setFormatter(formatter)
sh.setLevel(logging.INFO)
root.addHandler(sh)

root.info(
    'test mix extra in fmt',
    extra={
        'extra1': 'extra content 1',
        'extra2': 'extra content 2'
    })
root.info(
    'test mix extra in fmt',
    extra={
        'extra3': 'extra content 3',
        'extra4': 'extra content 4'
    })
```

output:

```shell
{"levelname": "INFO", "name": "root", "message": "test mix extra in fmt", "extra1": "extra content 1", "extra2": "extra content 2"}
{"levelname": "INFO", "name": "root", "message": "test mix extra in fmt", "extra3": "extra content 3", "extra4": "extra content 4"}
```



### Case 2. Output multiple attributes in one key
```python
import logging

from jsonformatter import JsonFormatter

MULTI_ATTRIBUTES_FORMAT = '''{
    "multi attributes in one key": "%(name)s - %(levelno)s - %(levelname)s - %(pathname)s - %(filename)s - %(module)s - %(lineno)d - %(funcName)s - %(created)f - %(asctime)s - %(msecs)d - %(relativeCreated)d - %(thread)d - %(threadName)s - %(process)d - %(message)s"
}
'''


root = logging.getLogger()
root.setLevel(logging.INFO)

formatter = JsonFormatter(MULTI_ATTRIBUTES_FORMAT)

sh = logging.StreamHandler()
sh.setFormatter(formatter)

sh.setLevel(logging.INFO)

root.addHandler(sh)
root.info('test multi attributes in one key')
```



### Case 3. Support `json.dumps` all optional parameters

```python
import logging

from jsonformatter import JsonFormatter

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


formatter = JsonFormatter(STRING_FORMAT, indent=4, ensure_ascii=False)

sh = logging.StreamHandler()
sh.setFormatter(formatter)

sh.setLevel(logging.INFO)

root.addHandler(sh)

root.info('test json optional paramter: 中文')
```



### Case 4. Solve cumtom `LogRecord` attribute is not `JSON serializable`

```python
import datetime
import json
import logging
import random
from collections import OrderedDict

from jsonformatter import JsonFormatter

# the key will add/replace `LogRecord` attribute.
# the value must be `callable` type and not support positional paramters, the returned value will be as the `LogRecord` attribute value.
RECORD_CUSTOM_ATTRS = {
    # `datetime.datetime` type is not JSON serializable.
    # solve it in three ways, choose which you like.
    # 1. use `LogRecord` attribute `Format`: %(asctme)s.
    # 2. use `json.dumps` optional parameter `default`.
    # 3. use `json.dumps` optional parameter `cls`.
    'asctime': lambda: datetime.datetime.today(),
    'user id': lambda: str(random.random())[2:10]
}

RECORD_CUSTOM_FORMAT = OrderedDict([
    ("User id",         "user id"),  # new custom attrs
    ("Name",            "name"),
    ("Levelno",         "levelno"),
    ("Levelname",       "levelname"),
    ("Pathname",        "pathname"),
    ("Filename",        "filename"),
    ("Module",          "module"),
    ("Lineno",          "lineno"),
    ("FuncName",        "funcName"),
    ("Created",         "created"),
    ("Asctime",         "%(asctime)s"),  # use `LogRecord` attribute `Format` to find matched key from RECORD_CUSTOM_ATTRS and call it value.
    ("Msecs",           "msecs"),
    ("RelativeCreated", "relativeCreated"),
    ("Thread",          "thread"),
    ("ThreadName",      "threadName"),
    ("Process",         "process"),
    ("Message",         "message")
])


# use `json.dumps` optional parameter `default`
def DEFAULT_SOLUTION(o):
    if not isinstance(o, (str, int, float, bool, type(None))):
        return str(o)
    else:
        return o

# use `json.dumps` optional parameter `cls`
class CLS_SOLUTION(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)

root = logging.getLogger()
root.setLevel(logging.INFO)

formatter = JsonFormatter(RECORD_CUSTOM_FORMAT, record_custom_attrs=RECORD_CUSTOM_ATTRS, default=DEFAULT_SOLUTION, cls=CLS_SOLUTION)

sh = logging.StreamHandler()
sh.setFormatter(formatter)

sh.setLevel(logging.INFO)

root.addHandler(sh)
root.info('record custom attrs')
```



## LogRecord Attributes 

Offical url: https://docs.python.org/3/library/logging.html#logrecord-attributes

Attribute name|Format|Description
-|-|-
args|You shouldn’t need to format this yourself.|The tuple of arguments merged into msg to produce message, or a dict whose values are used for the merge (when there is only one argument, and it is a dictionary).
asctime|%(asctime)s|Human-readable time when the LogRecord was created. By default this is of the form ‘2003-07-08 16:49:45,896’ (the numbers after the comma are millisecond portion of the time).
created|%(created)f|Time when the LogRecord was created (as returned by time.time()).
exc_info|You shouldn’t need to format this yourself.|Exception tuple (à la sys.exc_info) or, if no exception has occurred, None.
filename|%(filename)s|Filename portion of pathname.
funcName|%(funcName)s|Name of function containing the logging call.
levelname|%(levelname)s|Text logging level for the message ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
levelno|%(levelno)s|Numeric logging level for the message (DEBUG, INFO, WARNING, ERROR, CRITICAL).
lineno|%(lineno)d|Source line number where the logging call was issued (if available).
message|%(message)s|The logged message, computed as msg % args. This is set when Formatter.format() is invoked.
module|%(module)s|Module (name portion of filename).
msecs|%(msecs)d|Millisecond portion of the time when the LogRecord was created.
msg|You shouldn’t need to format this yourself.|The format string passed in the original logging call. Merged with args to produce message, or an arbitrary object (see Using arbitrary objects as messages).
name|%(name)s|Name of the logger used to log the call.
pathname|%(pathname)s|Full pathname of the source file where the logging call was issued (if available).
process|%(process)d|Process ID (if available).
processName|%(processName)s|Process name (if available).
relativeCreated|%(relativeCreated)d|Time in milliseconds when the LogRecord was created, relative to the time the logging module was loaded.
stack_info|You shouldn’t need to format this yourself.|Stack frame information (where available) from the bottom of the stack in the current thread, up to and including the stack frame of the logging call which resulted in the creation of this record.
thread|%(thread)d|Thread ID (if available).
threadName|%(threadName)s|Thread name (if available).