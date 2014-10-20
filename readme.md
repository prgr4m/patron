# Patron

## Overview
Patron is a generator for [Flask](http://flask.pocoo.org) modeled after 
[Padrino](http://padrinorb.com)'s generators particular to my workflow. I 
originally wrote Patron (prior name stencil) as an overall project management
tool (regardless of codebase) but have separated functionality into different
projects and have changed my workflow since then. A lot of scaffolds or best
practices lump both the frontend and backend together when they are 2 problems
to be solved separately.

This cli generator is solely focused on flask and does not include anything in
regards to front-end development. I use pyjade for templates since I use jade 
for templating with gulp and use a conversion script between the two. So what's
  so great about this then? Similar to padrino's generators,
Patron code is generated and injected for you with functionality pieced
together using only what you need incrementally. This tool's focus is for speed 
of development and not just as a base.

## Requirements
bower needs to be installed globally on your system. This is for ckeditor to be
used with blog addon in the admin interface... and just python 2.x.

## Usage
Patron help is pretty self explanatory... the only thing that might be confusing
is with the model generator when describing fields and relationships.

ex:
```
patron model public Person name:string-40:unique age:integer:default-21
```
'public' being the blueprint targeted models.py file

would be translated into:
```
...
name = db.Column(db.String(40), unique=True)
age = db.Column(db.Integer, default=21)
...
```

Another example:
```
cat_id:integer:foreign-nyaa.id
```
would be
```
cat_id = db.Column(db.Integer, db.ForeignKey('nyaa.id'))
```
Column attributes are: index, nullable, unique, default

so why not use parenthesis instead of a hyphen?

- less to type
- my terminal craps itself so I switched to a hyphen

when defining a relationship within a model its a little tricky. here's the 
following formats:

```
name:relation:Class:backref:lazytype-type
  ex: tags:relation:Tag:post:lazy-joined
      tags = db.relationship('Tag', backref='post', lazy='joined')
  ex: tags:relation:Tag:post:lazy-dynamic
      tags = db.relationship('Tag', backref='post', lazy='dynamic')
```
```
name:relation:Class:secondary-table_ref:backref-refname-lazytype
  ex: tags:relation:Tag:secondary-tags_posts:backref-posts-dynamic
      tags = db.relationship('Tag', secondary=tags_posts, backref=db.backref('posts', lazy='dynamic'))
```
Of course you're going to have to setup the secondary/join table yourself.

Lazy types are: select, joined, subquery, dynamic

For one-to-one relationships just tack on `uselist`

Model generation only generates what you tell it. Always make sure to actually
double check your models before running a migration.

All blueprints and models also generate their own unittest files and blueprints
auto register with the app factory.

blog addon autogenerates the admin addon.

## Todo

- form generator similar to model generator
- addons, addons, addons (just like padrino using flask-packages)
- argcompletion especially for model generation
- python 3.x support
- tutorial/documentation
- create list of packages being used for what purpose in documentation
- cli custom user directory setup
- revise static site generator
- revisit admin and move registration into public via injection

## Change Log

#### 0.2.2
- conversion to cookiecutter for users to be able to override scaffolds
- changed patron project configuration implementation from ini to json format
- ability to create a patron project json file with a project

#### 0.2.2
- converted scaffolds to cookiecutter so users can override

#### 0.2.1
- published python package

#### 0.2.0 and below
- model generators functionality
- blog addon functionality
- admin addon functionality
- static site generator functionality
- blueprint registration functionality
- initial project creation with scaffolding ripped out of stencil

## Thanks
@audreyr for making cookiecutter
@mitsuhiko for creating flask

## Copyright
Copyright (c) 2014 John Boisselle

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
of the Software, and to permit persons to whom the Software is furnished to do 
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.
