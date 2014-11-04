# -*- coding: utf-8 -*-
from __future__ import print_function
from contextlib import contextmanager
# import os
from os import path
import sys
from ..config import PatronConfig
from .helpers import (CodeInspector, is_name_valid, get_templates_dir,
                      generate_templates)

try:
    from io import StringIO
except ImportError:
    from cStringIO import StringIO

ORM_TYPES = ('sqlalchemy', 'peewee')
ADAPTER_TYPES = ('sqlite', 'postgres', 'mysql')


class ModelGenerator(object):
    """Basic model generation"""

    indent = " " * 4

    def __init__(self, namespace, name):
        """
        Constructor
        :raises StandardError:
            when a blueprint isn't registered with Stencil
        :raises ValueError:
            when an invalid name is used when creating a model
        :raises TypeError:
            when a model already exists in the blueprint model file
        """
        self.config = PatronConfig()
        if not self.config.has_blueprint(namespace):
            raise StandardError("ModelGenerator:Blueprint doesn't exist")
        # check filesystem for namespace/models.py
        self.namespace = namespace
        self.output_target = path.join(self.config.project_name,
                                       namespace, 'models.py')
        if not is_name_valid(name):
            raise ValueError("ModelGenerator:Model name is invalid")
        self.name = name.capitalize()
        if CodeInspector.has_collision(self.output_target, self.name):
            raise TypeError("ModelGenerator:Model already exists")
        self.stream = StringIO()
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
        print("Generated unittest at {}".format(test_filename))

    def _parse_fields(self, fields):
        """
        :raises ValueError:
            when establishing a relation and not enough params have
            been supplied
        """
        col_stmt_def = "{indent}{name} = db.Column({field_type})"
        rel_stmt_def = "{indent}{name} = db.relationship({relation_definition})"
        for field in fields:
            if ':' not in field:
                continue
            attribs = field.split(':')
            if attribs[1] == 'relation':
                data = dict(indent=self.indent, name=attribs[0])
                if len(attribs) < 3:
                    err = "Need at minimum a class and backref"
                    raise ValueError("ModelGenerator:{}".format(err))
                relation_definition = "'{class_name}', {rel_def}"
                rel_data = dict(class_name=attribs[2])
                lazy_keywords = ('select', 'joined', 'subquery', 'dynamic')
                r_def = []
                for attr in attribs[3:]:
                    if attr.startswith('backref-'):
                        b_ref = attr.split('-')[1:]
                        ref_def = "backref=db.backref('{}', lazy='{}')"
                        if len(b_ref) == 1:
                            lazy_type = 'dynamic'
                        else:
                            lazy_type = b_ref[1]
                        r_def.append(ref_def.format(b_ref[0], lazy_type))
                    elif attr.startswith('lazy-'):
                        lazy_type = attr.split('-')[1]
                        if lazy_type not in lazy_keywords:
                            r_def.append("lazy='dynamic'")
                        else:
                            r_def.append("lazy='{}'".format(lazy_type))
                    elif attr.startswith('secondary-'):
                        r_def.append("secondary={}".format(attr.split('-')[1]))
                    else:
                        if attr == 'uselist':
                            r_def.append("uselist=False")
                        else:
                            r_def.append("backref='{}'".format(attr))
                rel_data['rel_def'] = ', '.join(r_def)
                data['relation_definition'] = relation_definition\
                    .format(**rel_data)
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
                            f_type = "{}, default={}"\
                                .format(f_type, default_value)
                        elif '-' in attr and attr.split('-')[0] == 'foreign':
                            reference = attr.split('-')[1]
                            f_type = "{}, db.ForeignKey('{}')"\
                                .format(f_type, reference)
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
        print("Created {} model at {}".format(self.name, self.output_target),
              file=sys.__stdout__)
