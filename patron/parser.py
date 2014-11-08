# -*- coding: utf-8 -*-
import argparse
from .config import PatronConfig

parser, subparser = None, None
PARSER_DESC = "Patron - a generator for flask projects inspired by padrino"


def get_parser():
    global parser, subparser
    parser = argparse.ArgumentParser(description=PARSER_DESC)
    subparser = parser.add_subparsers(dest='subparser_name')
    if PatronConfig.is_present():
        project_parser()
    else:
        main_parser()
    return parser


def main_parser():
    init_help = "actions to be performed with patron itself"
    init_parser = subparser.add_parser('init', help=init_help)
    init_choices = ('check', 'user')
    choices_help = """
    'check' external dependencies or create the 'user' directory which
    contains the templates for the user to override to their liking."""
    init_parser.add_argument('action', choices=init_choices, help=choices_help)
    project_help = "create a flask project"
    name_help = "name of the flask project"
    project_parser = subparser.add_parser('project', help=project_help)
    project_parser.add_argument('name', help=name_help)
    dir_help = "rename target directory keeping project internals"
    project_parser.add_argument('-d', '--directory', help=dir_help)


def project_parser():
    add_blueprint()
    add_package()
    add_model()
    add_addons()
    add_task()


def add_blueprint():
    blueprint_help = "create a blueprint"
    blueprint_name_help = "name of blueprint"
    blueprint_route_help = "route_name:methods:variable-type"
    blueprint_parser = subparser.add_parser('blueprint', help=blueprint_help)
    blueprint_parser.add_argument('name', help=blueprint_name_help)
    blueprint_parser.add_argument('route', nargs='*', help=blueprint_route_help)


def add_package():
    package_help = "create a package. similar to blueprint without a view."
    package_name_help = "name of package/resource"
    package_parser = subparser.add_parser('pkg', help=package_help)
    package_parser.add_argument('name', help=package_name_help)
    # optional flags [-m(odel), -c(ommand), -a(dmin), -f(orm)]


def add_model():
    model_help = "generate a model for SQLAlchemy"
    model_blueprint_help = "name of blueprint"
    model_name_help = "name of model"
    model_field_help = "name:sqlalchemy_type-value:column_attr-value"
    model_parser = subparser.add_parser('model', help=model_help)
    model_parser.add_argument('blueprint', help=model_blueprint_help)
    model_parser.add_argument('name', help=model_name_help)
    model_parser.add_argument('field', help=model_field_help)


def add_addons():
    # check addons
    # don't add the ones that already exist
    pass


def add_task():
    task_help = "create task to be used with fabric"
    task_name_help = "name of the task"
    task_desc_help = "description of the task"
    task_parser = subparser.add_parser('task', help=task_help)
    task_parser.add_argument('name', help=task_name_help)
    task_parser.add_argument('description', help=task_desc_help)
