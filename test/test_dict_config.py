import logging
import logging.config

DICT_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console_jsonformatter': {
            '()': 'jsonformatter.JsonFormatter', # https://docs.python.org/3/library/logging.config.html#user-defined-objects
            'format': {
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
                "status": lambda **record_attrs: 'failed' if record_attrs['levelname'] in ['ERROR', 'CRITICAL'] else 'success'
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
