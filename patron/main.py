#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import print_function
import webbrowser
# import argcomplete
from .parser import get_parser
from .helpers import check_dependencies, setup_user_directory, create_task
from .project import create_project
from .model import create_model
from . import resource

args = None


def init_parser():
    if args.action == 'check':
        check_dependencies()
    elif args.action == 'user':
        setup_user_directory()
    else:
        webbrowser.open_new_tab("http://pythonhosted.org/patron")


def project_parser():
    options = dict(name=args.name)
    if hasattr(args, 'directory'):
        options['directory'] = args.directory
    create_project(**options)


def blueprint_parser():
    resource.create_blueprint(args.name, routes=args.route, templates=args.n)


def form_parser():
    print(args)


def model_parser():
    create_model(args.blueprint, args.name, args.field, args.r)


def package_parser():
    print(args)
    resource.create_package()


def addon_parser():
    print(args)


def task_parser():
    create_task(args.name, args.description)


def main():
    global args
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
    args = parser.parse_args()
    if args.subparser_name:
        subparser_processor[args.subparser_name]()
    else:
        parser.print_usage()

if __name__ == '__main__':
    main()
