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
    """
    tornado应用程序
    """

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
