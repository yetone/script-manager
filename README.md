script-manager
==============


[![Build Status](https://scrutinizer-ci.com/g/yetone/script-manager/badges/build.png?b=master)](https://scrutinizer-ci.com/g/yetone/script-manager/build-status/master)


A command-line interface. Just a simple and crude implementation of Flask-Script.


# Examples

If you create a `test.py` file like this:

```python
from script_manager import Manager

manager = Manager('I am a command')


@manager.command
def run(host='127.0.0.1', port=8080, hehe=1):
    print('Running at http://{}:{}'.format(host, port))


@manager.command
def test(name, age):
    """Just print my information

    :param name: This is my name
    :param age: This is my age
    """
    print('My name is {}, and I have {} years old.'.format(name, age))


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

and:

```shell
➜ python test.py test yetone 12
My name is yetone, and I have 12 years old.

```