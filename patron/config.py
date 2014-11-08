# -*- coding: utf-8 -*-
import json
from os import path

config_name = 'patron.json'
config = json.load(open(config_name)) if path.exists(config_name) else None


def is_present():
    return True if config else False


def create(project_name, directory_name):
    new_config = {
        'project_name': project_name,
        'factory_file': path.join(project_name, '__init__.py'),
        'settings_file': path.join(project_name, 'settings.py'),
        'addons': []
    }
    with open(path.join(directory_name, config_name), 'w') as config_file:
        json.dump(new_config, config_file, indent=2)


def project_name(self):
    return config['project_name']


def settings(self):
    return config['settings_file']


def factory_path(self):
    return config['factory_file']


def addons(new_addon=None):
    if not new_addon:
        return config['addons']
    config['addons'].append(new_addon)
    save_config()


def save_config(self):
    with open(config_name, 'w') as config_file:
        json.dump(config, config_file, indent=2)
