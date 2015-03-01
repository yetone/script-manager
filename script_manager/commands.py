__author__ = 'yetone'

import inspect
import argparse
from ._compat import text_type, izip


class Command(object):
    def __init__(self, func):
        self.arg_parser = argparse.ArgumentParser()
        args, varargs, keywords, defaults = inspect.getargspec(func)
        if inspect.ismethod(func):
            args = args[1:]

        defaults = defaults or []

        kwargs = dict(izip(*[reversed(l) for l in (args, defaults)]))

        for arg in args:
            if arg in kwargs:
                default = kwargs[arg]
                if isinstance(default, bool):
                    self.add_argument('-%s' % arg[0],
                                      '--%s' % arg,
                                      action="store_true",
                                      dest=arg,
                                      required=False,
                                      default=default)
                else:
                    self.add_argument('-%s' % arg[0],
                                      '--%s' % arg,
                                      dest=arg,
                                      type=text_type,
                                      required=False,
                                      default=default)
            else:
                self.add_argument(arg, type=text_type)

        self.func = func
        self.__doc__ = func.__doc__

    def add_argument(self, *args, **kwargs):
        self.arg_parser.add_argument(*args, **kwargs)

    def run(self, *args):
        _args = self.arg_parser.parse_args(args)
        self.func(**_args.__dict__)
