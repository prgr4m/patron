#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import print_function
# import argcomplete
from .parser import PatronParser
from .helpers import check_dependencies, setup_user_directory
from .project import FlaskProject

__version__ = '0.2.3'
cli_args = None

#     project_type[args.subparser_name](**options).create()
#     if args.subparser_name == 'model':
#         # takes a name and *fields of name:type
#         ModelGenerator(args.namespace, args.name).create(args.field)
#         # takes a name and *fields of name:type
#     elif args.subparser_name == 'task':
#         TaskGenerator(args.name, args.description).create()


def init_parser():
    if cli_args.action == 'check':
        check_dependencies()
    else:
        setup_user_directory()


def project_parser():
    options = dict(name=cli_args.name)
    if hasattr(cli_args, 'directory'):
        options['directory'] = cli_args.directory
    FlaskProject(**options).create()


def addon_parser():
    print(cli_args)


def blueprint_parser():
    # scaffold blueprint
    # parse fields and append
    print(cli_args)


def form_parser():
    print(cli_args)


def model_parser():
    print(cli_args)


def task_parser():
    print(cli_args)


def main():
    # models_parser = subparser.add_parser('model', help=models_help)
    # addon_parser = subparser.add_parser('addon', help=addon_help)
    # task_parser = subparser.add_parser('task', help=task_help)
    # static_parser = subparser.add_parser('static', help=static_help)
    # name_group = [project_parser, models_parser, blueprint_parser,
    #               task_parser, static_parser]  # add back forms_parser later
    # for p in name_group:
    #     p.add_argument('name', help=name_help[p])
    # addon_parser.add_argument('name', choices=Patron.get_addons(),
    #                           help=addon_name_help)
    # # field_group = [models_parser, forms_parser]
    # field_group = [models_parser]
    # model_field_ex = "Ex: 'username:string'"
    # model_field_help = "field_name:sqlalchemy_type {} {}"\
    #     .format(Patron.get_field_types(), model_field_ex)
    # field_help = {
    #     models_parser: model_field_help,
    #     # forms_parser: 'field_name:wtforms_type'
    # }
    # for p in field_group:
    #     p.add_argument('field', nargs='*', help=field_help[p])
    # task_description_help = "description of the task"
    # task_parser.add_argument('description', help=task_description_help)
    # argcomplete.autocomplete(parser)
    global cli_args
    parser = PatronParser.get_parser()
    subparser_processor = {
        'init': init_parser,
        'project': project_parser,
        'blueprint': blueprint_parser,
        'model': model_parser,
        'task': task_parser
    }
    cli_args = parser.parse_args()
    if cli_args.subparser_name:
        subparser_processor[cli_args.subparser_name]()
    else:
        parser.print_usage()

if __name__ == '__main__':
    main()
