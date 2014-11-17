Form Generator
==============
The form generator creates forms for use with WTForms. This generator just like 
all of the other generators follows the same pattern:

* attributes are separated by a `<colon>` ':'
* any default values to a type are separated by a `<hyphen>`  '-'
* multiple declarations are separated by a `<space>` ' '

To get help, run::

    patron form -h

The form generator has the following format::

    patron form [-b BLUEPRINT] [-v] name field [field ...]

where `name` and at least `one field` is required for generating a form.


Declaring fields for your wtforms
---------------------------------
The field type pattern is::

    name:field_type:label

Just like the model generator, the parser is forgiving in the sense that all is 
required at a minimum is just a name and a field type. The parser will just 
create a label from the name by capitalizing it. 

**Recognized WTForms Field types**:

+----------+-------------------+----------+---------------------+
| cli type | wtform field type | cli type | wtform field type   |
+==========+===================+==========+=====================+
| bool     | BooleanField      | date     | DateTimeField       |
+----------+-------------------+----------+---------------------+
| file     | FileField         | float    | FloatField          |
+----------+-------------------+----------+---------------------+
| integer  | IntegerField      | radio    | RadioField          |
+----------+-------------------+----------+---------------------+
| select   | SelectField       | multi    | SelectMultipleField |
+----------+-------------------+----------+---------------------+
| submit   | SubmitField       | string   | StringField         |
+----------+-------------------+----------+---------------------+
| hidden   | HiddenField       | pass     | PasswordField       |
+----------+-------------------+----------+---------------------+
| text     | TextAreaField     |          |                     |
+----------+-------------------+----------+---------------------+

Form generator examples
~~~~~~~~~~~~~~~~~~~~~~~

**Example #1** - Basic Usage::

    patron form Login name:string:Username password:pass confirm:pass

Rendered as::

    class Login(Form):
        name = StringField(u'Username')
        password = PasswordField(u'Password')
        confirm = PasswordField(u'Confirm')

Also, don't forget to make adjustments to your imports as the generator doesn't
touch the import statements.

Optional arguments
------------------
Similar to the model generator, the `-b` argument tells patron what 
blueprint to generate the form for. By default, it targets the `public` 
blueprint.

The other optional argument is the `-v` flag which tells the form generator to 
generate validation method stubs for each of your fields in your form.

Example::

    patron form SomeForm ... -v -b blueprint_or_pkg_name

Produces::
    
    class SomeForm(Form):
        ...

        def validate_name(form, field):
            pass
    
        ...

.. note::
   The form parser takes more arguments but it is much quicker to just 
   provide a **name:field_type:label** than to hack something through the cli. 
   I will make some additions in the next version. If you have any suggestions, 
   please open up an issue on bitbucket.
