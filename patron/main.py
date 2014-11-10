#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import print_function
import webbrowser
# import argcomplete
from .parser import get_parser
from .helpers import check_dependencies, setup_user_directory
from .project import create_project
from . import resource

cli_args = None


def init_parser():
    if cli_args.action == 'check':
        check_dependencies()
    elif cli_args.action == 'user':
        setup_user_directory()
    else:
        webbrowser.open_new_tab("http://pythonhosted.org/patron")


def project_parser():
    options = dict(name=cli_args.name)
    if hasattr(cli_args, 'directory'):
        options['directory'] = cli_args.directory
    create_project(**options)


def blueprint_parser():
    print(cli_args)
    resource.create_blueprint(cli_args.name, routes=cli_args.route)


def form_parser():
    print(cli_args)


def model_parser():
    print(cli_args)


def package_parser():
    print(cli_args)
    resource.create_package()


def addon_parser():
    print(cli_args)


def task_parser():
    print(cli_args)


def main():
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
    # argcomplete.autocomplete(parser)
    cli_args = parser.parse_args()
    if cli_args.subparser_name:
        subparser_processor[cli_args.subparser_name]()
    else:
        parser.print_usage()

if __name__ == '__main__':
    main()
