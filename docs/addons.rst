Add-ons
=======
Add-ons are pieces of functionality added to a project since patron has the use 
what you need mentality rather than throwing the kitchen sink at you. In order 
to get a list of add-ons used by patron run the following command::

    patron addon -h

The patron parser is adaptive in that it tracks what addons you have used via 
the 'patron.json' file in a project's root directory. Once an addon has been 
added to a project, it gets removed from the list. If all addons are used, the 
addon subparser won't be available.

Admin
-----
Generated with the following command::

    patron addon admin

The admin add-on uses Flask-Admin for the admin interface. When generated, it 
produces this folder structure::

    admin/
      |-- __init__.py
      |-- admin.py
      `-- views.py

As a convention, anything having to do with the admin addon will have an 
'admin.py' file within a blueprint/package. This way it doesn't pollute the 
'views.py' file as it contains setting up the admin and everything else that 
needs to hook into the admin by importing the other admin files from other 
blueprints. The 'admin.py' file within the admin package/blueprint contains an 
AdminMixin with a method that checks for roles within the application. 

Originally, anything dealing with users, logins and roles management was 
included with this add-on but as of 0.2.3, I've broken that out into its own 
add-on. This add-on automatically generates the `users` add-on. Also, you don't 
have to worry about hooking it up to your flask app because patron does that 
for you along with adding the dependencies to the requirements file.

.. note::
   Once this add-on has been added, patron immediately performs the following:

   1. Scans all 'models.py' files within the blueprints/packages in your project
   2. Creates an 'admin.py' and auto generates ModelViews for your models
   3. Auto registers all your ModelViews to be managed with the admin

   The Model Generator will create ModelViews for any Model created and 
   automatically registers it with the admin after the admin add-on has been 
   created.

   Also, the blueprints and packages generators automatically include an 
   admin.py file once the admin add-on has been added to a project.

API
---
Generated with the following command::

    patron addon api

The `api` add-on is for users who would like to create restful routes with 
flask's MethodView class instead of using the blueprint route generator. The 
api add-on creates the following directory structure::

    api/
     `-- __init__.py

So... what's the point? Well, patron automatically created a blueprint and 
registered it with the flask app factory and added another parser to patron. 

To get help, run the command::

    patron api -h

This will tell you that it expects a 'name' of the api resource.

So if you were to run the command::

    patron api Person

This will perform the following actions:

* create 'person.py' in the api directory
* auto hook it into the api

The contents of 'person.py' would be::

    # -*- coding: utf-8 -*-
    from flask import jsonify
    from flask.views import MethodView


    class PersonResource(MethodView):
        decorators = []

        def get(self, person_id):
            if person_id is None:
                pass  # return all
            else:
                pass  # return a single person

        def post(self):
            pass  # create a new person

        def put(self, person_id):
            pass  # update a single person

        def delete(self, person_id):
            pass  # delete a single person

The `api.add_url_rule(...)` stuff is already taken care of for you but you can 
always change that to your liking.

.. _front-end:

Front-End
---------
Generated with the following command::

    patron addon frontend

This provides a front-end work flow outside of the flask project package. I
typically separate my projects into client and server (hence the -d switch when
generating a project). The front-end work flow uses the following packages:

* gulp
* coffeegulp (to launch the gulp build process)
* sass (ruby sass since libsass chokes on new features and libs like bourbon, neat and bitters)
* jade (keeping consistent)
* browser-sync (livereload and proxy)
* imagemin (for image optimization)
* notify (system notifications when something goes wrong)
* uglify (of course)

The front-end add-on performs the following actions:

* checks to make sure you have a user directory setup
* if not, it'll setup the user directory with all scaffolds
* install necessary nodejs packages (can take a while if not setup prior to adding the add-on)
* create front-end work flow directory structure
* create a symlink/mklink to the frontend node_modules in the user directory
* prompts the user for what type of css frameworks/libs to choose from

  * bourbon, neat, bitters (optional)
  * bootstrap (optional)
  * normalize.css (default)
  * font-awesome (default)

* prompts the user for js libs

  * jquery (default)
  * requirejs (default)
  * angularjs (optional)

* automatically setup import directives and css libs into sass directory
* automatically configures js libs for requirejs

The directory structure produced will be outside of the flask project package::

    project_root/
      |-- project_dir/               <-- flask project
      |-- manage.py
      |-- gulpfile.coffee            <-- generated by front-end add-on
      |-- gulp/                      <-- gulp configuration and tasks
      |-- package.json               <-- generated by front-end add-on
      |-- node_modules/              <-- symlink to actual directory
      `-- frontend/                  <-- front-end add-on working directory
            |-- app/                 
            |     |-- app.coffee
            |     `-- main.coffee
            |-- assets/              
            |     |-- fonts/
            |     `-- img/
            |-- coffee/
            |     `-- vendor/
            `-- sass/
                  |-- base/
                  |     |-- _base.sass
                  |     |-- _mixins.sass
                  |     `-- _variables.sass
                  |-- lib/
                  |     |-- _normalize.scss
                  |     `-- font-awesome/
                  |-- modules/
                  |     `-- _modules.sass
                  `-- main.sass

Once generated, start up your flask development server by running::

    python manage.py runserver

and then in a separate process, within the project root directory, run::

    coffeegulp

This will auto open your system default web browser and proxy back to the flask
server. The gulp configuration also watches the jade files within the flask 
project and live reloads on all browsers. The really nice thing about 
browser-sync is that if you do something on a mobile client, it does the same 
on a desktop browser.

Everything you do within the 'frontend' directory will be processed and piped 
out to the static directory within your flask project.

+----------------+------------------------+
| frontend       | flask static directory |
+================+========================+
| app/           | app/                   |
+----------------+------------------------+
| sass/main.sass | css/main.css           |
+----------------+------------------------+
| assets/fonts/  | fonts/                 |
+----------------+------------------------+
| assets/img/    | img/                   |
+----------------+------------------------+
| coffee/        | js/                    |
+----------------+------------------------+

You don't have to create the directories, gulp will take care of that for you.

The `coffee` directory is for site-wide coffeescript/javascript. The vendor 
directory is where you keep all 3rd party javascript libs.

All images are placed in the assets/img directory for image optimization.

The `sass` directory is setup in a semi-smacss layout and all external libs are 
stored within the lib directory.

The `app` directory is for SPA development. The gulp configuration is setup to 
watch for all jade and coffeescript files within that directory. 'main.coffee' 
is where your AMD configuration is and 'app.coffee' is your entry point into 
your application. It's setup so you can organize your application by mv* types, 
domains or whatever you can think up.

If you don't like the setup, you can always go into the patron user directory 
and change the scaffolding to your liking. The scaffold can be found under the 
'templates/frontend' directory.

.. note::
   If you are having problems installing any of the node modules that patron 
   does on your behalf, the culprit on some linux systems is that you don't 
   have the appropriate graphics dev files installed to compile against. Use 
   your system package manager and install the dev files for jpg, gif, and png 
   files. If you don't have coffeegulp and bower installed globally, patron 
   will try to install those two for you.

Users
-----
