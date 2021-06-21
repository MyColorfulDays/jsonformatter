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
