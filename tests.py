__author__ = 'yetone'

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(__file__))))  # noqa

import pytest
import unittest
from script_manager import Manager
from script_manager.compat import PY2


def run(command_line, manager_run):
    sys.argv = command_line.split()
    exit_code = None

    try:
        manager_run()
    except SystemExit as e:
        exit_code = e.code

    return exit_code


class Test(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, capsys):
        self.capsys = capsys

    def test_simple_command_decorator(self):
        manager = Manager()

        @manager.command
        def hello_world():
            print('hello world')

        self.assertIn('hello-world', manager._command_map)

        run('manage.py hello_world', manager.run)
        out, err = self.capsys.readouterr()
        self.assertIn('hello world', out)

        run('manage.py hello-world', manager.run)
        out, err = self.capsys.readouterr()
        self.assertIn('hello world', out)

    def test_nested_command(self):

        test_manager = Manager()
        test0_manager = Manager()
        main_manager = Manager()

        @test_manager.command
        def hello():
            print('test.hello')

        @test_manager.command
        def hi(a, b, c=False, name='yetone'):
            print('test.hi: <a: {}, b: {}, c: {}, name: {}>'.format(a, b, c, name))

        @test0_manager.command
        def say():
            print('test0.say')

        @test0_manager.command
        def sing(a, b, c=False, name='yetone'):
            print('test0.sing: <a: {}, b: {}, c: {}, name: {}>'.format(a, b, c, name))

        main_manager.add_command('test', test_manager)
        main_manager.add_command('test0', test0_manager)

        self.assertIn('hello', test_manager._command_map)
        self.assertIn('hi', test_manager._command_map)
        self.assertIn('say', test0_manager._command_map)
        self.assertIn('sing', test0_manager._command_map)

        run('manage.py test hello', main_manager.run)
        out, err = self.capsys.readouterr()
        self.assertIn('test.hello', out)

        run('manage.py test hellos', main_manager.run)
        out, err = self.capsys.readouterr()
        self.assertIn('usage', out)

        run('manage.py test -h', main_manager.run)
        out, err = self.capsys.readouterr()
        self.assertIn('usage', out)

        run('manage.py test hi', main_manager.run)
        out, err = self.capsys.readouterr()
        if PY2:
            self.assertIn('too few arguments', err)
        else:
            self.assertIn('the following arguments are required', err)

        run('manage.py test hi -h', main_manager.run)
        out, err = self.capsys.readouterr()
        self.assertIn('usage', out)

        run('manage.py test hi -n foo 1 2 -c', main_manager.run)
        out, err = self.capsys.readouterr()
        self.assertIn('test.hi: <a: 1, b: 2, c: True, name: foo>', out)

        run('manage.py test hi -n foo 1 2', main_manager.run)
        out, err = self.capsys.readouterr()
        self.assertIn('test.hi: <a: 1, b: 2, c: False, name: foo>', out)

        run('manage.py test0 say', main_manager.run)
        out, err = self.capsys.readouterr()
        self.assertIn('test0.say', out)

        run('manage.py test0 hello', main_manager.run)
        out, err = self.capsys.readouterr()
        self.assertIn('usage', out)

        run('manage.py test0 -h', main_manager.run)
        out, err = self.capsys.readouterr()
        self.assertIn('usage', out)

        run('manage.py test0 sing -h', main_manager.run)
        out, err = self.capsys.readouterr()
        self.assertIn('usage', out)

        run('manage.py test0 sing -n foo 1 2 -c', main_manager.run)
        out, err = self.capsys.readouterr()
        self.assertIn('test0.sing: <a: 1, b: 2, c: True, name: foo>', out)

        run('manage.py test0 sing -n foo 1 2', main_manager.run)
        out, err = self.capsys.readouterr()
        self.assertIn('test0.sing: <a: 1, b: 2, c: False, name: foo>', out)

    def test_description(self):
        description = 'Test my description'
        manager = Manager(description=description)

        @manager.command
        def hello():
            print('hello')

        run('manage.py', manager.run)
        out, err = self.capsys.readouterr()
        self.assertIn(description, out)

        run('manage.py -h', manager.run)
        out, err = self.capsys.readouterr()
        self.assertIn(description, out)

        @manager.command
        def wow(a, b, c=1):
            '''I'm wow

            :param a: I'm a
            :param b: I'm b
            :param c: I'm c
            '''
            print('wow')

        run('manage.py -h', manager.run)
        out, err = self.capsys.readouterr()
        self.assertIn("I'm wow", out)
        self.assertNotIn("I'm a", out)

        run('manage.py wow -h', manager.run)
        out, err = self.capsys.readouterr()
        self.assertIn("I'm wow", out)
        self.assertIn("I'm a", out)
        self.assertIn("I'm b", out)
        self.assertIn("I'm c", out)

    def test_conflict_flag(self):
        manager = Manager()

        @manager.command
        def hello(host='127.0.0.1', boy=1, bird=2):
            print('hello')

        run('manage.py hello -h', manager.run)
        out, err = self.capsys.readouterr()
        self.assertIn('-H HOST, --host HOST', out)
        self.assertIn('-b BOY, --boy BOY', out)
        self.assertIn('--bird BIRD', out)


if not PY2:
    from py3_tests import *  # noqa
