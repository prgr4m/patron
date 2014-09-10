# -*- coding: utf-8 -*-
import os
import os.path as path
import shutil
import fnmatch
from . import (StencilConfig, is_name_valid, get_templates_dir,
               generate_templates)


class BlueprintGenerator(object):
    """Generates Blueprints"""
    def __init__(self, name):
        if is_name_valid(name):
            self.name = name.lower()
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
        for f in [x for x in os.listdir(template_root) if x not in ['.', '..']]:
            if fnmatch.fnmatch(f, '*.jade'):
                shutil.copyfile(path.join(template_root, f),
                                path.join(self.name, 'templates', f))
            elif f == 'views.py':
                template_file = {
                    f: [
                        dict(blueprint_name=self.name),
                        path.join(self.name, f)
                    ]
                }
                generate_templates(template_root, template_file)
            else:
                shutil.copyfile(path.join(template_root, f),
                                path.join(self.name, f))
        # hook into app factory to register the blueprint
        os.chdir(project_root)
        blueprint_data = {
            'forms': path.join(self.config.project_name, self.name, 'forms.py'),
            'models': path.join(self.config.project_name,
                                self.name, 'models.py'),
            'views': path.join(self.config.project_name, self.name, 'views.py')
        }
        self.config.create_blueprint(self.name, blueprint_data)
        # generate unittest for the blueprint
