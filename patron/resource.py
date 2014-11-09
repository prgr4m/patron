# -*- coding: utf-8 -*-
from __future__ import print_function
from os import path
import sys
from . import config


def resource_exists(resource_name):
    path_to_check = path.join(config.project_name, resource_name)
    return True if path.exists(path_to_check) else False


def create_blueprint(name, fields=None):
    if resource_exists(config.project_name, name):
        print("Blueprint '{}' already exists!".format(name))
        sys.exit()
    # check the resource type (blueprint, package) fields are optional


def parse_blueprint_fields(fields):
    pass


def create_package(name, options):
    pass
