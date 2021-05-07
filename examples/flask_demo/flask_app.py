#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
File: jsonformatter.py
Author: MyColorfulDays
Email: my_colorful_days@163.com
Github: https://github.com/MyColorfulDays
Description: Integrating jsonformatter with flask project.
"""

import json
import logging
import time
from collections import OrderedDict
from functools import wraps
from uuid import uuid4

import traceback
from dataclasses import dataclass
from jsonformatter import JsonFormatter
from flask import Flask, has_request_context, request, session, jsonify, g
from flask.logging import default_handler
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, event

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

# the key will add/replace `LogRecord` attribute (the keys of `extra` are `LogRecord` attribute too).
# the value must be `callable` type and not support positional paramters, the returned value will be as the `LogRecord` attribute value.
RECORD_CUSTOM_ATTRS = {
    # lambda no argument, only get path as url.
    'url': lambda: request.url if has_request_context() else None,
    'username': lambda: session['username'] if has_request_context() and ('username' in session) else None,
    'request_id': lambda: getattr(g, 'request_id', None) if has_request_context() else None,
    # arbitrary keyword arguments
    # e.g., [response, sql, request, redis, ..., bussiness], the default is bussiness, rewrite by `extra`.
    'type': lambda **record_attrs: record_attrs.get('type', 'bussiness'),
    'traceback': traceback.format_exc(),
    'status': lambda **record_attrs: 'failed' if record_attrs['levelname'] in ['ERROR', 'CRITICAL'] else 'success',
    'duration': lambda **record_attrs: record_attrs.get('duration', None),
}

RECORD_CUSTOM_FORMAT = OrderedDict([
    ("asctime", "asctime"),
    ("url", "url"),
    ("status", "status"),
    ("username", "username"),
    ("request_id", "request_id"),
    ("type", "type"),
    ("loggername", "name"),
    ("levelname", "levelname"),
    ("filename", "%(filename)s:%(lineno)s"),
    ("traceback", "traceback"),
    ("duration", "duration"),
    ("message", "message"),
])

FORMATTER = JsonFormatter(
    RECORD_CUSTOM_FORMAT,
    record_custom_attrs=RECORD_CUSTOM_ATTRS,
    mix_extra=True,
    # indent=4,
    ensure_ascii=False
)
app.logger.setLevel(logging.INFO)
default_handler.setLevel(logging.INFO)
default_handler.setFormatter(FORMATTER)


@event.listens_for(db.engine, "before_cursor_execute")
def implicitly_pass_vairables(conn, cursor, statement, parameters, context, executemany):
    context.start_query_ts = time.time()


@event.listens_for(db.engine, 'after_cursor_execute')
def get_implicitly_passed_vairables(conn, cursor, statement, parameters, context, executemany):
    duration = (time.time() - context.start_query_ts)
    app.logger.info({
        'sql': statement,
        'parameters': parameters
    }, extra={
        'type': 'sql',
        'duration': duration
    })


@dataclass
class User(db.Model):
    id: int
    email: str

    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    email = db.Column(db.String(128), unique=True)


@app.before_request
def set_custom_attr():
    g.start_ts = time.time()
    g.request_id = str(uuid4())

@admin.errorhandler(404)
def error_404(error):
    response = dict(status=0, message="404 Not Found")
    return jsonify(response), 404
 

@app.errorhandler(Exception)
def error_500(error):
    app.logger.exception(error,{
            'type': 'reponse',
            'duration': (time.time() - g.start_ts)
        })
    return traceback.format_exc(), 500


@app.after_request
def summary(response):
    app.logger.info(
        response.response,
        extra={
            'type': 'reponse',
            'duration': (time.time() - g.start_ts)
        })
    return response

def decrator(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        return func(*args,**kwargs)
    return wrapper


@app.route('/')
def index():
    app.logger.info('bussiness log')
    raise Exception("GG")
    return jsonify({'hello': 'world'})

index=app.route('/')(index)

@app.route('/users')
def users():
    users = User.query.all()
    app.logger.info('bussiness log')
    return jsonify(users)


if __name__ == '__main__':
    users = [
        User(email="user1@gmail.com"),
        User(email="user2@gmail.com")
    ]
    db.create_all()
    db.session.add_all(users)
    db.session.commit()
    # remove develop server log
    logger = logging.getLogger('werkzeug')
    logger.setLevel(logging.ERROR)
    app.run(debug=True)
