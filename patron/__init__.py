#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import print_function
# import argcomplete
from .parser import PatronParser
from .helpers import check_dependencies, setup_user_directory

__version__ = '0.2.3'

# if args.subparser_name in ['project', 'static']:
#     options = dict(name=args.name)
#     if hasattr(args, 'directory'):
#         options['directory'] = args.directory
#     }
#     project_type[args.subparser_name](**options).create()
#     if args.subparser_name == 'model':
#         # takes a name and *fields of name:type
#         ModelGenerator(args.namespace, args.name).create(args.field)
#         # takes a name and *fields of name:type
#     elif args.subparser_name == 'task':
#         TaskGenerator(args.name, args.description).create()


def init_parser(args):
    if args.action == 'check':
        check_dependencies()
    else:
        setup_user_directory()


def project_parser(args):
    # mysql-connector-python for mysql adapter
    print(args)


def addon_parser(args):
    print(args)


def controller_parser(args):
    print(args)


def blueprint_parser(args):
    print(args)


def form_parser(args):
    print(args)


def model_parser(args):
    print(args)


def task_parser(args):
    print(args)


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
    parser = PatronParser.get_parser()
    subparser_processor = {
        'init': init_parser,
        'project': project_parser,
    }
    args = parser.parse_args()
    subparser_processor[args.subparser_name](args)

if __name__ == '__main__':
    main()
