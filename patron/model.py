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
        for field in parse_model_fields(fields):
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


def parse_model_fields(fields):
    col_stmt_def = u"{indent}{name} = db.Column({field_type}{column_attrs})"
    field_map = get_known_fields(mode="all")
    for field in fields:
        if ':' not in field:  # just the name and column definition
            field_name = field.replace('-', '_') if '-' in field else field
            col_data = dict(indent=indent, name=field_name, field_type='',
                            column_attrs='')
            yield col_stmt_def.format(**col_data)
        attribs = field.split(':')
        field_name = attribs.pop(0).replace('-', '_')
        alchemy_raw = attribs.pop(0)  # check to see if it has a default value
        alchemy_type = alchemy_raw.split('-')[0] if '-' in alchemy_raw \
            else alchemy_raw
        if alchemy_type not in field_map:
            # just the name and column definition because of unknown type
            col_data = dict(indent=indent, name=field_name, field_type='',
                            column_attrs='')
            yield col_stmt_def.format(**col_data)
        col_data = dict(name=field_name)
        field_type_def = u"{field_type}({field_defaults})"
        field_type_data = dict(field_type=field_map[alchemy_type])
        if '-' in alchemy_raw:
            field_default_data = alchemy_raw.split('-')[1:]
            alchemy_type_defaults = []
            for field_data in field_default_data:
                if isinstance(field_data, str) and not field_data.isdigit():
                    alchemy_type_defaults.append("'%s'" % field_data)
                else:
                    alchemy_type_defaults.append(field_data)
            field_type_data['field_defaults'] = ", ".join(alchemy_type_defaults)
        else:
            field_type_data['field_defaults'] = ''
        col_data['field_type'] = field_type_def.format(field_type_data)
        if not attribs:
            col_data['column_attrs'] = ''
        else:
            column_keywords = {
                'index': u"index={value}",
                'nullable': u"nullable={value}",
                'unique': u"unique={value}",
                'default': u"default={value}"
            }
            parsed_col_attr = []
            for attrib in attribs:
                attr, attr_val = attrib.split('-') if '-' in attrib \
                    else (attrib, True)
                if attr not in column_keywords:
                    continue
                if isinstance(attr_val, str) and not attr_val.isdigit():
                    attr_val = "'%s'" % attr_val
                parsed_col_attr.append(column_keywords[attr]
                                       .format(value=attr_val))
            col_data['column_attrs'] = ", " + ", ".join(parsed_col_attr) \
                if parsed_col_attr else ''
        yield col_stmt_def.format(**col_data)


def parse_relations(relations):
    # name:Class:backref_name:lazy-type
    # name:Class:secondary-table_ref:backref-reference_name-lazy_type
    # lazy_types = ('select', 'joined', 'subquery', 'dynamic')
    # rel_stmt_def = "{indent}{name} = db.relationship({relation_definition})"
    # secondary_def = "secondary={}"
    # backref_def = "backref=db.backref('{}', lazy='{}')"
    # for rel in relations:
    #     if ':' not in relations:
    #         continue
    #     attribs = relations.split(':')
    pass
