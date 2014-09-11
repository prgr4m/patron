# -*- coding: utf-8 -*-
from __future__ import print_function
import imp
import os.path as path
import re
import cStringIO
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
    def create(project_name):
        """
        creates the base config file for stencil generated projects

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
        with open('stencil.cfg', 'w') as configfile:
            config.write(configfile)

    @staticmethod
    def generate_config(self):
        "creates a stencil config file by inspecting a projects structure"
        pass

    @property
    def project_name(self):
        """
        The stencil project name.

        This is used as a base to find where various blueprints live within a
        stencil project.

        :return: flask project name of the stencil project
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
        sets addons used in the stencil generated project

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
            addons.extend(new_addon)
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
        with open(self.name, 'w') as configfile:
            self.config.write(configfile)


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


class InjectorBase(object):
    """The base object for injecting code into an existing code base"""
    indent = " " * 4

    def __init__(self):
        """
        Takes in a file to read
        StringIo object to store dynamic content
        """
        self.stream = cStringIO.StringIO()

    def __del__(self):
        self.stream.close()

    def inject(self):
        raise NotImplementedError("InjectorBase::inject must be overridden")


class AdminManageInjector(InjectorBase):
    """
    Responsible for injecting admin management hooks into manage.py
    """
    def __init__(self):
        super(AdminManageInjector, self).__init__()
        self.target_file = "manage.py"

    def inject(self, snippets):
        # read manage.py in
        # insert the necessary imports
        # add flask-script command into file
        pass


class FactoryInjector(InjectorBase):
    """
    Responsible for registering extensions and blueprints with an app factory
    """
    def __init__(self):
        super(FactoryInjector, self).__init__()
        self.target_file = path.join()

    def inject(self):
        # is it a blueprint or an extension?
        # add import statements
        # register the blueprint or extension
        # both have an import statement either way
        pass


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
