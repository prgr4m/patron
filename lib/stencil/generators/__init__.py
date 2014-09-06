# -*- coding: utf-8 -*-
from __future__ import print_function
import imp
import os.path as path
import re


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

__all__ = [CodeInspector, is_name_valid]
