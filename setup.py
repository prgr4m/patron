# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from codecs import open
from os import path

current_dir = path.abspath(path.dirname(__file__))
with open(path.join(current_dir, 'description.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="patron",
    version="0.2.3",
    description="Flask generators influenced by Padrino's generators",
    long_description=long_description,
    author="John Boisselle",
    author_email="prgr4m@yahoo.com",
    url="https://bitbucket.org/prgr4m/patron",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Code Generators',
        'Environment :: Console',
        'Framework :: Flask',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Operating System :: OS Independent'
    ],
    install_requires=['cookiecutter>=0.7.1'],
    keywords="flask generators scaffolding cli",
    entry_points={
        'console_scripts': [
            'patron=patron.main:main'
        ]
    }
)
