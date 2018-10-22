__author__ = 'yetone'

import inspect
import argparse
from script_manager._compat import text_type, getargspec
from script_manager.utils import parse_docstring


class Command(object):
    def __init__(self, func, docstring=None):
        if docstring is None:
            docstring = parse_docstring(func.__doc__)
        self.docstring = docstring

        self.arg_parser = argparse.ArgumentParser(description=self.docstring and self.docstring.description)

        argspec = getargspec(func)
        args = argspec.args
        defaults = argspec.defaults

        if inspect.ismethod(func):
            args = args[1:]

        defaults = defaults or {}

        for arg in args + list(defaults.keys()):
            arg_kwargs = {}

            if self.docstring and arg in self.docstring.params:
                param = self.docstring.params[arg]
                if param.description:
                    arg_kwargs['help'] = param.description

            if arg not in defaults:
                self.add_argument(arg, type=text_type, **arg_kwargs)
                continue

            default = defaults[arg]

            arg_kwargs.update(dict(
                action='store',
                dest=arg,
                required=False,
                default=default
            ))

            if isinstance(default, bool):
                arg_kwargs['action'] = 'store_true'
            else:
                arg_kwargs['type'] = type(default)

            self.add_argument('-%s' % arg[0],
                              '--%s' % arg,
                              **arg_kwargs)

        self.func = func
        self.__doc__ = func.__doc__

    def add_argument(self, *args, **kwargs):
        self.arg_parser.add_argument(*args, **kwargs)

    def run(self, *args):
        _args = self.arg_parser.parse_args(args)
        self.func(**_args.__dict__)
