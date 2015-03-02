__author__ = 'yetone'

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)))

from script_manager import Manager
from scripts import test_manager, test0_manager

manager = Manager(description='The example manager')

manager.add_command('test', test_manager)
manager.add_command('test0', test0_manager)

if __name__ == '__main__':
    manager.run()
