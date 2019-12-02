script-manager
==============


[![Build Status](https://scrutinizer-ci.com/g/yetone/script-manager/badges/build.png?b=master)](https://scrutinizer-ci.com/g/yetone/script-manager/build-status/master)
[![Code Coverage](https://scrutinizer-ci.com/g/yetone/script-manager/badges/coverage.png?b=master)](https://scrutinizer-ci.com/g/yetone/script-manager/?branch=master)
[![PyPI Package latest release](https://img.shields.io/pypi/v/script-manager.svg)](https://pypi.org/project/script-manager)
[![PyPI Wheel](https://img.shields.io/pypi/wheel/script-manager.svg)](https://pypi.org/project/script-manager)


An elegant command-line interface. Usage like Flask-Script but more powerful and universal.


# Install

```shell
pip install script-manager
```


# Examples

If you create a `test.py` file like this:

```python
from typing import Optional, List
from script_manager import Manager

manager = Manager('I am a command')


@manager.command
def run(host: str = '127.0.0.1', port: int = 8080, hehe: Optional[List[int]] = None):
    print('Running at http://{}:{}'.format(host, port))
    if hehe is not None:
        print(sum(hehe))


@manager.command
def test(name, age):
    """Just print my information

    :param name: This is my name
    :param age: This is my age
    """
    print('My name is {}, and I am {} years old.'.format(name, age))


if __name__ == '__main__':
    manager.run()
```

Then you can run command in shell:

```shell
➜ python test.py -h
usage: test.py [-h] run test

I am a command

positional arguments:
  run
  test        Just print my information

optional arguments:
  -h, --help  show this help message and exit

```

and:

```shell
➜ python test.py run -h
usage: test.py [-h] [-H HOST] [-p PORT] [--hehe HEHE]

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST
  -p PORT, --port PORT
  --hehe HEHE

```

and:

```shell
➜ python test.py test -h
usage: test.py [-h] name age

Just print my information

positional arguments:
  name        This is my name
  age         This is my age

optional arguments:
  -h, --help  show this help message and exit

```

and:

```shell
➜ python test.py run -H 0.0.0.0 -p 8888
Running at http://0.0.0.0:8888

```

```shell
➜ python test.py run -H 0.0.0.0 -p 8888 --hehe 1 --hehe 2 --hehe 3
Running at http://0.0.0.0:8888
6

```

and:

```shell
➜ python test.py test yetone 12
My name is yetone, and I am 12 years old.

```
