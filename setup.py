# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from codecs import open
from os import path

current_dir = path.abspath(path.dirname(__file__))
with open(path.join(current_dir, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="patron",
    version="0.2.0",
    description="Flask generators influenced by Padrino's generators",
    long_description=long_description,
    author="John Boisselle",
    author_email="prgr4m@yahoo.com",
    url="https://bitbucket.org/prgr4m/patron",
    license="MIT",
    packages=find_packages(),
    package_data={
        '': ['data/**/*.py', 'data/**/*.txt', 'data/**/*.jade',
             'data/**/*.xml', 'data/**/*.png', 'data/**/*.ico']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audince :: Flask Developers',
        'Topic :: Software Development :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
    keywords="flask generators scaffolding",
    entry_points={
        'console_scripts': [
            'patron=patron:main'
        ]
    }
)
