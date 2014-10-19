# -*- coding: utf-8 -*-
from os import path
from cookiecutter.generate import generate_context, generate_files
from .helpers import PatronConfig, is_name_valid, get_templates_dir
from .injectors import FactoryInjector


class BlueprintGenerator(object):
    "Generates Blueprints"
    def __init__(self, name):
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
        self.scaffold = path.join(get_templates_dir(), 'blueprint')

    def create(self):
        # need to get input_dir (local to package or user directory)
        config_dict = dict(default_context=dict())
        context_file = path.join(self.scaffold, 'cookiecutter.json')
        context = generate_context(
            context_file=context_file,
            default_context=config_dict['default_context'])
        context['cookiecutter']['blueprint_name'] = self.name
        context['cookiecutter']['project_name'] = self.config.project_name
        generate_files(repo_dir=self.scaffold, context=context)
        self.config.create_blueprint(self.name)
        FactoryInjector().inject('blueprint', self.name.lower())
