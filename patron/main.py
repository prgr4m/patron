#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import print_function
# import argcomplete
from .parser import get_parser
from .helpers import check_dependencies, setup_user_directory
from .project import create_project
from . import resource

__version__ = '0.2.3'
cli_args = None
#         # takes a name and *fields of name:type
#         ModelGenerator(args.namespace, args.name).create(args.field)
#         # takes a name and *fields of name:type


def init_parser():
    if cli_args.action == 'check':
        check_dependencies()
    else:
        setup_user_directory()


def project_parser():
    options = dict(name=cli_args.name)
    if hasattr(cli_args, 'directory'):
        options['directory'] = cli_args.directory
    create_project(**options)


def blueprint_parser():
    # scaffold blueprint
    # parse fields and append
    print(cli_args)


def form_parser():
    print(cli_args)


def model_parser():
    print(cli_args)


def package_parser():
    print(cli_args)


def addon_parser():
    print(cli_args)


def task_parser():
    print(cli_args)


def main():
    # for p in field_group:
    #     p.add_argument('field', nargs='*', help=field_help[p])
    # argcomplete.autocomplete(parser)
    global cli_args
    parser = get_parser()
    subparser_processor = {
        'init': init_parser,
        'project': project_parser,
        'blueprint': blueprint_parser,
        'model': model_parser,
        'pkg': package_parser,
        'addon': addon_parser,
        'task': task_parser
    }
    cli_args = parser.parse_args()
    if cli_args.subparser_name:
        subparser_processor[cli_args.subparser_name]()
    else:
        parser.print_usage()

if __name__ == '__main__':
    main()
