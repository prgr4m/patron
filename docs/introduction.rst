Introduction
============

The philosophy behind this cli generator is to provide functionality 
*incrementally* to a project by generating code from prefab scripts into an 
existing (generated) code base. While other scaffolds provide you with a solid
base for your flask projects, this tool is more focused on *speed* of 
development and common patterns generally found in web development so you can 
spend more time writing actual code to solve specific problems.

Installation
------------
Install patron with `pip` command::

    pip install patron

External Dependencies
---------------------
Patron does have some external dependencies outside of the python ecosystem in 
regards to front-end tooling. If you use flask-assets, you should be aware that
it makes external calls to the respective tooling if there isn't a python 
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

* incremental functionality to an existing patron project via addons which append dependencies to the requirements file
* user template customization (as of 0.2.2 via cookiecutter)
* cli model generator


