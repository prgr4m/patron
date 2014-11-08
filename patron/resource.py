# -*- coding: utf-8 -*-
from __future__ import print_function
from os import path
from .config import PatronConfig

config = PatronConfig()


def resource_exists(resource_name):
    path_to_check = path.join(config.project_name, resource_name)
    return True if path.exists(path_to_check) else False


def create_blueprint(name):
    config = PatronConfig()
    if not resource_exists(config.project_name, name):
        pass
    else:
        print("Blueprint '{}' already exists!".format(name))


def parse_blueprint_fields(fields):
    pass


def create_package():
    pass
