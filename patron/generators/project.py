# -*- coding: utf-8 -*-
from __future__ import print_function
from os import path
# from cookiecutter.config import get_user_config
from cookiecutter.generate import generate_context, generate_files
from . import is_name_valid, get_templates_dir
from .config import PatronConfig


class FlaskProject(object):
    def __init__(self, name, directory=None):
        if is_name_valid(name):
            self.name = name
        else:
            raise StandardError("Name supplied to FlaskProject is not valid")
        self.root_path = directory if isinstance(directory, str) else name
        if path.exists(self.root_path):
            raise OSError("Directory already exists")
        self.scaffold = path.join(get_templates_dir(), 'base')

    def create(self):
        # need to get input_dir (local to package or from user directory)
        config_dict = dict(default_context=dict())
        context_file = path.join(self.scaffold, 'cookiecutter.json')
        context = generate_context(
            context_file=context_file,
            default_context=config_dict['default_context'])
        context['cookiecutter']['directory_name'] = self.root_path
        context['cookiecutter']['project_name'] = self.name
        generate_files(repo_dir=self.scaffold, context=context)
        PatronConfig.create(self.name, self.root_path)
