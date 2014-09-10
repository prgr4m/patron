# -*- coding: utf-8 -*-
from __future__ import print_function
import imp
import os.path as path
import re
from string import Template
import ConfigParser


class StencilConfig(object):
    "Config creator for stencil projects"
    def __init__(self):
        self.name = 'stencil.cfg'
        self.config = ConfigParser.SafeConfigParser()
        self.config.readfp(open(self.name))

    @staticmethod
    def is_present():
        return True if path.exists('stencil.cfg') else False

    @staticmethod
    def create(self, project_name=''):
        "creates the base config file for stencil generated projects"
        config = ConfigParser.SafeConfigParser()
        config.add_section('general')
        config.set('general', 'project_name', project_name)
        config.set('general', 'settings',
                        path.join(project_name, 'settings.py'))
        config.set('general', 'factory_file',
                        path.join(project_name, '__init__.py'))
        config.set('general', 'addons', '')
        config.add_section('public')
        config.set('public', 'forms',
                        path.join(project_name, 'public', 'forms.py'))
        config.set('public', 'models',
                        path.join(project_name, 'public', 'models.py'))
        config.set('public', 'views',
                        path.join(project_name, 'public', 'views.py'))
        with open('stencil.cfg', 'w') as configfile:
            config.write(configfile)

    @staticmethod
    def generate_config(self):
        "creates a stencil config file by inspecting a projects structure"
        pass

    def get_project_name(self):
        "returns the flask project name"
        return self.config.get('general', 'project_name')

    def get_settings_path(self):
        "returns the path of settings file"
        return self.config.get('general', 'settings')

    def get_factory_path(self):
        "returns the path of the file that create the flask app"
        return self.config.get('general', 'factory_file')

    def create_blueprint(self, blueprint_name):
        "creates a section associated with a blueprint with associated details"
        pass

    def has_blueprint(self, blueprint_name):
        "checks to see if blueprint exists in the config file"
        return self.config.has_section(blueprint_name)

    def get_blueprint_info(self, blueprint_name):
        "retrieves a list of files within the requested blueprint"
        pass

    def serialize(self):
        "writes config data back to file"
        pass


class CodeInspector(object):
    "Imports a given module and inspects for code generation collisions"
    @staticmethod
    def has_collision(module_path, attribute):
        ret_val = False
        try:
            test = imp.load_source('module_test', module_path)
            if hasattr(test, attribute):
                ret_val = True
            return ret_val
        except SyntaxError:
            raise SyntaxError("not a valid python source file")
        except Exception:  # should be SyntaxError
            raise TypeError("module_path was not a string!")


def is_name_valid(name_in):
    if len(name_in) < 3:
        return False
    if re.search(r'[^\w]', name_in):
        return False
    return True


def get_templates_dir():
    current_location = path.dirname(path.dirname(path.abspath(__file__)))
    return path.join(current_location, 'templates')


def generate_templates(template_root, template_files):
    """
    template has to be a dictionary with a key as the actual template
    and the value being an array in the following format:
        1 - a dictionary of values to be unpacked into the template
        2 - if applicable, the actual destination name of the template

    ex:
        templates = {
            'template_source': [
                dict(template_variable=value),
                'actual_name_on_file_once_generated' # if different from key
            ]
        }
    this method/function is ideal for batch jobs
    """
    for template_file, data in template_files.items():
        destination_file = data[1] if len(data) > 1 else template_file
        with open(destination_file, 'w') as f:
            template_source = path.join(template_root, template_file)
            template = Template(open(template_source, 'r').read())
            f.write(template.safe_substitute(**data[0]))

__all__ = []
