# -*- coding: utf-8 -*-
"""
Patron is a generator modeled after the Padrino framework's generators but for
the flask microframework.
"""
from __future__ import print_function
from setuptools import setup, find_packages

setup(
    name = "patron",
    version = "0.2.0",
    description = "Flask generators influenced by Padrino's generators",
    long_description = __doc__,
    author = "John Boisselle",
    author_email = "prgr4m@yahoo.com",
    url = "https://bitbucket.org/prgr4m/patron",
    license = "MIT",
    packages = find_packages(),
    package_data = {
        '': ['data/**/*.py', 'data/**/*.txt', 'data/**/*.jade',
             'data/**/*.xml', 'data/**/*.png', 'data/**/*.ico']
    },
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audince :: Flask Developers',
        'Topic :: Software Development :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
    keywords = "flask generators scaffolding",
    entry_points = {
        'console_scripts': [
            'patron=patron:main'
        ]
    }
)
