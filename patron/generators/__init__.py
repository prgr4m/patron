# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import os.path as path
import re
from string import Template
import ConfigParser


class PatronConfig(object):
    "Config creator for Patron projects"
    def __init__(self):
        self.config = ConfigParser.SafeConfigParser()
        self.filename = 'patron.cfg'
        self.config.readfp(open(self.filename))

    @staticmethod
    def is_present():
        return True if path.exists('patron.cfg') else False

    @staticmethod
    def create(project_name):
        """
        creates the base config file for Patron generated projects

        :param str project_name: the name of the flask project
        """
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
        with open('Patron.cfg', 'w') as configfile:
            config.write(configfile)

    @staticmethod
    def generate_config(self):
        "creates a Patron config file by inspecting a project's structure"
        pass

    @property
    def project_name(self):
        """
        The Patron project name.

        This is used as a base to find where various blueprints live within a
        Patron project.

        :return: flask project name of the Patron project
        :rtype: str
        """
        return self.config.get('general', 'project_name')

    @property
    def settings(self):
        """
        the settings file associated with the flask project

        :return: a path pointing to the settings file
        :rtype: str
        """
        return self.config.get('general', 'settings')

    @property
    def factory_path(self):
        """
        the factory function that creates the flask app

        :return: the path of the file that houses the factory
        :rtype: str
        """
        return self.config.get('general', 'factory_file')

    @property
    def addons(self):
        return self.config.get('general', 'addons')

    @addons.setter
    def addons(self, new_addon):
        """
        sets addons used in the Patron generated project

        :param new_addon:
            new_addon can either be a string or a list to be appended to the
            current addons already listed
        """
        current = self.config.get('general', 'addons')
        addons = current.split(',') if ',' in current else list(current)
        if not isinstance(new_addon, (str, list)):
            raise ValueError("Addon provided is an invalid type")
        if isinstance(new_addon, str):
            addons.append(new_addon)
        else:
            for a in [x for x in new_addon if x not in addons]:
                addons.append(a)
        self.config.set('general', 'addons', ",".join(addons))
        self.save_config()

    def create_blueprint(self, blueprint_name, blueprint_data):
        """
        creates a section associated with a blueprint along with its details

        :param str blueprint_name:
            the name of the blueprint
        :param dict blueprint_data:
            a dictionary with the 'key' as the filename/setting to be tracked
            along with the data (most of the time being a path)
        :raises: OSError:
            if the blueprint already exists in the config
        :rtype: None
        """
        if self.has_blueprint(blueprint_name):
            raise OSError("Blueprint already exists")
        blueprint_name = blueprint_name.lower()
        self.config.add_section(blueprint_name)
        for key, val in blueprint_data.items():
            self.config.set(blueprint_name, key, val)
        self.save_config()

    def has_blueprint(self, blueprint_name):
        """
        checks to see if blueprint exists in the config file

        :param str blueprint_name:
            the name of the blueprint
        :rtype: bool
        """
        return self.config.has_section(blueprint_name.lower())

    def get_blueprint_info(self, blueprint_name):
        """
        retrieves a list of data within the requested blueprint

        :param str blueprint_name:
            the name of the blueprint
        :return: returns the data associated with the blueprint (name, value)
        :rtype: list
        """
        return self.config.items(blueprint_name.lower())

    def save_config(self):
        "writes config data back to file"
        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)


class CodeInspector(object):
    "Imports a given module and inspects for code generation collisions"
    @staticmethod
    def has_collision(module_path, attribute):
        search_types = {
            'models': "class {}",
            'forms': "class {}",
            'views': "def {}",
            'fabfile': "def {}"
        }
        mod_name, file_ext = path.splitext(path.split(module_path)[-1])
        if mod_name not in search_types.keys():
            raise StandardError("CodeInspector:Unknown module type")
        search_pattern = search_types[mod_name].format(attribute)
        content = open(module_path, 'r').read()
        if re.search(search_pattern, content) is not None:
            return True
        return False


class RequirementsFileWriter(object):
    """Appends flask package dependencies"""
    def __init__(self, project_name):
        target_filename = "{}-requirements.txt".format(project_name.lower())
        if not path.exists(target_filename):
            raise OSError("FileNotFoundError")  # wish I was using python3
        self.requirements_file = open(target_filename, 'a')

    def __del__(self):
        self.requirements_file.close()

    def add_requirements(self, requirements):
        """
        appends dependencies to the requirements file

        :param str|list requirements:
            a list or str containing a python package dependency
        """
        if not isinstance(requirements, (str, list)):
            raise ValueError("Requirements need to either be a string or list")
        if isinstance(requirements, str):
            requirements = list(requirements)
        for req in requirements:
            self.requirements_file.write("{}{}".format(req, os.linesep))


def is_name_valid(name_in):
    if len(name_in) < 3:
        return False
    if re.search(r'[^\w]', name_in):
        return False
    return True


def get_templates_dir():
    current_location = path.dirname(path.dirname(path.abspath(__file__)))
    return path.join(current_location, 'data')


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
