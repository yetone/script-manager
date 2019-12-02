__author__ = 'yetone'

import sys
import inspect
from collections import OrderedDict

PY2 = sys.version_info[0] == 2


if not PY2:
    text_type = str
    izip = zip

    def iteritems(dict):
        return iter(dict.items())
else:
    text_type = unicode
    from itertools import izip

    def iteritems(dict):
        return dict.iteritems()


def to_str(cls):
    if '__str__' in cls.__dict__:
        return cls  # pragma: no cover

    def __str__(self):
        return '{}({})'.format(  # pragma: no cover
            self.__class__.__name__,
            ', '.join(
                '{}={}'.format(k, repr(v))
                for k, v in iteritems(self.__dict__)
            )
        )
    cls.__str__ = __str__
    if '__repr__' not in cls.__dict__:
        cls.__repr__ = cls.__str__
    return cls


@to_str
class ArgSpec(object):
    def __init__(self, argspec):
        self.varargs = argspec.varargs
        if hasattr(argspec, 'varkw'):
            self.varkw = argspec.varkw  # pragma: no cover
            self.kwonlyargs = OrderedDict(  # pragma: no cover
                (k, argspec.kwonlydefaults.get(k))
                for k in argspec.kwonlyargs
            )
            self.annotations = argspec.annotations
        else:
            self.varkw = argspec.keywords  # pragma: no cover
            self.kwonlyargs = OrderedDict()  # pragma: no cover
            self.annotations = {}
        args = argspec.args
        defaults = argspec.defaults or []
        dl = len(defaults)
        if dl != 0:
            args = args[: -dl]  # pragma: no cover
            defaults = zip(argspec.args[-dl:], defaults)  # pragma: no cover
        self.args = args
        self.defaults = OrderedDict(defaults)


def getargspec(func):
    if hasattr(inspect, 'getfullargspec'):
        argspec = inspect.getfullargspec(func)  # pragma: no cover
    else:
        argspec = inspect.getargspec(func)  # pragma: no cover
    return ArgSpec(argspec)


def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""
    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        if hasattr(cls, '__qualname__'):
            orig_vars['__qualname__'] = cls.__qualname__
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper
