from setuptools import find_packages, setup

version = '0.3.0'

setup(
    name='script-manager',
    version=version,
    keywords=('command-line interface', 'flask_script', 'argparse', 'script'),
    description='An elegant command-line interface. Usage like Flask-Script but more powerful and universal.',
    url='https://github.com/yetone/script-manager',
    license='MIT License',
    author='yetone',
    author_email='yetoneful@gmail.com',
    packages=find_packages(),
    platforms=['any'],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    tests_require=(
        'pytest',
    )
)
