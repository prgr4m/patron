# -*- coding: utf-8 -*-
from __future__ import print_function
from os import path
from cookiecutter.generate import generate_files
from ..config import PatronConfig
from .helpers import is_name_valid, create_context, get_scaffold

PROJECT_TYPES = ('simple', 'blueprint', 'mvc')


class FlaskProject(object):
    def __init__(self, name, directory=None):
        if is_name_valid(name):
            self.name = name
        else:
            raise StandardError("FlaskProject: Name given is not valid")
        self.root_path = directory if isinstance(directory, str) else name
        if path.exists(self.root_path):
            raise OSError("FlaskProject: Directory already exists")
        self.scaffold = get_scaffold('base')

    def create(self):
        context = create_context('base')
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
        self.scaffold = get_scaffold('static')

    def create(self):
        super(StaticProject, self).create()
