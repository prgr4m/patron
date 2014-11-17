.. _Model Generator:

Model Generator
===============
The model generator creates models for use with Flask-SQLAlchemy. This is
definitely inspired by padrino's tooling. Since I couldn't find one, I decided 
to build one. To get help run the following command within a patron project::

    patron model -h

This will mainly produce::

    patron model [-b BLUEPRINT] [-r Relation] name field [field ...]

The minimum requirements for using the model generator is providing a name of 
model and declaring at least one field. If not providing a blueprint, the 
generator will target the 'models.py' file in the `public` blueprint.

Declaring fields on a model
---------------------------
Field declaration has the following pattern::

  name:sqlalchemy_type:column_attr-value

  name
    Name of the field/attribute of the model

  sqlalchemy_type
    The sqlalchemy type that is being used for that column

  column_attr
    Other column attributes that would be defined

**Listing of available types to the generator**

+----------+-----------------+----------+-----------------+
| cli type | sqlalchemy type | cli type | sqlalchemy type |
+==========+=================+==========+=================+
| integer  | db.Integer      | float    | db.Float        |
+----------+-----------------+----------+-----------------+
| string   | db.String       | numeric  | db.Numeric      |
+----------+-----------------+----------+-----------------+
| text     | db.Text         | bool     | db.Boolean      |
+----------+-----------------+----------+-----------------+
| date     | db.Date         | binary   | db.LargeBinary  |
+----------+-----------------+----------+-----------------+
| datetime | db.DateTime     | pickle   | db.PickleType   |
+----------+-----------------+----------+-----------------+
| time     | db.Time         | unicode  | db.Unicode      |
+----------+-----------------+----------+-----------------+
| enum     | db.Enum         | unitext  | db.UnicodeText  |
+----------+-----------------+----------+-----------------+

The model generator supports the following column attributes:

* unique
* index
* nullable
* default

When using any of the column attributes, it will default to 'True' when there 
isn't a value provided.

Field declaration examples
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Example #1** - Basic usage/supplying values to SQLAlchemy types::

    patron model Person name:string-40 age:integer gender:enum-M-F:default-M

The code that gets generated is::

    class Person(db.Model):
        __tablename__ = 'person'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(40))
        age = db.Column(db.Integer)
        gender = db.Column(db.Enum('M', 'F'), default='M')

        def __str__(self):
            pass

        def __repr__(self):
            return "<Person: Customize me!>"

The main thing to notice is the model generator has the following pattern when 
declaring attributes to a model:

* attributes/fields to a model are separated by a `<space>` ' '
* traits of an attribute are delimited by a `<colon>` ':'
* any default values to a type are noted by a `<hyphen>` '-'

.. note::
   If you do not provide a sqlalchemy type with a value, it does not provide a 
   default, nor provide `parenthesis` after the sqlalchemy type. 
   
   For example:
  
     name:string
   
   Will produce:
     
     name = db.Column(db.String)
   
   The tools job is to scaffold as much code as possible with the least amount 
   of effort so the programmer can tweak to their needs. Please keep in mind of
   this particular side effect as the tool can't anticipate everything.

**Example #2** - Using a foreign key column attribute::

    patron model Cat name:string-20:unique owner_id:integer:foreign-person.id

The following code gets translated to::

    class Cat(db.Model):
        __tablename__ = 'cat'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(20), unique=True)
        owner_id = db.Column(db.Integer, db.ForeignKey('person.id'))

        def __str__(self):
            pass

        def __repr__(self):
            return "<Cat: Customize me!>"

Declaring relationships on a model
----------------------------------
In order to offer the option to the user, I've split off declaring relations 
into its own option. This is an `optional` argument to the model generator.

The relations option when viewing the cli help expects the following pattern 
when describing a relationship::

    name:Class:backref:lazy-type

The relationship parser of the model generator is expecting 4 parts, each 
delimited by a `<colon>` ':'

The parser is a little bit more forgiving and tries to fill in the blanks 
if the user hasn't supplied all of the information. At the extreme minimum, the 
parser just needs the name of the relationship attribute and the name of the 
`Class` that the model has a relationship with... But it's best to be explicit 
rather than implicit, right?

When viewing the SQLAlchemy documentation, there are many ways to declare a
backref on the model and the lazy types. Lazy types are: **select, joined, 
subquery, dynamic**. The generator defaults to 'dynamic' when a value isn't 
supplied to the lazy type.

The parser has the following pattern combinations when declaring a relationship 
between models::

    name:Class
    name:Class:backref_name
    name:Class:lazy_type
    name:Class:backref_name:lazy_type
    name:Class:backref-reference_name-lazy_type:lazy_type
    name:Class:secondary-table_reference:backref-reference_name-lazy_type

I will explain the last pattern combination for defining many-to-many 
relationships within its own example after I explain how the backref pattern 
works.

When defining a backref you can supply just the name which will produce::

    backref='name_given'

or you can use the `backref` keyword and then supply the values to alter the 
definition::

    backref-posts-subquery

produces::

    backref=db.backref('posts', lazy='subquery')

Unless being explicit with the backref definition, the generator is going to 
choose the `backref_name` approach to when declaring the relationship.

.. note::
   When a `backref_name` or `reference_name` isn't supplied, the generator will 
   default to using the Model name (lowercased) as the backref.


Relationship examples
~~~~~~~~~~~~~~~~~~~~~
Please note that the model generator `requires` at least one field definition 
but I am omitting that from the examples so you can just focus on how the 
relationships are being declared. The take away is knowing how the generator 
works, not the actual examples themselves.

**Example #1** - Using the backref name for declaring a relationship::

    patron model Post -r tags:Tag:post:joined

The command gets translated to::

    class Post(db.Model):
        ...
        tags = db.relationship('Tag', backref='post', lazy='joined')
        ...

**Example #2** - Declaring backref definition with values::

    patron model Post -r tags:Tag:backref-posts-dynamic:subquery

This will produce::

    class Post(db.Model):
        ...
        tags = db.relationship('Tag', backref=db.backref('posts', lazy='dynamic'), lazy='subquery')
        ...

**Example #3** - Declaring many-to-many relationships with `secondary`::

    patron model Post -r tags:Tag:secondary-tags_posts:backref-posts-dynamic

Produces::

    class Post(db.Model):
        ...
        tags = db.relationship('Tag', secondary=tags_posts, backref=db.backref('posts', lazy='dynamic'))
        ...

Just like how the `backref` is used as a keyword, `secondary` is also a keyword 
telling the generator that you are wanting the Model to look at the 
secondary/join table. Of course, you will have to write that yourself.

The model generator can take multiple relationships as well. To do so, just 
tack on another `-r` like so::

    patron model Post ... -r relation_def -r relation_def

By doing it this way, the parser doesn't mistake it for a field/column 
definition.

Next up is the :ref:`form generator<Form Generator>`.
