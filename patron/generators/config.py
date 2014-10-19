# -*- coding: utf-8 -*-
import json
from os import path


class PatronConfig(object):
    "Config creator/generator for Patron projects"
    def __init__(self):
        self.filename = 'patron.json'
        with open(self.filename, 'r') as patron_conf:
            self.contents = json.load(patron_conf)

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

    @staticmethod
    def generate_config():
        pass
