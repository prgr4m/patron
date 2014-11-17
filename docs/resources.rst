.. _Resources:

Resources
=========
Resources from a Patron perspective/context are containers of functionality for 
a flask application. Patron has two types of resources: Blueprints and 
Packages.

Blueprints
----------
To create a blueprint, run the following command::

    patron blueprint name_of_blueprint

This creates a blueprint (within the project package), injects blueprint
registration with the app factory and creates a unittest file in the test
directory (under the project root).

The default comes with an index route handler, its own templates directory and 
a jade template for rendering.

To create a blueprint with additional routes along with methods and variables, 
the parser uses the following pattern::

    patron blueprint name [route [route ...]]

where you can define multiple routes after the name delimited by a `<space>`.

A route has the following pattern: 

    **method:route_name:variable-type**

The only thing that is mandatory when declaring additional routes is the method 
definition and route name.

**Example #1**: Defining methods on routes::

    patron blueprint about get:profile get-post:contact

This will produce the following code in ProjectName/about/views.py::

    ...

    @about.route('/profile')
    def profile():
        return render_template('profile.jade')

    @about.route('/contact', methods=['GET', 'POST'])
    def contact():
        return render_template('contact.jade')

When defining multiple methods they are separated by a `<hyphen>`.


**Example #2**: Defining variables and types::

    patron blueprint social get:comment:comment_id-int put:images:image-path

This will produce::

    ...

    @social.route('/comment/<int:comment_id>')
    def comment(comment_id):
        return render_template('comment.jade')

    @social.route('/images/<path:image>', methods=['PUT'])
    def images(image):
        return render_template('images.jade')

If you omit the type it will default to a string.

One thing to notice is that by *default*, when generating blueprints, they come 
with their own templates. If you plan on using the blueprint generator to 
quickly stub out a REST api, you can add `-n` in the end of the command which 
tells patron to not include templates.

**Example #3**: Turning off templates::

    patron blueprint ninja post:turtles:attack get:pizza -n

This will produce::

    ...

    @ninja.route('/turtles/<attack>', methods=['POST'])
    def turtles(attack):
        pass

    @ninja.route('/pizza')
    def pizza():
        pass

Of course you still get the index route and template for free.


Packages
--------
A package is exactly what it is: a python package within your flask 
application. Whenever you want to group functionality together but you don't 
necessarily require a view to be associated like a blueprint, you would 
generate a package.

To generate a package::

    patron pkg name_of_package

This command will generate the following::

    package_name
      | - __init__.py
      | - commands.py
      | - forms.py
      | - helpers.py
      \ - models.py

commands.py
  Commands to be used in conjunction with manage.py (flask-script)

forms.py
  Where your forms live within that package

helpers.py
  Arbitrary code, decorators, etc.  that you need to hook into your application

models.py
  Where your models live within the package/grouping.

