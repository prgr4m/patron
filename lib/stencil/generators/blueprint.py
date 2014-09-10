# -*- coding: utf-8 -*-
import os
import os.path as path
from . import (StencilConfig, is_name_valid, get_templates_dir,
               generate_templates)


class BlueprintGenerator(object):
    """Generates Blueprints"""
    def __init__(self, name):
        if is_name_valid(name):
            self.name = name
        else:
            raise StandardError("Name given for the blueprint is invalid")
        self.config = StencilConfig()

