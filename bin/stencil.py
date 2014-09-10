#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
__author__ = "John Boisselle <ping_me@johnboisselle.com>"
__version__ = "0.1.2"

import argparse
import argcomplete
import os
import os.path as path
import sys

current_dir = path.dirname(path.realpath(__file__))
lib_dir = path.join(path.abspath(path.join(current_dir, os.pardir)), 'lib')
sys.path.insert(0, lib_dir)

cli_description = """Stencil - ステンシル - Sutenshiru
[a generator for flask projects]"""

project_help = "Create a modular flask project base"
project_dir_help = """rename the target directory while maintaining project
internals"""

models_help = "Models with SQLAlchemy"
forms_help = "Forms with WTForms"
blueprints_help = "Blueprint scaffolding"
addon_help = "Addons to a flask project"
fabric_help = "Create tasks to be used with fabric"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=cli_description)
    subparser = parser.add_subparsers(dest='subparser_name')
    project_parser = subparser.add_parser('project', help=project_help)
    project_parser.add_argument('-d', '--directory', help=project_dir_help)
    models_parser = subparser.add_parser('model', help=models_help)
    forms_parser = subparser.add_parser('form', help=forms_help)
    blueprint_parser = subparser.add_parser('blueprint', help=blueprints_help)
    # addon_parser = subparser.add_parser('addon', help=addon_help)
    task_parser = subparser.add_parser('task', help=fabric_help)

    name_group = [project_parser, models_parser, forms_parser, blueprint_parser,
                  task_parser]  # don't forget to add back addon_parser
    name_help = {
        project_parser: 'name of the project',
        models_parser: 'name of the model',
        forms_parser: 'name of the form',
        blueprint_parser: 'name of the blueprint',
        # addon_parser: 'name of the addon',
        task_parser: 'name of the task'
    }
    for p in name_group:
        p.add_argument('name', help=name_help[p])

    field_group = [models_parser, forms_parser]
    field_help = {
        models_parser: 'field_name:sqlalchemy_type',
        forms_parser: 'field_name:wtforms_type'
    }
    for p in field_group:
        p.add_argument('field', nargs='*', help=field_help[p])

    argcomplete.autocomplete(parser)
    from stencil import Stencil
    Stencil.run(parser.parse_args(), parser.prog)
