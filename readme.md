# Stencil - ステンシル - Sutenshiru

## Overview
Stencil is a generator for [Flask](http://flask.pocoo.org) modeled after 
[Padrino](http://padrinorb.com)'s generators particular to my workflow. I 
originally wrote Stencil as an overall project management tool (regardless of 
codebase) but have separated functionality into different projects and have
changed my workflow since then. A lot of scaffolds or best practices lump both
the frontend and backend together when they are 2 problems to be solved
separately.

This cli generator is solely focused on flask and does not include anything in
regards to front-end development. I use pyjade for templates since I use jade 
for templating with gulp and use a conversion script between the two (not
included). So what's so great about this then? Similar to padrino's generators,
stencil code is generated and injected for you with functionality pieced
together using only what you need. Have a project but don't need an admin?
Tired of handwriting your models completely from scratch?

## Requirements
bower needs to be installed globally on your system. This is for ckeditor to be
used with blog addon in the admin interface.

## Usage
Stencil help is pretty self explanatory... the only thing that might be confusing
is with the model generator when describing fields and relationships.

ex:
```
stencil model public Person name:string-40:unique age:integer:default-21
```
'public' being the blueprint targeted models.py file

would be translated into:
```
...
name = db.Column(db.String(40), unique=True)
age = db.Column(db.Integer, default=21)
...
```
so why not use parenthesis instead of a hyphen?

- less to type
- my terminal craps itself so I switched to a hyphen

when defining a relationship within a model its a little tricky. here's the 
following formats:

```
name:relationship:Class:backref
  ex: tags:relationship:Tag:post
      tags = db.relationship('Tag', backref='post', lazy='dynamic')
```
```
name:relationship:Class:backref:lazytype-type
  ex: tags:relationship:Tag:post:lazy-joined
      tags = db.relationship('Tag', backref='post', lazy='joined')
```
```
name:relationship:Class:secondary-table_ref:backref-refname-lazytype
  ex: tags:relationship:Tag:secondary-tags_posts:backref-posts-dynamic
      tags = db.relationship('Tag', secondary=tags_posts, backref=db.backref('posts', lazy='dynamic'))
```
Of course you're going to have to setup the secondary/join table yourself.

All blueprints and models also generate their own unittest files and blueprints
auto register with the app factory.

blog addon autogenerates the admin addon.

## Food for thought
Wouldn't it be cool if the respective flask extensions or even core had this 
functionality baked in? I know flask-sqlalchemy or whatever orm you use could 
use a little love in having a manage.py (either flask-script or click) hook to
do what I'm doing. They would definitely produce better looking code at that!

## Notice about this repo
I'm not accepting pull requests to change the templates used (pyjade) but will
be happy to have issues opened.

## Todo

- Form generator similar to model generator
- addons, addons, addons
- argcompletion especially for model generation
- unittests

## Copyright
Copyright (c) 2014 John Boisselle. MIT Licensed.

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
