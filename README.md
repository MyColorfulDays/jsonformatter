# jsonformatter
[![Downloads](https://static.pepy.tech/personalized-badge/jsonformatter?period=week&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads/Weekly)](https://pepy.tech/project/jsonformatter)



**jsonformatter** is a formatter for python logger output json log, e.g., output **LogStash**/**FileBeat** needed log.

You can easily **custom (add/replace)** `LogRecord` attribute (the keys of `extra` are `LogRecord` attribute too). 

If you are working with RESTful web service and using `Flask`, `Django`, `Tornado` or another web framework, through `context` implicitly pass custom attribute, e.g. `user_id`, `request_id` or`url` to `LogRecord` is very useful for tracing back issue (especially in distributed services) or tracking, statistics, analyzing network traffic.

Starting with 0.2.X version, **Python 2.7** and **python 3** are both supported,  if you are using a version lower than 0.2.X,  only **python 3** is supported.

If you like this package, welcome to star⭐ it :-)

[toc]

## Do you want join and help me

I want most famous packages are out of the box with jsonformatter, e.g. `JsonFormat.framework_or_package_name.wrapper(app_or_package)`, the `app` can be framework application instance or python package. 

The work is a little difficult and heavy and the next version `0.4.X` is delay too long. So, if you want work with me or have any suggestion, e.g. add wrapper as plugin in same namespace, welcome to new issue or contact me with email.

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

test_basic_config.py

```python
import logging

from jsonformatter import basicConfig

# default keyword parameter `format`: """{"levelname": "levelname", "name": "name", "message": "message"}"""
basicConfig(level=logging.INFO)
# `logging.info` is a shortcut to use root logger
logging.info('hello, jsonformatter')

```

output:

```shell
{"levelname": "INFO", "name": "root", "message": "hello, jsonformatter"}
```



### Case 2. Complete config in python code

test_code_config.py

```python
import logging

from jsonformatter import JsonFormatter

# The `format` can be `json`, `OrderedDict`, `dict`.
# If `format` is `dict` and python version < 3.7.0, the output order is sorted keys, otherwise consistent with defined order.
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

root.info("hello, %s", 'jsonformatter')

```

output:

```shell
{"Name": "root", "Levelno": 20, "Levelname": "INFO", "Pathname": "test_code_config.py", "Filename": "test_code_config.py", "Module": "test_code_config", "Lineno": 36, "FuncName": "<module>", "Created": 1607753179.1741621, "Asctime": "2020-12-12 14:06:19,174", "Msecs": 174.1621494293213, "RelativeCreated": 38.06352615356445, "Thread": 16312, "ThreadName": "MainThread", "Process": 15464, "Message": "hello, jsonformatter"}
```



### Case 3. Custom(add/replace) `LogRecord` attribute

test_custom_attribute.py

```python
import datetime
import logging

from jsonformatter import JsonFormatter

# The key will add/replace `LogRecord` attribute (the keys of `extra` are `LogRecord` attribute too).
# The value must be `callable` type and only supports no argument or arbitrary keyword arguments.
# The `callable` type returned value will be as the `LogRecord` attribute value.
# If the returned object is not JSON serializable, see "How to solve `Object of type '*' is not JSON serializable`".
RECORD_CUSTOM_ATTRS = {
    # Replace attribute `asctime`, the value is a lambda without argument
    'asctime': lambda: datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
    # Add attribute `status`, the value is a lambda with arbitrary keyword arguments.
    'status': lambda **record_attrs: 'failed' if record_attrs['levelname'] in ['ERROR', 'CRITICAL'] else 'success',

}

# The custom attribute `app` not in `RECORD_CUSTOM_ATTRS`, it will stay the same.
STRING_FORMAT = '''{
    "App":             "app",
    "Asctime":         "asctime",
    "Status":          "status",
    "Message":         "message"
}'''


formatter = JsonFormatter(
    STRING_FORMAT,
    record_custom_attrs=RECORD_CUSTOM_ATTRS
)
sh = logging.StreamHandler()
sh.setFormatter(formatter)
sh.setLevel(logging.INFO)
root = logging.getLogger()
root.setLevel(logging.INFO)
root.addHandler(sh)

root.info("hello, custom %s", 'jsonformatter')

```

```shell
{"App": "app", "Asctime": "2020-12-12 14:09:56.237", "Status": "success", "Message": "hello, custom jsonformatter"}
```



### Case 4. Using `logging.config.fileConfig` or  `jsonformatter.fileConfig`

Because the `logging.config.fileConfig` only support three formatter keyword arguments `class`, `datefmt`, `format`,  if you want use the other keyword arguments, you should use `jsonformatter.fileConfig` and pass the other keyword arguments in python code.

logger_config.ini:
```shell
[loggers]
keys=root

[logger_root]
level=INFO
handlers=console_handler, file_handler

###############################################
[handlers]
keys=console_handler, file_handler

[handler_console_handler]
class=StreamHandler
level=INFO
formatter=form01
args=(sys.stdout,)

[handler_file_handler]
class=FileHandler
level=INFO
formatter=form01
args=('jsonformatter.log', 'a')

###############################################
[formatters]
keys=console_formatter, file_formatter

[formatter_console_formatter]
class=jsonformatter.JsonFormatter
# `app` and `status` are custom attribute, so the `record_custom_attrs` will be passed in python code.
format={"app": "app","name": "name","levelno": "levelno","levelname": "levelname","pathname": "pathname","filename": "filename","module": "module","lineno": "lineno","funcName": "funcName","created": "created","asctime": "asctime","msecs": "msecs","relativeCreated": "relativeCreated","thread": "thread","threadName": "threadName","process": "process","message": "message","status": "status"}

[formatter_file_formatter]
class=jsonformatter.JsonFormatter
# `app` and `status` are custom attribute, so the `record_custom_attrs` will be passed in python code.
format={"app": "app","name": "name","levelno": "levelno","levelname": "levelname","pathname": "pathname","filename": "filename","module": "module","lineno": "lineno","funcName": "funcName","created": "created","asctime": "asctime","msecs": "msecs","relativeCreated": "relativeCreated","thread": "thread","threadName": "threadName","process": "process","message": "message","status": "status"}
```
test_file_config.py
```python3
import logging
import os

from jsonformatter import fileConfig

# because of `logging.config.fileConfig` only support formatter three keyword arguments `class`, `datefmt`, `format` in config file, you should use `jsonformatter.fileConfig` and pass the optiontal keyword argument `defaults`.
fileConfig(
	os.path.join(os.path.dirname(__file__), 'logger_config.ini'),
	defaults={
		# `formatter_form01` will use these default keyword arguments, config file duplicate keyword arguments will overwrite defaults.
		'formatter_form01': {
			'record_custom_attrs': {
				'app': lambda: 'jsonformatter',
				'status': lambda **record_attrs: 'failed' if record_attrs['levelname'] in ['ERROR', 'CRITICAL'] else 'failed'
			}
		},
		# all `JsonFormatter` instances will use these default keyword arguments, 'formatter_form01' duplicate keyword arguments will overwrite these.
		'jsonformatter': {
			'datefmt':'%Y-%m-%d %H-%M-%S.%f',
			'record_custom_attrs': {
				'app': lambda: 'jsonformatter',
				'status': lambda **record_attrs: 'failed' if record_attrs['levelname'] in ['ERROR', 'CRITICAL'] else 'failed'
			}
		},
	})
root = logging.getLogger()
root.info("hello, %s", 'jsonformatter')

```

output:

```shell
{"name": "root", "levelno": 20, "levelname": "INFO", "pathname": "test_file_config.py", "filename": "test_file_config.py", "module": "test_file_config", "lineno": 33, "funcName": "<module>", "created": 1607753727.1819582, "asctime": "2020-12-12 14:15:27", "msecs": 181.95819854736328, "relativeCreated": 41.968584060668945, "thread": 1896, "threadName": "MainThread", "process": 8548, "message": "hello, jsonformatter", "status": "success"}
```



### Case 5. Using `logging.config.dictConfig` 

test_dict_config.py

```python
import logging
import logging.config

DICT_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console_jsonformatter': {
            '()': 'jsonformatter.JsonFormatter', # https://docs.python.org/3/library/logging.config.html#user-defined-objects
            'format': """{
                "Name": "name",
                "Levelno": "levelno",
                "Levelname": "levelname",
                "Pathname": "pathname",
                "Filename": "filename",
                "Module": "module",
                "Lineno": "lineno",
                "FuncName": "funcName",
                "Created": "created",
                "Asctime": "asctime",
                "Msecs": "msecs",
                "RelativeCreated": "relativeCreated",
                "Thread": "thread",
                "ThreadName": "threadName",
                "Process": "process",
                "Message": "message",
                "status": "status"
            }""",
            'record_custom_attrs': {
                'status': lambda **record_attrs: 'failed' if record_attrs['levelname'] in ['ERROR', 'CRITICAL'] else 'success'
            },
            'mix_extra': True
        },
    },
    'handlers': {
        'console_handler': {
            'level': 'INFO',
            'formatter': 'console_jsonformatter',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': { # root logger
            'handlers': ['console_handler'],
            'level': 'INFO',
            'propagate': False
        },
    }
}

logging.config.dictConfig(DICT_CONFIG)
logging.info("hello, %s", 'jsonformatter')

```

output:

```shell
{"Name": "root", "Levelno": 20, "Levelname": "INFO", "Pathname": "test_dict_config.py", "Filename": "test_dict_config.py", "Module": "test_dict_config", "Lineno": 73, "FuncName": "<module>", "Created": 1607754142.6466718, "Asctime": "2020-12-12 14:22:22,646", "Msecs": 646.6717720031738, "RelativeCreated": 40.04716873168945, "Thread": 10716, "ThreadName": "MainThread", "Process": 8060, "Message": "hello, jsonformatter", "status": "success"}
```



## More Usage

### Case 1. Mix `extra` to output

test_mix.py

```python
import logging

from jsonformatter import JsonFormatter

root = logging.getLogger()
root.setLevel(logging.INFO)

sh = logging.StreamHandler()
formatter = JsonFormatter(
    ensure_ascii=False,
    mix_extra=True,
    mix_extra_position='tail'  # optional: head, mix
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

test_multi_attrs_in_one.py

```python
import logging

from jsonformatter import JsonFormatter

MULTI_ATTRIBUTES_FORMAT = '''{
    "multi attributes in one key": "%(name)s - %(levelno)s - %(levelname)s - %(pathname)s - %(filename)s - %(module)s - %(lineno)d - %(funcName)s - %(created)f - %(asctime)s - %(msecs)d - %(relativeCreated)d - %(thread)d - %(threadName)s - %(process)d - %(message)s"
}'''

formatter = JsonFormatter(MULTI_ATTRIBUTES_FORMAT)
sh = logging.StreamHandler()
sh.setFormatter(formatter)
sh.setLevel(logging.INFO)
root = logging.getLogger()
root.setLevel(logging.INFO)
root.addHandler(sh)

root.info('test multi attributes in one key')

```

output:

```shell
{"multi attributes in one key": "root - 20 - INFO - test_multi_attrs_in_one.py - test_multi_attrs_in_one.py - test_multi_attrs_in_one - 18 - <module> - 1607755317.007021 - 2020-12-12 14:41:57,007 - 7 - 38 - 12160 - MainThread - 15956 - test multi attributes in one key"}
```



### Case 3. Support `json.dumps` all optional arguments

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

formatter = JsonFormatter(STRING_FORMAT, indent=4, ensure_ascii=False)
sh = logging.StreamHandler()
sh.setFormatter(formatter)
sh.setLevel(logging.INFO)
root = logging.getLogger()
root.setLevel(logging.INFO)
root.addHandler(sh)

root.info('test json optional paramter: 中文')

```

```shell
{
    "Name": "root",
    "Levelno": 20,
    "Levelname": "INFO",
    "Pathname": "test_json_opt_args.py",
    "Filename": "test_json_opt_args.py",
    "Module": "test_json_opt_args",
    "Lineno": 32,
    "FuncName": "<module>",
    "Created": 1607755409.3337555,
    "Asctime": "2020-12-12 14:43:29,333",
    "Msecs": 333.7554931640625,
    "RelativeCreated": 39.05749320983887,
    "Thread": 13140,
    "ThreadName": "MainThread",
    "Process": 12480,
    "Message": "test json optional paramter: 中文"
}
```



## Integrating with framework or package

### Case 1. `Flask`，auto log `request_id`, `user_id`

test_flask.py

```python
#!/usr/bin/env python3.7

import logging
import sys
import time
import traceback
from collections import OrderedDict
from functools import wraps
from uuid import uuid4


from jsonformatter import JsonFormatter
from flask import Flask, has_request_context, request, session, g, jsonify
from flask.logging import default_handler

app = Flask(__name__)

RECORD_CUSTOM_ATTRS = {
    # no argument
    'url': lambda: request.url if has_request_context() else None,
    'method': lambda: request.method if has_request_context() else None,
    'user_id': lambda: session['user_id'] if has_request_context() and ('user_id' in session) else None,
    'request_id': lambda: g.request_id if has_request_context() else None,
    # arbitrary keyword arguments
    'type': lambda **record_attrs: record_attrs.get('type', 'bussiness'),
    'duration': lambda **record_attrs: record_attrs.get('duration', None),
    'exc_type': lambda: str(sys.exc_info()[0]) if sys.exc_info()[0] else None,
}

RECORD_CUSTOM_FORMAT = OrderedDict([
    ("log_time", "asctime"),
    ("url", "url"),
    ("method", "method"),
    ("user_id", "user_id"),
    ("request_id", "request_id"),
    ("type", "type"),
    ("logger", "name"),
    ("level", "levelname"),
    ("exc_type", "exc_type"),
    ("file", "%(filename)s:%(lineno)s"),
    ("message", "message"),
    ("duration", "duration"),
])

formatter = JsonFormatter(
    RECORD_CUSTOM_FORMAT,
    record_custom_attrs=RECORD_CUSTOM_ATTRS
)
default_handler.setFormatter(formatter)
default_handler.setLevel(logging.INFO)
app.logger.setLevel(logging.INFO)


@app.before_request
def set_custom_attr():
    g.start_ts = time.time()
    g.request_id = str(uuid4())


@app.errorhandler(404)
def not_found(error):
    app.logger.error(
        'not found',
        extra={
            'type': 'notfound',
            'duration': (time.time() - g.start_ts)
        })
    return {
        'code': getattr(error, 'code', 404),
        'status': 'failed',
        'content': None,
        'msg': 'not found'
    }, 404


@app.errorhandler(Exception)
def error_500(error):
    app.logger.exception(
        getattr(error, 'msg', str(error)),
        extra={
            'type': 'exception',
            'duration': (time.time() - g.start_ts)
        })
    return {
        'code': getattr(error, 'code', 500),
        'status': 'failed',
        'content': None,
        'msg': getattr(error, 'msg', str(error))
    }, 500


@app.after_request
def summary(response):
    app.logger.info(
        response.data,
        extra={
            'type': 'reponse',
            'duration': (time.time() - g.start_ts)
        })
    return response


def success_restful(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return jsonify({
            'code': None,
            'status': 'success',
            'content': result,
            'msg': None
        })
    return wrapper


@app.route('/', methods=['GET', 'POST'])
@success_restful
def index():
    app.logger.info(request.values)
    app.logger.info('bussiness log')
    return {'hello': 'jsonformatter'}


@app.route('/error')
@success_restful
def error():
    raise Exception('uncaught exception')

if __name__ == '__main__':
    # remove develop server log
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.ERROR)
    app.run()

```

success output:

```shell
{"log_time": "2020-12-13 00:07:42,296", "url": "http://localhost:5000/", "method": "GET", "user_id": null, "request_id": "97016050-b6ae-4dcf-9130-595ef279628f", "type": "bussiness", "logger": "test_flask", "level": "INFO", "exc_type": null, "file": "test_flask.py:120", "message": "CombinedMultiDict([ImmutableMultiDict([]), ImmutableMultiDict([])])", "duration": null}
{"log_time": "2020-12-13 00:07:42,298", "url": "http://localhost:5000/", "method": "GET", "user_id": null, "request_id": "97016050-b6ae-4dcf-9130-595ef279628f", "type": "bussiness", "logger": "test_flask", "level": "INFO", "exc_type": null, "file": "test_flask.py:121", "message": "bussiness log", "duration": null}
{"log_time": "2020-12-13 00:07:42,299", "url": "http://localhost:5000/", "method": "GET", "user_id": null, "request_id": "97016050-b6ae-4dcf-9130-595ef279628f", "type": "reponse", "logger": "test_flask", "level": "INFO", "exc_type": null, "file": "test_flask.py:98", "message": "b'{\"code\":null,\"content\":{\"hello\":\"jsonformatter\"},\"msg\":null,\"status\":\"success\"}\\n'", "duration": 0.0039033889770507812}
```

not found output:

```shell
{"log_time": "2020-12-13 00:07:42,345", "url": "http://localhost:5000/favicon.ico", "method": "GET", "user_id": null, "request_id": "06480af7-9ee8-4ffe-8158-473cf3e2157f", "type": "notfound", "logger": "test_flask", "level": "ERROR", "exc_type": "<class 'werkzeug.exceptions.NotFound'>", "file": "test_flask.py:66", "message": "not found", "duration": 0.0}
{"log_time": "2020-12-13 00:07:42,346", "url": "http://localhost:5000/favicon.ico", "method": "GET", "user_id": null, "request_id": "06480af7-9ee8-4ffe-8158-473cf3e2157f", "type": "reponse", "logger": "test_flask", "level": "INFO", "exc_type": null, "file": "test_flask.py:98", "message": "b'{\"code\":404,\"content\":null,\"msg\":\"not found\",\"status\":\"failed\"}\\n'", "duration": 0.0009851455688476562}
```

failed output:

```shell
{"log_time": "2020-12-13 00:07:54,313", "url": "http://localhost:5000/error", "method": "GET", "user_id": null, "request_id": "e451ce9f-16dc-4003-b4c1-98e3336c7df6", "type": "exception", "logger": "test_flask", "level": "ERROR", "exc_type": "<class 'Exception'>", "file": "test_flask.py:82", "message": "uncaught exception\nTraceback (most recent call last):\n  File \"D:\\ProgramData\\Anaconda3\\envs\\py374\\lib\\site-packages\\flask\\app.py\", line 1950, in full_dispatch_request\n    rv = self.dispatch_request()\n  File \"D:\\ProgramData\\Anaconda3\\envs\\py374\\lib\\site-packages\\flask\\app.py\", line 1936, in dispatch_request\n    return self.view_functions[rule.endpoint](**req.view_args)\n  File \"test_flask.py\", line 107, in wrapper\n    result = func(*args, **kwargs)\n  File \"test_flask.py\", line 128, in error\n    raise Exception('uncaught exception')\nException: uncaught exception", "duration": 0.0009734630584716797}
{"log_time": "2020-12-13 00:07:54,318", "url": "http://localhost:5000/error", "method": "GET", "user_id": null, "request_id": "e451ce9f-16dc-4003-b4c1-98e3336c7df6", "type": "reponse", "logger": "test_flask", "level": "INFO", "exc_type": null, "file": "test_flask.py:98", "message": "b'{\"code\":500,\"content\":null,\"msg\":\"uncaught exception\",\"status\":\"failed\"}\\n'", "duration": 0.00585627555847168}
```





### Case 2. In `Django`

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



### Case 3. In `Tornado` 

```python
#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
File: app.py
Author: MyColorfulDays
Email: my_colorful_days@163.com
Github: https://github.com/MyColorfulDays
Description: Intergrating with tornado.
"""

import asyncio
import contextvars
import functools
import importlib
import json
import logging
import os
import time
import traceback
import uuid
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor

import tornado.ioloop
import tornado.web
from jsonformatter import JsonFormatter
from tornado.options import define, options, parse_command_line
from tornado.process import cpu_count


def when_finish(request_hander: tornado.web.RequestHandler) -> None:
    logging.info(
        getattr(request_hander, 'response'), extra={
            'type': 'response',
            'duration': request_hander.request.request_time()
        })

CURRENT_ENV_SETTINGS = {
    # 'environment': 'product',
    'environment': 'develop',
    'debug': False,
    'name': 'tornado_jsonformatter',
    'port': 8000,
    'log_function': when_finish,  # called when `RequestHandler.finish()` be executed
    'default_handler_class': None # 404 handler
}

formatter = JsonFormatter(
    OrderedDict([
        ("asctime", "asctime"),
        ("environment", CURRENT_ENV_SETTINGS['environment']),
        ("debug", str(CURRENT_ENV_SETTINGS['debug'])),
        ("service", CURRENT_ENV_SETTINGS['name']),
        ("url", "url"),
        ("method", "method"),
        ("uid", "uid"),
        ("logger", "name"),
        ("level", "levelname"),
        ("trace_id", "trace_id"),
        ("module", "%(module)s.py:%(lineno)s"),
        ("message", "message"),
    ]),
    record_custom_attrs={
        'trace_id': lambda: (REQUEST_CONTEXT.get()).get('trace_id', None),
        'url': lambda: (REQUEST_CONTEXT.get()).get('url', None),
        'method': lambda: (REQUEST_CONTEXT.get()).get('method', None),
        'uid': lambda: (REQUEST_CONTEXT.get()).get('uid', None),
    },
    mix_extra=True
)
sh = logging.StreamHandler()
sh.setFormatter(formatter)
sh.setLevel(logging.INFO)
root = logging.getLogger()
root.setLevel(logging.INFO)
root.addHandler(sh)

REQUEST_CONTEXT = contextvars.ContextVar(
    'request_context',
    default={
        'url': None,
        'uid': None,
        'trace_id': None
    }
)


class Application(tornado.web.Application):

    def __init__(self, *args, **settings):
        tornado.web.Application.__init__(self, *args, **settings)
        self.executor = ThreadPoolExecutor(max_workers=(cpu_count() * 5))
        self.request_context = REQUEST_CONTEXT


class BaseHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.executor = self.application.executor
        self.request_context = self.application.request_context
        self.response = None

    async def prepare(self):
        context = self.request_context.get()
        context['url'] = self.request.path
        context['method'] = self.request.method
        context['uid'] = self.current_user
        context['trace_id'] = str(uuid.uuid4())

    async def run_in_executor(self, function, *args, **kwargs):
        f = functools.partial(function, *args, **kwargs)
        ctx = contextvars.copy_context()
        return await tornado.ioloop.IOLoop.current().run_in_executor(
            self.executor,
            ctx.run,
            f
        )

    def restful(self, res):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.response = json.dumps(res, ensure_ascii=False)
        # `self.finish` will call `log_function`
        self.write(self.response)

    def success(self, content):
        self.restful({
            'code': None,
            'status': 'success',
            'content': content,
            'msg': None
        })

    def failed(self, msg=None, code=-1):
        self.restful({
            'code': code,
            'status': 'failed',
            'content': None,
            'msg': msg
        })

    def log_exception(self, typ, value, tb):
        """before `write_error`, log exception.

        Args:
            typ (TYPE): Description
            value (TYPE): Description
            tb (TYPE): Description
        """
        logging.exception('', extra={
            'type': 'exception'
        })

    def write_error(self, status_code, **kwargs):
        """process uncaught exception.
        """
        error_msg = ''.join(traceback.format_exception(*kwargs['exc_info']))
        # logging.error('traceback parameters: %s' % self.request.arguments)
        self.failed(error_msg, status_code)

    def on_finish(self):
        pass


class IndexHandler(BaseHandler):

    async def get(self):
        logging.info('bussiness log')
        self.success({'hello': 'jsonformatter'})


class LoginHandler(BaseHandler):

    async def get(self):
        username = self.get_query_argument('username', None)
        password = self.get_query_argument('password', None)
        logging.info(self.request.arguments)  # bussiness log
        logging.info(self.request.body)  # bussiness log
        if not (username and password):
            self.failed(1, 'username and password must not null')
            return  # if not return, the blow codes will be executed.
        self.success({'hello': 'jsonformatter'})


class NotFoundhandler(BaseHandler):

    async def get(self):
        self.failed(404, 404)


def thread_job(seconds, **kwargs):
    logging.info(kwargs)
    logging.info(seconds)
    logging.info('bussiness log')
    time.sleep(seconds)


class JobHandler(BaseHandler):

    async def get(self):
        job_num = self.get_argument('job_num', default=1)
        logging.info(job_num)
        await self.run_in_executor(thread_job, 5, kwargs1=1, kwargs2=2)
        self.success({'hello': 'jsonformatter'})

CURRENT_ENV_SETTINGS['default_handler_class'] = NotFoundhandler


def main():
    define('port', default=8000, help="run on the given port", type=int)
    parse_command_line()

    app = Application([
        (r"/", IndexHandler),
        (r"/login", LoginHandler),
        (r"/error", NotFoundhandler),
        (r"/job", JobHandler),
    ], **CURRENT_ENV_SETTINGS
    )
    port = getattr(options, 'port', None) or CURRENT_ENV_SETTINGS.get('port', 8000)
    app.listen(port)

    logging.info("Service starts on port: %s" % port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()

```



### Case4. In `Celery`

TODO

### Case5. In `requests`
TODO



### CaseN. Join me for more package



## FAQ
### How to solve `Object of type '*' is not JSON serializable`

1. using `LogRecord` attribute `Format`: `%(attribute)s/d/f`.

```python
import datetime
import json
import logging
import random
from collections import OrderedDict

from jsonformatter import JsonFormatter

RECORD_CUSTOM_ATTRS = {
    'now': lambda: datetime.datetime.today() #  Object of type 'datetime' is not JSON serializable
}
RECORD_CUSTOM_FORMAT = OrderedDict([
    ("Now",     "%(now)s"), #  using format solve raise exception: Object of type 'datetime' is not JSON serializable.
    ("Message", "message")
])
formatter = JsonFormatter(RECORD_CUSTOM_FORMAT, record_custom_attrs=RECORD_CUSTOM_ATTRS)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(formatter)
root = logger.getLogger()
root.addHandler(sh)
root.info("Solving 'datetime' is not JSON serializable`")
```

2. using `json.dumps` optional keyword argument `cls`

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
    'now': lambda: datetime.datetime.today()
}

RECORD_CUSTOM_FORMAT = OrderedDict([
    ("Now",     "now"),
    ("Message", "message")
])


class CLS_SOLUTION(json.JSONEncoder): #  using `json.dumps` optional argument `cls`
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)

formatter = JsonFormatter(
    RECORD_CUSTOM_FORMAT,
    record_custom_attrs=RECORD_CUSTOM_ATTRS,
    cls=CLS_SOLUTION
)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(formatter)
root = logger.getLogger()
root.addHandler(sh)
root.info("Solving 'datetime' is not JSON serializable`")
```

3. using `json.dumps` optional keyword argument `default`

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
    'now': lambda: datetime.datetime.today()
}

RECORD_CUSTOM_FORMAT = OrderedDict([
    ("Now",     "now"),
    ("Message", "message")
])

# using `json.dumps` optional argument `default`
def DEFAULT_SOLUTION(o):
    if not isinstance(o, (str, int, float, bool, type(None))):
        return str(o)
    else:
        return o

formatter = JsonFormatter(
    RECORD_CUSTOM_FORMAT,
    record_custom_attrs=RECORD_CUSTOM_ATTRS,
    default=DEFAULT_SOLUTION
)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(formatter)
root = logger.getLogger()
root.addHandler(sh)
root.info("Solving 'datetime' is not JSON serializable`")
```

### Why nested type  `dict`, `list`, `tuple`  be converted to string

https://github.com/MyColorfulDays/jsonformatter/issues/8#issuecomment-756900220

### How to output nested type `dict`, `list`, `tuple` without quote

https://github.com/MyColorfulDays/jsonformatter/issues/8#issuecomment-757339770

```python
import logging
from collections import OrderedDict

from jsonformatter import JsonFormatter


RECORD_CUSTOM_FORMAT = OrderedDict([
    ("Message", "msg")
])


formatter = JsonFormatter(
    RECORD_CUSTOM_FORMAT
)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(formatter)
root = logger.getLogger()
root.addHandler(sh)
root.info({'hello': 'world'})

```

### Why log output multiple times

https://github.com/MyColorfulDays/jsonformatter/issues/9#issuecomment-812815004



### How to define custom attribute in config file

https://github.com/MyColorfulDays/jsonformatter/issues/5#issuecomment-829355938




## LogRecord Attributes 

Offical url: https://docs.python.org/3/library/logging.html#logrecord-attributes

Attribute name  | Format                                      | Description
-               | -                                           | -
args            | You shouldn’t need to format this yourself. | The tuple of arguments merged into msg to produce message, or a dict whose values are used for the merge (when there is only one argument, and it is a dictionary).
asctime         | %(asctime)s                                 | Human-readable time when the LogRecord was created. By default this is of the form ‘2003-07-08 16:49:45,896’ (the numbers after the comma are millisecond portion of the time).
created         | %(created)f                                 | Time when the LogRecord was created (as returned by time.time()).
exc_info        | You shouldn’t need to format this yourself. | Exception tuple (à la sys.exc_info) or, if no exception has occurred, None.
filename        | %(filename)s                                | Filename portion of pathname.
funcName        | %(funcName)s                                | Name of function containing the logging call.
levelname       | %(levelname)s                               | Text logging level for the message ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
levelno         | %(levelno)s                                 | Numeric logging level for the message (DEBUG, INFO, WARNING, ERROR, CRITICAL).
lineno          | %(lineno)d                                  | Source line number where the logging call was issued (if available).
message         | %(message)s                                 | The logged message, computed as msg % args. This is set when Formatter.format() is invoked.
module          | %(module)s                                  | Module (name portion of filename).
msecs           | %(msecs)d                                   | Millisecond portion of the time when the LogRecord was created.
msg             | You shouldn’t need to format this yourself. | The format string passed in the original logging call. Merged with args to produce message, or an arbitrary object (see Using arbitrary objects as messages).
name            | %(name)s                                    | Name of the logger used to log the call.
pathname        | %(pathname)s                                | Full pathname of the source file where the logging call was issued (if available).
process         | %(process)d                                 | Process ID (if available).
processName     | %(processName)s                             | Process name (if available).
relativeCreated | %(relativeCreated)d                         | Time in milliseconds when the LogRecord was created, relative to the time the logging module was loaded.
stack_info      | You shouldn’t need to format this yourself. | Stack frame information (where available) from the bottom of the stack in the current thread, up to and including the stack frame of the logging call which resulted in the creation of this record.
thread          | %(thread)d                                  | Thread ID (if available).
threadName      | %(threadName)s                              | Thread name (if available).