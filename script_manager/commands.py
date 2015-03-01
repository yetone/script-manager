__author__ = 'yetone'

import inspect
import argparse
from itertools import izip
from ._compat import text_type


class Option(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class Command(object):
    def __init__(self, func):
        args, varargs, keywords, defaults = inspect.getargspec(func)
        if inspect.ismethod(func):
            args = args[1:]

        defaults = defaults or []

        kwargs = dict(izip(*[reversed(l) for l in (args, defaults)]))

        option_list = []

        for arg in args:
            if arg in kwargs:
                default = kwargs[arg]
                if isinstance(default, bool):
                    option_list.append(Option('-%s' % arg[0],
                                              '--%s' % arg,
                                              action="store_true",
                                              dest=arg,
                                              required=False,
                                              default=default))
                else:
                    option_list.append(Option('-%s' % arg[0],
                                              '--%s' % arg,
                                              dest=arg,
                                              type=text_type,
                                              required=False,
                                              default=default))
            else:
                option_list.append(Option(arg, type=text_type))

        self.func = func
        self.__doc__ = func.__doc__
        self.option_list = option_list

    def run(self, *args):
        parser = argparse.ArgumentParser()
        for option in self.option_list:
            parser.add_argument(*option.args, **option.kwargs)
        _args = parser.parse_args(args)
        self.func(**_args.__dict__)
