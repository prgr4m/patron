# -*- coding: utf-8 -*-
import os
import os.path as path
from . import StencilConfig


class AddonManager(object):
    """Manages various types of flask project addons"""
    def __init__(self):
        self.config = StencilConfig()

    @staticmethod
    def list_addons():
        "lists all known addons"
        return ['admin', 'api', 'banner', 'blog', 'commerce', 'humanizer',
                'mail', 'sitemap', 'websockets']

    def create(self, addon_name):
        if addon_name not in AddonManager.list_addons():
            raise ValueError("Unknown addon value!")
        getattr(self, "__{}".format(addon_name))()

    def __admin(self):
        project_name = self.config.project_name
        admin_root = path.join(project_name, 'admin')
        admin_templates_dir = path.join(project_name, 'templates', 'admin')
        os.mkdir(admin_root)
        os.mkdir(admin_templates_dir)
        os.mkdir(path.join(project_name, 'media'))
        # create files over
        # views.py takes $project_name
        # hook into app factory (both the admin blueprint and auth)
        # hook into manage.py the commands
        # add to stencil config addons
        pass

    def __api(self):
        # create an api blueprint (not an actual blueprint) but package in the
        # sense of a directory, __init__.py which contains the flask-restful code
        # and whatever resources to live within the directory
        #
        # register with factory injector
        # create unittest
        # add to stencil config addons
        pass

    def __sitemap(self):
        # create route in public blueprint
        # add to stencil config addons
        pass

    def __blog(self):
        # hmmm.... an extension of a blueprint? or a more detailed setup...
        pass

    def __humanizer(self):
        # this is in the same category of an api but not even registered with the
        # app itself but with the admin and the public blueprint. it gets its own
        # directory because it stores its own models, admin interfaces, csv data and
        # flask-script commands
        pass

    def __mail(self):
        # this is an extension setup... and settings.py config setup
        # add to requirements.txt
        pass

    def __ecommerce(self):
        # creates a package and not a blueprint
        # satchless models
        # admin interfaces
        # and unittests
        pass

    def __banner(self):
        # banning admin interface
        # banning manage.py commands
        # package not a blueprint
        # helper decorator / function to be called before a request on the
        #   public side
        pass

    def __websockets(self):
        # add websocket functionality to a project as a blueprint to keep things
        # separated from other blueprints and should have its own routes to begin
        # with...
        pass
