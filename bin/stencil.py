#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
__author__ = "John Boisselle <ping_me@johnboisselle.com>"
__version__ = "0.2.0"

import argparse
import argcomplete
import os
import os.path as path
import sys

current_dir = path.dirname(path.realpath(__file__))
lib_dir = path.join(path.abspath(path.join(current_dir, os.pardir)), 'lib')
sys.path.insert(0, lib_dir)

from stencil import Stencil

cli_description = """Stencil - ステンシル - Sutenshiru
[a generator for flask projects]"""

project_help = "Create a modular flask project base"
project_dir_help = """rename the target directory while maintaining project
internals"""

models_help = "Models with Flask-SQLAlchemy"
forms_help = "Forms with WTForms"
blueprints_help = "Blueprint scaffolding"
addon_help = "Addons to a flask project"
task_help = "Create tasks to be used with fabric"
package_help = "Similar to blueprints but without a url endpoint"
static_help = "Create a static site generator w/o a database"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=cli_description)
    subparser = parser.add_subparsers(dest='subparser_name')
    project_parser = subparser.add_parser('project', help=project_help)
    project_parser.add_argument('-d', '--directory', help=project_dir_help)
    models_parser = subparser.add_parser('model', help=models_help)
    forms_parser = subparser.add_parser('form', help=forms_help)
    blueprint_parser = subparser.add_parser('blueprint', help=blueprints_help)
    addon_parser = subparser.add_parser('addon', help=addon_help)
    task_parser = subparser.add_parser('task', help=task_help)
    package_parser = subparser.add_parser('pkg', help=package_help)
    static_parser = subparser.add_parser('static', help=static_help)

    namespace_help = "name of blueprint/package to be targeted"
    namespace_group = [models_parser, forms_parser]
    for p in namespace_group:
        p.add_argument('namespace', help=namespace_help)

    name_group = [project_parser, models_parser, forms_parser, blueprint_parser,
                  task_parser, package_parser, static_parser]
    name_help = {
        project_parser: 'name of the project',
        models_parser: 'name of the model',
        forms_parser: 'name of the form',
        blueprint_parser: 'name of the blueprint',
        task_parser: 'name of the task',
        package_parser: 'name of the package',
        static_parser: 'name of the static project'
    }
    for p in name_group:
        p.add_argument('name', help=name_help[p])

    addon_name_help = "Name of the addon to generate"
    addon_parser.add_argument('name', choices=Stencil.get_addons(),
                              help=addon_name_help)

    field_group = [models_parser, forms_parser]
    model_field_ex = "Ex: 'username:string'"
    model_field_help = "field_name:sqlalchemy_type {} {}"\
        .format(Stencil.get_field_types(), model_field_ex)
    field_help = {
        models_parser: model_field_help,
        forms_parser: 'field_name:wtforms_type'
    }
    for p in field_group:
        p.add_argument('field', nargs='*', help=field_help[p])

    task_description_help = "description of the task"
    task_parser.add_argument('description', help=task_description_help)

    argcomplete.autocomplete(parser)
    Stencil.run(parser.parse_args(), parser.prog)
