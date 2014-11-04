# -*- coding: utf-8 -*-
import argparse
from .config import PatronConfig
from .generators.model import ORM_TYPES, ADAPTER_TYPES
from .generators.project import PROJECT_TYPES

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
        project_help = "create a flask project"
        name_help = "name of the flask project"
        project_parser = self.subparser.add_parser('project', help=project_help)
        project_parser.add_argument('name', help=name_help)

        dir_help = "rename target directory keeping project internals"
        project_parser.add_argument('-d', '--directory', help=dir_help)

        type_help = "type of project scaffold. default: blueprint"
        type_choices = PROJECT_TYPES
        project_parser.add_argument('-t', '--type', choices=type_choices,
                                    default='blueprint', help=type_help)

        adapter_help = "database being used. default: sqlite"
        adapter_choices = ADAPTER_TYPES
        project_parser.add_argument('-a', '--adapter', choices=adapter_choices,
                                    default='sqlite', help=adapter_help)

        orm_help = "type of orm used with project. default: sqlalchemy"
        orm_choices = ORM_TYPES
        project_parser.add_argument('-o', '--orm', choices=orm_choices,
                                    default='sqlalchemy', help=orm_help)

    def _project_parser(self):
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


class AddonParser(object):
    # read config
    # exclude already existing addons used
    pass


class ORMParser(object):
    def __init__(self, parser, orm_type='sqlalchemy'):
        error_message = "ORMParser:{}"
        if not isinstance(parser, argparse.ArgumentParser):
            parser_error = "parser not an instance of ArgumentParser"
            raise StandardError(error_message.format(parser_error))
        if orm_type not in ORM_TYPES:
            orm_error = "Unknown ORM type used"
            raise StandardError(error_message.format(orm_error))
        self.parser = parser
        self.orm_type = orm_type

    def create_subparser(self):
        getattr(self, "_{}".format(self.orm_type))()

    def _sqlalchemy(self):
        pass

    def _peewee(self):
        pass


class FormParser(object):
    @staticmethod
    def create_subparser(parser):
        pass
