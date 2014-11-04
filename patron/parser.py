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
        project_help = "create a flask project"
        name_help = "name of the flask project"
        project_parser = self.subparser.add_parser('project', help=project_help)
        project_parser.add_argument('name', help=name_help)

        dir_help = "rename target directory keeping project internals"
        project_parser.add_argument('-d', '--directory', help=dir_help)

        type_help = "type of project scaffold. default: blueprint"
        type_choices = ('tiny', 'blueprint', 'mvc')
        project_parser.add_argument('-t', '--type', choices=type_choices,
                                    default='blueprint', help=type_help)

        adapter_help = "database being used. default: sqlite"
        adapter_choices = ('sqlite', 'postgres', 'mysql')
        project_parser.add_argument('-a', '--adapter', choices=adapter_choices,
                                    default='sqlite', help=adapter_help)

        orm_help = "type of orm used with project. default: alchemy"
        orm_choices = ('alchemy', 'peewee', 'none')
        project_parser.add_argument('-o', '--orm', choices=orm_choices,
                                    default='alchemy', help=orm_help)

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
