Patron Changelog
================

0.2.3
-----

16 NOV 2014

* rewrite of project so it doesn't smell like java
* added python 3 support
* multi-page documentation format for easier organization and navigation
* rewrite of parser to show only relevant options when dealing with a project or not
* added check of minimal external dependencies
* removed '|' in cookiecutter filenames in case of users running Windows
* removal of static site generator as a project scaffold
* removal of blog addon
* added packages generation to flask projects
* added the ability to add extra routes to blueprints from cli
* added cli option to open official docs in browser
* ability to add extra routes to blueprint scaffolding along with option to exclude templates generated
* revised sqlalchemy model generator to have relations as an option along with fields without mixing the two
* added wtforms generator
* revised frontend addon workflow
* revised admin addon to have cleaner structure and moved users out into its own addon/blueprint
* added api parser for creating Resource/MethodView based api rather than just using function based routes

0.2.2
-----

21 OCT 2014

* conversion to cookiecutter for users to be able to override scaffolds
* changed patron project configuration implementation from ini to json format
* added option in cli to create user template directory
* fixed minor bugs in code being generated
* added front-end work flow to addons
* added public facing documentation

0.2.1
-----

01 OCT 2014

* published python package

0.2.0 and below
---------------

* model generators functionality
* blog addon functionality
* admin addon functionality
* static site generator functionality
* blueprint registration functionality
* initial project creation with scaffolding ripped out of stencil


