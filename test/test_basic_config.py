import logging

from jsonformatter import basicConfig

# default keyword parameter `format`: """{"levelname": "levelname", "name": "name", "message": "message"}"""
basicConfig(level=logging.INFO)
# `logging.info` is a shortcut to use root logger
logging.info('Hello, jsonformatter')
