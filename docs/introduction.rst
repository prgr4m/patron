Introduction
============

Why?
----
I wanted tooling for flask that would make my life easier (and faster) like 
the generators for the padrino framework. There are tools out there 
that scaffold projects (and I've accommodated users of cookiecutter as of 
0.2.2) but this tool's focus is on rapid development rather than being a 
padrino clone. 

The other focus of this tool is *incremental* feature usage in projects. Flask 
isn't Django and you shouldn't have the kitchen sink rolled into your project. 
You should only use what you need and that is the primary focus of this tool.

Features
--------

* project generation

  * follows the factory pattern when creating a flask application
  * uses blueprints and packages for containing site functionality
  * includes prefab scripts for deployment to be altered (wsgi, fcgi, passenger)
  * includes fabric stub file with a cli interface for simple stubbing tasks

* blueprints generation

  * define routes along with route params/variables from the cli
  * auto registration / code injection with flask app
  * creates template directory within the blueprint itself
  * creates unittest stubs for testing the blueprint/routes

* package generation for grouping application functionality
* incremental functionality to an existing patron project via addons
* user template customization via cookiecutter
* flask-sqlalchemy model generator
* wtforms generator
* api generator using ModelView rather than blueprint routes
* separation of frontend workflow from flask backend
* adaptive cli parser displaying only the necessary options available to the user

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

* nodejs (npm)
* ruby (sass)

Patron itself doesn't use Flask-Assets in the scaffolds that it uses. It uses 
a front-end work flow based off of gulp separated from the project package. 
For more details on the external dependencies you can read up on the 
:ref:`front-end` work flow.

Next up is :ref:`basic usage <Basic Usage>`
