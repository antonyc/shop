
__author__ = 'chapson'

from collections import namedtuple

generators = ('order_status_changed',)
import order_status_changed

api = namedtuple('Generators', generators)._make((order_status_changed.Generator(),))