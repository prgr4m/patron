Introduction
============

Why?
----
I wanted tooling for flask that would make my life easier (and faster) like 
the generators for the padrino framework. There are tools out there 
that scaffold projects (and I've accommodated users of cookiecutter as of 
0.2.2) but this tool's focus is on rapid development rather than being a 
padrino clone. There isn't a 1:1 match between padrino and flask when it comes 
to composing an application nor should there be.

The other focus of this tool is *incremental* feature usage in projects. Flask 
isn't Django and you shouldn't have the kitchen sink rolled into the scaffold. 
You should only use what you need. Each feature will list what dependencies it 
may have, why, and where to tweak to suit your needs.

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
* user template customization
* cli model generator

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

Patron external dependencies are:

* nodejs
* ruby

Patron itself doesn't use Flask-Assets in the scaffolds that it uses. It uses 
a front-end work flow based off of gulp separated from the project package. 
For more details on the external dependencies you can read up on the 
:ref:`front-end` work flow.
