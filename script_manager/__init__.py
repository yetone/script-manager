__author__ = 'yetone'

import sys
from .commands import Command


class Manager(object):
    def __init__(self):
        self._command_map = {}

    def add_command(self, command_name, command):
        self._command_map[command_name] = command

    def command(self, func):
        command = Command(func)
        self.add_command(func.__name__, command)
        return func

    def run(self, *args, **kwargs):
        if not args:
            args = sys.argv[1:]
        args = list(args)
        command_name = args.pop(0)
        command = self._command_map[command_name]
        command.run(*args, **kwargs)
