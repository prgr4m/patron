# -*- coding: utf-8 -*-
import os
import os.path as path
import shutil
import fnmatch
from . import (StencilConfig, is_name_valid, get_templates_dir,
               generate_templates)
from .injectors import FactoryInjector


class BlueprintGenerator(object):
    """Generates Blueprints"""
    def __init__(self, name):
        if is_name_valid(name):
            self.name = name
        else:
            raise StandardError("Name given for the blueprint is invalid")
        self.config = StencilConfig()
        if self.config.has_blueprint(name):
            raise StandardError("Blueprint already exists")
        path_check = path.join(self.config.project_name, self.name)
        if path.exists(path_check):
            raise OSError("Blueprint already exists")

    def create(self):
        project_root = os.getcwd()
        template_root = path.join(get_templates_dir(), 'blueprint')
        os.chdir(self.config.project_name)
        os.makedirs(path.join(self.name, 'templates'))
        open(path.join(self.name, '__init__.py'), 'w').close()
        for f in [x for x in os.listdir(template_root)
                  if x not in ['.', '..', 'unittest.py']]:
            if fnmatch.fnmatch(f, '*.jade'):
                shutil.copyfile(path.join(template_root, f),
                                path.join(self.name.lower(), 'templates', f))
            elif f == 'views.py':
                template_file = {
                    f: [
                        dict(blueprint_name=self.name.lower()),
                        path.join(self.name.lower(), f)
                    ]
                }
                generate_templates(template_root, template_file)
            else:
                shutil.copyfile(path.join(template_root, f),
                                path.join(self.name.lower(), f))
        os.chdir(project_root)
        blueprint_data = {
            'forms': path.join(self.config.project_name,
                               self.name.lower(), 'forms.py'),
            'models': path.join(self.config.project_name,
                                self.name, 'models.py'),
            'views': path.join(self.config.project_name,
                               self.name.lower(), 'views.py')
        }
        self.config.create_blueprint(self.name, blueprint_data)
        template_file = {
            'unittest.py': [
                dict(project_name=self.config.project_name,
                     blueprint_name=self.name.capitalize()),
                path.join('tests',
                          "test_{}_blueprint.py".format(self.name.lower()))
            ]
        }
        generate_templates(template_root, template_file)
        FactoryInjector().inject('blueprint', self.name.lower())
