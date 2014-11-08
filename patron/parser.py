# -*- coding: utf-8 -*-
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
        getattr(self, "_{}_parser".format(self.parser_type))()
        return self.parser

    def _main_parser(self):
        init_help = "actions to be performed with patron itself"
        init_parser = self.subparser.add_parser('init', help=init_help)
        init_choices = ('check', 'user')
        choices_help = """
        'check' external dependencies or create the 'user' directory which
        contains the templates for the user to override to their liking."""
        init_parser.add_argument('action', choices=init_choices,
                                 help=choices_help)
        project_help = "create a flask project"
        name_help = "name of the flask project"
        project_parser = self.subparser.add_parser('project', help=project_help)
        project_parser.add_argument('name', help=name_help)

        dir_help = "rename target directory keeping project internals"
        project_parser.add_argument('-d', '--directory', help=dir_help)

    def _project_parser(self):
        self._add_blueprint()
        self._add_model()
        self._add_addons()
        self._add_task()

    def _add_blueprint(self):
        blueprint_help = "create a blueprint"
        blueprint_name_help = "name of blueprint"
        blueprint_route_help = "route_name:methods:variable-type"
        blueprint_parser = self.subparser.add_parser('blueprint',
                                                     help=blueprint_help)
        blueprint_parser.add_argument('name', help=blueprint_name_help)
        blueprint_parser.add_argument('route', nargs='*',
                                      help=blueprint_route_help)

    def _add_model(self):
        model_help = "generate a model for SQLAlchemy"
        model_blueprint_help = "name of blueprint"
        model_name_help = "name of model"
        model_field_help = "name:sqlalchemy_type-value:column_attr-value"
        model_parser = self.subparser.add_parser('model', help=model_help)
        model_parser.add_argument('blueprint', help=model_blueprint_help)
        model_parser.add_argument('name', help=model_name_help)
        model_parser.add_argument('field', help=model_field_help)

    def _add_addons(self):
        # check addons
        # don't add the ones that already exist
        pass

    def _add_task(self):
        task_help = "create task to be used with fabric"
        task_name_help = "name of the task"
        task_desc_help = "description of the task"
        task_parser = self.subparser.add_parser('task', help=task_help)
        task_parser.add_argument('name', help=task_name_help)
        task_parser.add_argument('description', help=task_desc_help)
