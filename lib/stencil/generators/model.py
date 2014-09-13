# -*- coding: utf-8 -*-
from __future__ import print_function
import cStringIO
from contextlib import contextmanager
import os
import sys
from . import StencilConfig, CodeInspector, is_name_valid


class ModelGenerator(object):
    """Basic model generation"""

    indent = " " * 4

    def __init__(self, namespace, name):
        config = StencilConfig()
        if not config.has_blueprint(namespace):
            raise OSError("ModelGenerator:Blueprint doesn't exist")
        for key, val in config.get_blueprint_info(namespace):
            if key == 'models':
                self.output_target = val
                break
        if not is_name_valid(name):
            raise ValueError("ModelGenerator:Model name is invalid")
        self.name = name.capitalize()
        if CodeInspector.has_collision(self.output_target, self.name):
            raise TypeError("ModelGenerator:Model already exists")
        self.stream = cStringIO.StringIO()
        sys.stdout = self.stream

    def __del__(self):
        self.stream.close()
        sys.stdout = sys.__stdout__

    def create(self, *fields):
        with self._model():
            for field in self._parse_fields(*fields):
                print(field)
        self._serialize()
        # create unittest
        pass

    def _parse_fields(self, *fields):
        pass

    @contextmanager
    def _model(self):
        model_def = "class {}(db.Model):".format(self.name)
        id_def = "{}id = db.Column(db.Integer, primary_key=True)"\
            .format(self.indent)
        print(os.linesep)
        print(model_def)
        print(id_def)
        yield
        print(os.linesep)
        print("def __str__(self):")
        print("{}pass".format(self.indent))
        print(os.linesep)
        print("def __repr__(self):")
        print("{}return \"<{}: Customize me!>\"".format(self.indent,
                                                        self.name))
        print(os.linesep)

    def _serialize(self):
        with open(self.output_target, 'a') as outfile:
            outfile.write(self.stream.getvalue())
