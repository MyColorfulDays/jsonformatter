import datetime
import logging

from jsonformatter import JsonFormatter

# key: string
# value: object, `LogRecord` attribute name(the keys of `extra` are `LogRecord` attribute too) or other types.
# If the value is `callable` type, only support no positional arguments or arbitrary keyword arguments.
DICT_FORMAT = {
    "app":             "app",
    "version":         1.0,
    "asctime":         lambda: datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],  # no positional arguments, replace `LogRecord.asctime`
    "status":          lambda **record_attrs: 'failed' if record_attrs['levelname'] in ['ERROR', 'CRITICAL'] else 'success',  # arbitrary keyword arguments, the key `status` will be added to `LogRecord` as the attribute name 
    "message":         "message"
}


formatter = JsonFormatter(DICT_FORMAT)
sh = logging.StreamHandler()
sh.setFormatter(formatter)
sh.setLevel(logging.INFO)
root = logging.getLogger()
root.setLevel(logging.INFO)
root.addHandler(sh)

root.info("Hello, custom %s", 'jsonformatter')
