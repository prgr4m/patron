# -*- coding: utf-8 -*-
from __future__ import print_function
import cStringIO
from contextlib import contextmanager
# import os
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

    def create(self, fields):
        with self._model():
            for field in self._parse_fields(fields):
                print(field)
        self._serialize()
        template_root = path.join(get_templates_dir(), 'model')
        fname_fmt = "test_{model_name}_model.py"\
            .format(model_name=self.name.lower())
        test_filename = path.join('tests', fname_fmt)
        template_file = {
            'unittest.py': [
                dict(project_name=self.config.project_name,
                     blueprint_name=self.namespace,
                     model_name=self.name),
                test_filename
            ]
        }
        generate_templates(template_root, template_file)

    def _parse_fields(self, fields):
        col_stmt_def = "{indent}{name} = db.Column({field_type})"
        rel_stmt_def = "{indent}{name} = db.relationship({relation_defintion})"
        for field in fields:
            if ':' not in field:
                continue
            attribs = field.split(':')
            if attribs[1] == 'relationship':
                data = dict(indent=self.indent, name=attribs[0])
                # need to walk through the attributes
                # one-to-one
                # db.relationship('ClassName', backref='name', uselist=False)
                #
                # one-to-many
                # class and backref
                # class, backref-name-lazy_type,
                # lazy-{select,joined,subquery,dynamic}
                #
                # many-to-many
                # class, secondary-table_name, backref-name-lazy_type
                field_def = rel_stmt_def.format(**data)
            else:
                f_map = ModelGenerator.get_known_fields(mode="all")
                user_field_type = attribs[1].split('-')[0] if '-' in attribs[1]\
                    else attribs[1].split('-')[0]
                if user_field_type not in f_map:
                    raise KeyError("ModelGenerator:Unknown field type given")
                f_name = attribs[0]
                # setup default values for a type if it isn't present...
                field_type = attribs[1]
                if '-' in field_type:
                    f_info = field_type.split('-')
                    f_type = "{}({})".format(f_map[f_info[0]], f_info[1])
                elif field_type == 'string':
                    f_type = "{}({})".format(f_map[field_type], 50)
                else:
                    f_type = f_map[attribs[1]]
                if len(attribs) > 2:
                    working_attribs = attribs[2:]
                    for attr in working_attribs:
                        if attr in ['index', 'nullable', 'unique']:
                            f_type = "{}, {}=True".format(f_type, attr)
                        elif '-' in attr and attr.split('-')[0] == 'default':
                            default_value = attr.split('-')[1]
                            f_type = "{}, default={}".format(f_type, default_value)
                        elif '-' in attr and attr.split('-')[0] == 'foreign':
                            reference = attr.split('-')[1]
                            f_type = "{}, db.ForeignKey('{}')".format(f_type,
                                                                    reference)
                        else:
                            continue
                field_def = col_stmt_def.format(indent=self.indent,
                                                name=f_name,
                                                field_type=f_type)
            yield field_def

    @contextmanager
    def _model(self):
        model_def = "class {}(db.Model):".format(self.name)
        table_def = "{}__tablename__ = '{}'".format(self.indent,
                                                    self.name.lower())
        id_def = "{}id = db.Column(db.Integer, primary_key=True)"\
            .format(self.indent)
        print()
        print(model_def)
        print(table_def)
        print(id_def)
        yield
        print()
        print("{}def __str__(self):".format(self.indent))
        print("{}pass".format(self.indent * 2))
        print()
        print("{}def __repr__(self):".format(self.indent))
        print("{}return \"<{}: Customize me!>\"".format(self.indent * 2,
                                                        self.name))
        print()

    @staticmethod
    def get_known_fields(mode='keys'):
        field_map = {
            'smallint': 'db.SmallInteger',
            'integer': 'db.Integer',
            'bigint': 'db.BigInteger',
            'string': 'db.String',
            'text': 'db.Text',
            'date': 'db.Date',
            'datetime': 'db.DateTime',
            'time': 'db.Time',
            'enum': 'db.Enum',
            'float': 'db.Float',
            'numeric': 'db.Numeric',
            'bool': 'db.Boolean',
            'binary': 'db.LargeBinary',
            'pickle': 'db.PickleType',
            'unicode': 'db.Unicode',
            'unitext': 'db.UnicodeText'
        }
        if mode == 'keys':
            return field_map.keys()
        return field_map

    def _serialize(self):
        with open(self.output_target, 'a') as outfile:
            outfile.write(self.stream.getvalue())
