Add-ons
=======
Add-ons are pieces of functionality added to a project since patron has the use 
what you need mentality rather than throwing the kitchen sink at you. In order 
to get a list of add-ons used by patron run the following command::

    patron addon -h

Admin
-----
Generated with the following command::

    patron addon admin

This admin add-on appends its dependencies to the requirements file, registers 
itself with the flask app and injects cli commands into manage.py. It comes 
with Flask-Login and Flask-Principal with preconfigured routes.

API
---


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

Once generated, start up your flask development server by running:

    python manage.py runserver

and then in a separate process, within the root directory, run:

    coffeegulp

This will auto open your system default web browser and proxy back to the flask
server. It also watches the jade files within the flask project and reloads on 
all browsers. The really nice thing about browser-sync is that if you do 
something in one client, it does it in all clients.

If you don't like the setup, you can always go into the patron user directory 
and change the scaffolding to your liking. The directory is labeled 'frontend' 
under the 'templates' directory.

**Note**:

If you are having problems installing any of the node modules that patron does 
on your behalf, the culprit on some linux systems is that you don't have the 
appropriate graphics dev files installed to compile against. Use your system 
package manager and install the dev files for jpg, gif, and png files. If you 
don't have coffeegulp and bower installed globally, patron will try to install 
those two for you.

Users
-----
