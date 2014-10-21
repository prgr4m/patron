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
spend more time writing actual code to solve specific problems.

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

* incremental functionality to an existing patron project via addons which append dependencies to the requirements file
* user template customization (as of 0.2.2 via cookiecutter)
* cli model generator

Command Line Reference
======================
To view the help at any time run the command with `-h` or `--help`:

    patron -h

Also, each respective command group has their own help, so just run a command 
and tack on a `-h` or `--help`:

Example:

    patron addon -h

Projects
--------
Generate a project::

    patron project NameOfProject

Generate a project under a different directory name::

    patron project -d server NameOfProject

Generate a static website generator using flask::

    patron static NameOfProject

Generate a static website generator under a different directory name::

    patron static -d server NameOfProject

---------

**Note**:
  The rest of the commands below require you to be within the root of a patron 
  generated project.

---------

Blueprints
----------
To create a blueprint, run the following command::

    patron blueprint name_of_blueprint

This creates a blueprint (within the project package), injects blueprint
registration with the app factory and creates a unittest file in the test
directory (under the project root).

Task
----
To create a task (using fabric), run the following command::

    patron task name_of_task "description of task"

This will create a stub in the fabfile.py file in the project root directory.

Model Generator
---------------
The model generator creates models for use with Flask-SQLAlchemy. This is
definitely inspired by padrino's tooling. Since I couldn't find one, I decided 
to build it. This is probably the most confusing part of the tooling for a 
first time user so here are a couple of examples. To get help, run::

    patron model -h

**Example #1 - Basic usage**::

    patron model public Person name:string-40:unique age:integer:default-21

The command targets the models.py file within the public blueprint.

The code that gets generated is this::

    class Person(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(40), unique=True)
        age = db.Column(db.Integer, default=21)

        def __str__(self):
            pass

        def __repr__(self):
            return "<Person: Customize me!>"

**Example #2 - Using a foreign key**::

    patron model public Cat cat_id:integer:foreign-neko.id

The following code gets translated to::

    class Cat(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        cat_id = db.Column(db.Integer, db.ForeignKey('neko.id'))

        def __str__(self):
            pass

        def __repr__(self):
            return "<Cat: Customize me!>"


All models generated have a unittest file generated for them upon creation 
under the tests directory within the project root.

Add-ons
-------
Add-ons are pieces of functionality added to a project since patron has the use 
what you need mentality rather than throwing the kitchen sink at you. In order 
to get a list of add-ons used by patron run the following command::

    patron addon -h

Admin
^^^^^
Generated with the following command::

    patron addon admin

This admin add-on appends its dependencies to the requirements file, registers 
itself with the flask app and injects cli commands into manage.py. It comes 
with Flask-Login and Flask-Principal with preconfigured routes.

Blog
^^^^
Generated with the following command::

    patron addon blog

This command auto generates the admin addon if not already created, injects 
code into the sitemap to track blog posts and registers itself with the admin
addon.


