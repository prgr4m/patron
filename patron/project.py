# -*- coding: utf-8 -*-
from __future__ import print_function
from os import path
from cookiecutter.generate import generate_files
from .config import PatronConfig
from .helpers import is_name_valid, create_context, get_scaffold


class FlaskProject(object):
    def __init__(self, name, directory=None, adapter='sqlite'):
        if is_name_valid(name):
            self.name = name
        else:
            raise StandardError("FlaskProject: Name given is not valid")
        project_path = directory if directory else name
        if path.exists(project_path):
            raise OSError("FlaskProject: Directory already exists")
        self.root_path = project_path

    def create(self):
        context = create_context('base')
        context['cookiecutter']['directory_name'] = self.root_path
        context['cookiecutter']['project_name'] = self.name
        context['cookiecutter']['root_project_name'] = self.name.lower()
        generate_files(repo_dir=get_scaffold('base'), context=context)
        PatronConfig.create(self.name, self.root_path)
