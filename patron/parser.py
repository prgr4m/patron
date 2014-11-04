# -*- coding: utf-8 -*-
# Purpose:
# This is the manager/factory to send the right kind of parser pending on
# conditions and features...
#
# Why:
# I only want to present the user the types of options that are necessary to
# their project since I plan on creating different types of scaffolds for the
# user rather than overloading the main parser when its not necessarily
# appropriate.
#
# Types of parsers:
# - Initial
#   This type of parser is for generating project types and general
#   configuration for the tooling as a whole
# - Main
#   This is the meat and potatoes parser in which is augmented with options only
#   pertaining to the type of project that the user has chosen. The different
#   project types I am choosing are: [tiny | blueprint | mvc]. Tiny would be for
#   a very basic scaffold type with just an project package and an app, model,
#   view and main file structure with the obligatory static and template
#   folders. Blueprint is the current standard and the mvc scaffold would be
#   akin to a padrino scaffold setup but using flask.
#
# Initial logic:
# - is the current working directory a patron project?
# - no: give the initial parser
# - yes: dynamically create the appropriate parser based on patron.json
#
# Initial parser:
# - check external dependencies
# - setup user directory
# - project generation
#   Type: 'tiny', 'blueprint', 'mvc'
#   ORM: alchemy, peewee, mongo
import argparse
from .config import PatronConfig

PARSER_DESC = "Patron - a generator for flask projects inspired by padrino"


class PatronParser(object):
    def __init__(self, parser_type='main'):
        if parser_type not in ['main', 'project']:
            raise StandardError("PatronParser:Unknown parser type")
        self.parser = argparse.ArgumentParser(description=PARSER_DESC)
        self.parser_type = parser_type
        self.subparser = self.parser.add_subparsers(dest='subparser_name')

    @staticmethod
    def get_parser():
        if PatronConfig.is_present():
            parser = PatronParser(parser_type='project').create()
        else:
            parser = PatronParser().create()
        return parser

    def create(self):
        getattr(self, "_{}".format(self.parser_type))()
        return self.parser

    def _main(self):
        self._add_init()
        self._add_project()

    def _add_init(self):
        init_help = "actions to be performed with patron itself"
        init_parser = self.subparser.add_parser('init', help=init_help)
        init_choices = ('templates', 'frontend', 'check')
        choices_help = """
        templates: create user templates directory
        frontend: create global npm modules directory for convenience
        check: checks system for external dependencies
        """
        init_parser.add_argument('action', choices=init_choices,
                                 help=choices_help)

    def _add_project(self):
        # orm
        # scaffold type
        project_help = "create a flask project"
        name_help = "name of the flask project"
        project_parser = self.subparser.add_parser('project', help=project_help)
        project_parser.add_argument('name', help=name_help)
        adapter_help = "database being used. default: sqlite"
        adapter_choices = ('sqlite', 'postgres', 'mysql')
        project_parser.add_argument('-a', '--adapter', choices=adapter_choices,
                                    default='sqlite', help=adapter_help)
        orm_help = "type of orm used with project"
        orm_choices = ('alchemy', 'peewee', 'mongoalchemy')

    def _project(self):
        # what type of project is it? [tiny, default, mvc]
        # what type of orm is being used?
        self._add_task()

    def _add_task(self):
        task_help = "create task to be used with fabric"
        task_name_help = "name of the task"
        task_desc_help = "description of the task"
        task_parser = self.subparser.add_parser('task', help=task_help)
        task_parser.add_argument('name', help=task_name_help)
        task_parser.add_argument('description', help=task_desc_help)


class ORMParser(object):
    pass


class FormParser(object):
    pass
