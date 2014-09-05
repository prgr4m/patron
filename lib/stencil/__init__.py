# -*- coding: utf-8 -*-
import sys

class Stencil:
    "The interface between the cli and the library"
    @staticmethod
    def run(args, prog_name):
        #print(args)
        if args.subparser_name == 'project':
            # takes a name (maybe even type -- old school and classy)
            print("project name: {}".format(args.name))
        elif args.subparser_name == 'model':
            # takes a name and *fields of name:type
            print('model stuff')
        elif args.subparser_name == 'form':
            # takes a name and *fields of name:type
            print('form stuff')
        elif args.subparser_name == 'blueprint':
            # takes a name
            print('blueprint stuff')
        elif args.subparser_name == 'addon':
            # has multiple addons... maybe even groups...
            print('addon stuff')
        elif args.subparser_name == 'fabric':
            # takes a name
            print('fabric stuff')
        else:
            print("Please run: '{} -h' for usage info".format(prog_name))
            sys.exit(0)

__all__ = [Stencil]
