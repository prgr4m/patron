.. Patron documentation master file, created by
   sphinx-quickstart on Tue Oct 21 07:07:31 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Patron documentation
====================

**Patron** is a cli generator for `Flask`_ modeled after `Padrino's`_ 
generators but following flask conventions.

.. _Flask: http://flask.pocoo.org
.. _Padrino's: http://www.padrinorb.com/guides/generators

The philosophy behind this cli generator is to provide functionality 
*incrementally* to a project by generating code from prefab scripts into an 
existing (generated) code base. While other scaffolds provide you with a solid
base for your flask projects, this tool is more focused on *speed* of 
development and common patterns generally found in web development so you can 
spend more time writing actual code to solve specific problems. This project is
not meant to be a clone of padrino retrofitted to flask. Its a generator.

Installation
------------
Install patron with `pip` command:

    pip install patron

External Dependencies
---------------------
Patron does have some external dependencies outside of the python ecosystem in 
regards to front-end tooling. If you use flask-assets, you should be aware that
it makes external calls to its respective tooling if there isn't a python 
equivalent.

* nodejs/npm (gulp, bower, etc)
* ruby for sass since libsass chokes on newer features

Features
--------

* project generation

  * follows the factory pattern when creating a flask application
  * uses blueprints for containing site functionality
  * includes prefab scripts for deployment to be altered (wsgi, fcgi, passenger)
  * static website generator (for use without a database)
  * includes a sitemap
  * includes fabric stub file with a cli interface for simple stubbing tasks

* blueprint generation

  * auto registration / code injection with flask app
  * creates template directory within the blueprint itself
  * creates unittest stubs for testing the blueprint

* incremental functionality to an existing patron project via addons
* user template customization (as of 0.2.2 via cookiecutter)
* cli model generator

Command Line Reference
----------------------
To view the help at any time run the command with `-h` or `--help`:

    patron -h


