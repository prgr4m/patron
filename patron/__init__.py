#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import print_function
import argparse
# import argcomplete
import sys
from .generators.helpers import PatronConfig
from .generators.project import FlaskProject, StaticProject
from .generators.blueprint import BlueprintGenerator
from .generators.task import TaskGenerator
from .generators.addons import AddonManager
from .generators.model import ModelGenerator


class Patron(object):
    "The interface between the cli and the library"
    @staticmethod
    def get_addons():
        return AddonManager.list_addons()

    @staticmethod
    def get_field_types():
        return ModelGenerator.get_known_fields()

    @staticmethod
    def run(args, prog_name):
        # print(args)
        project_dependent = ['model', 'form', 'blueprint', 'task', 'admin',
                             'addon', 'pkg']
        if args.subparser_name in ['project', 'static']:
            options = dict(name=args.name)
            if hasattr(args, 'directory'):
                options['directory'] = args.directory
            project_type = {
                'project': FlaskProject,
                'static': StaticProject
            }
            project_type[args.subparser_name](**options).create()
        elif args.subparser_name in project_dependent:
            if not PatronConfig.is_present():
                print("Need to be in a Patron generated project root!")
                sys.exit()
            if args.subparser_name == 'model':
                # takes a name and *fields of name:type
                ModelGenerator(args.namespace, args.name).create(args.field)
            elif args.subparser_name == 'form':
                # takes a name and *fields of name:type
                print('form stuff')
            elif args.subparser_name == 'blueprint':
                BlueprintGenerator(args.name).create()
            elif args.subparser_name == 'addon':
                AddonManager().create(args.name)
            elif args.subparser_name == 'task':
                TaskGenerator(args.name, args.description).create()
        else:
            print("Please run: '{} -h' for usage info".format(prog_name))
            sys.exit(0)


def main():
    cli_desc = "Patron - a generator for flask projects inspired by padrino"

    project_help = "Create a modular flask project base"
    dir_help = "rename the target directory while maintaining project internals"

    models_help = "Models with Flask-SQLAlchemy"
    # forms_help = "Forms with WTForms"
    blueprints_help = "Blueprint scaffolding"
    addon_help = "Addons to a flask project"
    task_help = "Create tasks to be used with fabric"
    static_help = "Create a static site generator w/o a database"

    parser = argparse.ArgumentParser(description=cli_desc)
    subparser = parser.add_subparsers(dest='subparser_name')
    project_parser = subparser.add_parser('project', help=project_help)
    models_parser = subparser.add_parser('model', help=models_help)
    # forms_parser = subparser.add_parser('form', help=forms_help)
    blueprint_parser = subparser.add_parser('blueprint',
                                            help=blueprints_help)
    addon_parser = subparser.add_parser('addon', help=addon_help)
    task_parser = subparser.add_parser('task', help=task_help)
    static_parser = subparser.add_parser('static', help=static_help)

    directory_group = [project_parser, static_parser]
    for p in directory_group:
        p.add_argument('-d', '--directory', help=dir_help)

    namespace_help = "name of blueprint/package to be targeted"
    # namespace_group = [models_parser, forms_parser]
    namespace_group = [models_parser]
    for p in namespace_group:
        p.add_argument('namespace', help=namespace_help)

    name_group = [project_parser, models_parser, blueprint_parser,
                  task_parser, static_parser]  # add back forms_parser later
    name_help = {
        project_parser: 'name of the project',
        models_parser: 'name of the model',
        # forms_parser: 'name of the form',
        blueprint_parser: 'name of the blueprint',
        task_parser: 'name of the task',
        static_parser: 'name of the static project'
    }
    for p in name_group:
        p.add_argument('name', help=name_help[p])

    addon_name_help = "Name of the addon to generate"
    addon_parser.add_argument('name', choices=Patron.get_addons(),
                              help=addon_name_help)

    # field_group = [models_parser, forms_parser]
    field_group = [models_parser]
    model_field_ex = "Ex: 'username:string'"
    model_field_help = "field_name:sqlalchemy_type {} {}"\
        .format(Patron.get_field_types(), model_field_ex)
    field_help = {
        models_parser: model_field_help,
        # forms_parser: 'field_name:wtforms_type'
    }
    for p in field_group:
        p.add_argument('field', nargs='*', help=field_help[p])

    task_description_help = "description of the task"
    task_parser.add_argument('description', help=task_description_help)

    # argcomplete.autocomplete(parser)
    Patron.run(parser.parse_args(), parser.prog)

if __name__ == '__main__':
    main()
