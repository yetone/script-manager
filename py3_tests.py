import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(__file__))))  # noqa

import unittest
from typing import Optional, List

import pytest

from script_manager import Manager


def run(command_line, manager_run):
    sys.argv = command_line.split()
    exit_code = None

    try:
        manager_run()
    except SystemExit as e:
        exit_code = e.code

    return exit_code


class Py3Test(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, capsys):
        self.capsys = capsys

    def test_annotation(self):
        manager = Manager()

        @manager.command
        def hello_world(initial: int, worlds: Optional[List[int]] = None):
            print(f'sum: {initial + sum(worlds or [])}!')
            if worlds is None:
                return
            print(','.join(map(str, reversed(worlds))))

        run('manage.py hello-world -h', manager.run)
        out, err = self.capsys.readouterr()
        self.assertIn('-w WORLDS, --worlds WORLDS', out)
        run('manage.py hello-world 233', manager.run)
        out, err = self.capsys.readouterr()
        self.assertIn('sum: 233!', out)
        run('manage.py hello-world 1 -w 1 -w 2 -w 3', manager.run)
        out, err = self.capsys.readouterr()
        self.assertIn('sum: 7!', out)
        self.assertIn('3,2,1', out)
