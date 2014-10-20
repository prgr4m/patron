# -*- coding: utf-8 -*-
from os import path
from cookiecutter.generate import generate_files
from .helpers import PatronConfig, is_name_valid, get_scaffold, create_context
from .injectors import FactoryInjector


class BlueprintGenerator(object):
    "Generates Blueprints"
    def __init__(self, name, custom_scaffold=None):
        if is_name_valid(name):
            self.name = name
        else:
            raise StandardError("Name given for the blueprint is invalid")
        self.config = PatronConfig()
        if self.config.has_blueprint(name):
            raise StandardError("Blueprint already exists")
        path_check = path.join(self.config.project_name, self.name)
        if path.exists(path_check):
            raise OSError("Blueprint already exists")
        if custom_scaffold:
            self.scaffold = get_scaffold(custom_scaffold)
        else:
            self.scaffold = get_scaffold('blueprint')

    def create(self):
        context = create_context('blueprint')
        context['cookiecutter']['blueprint_name'] = self.name
        context['cookiecutter']['project_name'] = self.config.project_name
        generate_files(repo_dir=self.scaffold, context=context)
        self.config.create_blueprint(self.name)
        FactoryInjector().inject('blueprint', self.name.lower())
