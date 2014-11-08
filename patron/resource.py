# -*- coding: utf-8 -*-
from __future__ import print_function
from os import path
import sys
from .config import PatronConfig

config = PatronConfig()


def resource_exists(resource_name):
    path_to_check = path.join(config.project_name, resource_name)
    return True if path.exists(path_to_check) else False


def create_resource(name, resource_type='blueprint', fields=None):
    if resource_exists(config.project_name, name):
        print("Blueprint '{}' already exists!".format(name))
        sys.exit()
    # check the resource type (blueprint, package) fields are optional


def parse_blueprint_fields(fields):
    pass
