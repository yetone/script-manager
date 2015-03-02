__author__ = 'yetone'

from script_manager import Manager

test_manager = Manager(description='The test manager')

test0_manager = Manager(description='The test0 manager')


@test_manager.command
def hello(a, b, c=False, name='yetone'):
    print('test.hello: <a: {}, b: {}, c: {}> by {}'.format(a, b, c, name))


@test_manager.command
def hi(a, b, c=False, name='yetone'):
    print('test.hi: <a: {}, b: {}, c: {}> by {}'.format(a, b, c, name))


@test0_manager.command
def say(a, b, c=False, name='yetone'):
    print('test0.say: <a: {}, b: {}, c: {}> by {}'.format(a, b, c, name))


@test0_manager.command
def sing(a, b, c=False, name='yetone'):
    print('test0.sing: <a: {}, b: {}, c: {}> by {}'.format(a, b, c, name))
