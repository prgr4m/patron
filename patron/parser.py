# -*- coding: utf-8 -*-
import argparse
from . import config
from .addon import get_known_addons

parser, subparser = None, None
PARSER_DESC = "Patron - a generator for flask projects inspired by padrino"


def get_parser():
    global parser, subparser
    parser = argparse.ArgumentParser(description=PARSER_DESC)
    subparser = parser.add_subparsers(dest='subparser_name')
    if config.is_present():
        project_parser()
    else:
        main_parser()
    return parser


def main_parser():
    init_help = "actions to be performed with patron itself"
    init_parser = subparser.add_parser('init', help=init_help)
    init_choices = ('check', 'user', 'docs')
    choices_help = """
    'check' external dependencies, create the 'user' directory which
    contains the templates for the user to override to their liking or
    open up the 'docs' in a web browser."""
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
    add_form()
    add_addons()
    add_task()


def add_blueprint():
    blueprint_help = "create a blueprint"
    blueprint_name_help = "name of blueprint"
    blueprint_route_help = "method:route_name:variable_name-type"
    blueprint_tpl_help = "no templates generated for extra routes created"
    blueprint_parser = subparser.add_parser('blueprint', help=blueprint_help)
    blueprint_parser.add_argument('name', help=blueprint_name_help)
    blueprint_parser.add_argument('route', nargs='*', help=blueprint_route_help)
    blueprint_parser.add_argument('-n', action='store_false',
                                  help=blueprint_tpl_help)


def add_package():
    package_help = "create a package. similar to blueprint without a view."
    package_name_help = "name of package/resource"
    package_parser = subparser.add_parser('pkg', help=package_help)
    package_parser.add_argument('name', help=package_name_help)
    # optional flags [-m(odel), -c(ommand), -a(dmin), -f(orm)]


def add_model():
    model_help = "generate a model for SQLAlchemy"
    model_blueprint_help = "name of blueprint to create model. default: public"
    model_name_help = "name of model"
    model_field_help = "name:sqlalchemy_type:column_attr-value"
    model_relation_help = "name:class:backref:lazy-type"
    model_parser = subparser.add_parser('model', help=model_help)
    model_parser.add_argument('-b', '--blueprint', default='public',
                              help=model_blueprint_help)
    model_parser.add_argument('name', help=model_name_help)
    model_parser.add_argument('field', nargs='+', help=model_field_help)
    model_parser.add_argument('-r', action='append', help=model_relation_help)


def add_form():
    form_help = "generate a form for WTForms"
    form_blueprint_help = "name of blueprint to create form in. default: public"
    form_name_help = "name of form"
    form_field_help = "name:wtf_type:label:validators"
    form_validators_help = "generate validation methods for fields created."
    form_parser = subparser.add_parser('form', help=form_help)
    form_parser.add_argument('-b', '--blueprint', default='public',
                             help=form_blueprint_help)
    form_parser.add_argument('name', help=form_name_help)
    form_parser.add_argument('field', nargs='+', help=form_field_help)
    form_parser.add_argument('-v', '--validators', action='store_true',
                             help=form_validators_help)


def add_addons():
    installed_addons = config.addons()
    addons = [a for a in get_known_addons() if a not in installed_addons]
    if addons:
        addon_help = "addon functionality to your flask project"
        addon_choices = addons
        addon_name_help = "name of the addon to install"
        addon_parser = subparser.add_parser('addon', help=addon_help)
        addon_parser.add_argument('name', choices=addon_choices,
                                  help=addon_name_help)
    # add addon parser for those that require a generator (ex: 'api')


def add_task():
    task_help = "create task to be used with fabric"
    task_name_help = "name of the task"
    task_desc_help = "description of the task"
    task_parser = subparser.add_parser('task', help=task_help)
    task_parser.add_argument('name', help=task_name_help)
    task_parser.add_argument('description', help=task_desc_help)
