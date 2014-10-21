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
Install patron with `pip` command::

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
To view the help at any time run the command with `-h` or `--help`::

    patron -h

Also, each respective command group has their own help, so just run a command 
and tack on a `-h` or `--help`:

Example::

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
to build one. This is probably the most confusing part of the tooling for a 
first time user so here are a couple of examples. To get help, run::

    patron model -h

**Example #1 - Basic usage**::

    patron model public Person name:string-40:unique age:integer:default-21

The command targets the models.py file within the public blueprint.

The code that gets generated inside of models.py is this::

    class Person(db.Model):
        __tablename__ = 'person'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(40), unique=True)
        age = db.Column(db.Integer, default=21)

        def __str__(self):
            pass

        def __repr__(self):
            return "<Person: Customize me!>"

The main thing to notice is the model generator has the following pattern when 
declaring attributes to a model:

* attributes/fields to a model are separated by a space ' '
* traits of an attribute are delimited by a colon ':'
* any default values to a type are noted by a hyphen '-'

Here are the column attributes that are scanned for:

* index
* nullable
* unique
* default

**Example #2 - Using a foreign key**::

    patron model public Cat cat_id:integer:foreign-neko.id

The following code gets translated to::

    class Cat(db.Model):
        __tablename__ = 'cat'
        id = db.Column(db.Integer, primary_key=True)
        cat_id = db.Column(db.Integer, db.ForeignKey('neko.id'))

        def __str__(self):
            pass

        def __repr__(self):
            return "<Cat: Customize me!>"

When declaring a one-to-one relationship you can tack on `uselist` at the end 
of the column.

There are 2 types of attribute definitions:

* columns
* relations

When declaring an attribute to a model, the name is provided and then the type
separated by a colon. If the 2nd type passed in is a recognized sqlalchemy type 
(see cli help for types) then the attribute definition is a column type. If the
2nd type passed in using the keyword 'relation' then it tells the model 
generator that its a relationship declaration.

**Example #3 - Declaring simple relationships**::

    patron model public Post tags:relation:Tag:post:lazy-joined

The command get translated to::

    class Post(db.Model):
        __tablename__ = 'post'
        id = db.Column(db.Integer, primary_key=True)
        tags = db.relationship('Tag', backref='post', lazy='joined')

        def __str__(self):
            pass

        def __repr__(self):
            return "<Post: Customize me!>"

The lazy types are:

* select
* joined
* subquery
* dynamic

The pattern to recognize is:

    name:relation:Class:backref:lazy-type

**Example #4 - Declaring relationships**::

    patron model public Article tags:relation:Tag:secondary-tags_posts:backref-posts-dynamic

This commands is translated to::

    class Article(db.Model):
        __tablename__ = 'article'
        id = db.Column(db.Integer, primary_key=True)
        tags = db.relationship('Tag', secondary=tags_posts, backref=db.backref('posts', lazy='dynamic'))

        def __str__(self):
            pass

        def __repr__(self):
            return "<Article: Customize me!>"

The pattern to recognize for this type of relationship is:

    name:relation:Class:secondary-table_ref:backref-refname-lazytype

Of course you are going to have to setup the secondary/join table yourself.

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

Todo
====

* form generator similar to model generator
* addons (at a minimum matching padrino's set but adding on other patterns)
* argcompletion for cli (linux)
* python 3.x support
* create list of packages being used by each addon and why
* revise static site generator
* revise admin addon and move registration into public via injection

Change Log
==========
0.2.2

* conversion to cookiecutter for users to be able to override scaffolds
* changed patron project configuration implementation from ini to json format
* added option in cli to create user template directory
* fixed minor bugs in code being generated
* temporarily took out bower call for ckeditor until done with documentation

0.2.1

* published python package

0.2.0 and below

* model generators functionality
* blog addon functionality
* admin addon functionality
* static site generator functionality
* blueprint registration functionality
* initial project creation with scaffolding ripped out of stencil

----

Copyright (c) 2014, John Boisselle. MIT Licensed.
