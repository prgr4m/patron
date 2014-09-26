# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import os.path as path
import shutil
from . import (StencilConfig, RequirementsFileWriter, FactoryInjector,
               ManageInjector, get_templates_dir, generate_templates)


class AddonManager(object):
    """Manages various types of flask project addons"""
    def __init__(self):
        self.config = StencilConfig()
        self.requirements = RequirementsFileWriter(self.config.project_name)

    @staticmethod
    def list_addons():
        "lists all known addons"
        return ['admin', 'api', 'ban', 'blog', 'commerce', 'humanizer', 'mail']

    def create(self, addon_name):
        if addon_name not in AddonManager.list_addons():
            raise ValueError("Unknown addon value!")
        getattr(self, "_{}".format(addon_name))()

    def _admin(self):
        if self.config.has_blueprint('admin'):
            raise OSError("admin addon already exits")
        templates_root = path.join(get_templates_dir(), 'admin')
        project_name = self.config.project_name
        admin_root = path.join(project_name, 'admin')
        admin_templates_dir = path.join(project_name, 'templates', 'admin')
        media_dir = path.join(project_name, 'static', 'media')
        os.mkdir(admin_root)
        open(path.join(admin_root, '__init__.py'), 'w').close()
        os.mkdir(admin_templates_dir)
        os.mkdir(media_dir)
        for f in [x for x in os.listdir(templates_root)
                  if x not in ['.', '..', 'templates', 'unittest', 'auth.py',
                               'views.py']]:
            shutil.copyfile(path.join(templates_root, f),
                            path.join(admin_root, f))
        template_file = {
            'views.py': [
                dict(project_name=project_name),
                path.join(admin_root, 'views.py')
            ]
        }
        generate_templates(templates_root, template_file)
        shutil.copyfile(path.join(templates_root, 'auth.py'),
                        path.join(admin_root, 'auth.py'))
        for f in [x for x in os.listdir(path.join(templates_root, 'templates'))
                  if x not in ['.', '..']]:
            shutil.copyfile(path.join(templates_root, 'templates', f),
                            path.join(admin_templates_dir, f))
        FactoryInjector().inject('admin')
        test_directory = path.join(templates_root, 'unittest')
        test_file = {
            'unittest.py': [
                dict(project_name=project_name, blueprint_name='Admin'),
                path.join('tests', 'test_admin.py')
            ]
        }
        generate_templates(test_directory, test_file)
        ManageInjector().inject('admin')
        self.config.addons = 'admin'
        admin_data = {}
        admin_package_files = ['forms', 'models', 'views', 'auth']
        for f in admin_package_files:
            admin_data[f] = path.join(project_name, 'admin', "{}.py".format(f))
        admin_data['templates'] = path.join(project_name, 'templates', 'admin')
        self.config.create_blueprint('admin', admin_data)
        packages = ['flask-admin', 'flask-login', 'flask-principal']
        self.requirements.add_requirements(packages)

    def _api(self):
        # check to see if api already exists
        # check to see if admin already exists
        # create an api blueprint (not an actual blueprint) but package in the
        # sense of a directory, __init__.py which contains the flask-restful
        # code and whatever resources to live within the directory
        # register with factory injector
        # requires auth - do I just want to call admin?
        # create unittest
        # add to stencil config addons
        # add to requirements file (flask-jwt, flask-mitten as well?)
        print("generating api addon -- still needs to be implemented")
        # self.config.addons = ['admin','api']

    def _blog(self):
        # hmmm.... an extension of a blueprint? or a more detailed setup...
        # add whooshalchemy to requirements file
        # ckeditor add to admin static
        # check to see if admin already exists
        # if so, inject and change definition of admin to inlcude static
        # if not, copy over admin templating
        print("generating blog addon -- still needs to be implemented")

    def _humanizer(self):
        # this is in the same category of an api but not even registered with
        # the app itself but with the admin and the public blueprint. it gets
        # its own directory because it stores its own models, admin interfaces,
        # csv data and flask-script commands
        print("generating humanizer addon -- still needs to be implemented")

    def _mail(self):
        # this is an extension setup... and settings.py config setup
        # add to requirements.txt
        print("generating mail addon -- still needs to be implemented")

    def _commerce(self):
        # creates a package and not a blueprint
        # satchless models
        # admin interfaces
        # and unittests
        # add to requirements file
        print("generating commerce addon -- still needs to be implemented")

    def _ban(self):
        # banning admin interface
        # banning manage.py commands
        # package not a blueprint
        # helper decorator / function to be called before a request on the
        #   public side
        print("generating banner addon -- still needs to be implemented")
