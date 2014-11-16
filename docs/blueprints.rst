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
the parser uses the following pattern:

    patron blueprint name 
