.. _Blueprints:

Blueprints
==========
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

Example #1::

    patron blueprint about get:profile get-post:contact

This will produce::

    @about.route('/profile')
    def profile():
        return render_template('profile.jade')

    @about.route('/contact', methods=['GET', 'POST'])
    def contact():
        return render_template('contact.jade')
