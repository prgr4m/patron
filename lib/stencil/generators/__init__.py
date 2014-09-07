# -*- coding: utf-8 -*-
from __future__ import print_function
import imp
import os.path as path
import re
from string import Template


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
    # template has to be a dictionary with a key as the actual template
    # and the value being an array in the following format:
    # 1 - a dictionary of values to be unpacked into the template
    # 2 - if applicable, the actual destination name of the template
    # ex:
    # templates = {
    #   'template_source': [
    #       dict(template_variable=value),
    #       'actual_name_on_file_once_generated' # if different from key
    #   ]
    # }
    # this method/function is ideal for batch jobs
    for template_file, data in template_files.items():
        destination_file = data[1] if len(data) > 1 else template_file
        with open(destination_file, 'w') as f:
            template_source = path.join(template_root, template_file)
            template = Template(open(template_source, 'r').read())
            f.write(template.safe_substitute(**data[0]))

__all__ = [CodeInspector, is_name_valid, get_templates_dir]
