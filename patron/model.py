# -*- coding: utf-8 -*-
from __future__ import print_function
from contextlib import contextmanager
import io
from os import path
import sys
from . import config
from .helpers import get_stream
from .resource import resource_exists

indent = " " * 4


def create_model(blueprint_name, model_name, fields, relations):
    if not resource_exists(blueprint_name):
        error_msg = "Blueprint '{}' does not exist"
        raise StandardError(error_msg.format(blueprint_name))
    target_filename = path.join(config.get_project_name(), blueprint_name,
                                'models.py')
    if not path.exists(target_filename):
        error_message = "'models.py' does not exist in blueprint '{}'"
        raise OSError(error_message.format(blueprint_name))
    stream = get_stream()
    sys.stdout = stream
    with model(model_name):
        for field in parse_fields(fields):
            print(field)
        if relations:
            for relation in parse_relations(relations):
                print(relation)
    with io.open(target_filename, 'at') as outfile:
        outfile.write(stream.getvalue())
    stream.close()
    sys.stdout = sys.__stdout__
    print(u"Created {} model at {}".format(model_name, target_filename))


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


@contextmanager
def model(name):
    model_def = u"class {}(db.Model):".format(name)
    table_def = u"{}__tablename__ = '{}'".format(indent, name.lower())
    id_def = u"{}id = db.Column(db.Integer, primary_key=True)".format(indent)
    print()
    print(model_def)
    print(table_def)
    print(id_def)
    yield
    print()
    print(u"{}def __str__(self):".format(indent))
    print(u"{}pass".format(indent * 2))
    print()
    print(u"{}def __repr__(self):".format(indent))
    print(u"{}return \"<{}: Customize me!>\"".format(indent * 2, name))
    print()


def parse_fields(fields):
    col_stmt_def = "{indent}{name} = db.Column({field_type})"
    for field in fields:
        if ':' not in field:
            continue
        attribs = field.split(':')
        # mandatory is name:field_type


def parse_relations(relations):
    rel_stmt_def = "{indent}{name} = db.relationship({relation_definition})"
    for rel in relations:
        if ':' not in relations:
            continue
        attribs = relations.split(':')
