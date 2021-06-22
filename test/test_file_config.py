import logging
import os

from jsonformatter import fileConfig

# because of `logging.config.fileConfig` only support formatter three keyword arguments `class`, `datefmt`, `format` in config file, you should use `jsonformatter.fileConfig` and pass the optiontal keyword argument `defaults`.
fileConfig(
    os.path.join(os.path.dirname(__file__), 'logger_config.ini'),
    defaults={
        # all `JsonFormatter` instances will use these default keyword arguments, 'formatter_file_formatter' duplicate keyword arguments will overwrite these.
        'jsonformatter_all_instances': {
            'datefmt':'%Y-%m-%d %H-%M-%S',
            'record_custom_attrs': {
                'app': lambda: 'jsonformatter',
                'status': lambda **record_attrs: 'failed' if record_attrs['levelname'] in ['ERROR', 'CRITICAL'] else 'success'
            },
            'indent': 4
        },
        # `formatter_file_formatter`
        'formatter_file_formatter': {
            'indent': None  #  duplicate keyword arguments, overwrite.
        }
    })
root = logging.getLogger()
root.info("Hello, %s", 'jsonformatter')
