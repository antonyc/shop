
__author__ = 'chapson'

from collections import namedtuple

generators = ('time_to_return','order_status_changed',)
from . import order_status_changed
from . import time_to_return

api = namedtuple('Generators', generators)._make((
    _.Generator() for _ in (time_to_return, order_status_changed)))