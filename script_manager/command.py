__author__ = 'yetone'

import inspect
import argparse
from script_manager.compat import text_type, getargspec
from script_manager.compat.typing import Optional, Union, Tuple, List, _GenericAlias
from script_manager.utils import parse_docstring


ACTION = str
ACTION_STORE = 'store'  # type: ACTION
ACTION_APPEND = 'append'  # type: ACTION


def guess_type(t):
    # type: (Optional[Union[_GenericAlias, type]]) -> Tuple[type, ACTION, bool]
    if isinstance(t, type):
        if t in (list, tuple):
            return text_type, ACTION_APPEND, True
        return t, ACTION_STORE, True
    if not isinstance(t, _GenericAlias):
        return text_type, ACTION_STORE, False
    if t == Optional[List[int]]:
        return int, ACTION_APPEND, False
    if t == Optional[List[str]]:
        return text_type, ACTION_APPEND, False
    if t == List[int]:
        return int, ACTION_APPEND, True
    if t == List[str]:
        return text_type, ACTION_APPEND, True
    if t.__origin__ is list:
        return text_type, ACTION_APPEND, True
    return text_type, ACTION_STORE, False


class Command(object):
    def __init__(self, func, docstring=None):
        if docstring is None:
            docstring = parse_docstring(func.__doc__)
        self.docstring = docstring

        self.arg_parser = argparse.ArgumentParser(
            description=self.docstring and self.docstring.description
        )

        argspec = getargspec(func)
        args = argspec.args
        defaults = argspec.defaults

        if inspect.ismethod(func):
            args = args[1:]

        defaults = defaults or {}

        for arg in args + list(defaults.keys()):
            if arg == 'help':
                raise Exception("Your arg can't named as 'help'!")

            arg_kwargs = {}

            if self.docstring and arg in self.docstring.params:
                param = self.docstring.params[arg]
                if param.description:
                    arg_kwargs['help'] = param.description

            arg_type, arg_action, arg_required = guess_type(argspec.annotations.get(arg))

            if arg not in defaults:
                self.add_argument(arg, type=arg_type, **arg_kwargs)
                continue

            default = defaults[arg]

            arg_kwargs.update(dict(
                action=arg_action,
                dest=arg,
                required=arg_required,
                default=default
            ))

            if isinstance(default, bool):
                arg_kwargs['action'] = 'store_true'
            else:
                arg_kwargs['type'] = arg_type

            prefix_letter = arg[0]
            if prefix_letter == 'h':
                prefix_letter = 'H'

            brief_flag = '-%s' % prefix_letter
            flag = '--%s' % arg

            string_actions = self.get_string_actions()

            if brief_flag in string_actions:
                brief_flag = None

            arg_args = filter(None, (brief_flag, flag))

            self.add_argument(*arg_args, **arg_kwargs)

        self.func = func
        self.__doc__ = func.__doc__

    def add_argument(self, *args, **kwargs):
        self.arg_parser.add_argument(*args, **kwargs)

    def get_string_actions(self):
        return self.arg_parser._option_string_actions

    def run(self, *args):
        _args = self.arg_parser.parse_args(args)
        self.func(**_args.__dict__)
