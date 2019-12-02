__author__ = 'yetone'

import sys
import argparse
from script_manager.command import Command
from script_manager.utils import parse_docstring


class Manager(object):
    def __init__(self, description=None):
        self._command_map = {}
        self.docstring = parse_docstring(description)
        self.arg_parser = argparse.ArgumentParser(
            description=self.docstring and self.docstring.description
        )

    def add_command(self, command_name, cmd):
        command_name = command_name.replace('_', '-')
        self._command_map[command_name] = cmd
        self.arg_parser.add_argument(
            command_name,
            help=cmd.docstring and cmd.docstring.description
        )

    def command(self, func):
        cmd = Command(func)
        self.add_command(func.__name__, cmd)
        return func

    def run(self, *args, **kwargs):
        if not args:
            args = sys.argv[1:]

        args = list(args)
        if not args:
            self.arg_parser.print_help()
            return

        command_name = args.pop(0)
        command_name = command_name.replace('_', '-')
        cmd = self._command_map.get(command_name)

        if not cmd:
            self.arg_parser.print_help()
            return

        cmd.run(*args, **kwargs)
