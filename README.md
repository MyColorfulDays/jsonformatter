# jsonformatter -- A formatter for python log json format

**jsonformatter** is a json formatter for python log handler, you can use it easily output LogStash needed format or other custom json format.

jsonformatter requires Python 3.X.



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

## Basic Usage
### Case 1. config in python code
```python3
import logging

from jsonformatter import JsonFormatter

# format can be json string, OrderedDict, dict.
# if format is dict and python version<3.7.0, the output order is same of sorted keys.
# the key needn't same as attribute name, can be whatever you like.
# the value can be `Attribute name` or `Format`(`Attribute name` will diplay `LogRecord.attribute`, `Format` will diplay `str(LogRecord.attribute)`).
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

### Case 2. config from config file
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
format={"Name": "name","Levelno": "levelno","Levelname": "levelname","Pathname": "pathname","Filename": "filename","Module": "module","Lineno": "lineno","FuncName": "funcName","Created": "created","Asctime": "asctime","Msecs": "msecs","RelativeCreated": "relativeCreated","Thread": "thread","ThreadName": "threadName","Process": "process","Message": "message"}
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

### Case 3. add/replace `LogRecord`'s attribute value
```python3
import datetime
import json
import logging
import random
from collections import OrderedDict

from jsonformatter import JsonFormatter

# the key will add/replace `LogRecord`'s attribute
# the value must be `callable` type and not support paramters, it returned value will as the value of LogRecord's attribute
RECORD_CUSTOM_ATTRS = {
    # datetime.datetime type is not JSON serializable.
    # solve it in three ways.
    # 1. use `Format` %(asctme)s.
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
    ("Asctime",         "%(asctime)s"),  # use `Format` to convert returned value to string.
    ("Msecs",           "msecs"),
    ("RelativeCreated", "relativeCreated"),
    ("Thread",          "thread"),
    ("ThreadName",      "threadName"),
    ("Process",         "process"),
    ("Message",         "message")
])


def DEFAULT_SOLUTION(o):
    if not isinstance(o,(str, int, float, bool, type(None))):
        return str(o)
    else:
        return o

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

