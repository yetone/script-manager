__author__ = 'yetone'

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(__file__))))

from script_manager import Manager
from script_manager._compat import PY2


def run(command_line, manager_run):
    sys.argv = command_line.split()
    exit_code = None

    try:
        manager_run()
    except SystemExit as e:
        exit_code = e.code

    return exit_code


def test_simple_command_decorator(capsys):
    manager = Manager()

    @manager.command
    def hello():
        print('hello')

    assert 'hello' in manager._command_map

    run('manage.py hello', manager.run)
    out, err = capsys.readouterr()
    assert 'hello' in out


def test_nested_command(capsys):

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

    assert 'hello' in test_manager._command_map
    assert 'hi' in test_manager._command_map
    assert 'say' in test0_manager._command_map
    assert 'sing' in test0_manager._command_map

    run('manage.py test hello', main_manager.run)
    out, err = capsys.readouterr()
    assert 'test.hello' in out

    run('manage.py test hellos', main_manager.run)
    out, err = capsys.readouterr()
    assert 'usage' in out

    run('manage.py test -h', main_manager.run)
    out, err = capsys.readouterr()
    assert 'usage' in out

    run('manage.py test hi', main_manager.run)
    out, err = capsys.readouterr()
    if PY2:
        assert 'too few arguments' in err
    else:
        assert 'the following arguments are required' in err

    run('manage.py test hi -h', main_manager.run)
    out, err = capsys.readouterr()
    assert 'usage' in out

    run('manage.py test hi -n foo 1 2 -c', main_manager.run)
    out, err = capsys.readouterr()
    assert 'test.hi: <a: 1, b: 2, c: True, name: foo>' in out

    run('manage.py test hi -n foo 1 2', main_manager.run)
    out, err = capsys.readouterr()
    assert 'test.hi: <a: 1, b: 2, c: False, name: foo>' in out

    run('manage.py test0 say', main_manager.run)
    out, err = capsys.readouterr()
    assert 'test0.say' in out

    run('manage.py test0 hello', main_manager.run)
    out, err = capsys.readouterr()
    assert 'usage' in out

    run('manage.py test0 -h', main_manager.run)
    out, err = capsys.readouterr()
    assert 'usage' in out

    run('manage.py test0 sing -h', main_manager.run)
    out, err = capsys.readouterr()
    assert 'usage' in out

    run('manage.py test0 sing -n foo 1 2 -c', main_manager.run)
    out, err = capsys.readouterr()
    assert 'test0.sing: <a: 1, b: 2, c: True, name: foo>' in out

    run('manage.py test0 sing -n foo 1 2', main_manager.run)
    out, err = capsys.readouterr()
    assert 'test0.sing: <a: 1, b: 2, c: False, name: foo>' in out


def test_description(capsys):
    description = 'Test my description'
    manager = Manager(description=description)

    @manager.command
    def hello():
        print('hello')

    run('manage.py', manager.run)
    out, err = capsys.readouterr()
    assert description in out

    run('manage.py -h', manager.run)
    out, err = capsys.readouterr()
    assert description in out
