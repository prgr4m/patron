# -*- coding: utf-8 -*-
import json
from os import path
from .model import ORM_TYPES
from .project import PROJECT_TYPES


class PatronConfig(object):
    "Config creator/generator for Patron projects"
    def __init__(self):
        self.filename = 'patron.json'
        self.contents = json.load(open(self.filename))

    @staticmethod
    def is_present():
        return True if path.exists('patron.json') else False

    @staticmethod
    def create(project_name, directory_name, project_type='blueprint',
               orm_type='sqlalchemy'):
        error_format = "PatronConfig:{}"
        if project_type not in PROJECT_TYPES:
            project_error = "Unknown project type"
            raise StandardError(error_format.format(project_error))
        if orm_type not in ORM_TYPES:
            orm_error = "Unknown orm type"
            raise StandardError(error_format.format(orm_error))
        simple_config = {
            'factory_file': path.join(project_name, 'app.py'),
            'settings_file': path.join(project_name, 'settings.py')
        }
        new_config = {
            'project_name': project_name,
            'scaffold_type': project_type,
            'factory_file': path.join(project_name, '__init__.py'),
            'settings_file': path.join(project_name, 'settings.py'),
            'orm': orm_type,
            'addons': []
        }
        if project_type == 'simple':
            new_config.update(simple_config)
        with open(path.join(directory_name, 'patron.json'), 'w') as config_file:
            json.dump(new_config, config_file, indent=2)

    @property
    def project_name(self):
        return self.contents['project_name']

    @property
    def settings(self):
        return self.contents['settings_file']

    @property
    def factory_path(self):
        return self.contents['factory_file']

    @property
    def orm(self):
        return self.contents['orm']

    @property
    def addons(self):
        return self.contents['addons']

    @addons.setter
    def addons(self, new_addon):
        if new_addon not in self.contents['addons']:
            self.contents['addons'].append(new_addon)
            self.save_config()

    def save_config(self):
        with open(self.filename, 'w') as config_file:
            json.dump(self.contents, config_file, indent=2)
