# -*- coding: utf-8 -*-
import os
from os import path
from string import Template
from . import CodeInspector, is_name_valid, get_templates_dir


class TaskGenerator(object):
    """Generate tasks for use with fabric"""
    def __init__(self, name, description):
        if not is_name_valid(name):
            raise StandardError("Invalid name supplied to TaskGenerator")
        self.name = name.lower()
        self.description = description

    def create(self):
        if not path.exists('fabfile.py'):
            # FileNotFoundError in 3.4
            raise OSError("fabfile.py does not exist in this directory")
        if CodeInspector.has_collision('fabfile.py', self.name):
            raise StandardError("Task already exists in fabfile")
        template_root = path.join(get_templates_dir(), 'task')
        source_template_file = path.join(template_root, 'task_template.txt')
        template = Template(open(source_template_file, 'r').read())
        template_data = dict(task_name=self.name,
                             task_description=self.description)
        task_contents = os.linesep + template.safe_substitute(**template_data)
        with open('fabfile.py', 'a') as fabfile:
            fabfile.write(task_contents)
