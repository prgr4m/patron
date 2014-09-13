# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from .generators import StencilConfig
from .generators.project import FlaskProject
from .generators.blueprint import BlueprintGenerator
from .generators.task import TaskGenerator
from .generators.addons import AddonManager


class Stencil(object):
    "The interface between the cli and the library"
    @staticmethod
    def get_addons():
        return AddonManager.list_addons()

    @staticmethod
    def run(args, prog_name):
        print(args)
        # addons (based off existing project, and common patterns),
        # extras (static site generator)
        project_dependent = ['model', 'form', 'blueprint', 'task', 'admin',
                             'addon', 'pkg']
        if args.subparser_name == 'project':
            # takes a name (maybe even type -- old school and classy)
            options = dict(name=args.name)
            if hasattr(args, 'directory'):
                options['directory'] = args.directory
            FlaskProject(**options).create()
        elif args.subparser_name in project_dependent:
            # check to see if config is present
            if not StencilConfig.is_present():
                print("Need to be in a stencil generated project root!")
                sys.exit()
            if args.subparser_name == 'model':
                # takes a name and *fields of name:type
                print('model stuff')
            elif args.subparser_name == 'form':
                # takes a name and *fields of name:type
                print('form stuff')
            elif args.subparser_name == 'blueprint':
                BlueprintGenerator(args.name).create()
            elif args.subparser_name == 'addon':
                AddonManager().create(args.name)
            elif args.subparser_name == 'task':
                TaskGenerator(args.name, args.description).create()
            elif args.subparser_name == 'pkg':
                # still needs to be implemented
                print("Package creation")
        else:
            print("Please run: '{} -h' for usage info".format(prog_name))
            sys.exit(0)

__all__ = []
