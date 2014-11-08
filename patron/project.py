# -*- coding: utf-8 -*-
from __future__ import print_function
from os import path
from cookiecutter.generate import generate_files
from . import config
from .helpers import is_name_valid, create_context, get_scaffold


def create_project(name, directory=None):
    if not is_name_valid(name):
        raise StandardError("Name given is invalid")
    project_path = directory if directory else name
    if path.exists(project_path):
        raise OSError("Directory already exists")
    context = create_context('base')
    context['cookiecutter']['directory_name'] = project_path
    context['cookiecutter']['project_name'] = name
    context['cookiecutter']['root_project_name'] = name.lower()
    generate_files(repo_dir=get_scaffold('base'), context=context)
    config.create(name, project_path)
