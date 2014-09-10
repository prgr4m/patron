# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from .generators import StencilConfig
from .generators.project import FlaskProject


class Stencil(object):
    "The interface between the cli and the library"
    @staticmethod
    def run(args, prog_name):
        print(args)
        # generators (for forms and models)
        # addons (based off existing project, and common patterns),
        # extras (static site generator)
        if args.subparser_name == 'project':
            # takes a name (maybe even type -- old school and classy)
            options = dict(name=args.name)
            if hasattr(args, 'directory'):
                options['directory'] = args.directory
            FlaskProject(**options).create()
        else:
            if args.subparser_name == 'model':
                # takes a name and *fields of name:type
                print('model stuff')
            elif args.subparser_name == 'form':
                # takes a name and *fields of name:type
                print('form stuff')
            elif args.subparser_name == 'blueprint':
                # takes a name
                print('blueprint stuff')
                if not StencilConfig.is_present():
                    print("Need to be in project root!")
                    sys.exit()
            elif args.subparser_name == 'addon':
                # has multiple addons... maybe even groups...
                print('addon stuff')
            elif args.subparser_name == 'fabric':
                # takes a name
                print('fabric stuff')
            else:
                print("Please run: '{} -h' for usage info".format(prog_name))
                sys.exit(0)

__all__ = []
