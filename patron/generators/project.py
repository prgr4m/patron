# -*- coding: utf-8 -*-
from __future__ import print_function
from os import path
from cookiecutter.generate import generate_context, generate_files
from .helpers import PatronConfig, is_name_valid, get_templates_dir


class FlaskProject(object):
    def __init__(self, name, directory=None):
        if is_name_valid(name):
            self.name = name
        else:
            raise StandardError("FlaskProject: Name given is not valid")
        self.root_path = directory if isinstance(directory, str) else name
        if path.exists(self.root_path):
            raise OSError("FlaskProject: Directory already exists")
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


class StaticProject(FlaskProject):
    """
    Very similar to a standard flask project minus the database dependencies
    and includes Flask-FlatPages and Frozen-Flask.
    """
    def __init__(self, name, directory=None):
        super(StaticProject, self).__init__(name, directory)
        self.scaffold = path.join(get_templates_dir(), 'static')

    def create(self):
        super(StaticProject, self).create()
