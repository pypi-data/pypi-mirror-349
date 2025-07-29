#!/usr/bin/env python

# ...

from distutils.core import setup
from setuptools import setup, Extension

setup(name='greenlet-qpython',
      version='3.1.1',
      description='Greenlets are lightweight coroutines for in-process concurrent programming.',
      author='The greenlet Development Team',
      author_email='support@qpython.org',
      url='https://pypi.org/project/greenlet/',
      packages=['greenlet',],
      package_data={
        'greenlet':[
"__init__.py",
"_greenlet.cpython-312.so",
"platform/*",
"tests/*"
        ]
},
      long_description="""
Greenlets are lightweight coroutines for in-process concurrent programming.

The “greenlet” package is a spin-off of Stackless, a version of CPython that supports micro-threads called “tasklets”. Tasklets run pseudo-concurrently (typically in a single or a few OS-level threads) and are synchronized with data exchanges on “channels”.

A “greenlet”, on the other hand, is a still more primitive notion of micro-thread with no implicit scheduling; coroutines, in other words. This is useful when you want to control exactly when your code runs. You can build custom scheduled micro-threads on top of greenlet; however, it seems that greenlets are useful on their own as a way to make advanced control flow structures. For example, we can recreate generators; the difference with Python’s own generators is that our generators can call nested functions and the nested functions can yield values too. (Additionally, you don’t need a “yield” keyword. See the example in test_generator.py).

Greenlets are provided as a C extension module for the regular unmodified interpreter.

""",
      license="MIT License",
     )
