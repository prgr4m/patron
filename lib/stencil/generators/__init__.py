# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import os.path as path
import re
# import sys
import cStringIO
from string import Template
import ConfigParser


class StencilConfig(object):
    "Config creator for stencil projects"
    def __init__(self):
        self.config = ConfigParser.SafeConfigParser()
        self.filename = 'stencil.cfg'
        self.config.readfp(open(self.filename))

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
        "creates a stencil config file by inspecting a project's structure"
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


class InjectorBase(object):
    """The base object for injecting code into an existing code base"""
    indent = " " * 4

    def __init__(self):
        """
        Initializing the common base for code injection

        :param str target:
            the path of the target file to inject code to (safely)
        """
        self.config = StencilConfig()
        self.stream = cStringIO.StringIO()

    def __del__(self):
        self.stream.close()

    def inject(self):
        raise NotImplementedError("InjectorBase::inject must be overridden")

    def read_target(self):
        with open(self.target_file) as f:
            for line in f:
                yield line.rstrip()


class ManageInjector(InjectorBase):
    """
    Responsible for injecting admin management hooks into manage.py
    """
    def __init__(self):
        super(ManageInjector, self).__init__()
        self.target_file = "manage.py"

    def inject(self, directive):
        """
        The method responsible for injecting code snippets into a (flask-script)
        manage.py file.

        :param str directive:
            a known key to perform associated script injections
        """
        known_directives = ['admin']  # livereload, etc, will come later
        if directive not in known_directives:
            raise ValueError("ManageInjector:Unknown directive value")
        getattr(self, "_{}".format(directive))()

    def _admin(self):
        match_queue = [r'db, migrate$', r"'db', MigrateCommand\)$"]
        imp_stmnt = "from {proj_name}.admin.commands import UserAdminCommand"\
            .format(proj_name=self.config.project_name)
        mgr_cmd = "manager.add_command('user', UserAdminCommand)"
        inject_queue = [imp_stmnt, mgr_cmd]
        current_search = match_queue.pop(0)
        current_inject = inject_queue.pop(0)
        for line in self.read_target():
            if current_search is not None:
                if re.search(current_search, line) is not None:
                    line = "{line_in}{linesep}{injected_code}"\
                        .format(line_in=line, linesep=os.linesep,
                                injected_code=current_inject)
                    if len(match_queue) > 0:
                        current_search = match_queue.pop(0)
                        current_inject = inject_queue.pop(0)
                    else:
                        current_search = None
            print(line, file=self.stream)
        with open(self.target_file, 'w') as new_manage:
            new_manage.write(self.stream.getvalue())


class FactoryInjector(InjectorBase):
    """
    Responsible for registering extensions and blueprints with an app factory
    """
    def __init__(self):
        super(FactoryInjector, self).__init__()
        self.target_file = self.config.factory_path

    def inject(self, directive, name=None):
        """
        The method responsible for injecting code snippets into the app factory
        file.

        :param str directive:
            a key that is used to look up known directives on how to inject code
            into an app factory. I decided to keep file hacks contained rather
            than dynamically through the method.
        """
        known_directives = ['admin', 'blueprint', 'api']
        if directive not in known_directives:
            raise ValueError("FactoryInjector:Unknown value for directive")
        if directive == 'blueprint' and name is not None:
            injection_context = self._blueprint(name)
        else:
            injection_context = getattr(self, "_{}".format(directive))()
        content = open(self.target_file, 'r').read()
        inject_line = "{linesep}{stmt}"
        for section in re.split(r'\n\n', content):
            if re.search(r'import', section) is not None:
                for imp_stmt in injection_context['import']:
                    section += inject_line.format(linesep=os.linesep,
                                                  stmt=imp_stmt)
                print(section, file=self.stream)
            elif re.search(r'def register_extensions', section) is not None \
                    and 'extension' in injection_context:
                for ext_stmt in injection_context['extension']:
                    section += inject_line.format(linesep=os.linesep,
                                                  stmt=ext_stmt)
                print(os.linesep + section, file=self.stream)
            elif re.search(r'def register_blueprints', section) is not None \
                    and 'blueprint' in injection_context:
                section += inject_line\
                    .format(linesep=os.linesep,
                            stmt=injection_context['blueprint'])
                print(os.linesep + section, file=self.stream)
            else:
                print(os.linesep + section, file=self.stream)
        with open(self.target_file, 'w') as init_file:
            init_file.write(self.stream.getvalue().rstrip())

    def _admin(self):
        project_name = self.config.project_name
        injection_directive = {
            'import': [
                "from {proj_name}.admin.views import admin"
                .format(proj_name=project_name),
                "from {proj_name}.admin.auth import login_manager, principals"
                .format(proj_name=project_name)
            ],
            'extension': [
                "{}principals.init_app(app)".format(self.indent),
                "{}login_manager.init_app(app)".format(self.indent),
                "{}admin.init_app(app)".format(self.indent)
            ]
        }
        return injection_directive

    def _blueprint(self, name):
        project_name = self.config.project_name
        injection_directive = {
            'import': [
                "from {proj_name}.{bp_name}.views import {bp_name}"
                .format(proj_name=project_name, bp_name=name)
            ],
            'blueprint':
                "{ndnt}app.register_blueprint({bp_nm}, url_prefix='/{bp_nm}')"
                .format(ndnt=self.indent, bp_nm=name)
        }
        return injection_directive

    def _api(self):
        # only responsible for including api
        pass


class SettingsInjector(InjectorBase):
    """Injects attributes into the Config object"""
    def __init__(self):
        super(SettingsInjector, self).__init__()
        self.target_file = self.config.settings

    def inject(self, directive, section='DevConfig'):
        known_directives = ['mail', 'flat_pages']
        if directive not in known_directives:
            raise ValueError('SettingsInjector:Uknown directive for injection')
        injection_context = getattr(self, "_{}".format(directive))()
        # make sure that there is 2 spaces between each class!
        watching, linesep = False, os.linesep
        for src_line in self.read_target():
            if watching:
                if src_line == '':
                    self.stream.writelines(["{}{}{}".format(self.indent,
                                                            line,
                                                            linesep)
                                            for line in injection_context])
            if re.search(section, src_line):
                watching = True
            self.stream.write("{}{linesep}".format(src_line, linesep))

    def _mail(self):
        """
        This targets the general Config object
        """
        pass

    def _flat_pages(self):
        injection_directive = [
            "FLATPAGES_ROOT = path.join('${proj_name}', 'articles')"
            .format(self.config.project_name),
            "FLATPAGES_AUTO_RELOAD = DEBUG",
            "FLATPAGES_EXTENSION = '.md'",
            "FLATPAGES_ENCODING = 'utf8'"
        ]
        return injection_directive


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
