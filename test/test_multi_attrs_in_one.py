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
