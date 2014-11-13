# -*- coding: utf-8 -*-
from __future__ import print_function
import io
from os import path
import sys
from . import config
from .helpers import get_stream
from .resource import resource_exists

indent = " " * 4


def create_form(blueprint_name, form_name, form_fields, validators):
    if not resource_exists(blueprint_name):
        error_msg = "Blueprint '{}' does not exist"
        raise StandardError(error_msg.format(blueprint_name))
    target_filename = path.join(config.get_project_name(), blueprint_name,
                                'forms.py')
    if not path.exists(target_filename):
        error_message = "'forms.py' does not exist in blueprint '{}'"
        raise OSError(error_message.format(blueprint_name))
    stream = get_stream()
    sys.stdout = stream
    form(form_name)
    parse_form_fields(form_fields):
    if validators:
        print(u"")
        create_validation_methods(form_fields):
    with io.open(target_filename, 'at') as outfile:
        outfile.write(stream.getvalue())
    stream.close()
    sys.stdout = sys.__stdout__
    print(u"Created {} form at {}".format(form_name, target_filename))


def form(form_name):
    form_def = u"class {}(Form):".format(form_name)
    print(u"")
    print(u"")
    print(form_def)


def get_known_fields():
    form_field_map = {
        'bool': 'BooleanField',
        'date': 'DateTimeField',
        'file': 'FileField',
        'float': 'FloatField',
        'int': 'IntegerField',
        'radio': 'RadioField',
        'select': 'SelectField',
        'multi': 'SelectMultipleField',
        'submit': 'SubmitField',
        'string': 'StringField',
        'hidden': 'HiddenField',
        'pass': 'PasswordField',
        'text': 'TextAreaField',
        'form': 'FormField',
        'field': 'FieldList'
    }
    return form_field_map


def parse_form_fields(form_fields):
    pass


def create_validation_method(form_fields):
    validation_def = u"{indent}def validate_{field_name}(form, field):"
    validation_body = u"{indent}{indent}pass"
    for field in form_fields:
        if ':' not in field:
            continue
        field_name = field.split(':')[0].lower()
        print(u"")
        print(validation_def.format(indent=indent, field_name=field_name))
        print(validation_body.format(indent=indent))
