from setuptools import setup, find_packages

version = '0.1.0'

setup(
    name='script-manager',
    version=version,
    keywords=('command-line interface', 'flask_script', 'argparse', 'script'),
    description='A command-line interface. Just a simple and crude implementation of Flask-Script.',
    url='http://github.com/yetone/script-manager',
    license='MIT License',
    author='yetone',
    author_email='i@yetone.net',
    packages=find_packages(),
    platforms='any',
    tests_require=(
        'pytest',
    )
)
