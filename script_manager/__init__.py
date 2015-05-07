__author__ = 'yetone'

import sys
import argparse
from .commands import Command


class Manager(object):
    def __init__(self, description=None):
        self._command_map = {}
        self.arg_parser = argparse.ArgumentParser(description=description)

    def add_command(self, command_name, command):
        self._command_map[command_name] = command
        self.arg_parser.add_argument(command_name)

    def command(self, func):
        command = Command(func)
        self.add_command(func.__name__, command)
        return func

    def run(self, *args, **kwargs):
        if not args:
            args = sys.argv[1:]
        args = list(args)
        try:
            command_name = args.pop(0)
            command = self._command_map[command_name]
        except (IndexError, KeyError):
            self.arg_parser.print_help()
            return
        command.run(*args, **kwargs)
