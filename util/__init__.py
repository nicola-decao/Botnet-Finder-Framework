
from time import time
from datetime import datetime


def __now():
    return datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S.%f')


def log(string):
    print(__now() + ' Log: ' + str(string))


def warning(string):
    print(__now() + ' Warning: ' + str(string))
