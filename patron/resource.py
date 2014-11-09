# -*- coding: utf-8 -*-
from __future__ import print_function
from os import path
import sys
from cookiecutter.generate import generate_files
from . import config
from .helpers import is_name_valid, get_scaffold, create_context


def resource_exists(resource_name):
    path_to_check = path.join(config.project_name, resource_name)
    return True if path.exists(path_to_check) else False


def create_blueprint(name, fields=None):
    if not is_name_valid(name):
        raise StandardError("'{}' is an invalid name".format(name))
    if resource_exists(config.get_project_name(), name):
        raise OSError("Blueprint '{}' already exists".format(name))
    scaffold = get_scaffold('blueprint')
    context = create_context('blueprint')
    context['cookiecutter']['blueprint_name'] = name
    context['cookiecutter']['project_name'] = config.get_project_name()
    generate_files(repo_dir=scaffold, context=context)
    if fields:
        view_filename = path.join(config.get_project_name(), name, 'views.py')
        content = parse_blueprint_fields(fields)
        with open(view_filename, 'a') as view_file:
            view_file.write(content)
    # if admin addon was added, include admin.py
    # factory_injector.inject('blueprint', name.lower())


def parse_blueprint_fields(fields):
    # route_name:methods:variable-type
    pass


def create_package(name, options):
    # options: -m(odel), -f(orms), -a(dmin), -c(ommands)
    # all inclusive unless explicit
    # admin being the exception... has to be added
    pass
