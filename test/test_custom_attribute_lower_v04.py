import datetime
import logging

from jsonformatter import JsonFormatter

# The key will add/replace `LogRecord` attribute (the keys of `extra` are `LogRecord` attribute too).
# The value must be `callable` type and only supports no argument or arbitrary keyword arguments.
# The `callable` type returned value will be as the `LogRecord` attribute value.
# If the returned object is not JSON serializable, see "How to solve `Object of type '*' is not JSON serializable`".
RECORD_CUSTOM_ATTRS = {
    "version": lambda: 1.0,
    # Replace attribute `asctime`, the value is a lambda without argument
    'asctime': lambda: datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
    # Add attribute `status`, the value is a lambda with arbitrary keyword arguments.
    'status': lambda **record_attrs: 'failed' if record_attrs['levelname'] in ['ERROR', 'CRITICAL'] else 'success',
}

# key: string
# value: string
# The custom attribute `app` not in `RECORD_CUSTOM_ATTRS`, it will stay the same.
STRING_FORMAT = '''{
    "app":             "app",
    "version":         "version",
    "asctime":         "asctime",
    "status":          "status",
    "message":         "message"
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

root.info("Hello, custom %s", 'jsonformatter')
