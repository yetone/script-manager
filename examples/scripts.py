__author__ = 'yetone'

from script_manager import Manager

test_manager = Manager()

test0_manager = Manager()


@test_manager.command
def test(a, b, c=False, name='yetone'):
    print('test.test: <a: {}, b: {}, c: {}> by {}'.format(a, b, c, name))


@test_manager.command
def test0(a, b, c=False, name='yetone'):
    print('test.test0: <a: {}, b: {}, c: {}> by {}'.format(a, b, c, name))


@test0_manager.command
def test(a, b, c=False, name='yetone'):
    print('test0.test: <a: {}, b: {}, c: {}> by {}'.format(a, b, c, name))


@test0_manager.command
def test0(a, b, c=False, name='yetone'):
    print('test0.test0: <a: {}, b: {}, c: {}> by {}'.format(a, b, c, name))
