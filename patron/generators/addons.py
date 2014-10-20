# -*- coding: utf-8 -*-
from __future__ import print_function
import os
from os import path
import shutil
import subprocess
from cookiecutter.generate import generate_files
from .helpers import (PatronConfig, RequirementsFileWriter, get_templates_dir,
                      create_context, get_scaffold)
from .blueprint import BlueprintGenerator
from .injectors import (FactoryInjector, ManageInjector, AdminInjector,
                        SitemapInjector)


class AddonManager(object):
    """Manages various types of flask project addons"""
    def __init__(self):
        self.config = PatronConfig()
        project_name = self.config.project_name
        self.requirements = RequirementsFileWriter(project_name.lower())

    @staticmethod
    def list_addons():
        "lists all known addons"
        # return ['admin', 'api', 'ban', 'blog', 'commerce', 'humanizer',
        #         'mail']
        return ['admin', 'blog']

    def create(self, addon_name):
        if addon_name not in AddonManager.list_addons():
            raise ValueError("AddonManager:Unknown addon value!")
        getattr(self, "_{}".format(addon_name))()

    def _admin(self):
        if self.config.has_blueprint('admin'):
            raise OSError("admin addon already exits")
        # check also if admin directory or admin.py file exists before running
        # scaffold
        scaffold_dir = get_scaffold('admin')
        context = create_context('admin')
        context['cookiecutter']['project_name'] = self.config.project_name
        generate_files(repo_dir=scaffold_dir, context=context)
        FactoryInjector().inject('admin')
        ManageInjector().inject('admin')
        self.config.addons = 'admin'
        self.config.create_blueprint('admin')
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
        # add whooshalchemy to requirements file?
        template_root = path.join(get_templates_dir(), 'blog')
        target_dir = path.join(self.config.project_name, 'blog')
        if not self.config.has_blueprint('admin'):
            self._admin()
            print("auto generated admin addon")
        BlueprintGenerator('blog').create()
        remove_files = ['models.py', 'views.py', 'forms.py',
                        path.join('templates', 'index.jade')]
        for f in remove_files:
            os.remove(path.join(target_dir, f))
        for f in [f for f in os.listdir(template_root)
                  if f not in ['.', '..', 'templates', 'admin_templates']]:
            shutil.copyfile(path.join(template_root, f),
                            path.join(target_dir, f))
        template_root = path.join(template_root, 'templates')
        target_dir = path.join(target_dir, 'templates')
        for f in [f for f in os.listdir(template_root)
                  if f not in ['.', '..']]:
            shutil.copyfile(path.join(template_root, f),
                            path.join(target_dir, f))
        template_root = path.join(get_templates_dir(), 'blog',
                                  'admin_templates')
        target_dir = path.join(self.config.project_name, 'templates', 'admin')
        for f in [f for f in os.listdir(template_root) if f not in ['.', '..']]:
            shutil.copyfile(path.join(template_root, f),
                            path.join(target_dir, f))
        AdminInjector().inject('blog')
        SitemapInjector().inject('blog')
        ckeditor_options = {
            'basic': 'ckeditor#basic/4.3.3',
            'standard': 'ckeditor#standard/4.3.3',
            'full': 'ckeditor#standard/4.3.3'
        }
        bower_install = ["bower", "install", ckeditor_options['standard']]
        subprocess.call(bower_install)

    def _humanizer(self):
        # this is in the same category of an api but not even registered with
        # the app itself but with the admin and the public blueprint. it gets
        # its own directory because it stores its own models, admin interfaces,
        # csv data and flask-script commands
        print("generating humanizer addon -- still needs to be implemented")

    def _mail(self):
        # this is an extension setup... and settings.py config setup
        # add to requirements.txt
        # also add a contact form to public/forms
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
        # useful for setting up rules if forms get abused until you can
        # properly setup rules for your webserver
        print("generating banner addon -- still needs to be implemented")
