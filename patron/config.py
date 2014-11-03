# -*- coding: utf-8 -*-
import json
from os import path


class PatronConfig(object):
    "Config creator/generator for Patron projects"
    def __init__(self):
        self.filename = 'patron.json'
        self.contents = json.load(open(self.filename))

    @staticmethod
    def is_present():
        return True if path.exists('patron.json') else False

    @staticmethod
    def create(project_name, directory_name):
        new_config = {
            'project_name': project_name,
            'factory_file': path.join(project_name, '__init__.py'),
            'settings_file': path.join(project_name, 'settings.py'),
            'addons': [],
            'blueprints': ['public']
        }
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
    def addons(self):
        return self.contents['addons']

    @addons.setter
    def addons(self, new_addon):
        if new_addon not in self.contents['addons']:
            self.contents['addons'].append(new_addon)
            self.save_config()

    def create_blueprint(self, blueprint_name):
        if blueprint_name not in self.contents['blueprints']:
            self.contents['blueprints'].append(blueprint_name)
            self.save_config()

    def has_blueprint(self, blueprint_name):
        return True if blueprint_name in self.contents['blueprints'] else False

    def save_config(self):
        with open(self.filename, 'w') as config_file:
            json.dump(self.contents, config_file, indent=2)