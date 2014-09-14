# -*- coding: utf-8 -*-
from __future__ import print_function
import cStringIO
from contextlib import contextmanager
import os
import os.path as path
import sys
from . import (StencilConfig, CodeInspector, is_name_valid, get_templates_dir,
               generate_templates)


class ModelGenerator(object):
    """Basic model generation"""

    indent = " " * 4

    def __init__(self, namespace, name):
        self.config = StencilConfig()
        if not self.config.has_blueprint(namespace):
            raise OSError("ModelGenerator:Blueprint doesn't exist")
        for key, val in self.config.get_blueprint_info(namespace):
            if key == 'models':
                self.namespace = namespace
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
        template_root = path.join(get_templates_dir(), 'model')
        test_filename = path.join('tests',
                                  "test_{model_name}_model.py"\
                                    .format(model_name=self.name))
        template_file = {
            'unittest.py': [
                dict(project_name=self.config.project_name,
                     blueprint_name=self.namespace,
                     model_name=self.name),
                test_filename
            ]
        }
        generate_templates(template_root, template_file)

    def _parse_fields(self, *fields):
        field_stmt_def = "{indent}{name} = db.Column({field_type}){linesep}"
        # for the time being its only name:field_type and only supporting basic
        # types: integer, string(size), text, datetime, float, boolean
        #
        # eventually I'll add more (like length - if applicable) and parameters
        # passed to the Column definition...
        # also, I could just create an empty column for custom types or for
        # defining relationships between models
        for field in fields:
            if ':' not in field:
                # debating on just giving name and making empty column or for
                # defining a relationship field... for now I just want to make
                # this work and then I'll refine it...
                continue
            # else:  # for later when I add the new features
            attribs = field.split(':')

            # look up type and inject to field_type
            field_def = field_stmt_def.format(indent=self.indent,
                                              name=None,
                                              field_type=None,
                                              linesep=os.linesep)
            yield field_def

    @contextmanager
    def _model(self):
        model_def = "class {}(db.Model):".format(self.name)
        table_def = "{}__tablename__ = '{}'".format(self.indent, self.name)
        id_def = "{}id = db.Column(db.Integer, primary_key=True)"\
            .format(self.indent)
        print(os.linesep)
        print(model_def + os.linesep)
        print(table_def + os.linesep)
        print(id_def + os.linesep)
        yield
        print(os.linesep)
        print("def __str__(self):" + os.linesep)
        print("{}pass".format(self.indent) + os.linesep)
        print(os.linesep)
        print("def __repr__(self):" + os.linesep)
        print("{}return \"<{}: Customize me!>\"".format(self.indent,
                                                        self.name))
        print(os.linesep)

    def get_known_fields(self):
        field_map = {
            'smallint': 'db.SmallInteger',
            'integer': 'db.Integer',
            'bigint': 'db.BigInteger'
            'string': 'db.String(50)',
            'text': 'db.Text',
            'date': 'db.Date',
            'datetime': 'db.DateTime',
            'time': 'db.Time()',
            'enum': 'db.Enum()',
            'float': 'db.Float()',
            'numeric': 'db.Numeric()',
            'bool': 'db.Boolean()',
            'binary': 'db.LargeBinary()',
            'pickle': 'db.PickleType()',
            'unicode': 'db.Unicode()',
            'unitext': 'db.UnicodeText()'
        }
        return field_map

    def _serialize(self):
        with open(self.output_target, 'a') as outfile:
            outfile.write(self.stream.getvalue())
