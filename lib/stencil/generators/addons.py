# -*- coding: utf-8 -*-
"""
This file contains a list of functions to generate addons since it there isn't
any state to be maintained other than within the StencilConfig object when
dealing with a generated flask project.
"""

def generate_admin():
    # read from config where the admin blueprint will be residing
    # create files over
    # hook into app factory (both the admin blueprint and auth)
    # hook into manage.py the commands
    # add to stencil config addons
    pass

def generate_api():
    # create an api blueprint (not an actual blueprint) but package in the
    # sense of a directory, __init__.py which contains the flask-restful code
    # and whatever resources to live within the directory
    #
    # register with factory injector
    # create unittest
    # add to stencil config addons
    pass

def generate_sitemap():
    # create route in public blueprint
    # add to stencil config addons
    pass

def generate_blog():
    # hmmm.... an extension of a blueprint? or a more detailed setup...
    pass

def generate_humanizer():
    # this is in the same category of an api but not even registered with the
    # app itself but with the admin and the public blueprint. it gets its own
    # directory because it stores its own models, admin interfaces, csv data and
    # flask-script commands
    pass

def generate_mail():
    # this is an extension setup... and settings.py config setup
    # add to requirements.txt
    pass

def generate_ecommerce():
    # creates a package and not a blueprint
    # satchless models
    # admin interfaces
    # and unittests
    pass

def banner():
    # banning admin interface
    # banning manage.py commands
    # package not a blueprint
    # helper decorator / function to be called before a request on the
    #   public side
    pass

def websockets():
    # add websocket functionality to a project as a blueprint to keep things
    # separated from other blueprints and should have its own routes to begin
    # with...
    pass
