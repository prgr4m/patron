Model Generator
===============
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

This command gets translated to::

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


