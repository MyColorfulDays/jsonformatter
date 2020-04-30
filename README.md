Table of Contents
=================

* [jsonformatter \-\- for python log json](#jsonformatter----for-python-log-json)
  * [Installation](#installation)
  * [Basic Usage](#basic-usage)
    * [Case 1\. Use default config](#case-1-use-default-config)
    * [Case 2\. config in python code](#case-2-config-in-python-code)
    * [Case 3\. config from config file](#case-3-config-from-config-file)
  * [More Usage](#more-usage)
    * [Case 1\. output multiple attributes in one key](#case-1-output-multiple-attributes-in-one-key)
    * [Case 2\. support json\.dumps all optional parameters](#case-2-support-jsondumps-all-optional-parameters)
    * [Case 3\. support cumtom(add/replace) LogRecord  attribute](#case-3-support-cumtomaddreplace-logrecord--attribute)
  * [LogRecord Attributes](#logrecord-attributes)



# jsonformatter -- for python log json

**jsonformatter** is a formatter for python output json log,  you can easily output **LogStash** needed log format or other **custom** json format  and  you can easily **custom(add/replace)** `LogRecord` attribute.

**Python 2.7** and **python 3** are supported from version 0.2.X,  if you are using a version lower than 0.2.X,  **python 3** is only supported.



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

### Case 1. Use default config

```python
import logging

from jsonformatter import JsonFormatter

root = logging.getLogger()
root.setLevel(logging.INFO)

formatter = JsonFormatter()

sh = logging.StreamHandler()
sh.setFormatter(formatter)
sh.setLevel(logging.INFO)

root.addHandler(sh)

root.info("test %s config", 'default')
```

output:

```shell
{"levelname": "INFO", "name": "root", "message": "test default config"}
```



### Case 2. config in python code

```python3
import logging

from jsonformatter import JsonFormatter

# `format` can be json, OrderedDict, dict.
# If `format` is `dict` and python version<3.7.0, the output ordered is sorted keys, otherwise will same as define ordered.
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



### Case 3. config from config file

config file:
```shell
$ cat logger_config.ini
[loggers]
keys=root

[logger_root]
level=DEBUG
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



## More Usage

### Case 1. output multiple attributes in one key
```python3
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



### Case 2. support `json.dumps` all optional parameters

```python3
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



### Case 3. support cumtom(add/replace) `LogRecord`  attribute

```python3
import datetime
import json
import logging
import random
from collections import OrderedDict

from jsonformatter import JsonFormatter

# the key will add/replace `LogRecord` attribute.
# the value must be `callable` type and not support paramters, the returned value will be as the `LogRecord` attribute value.
RECORD_CUSTOM_ATTRS = {
    # `datetime.datetime` type is not JSON serializable.
    # solve it in three ways.
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