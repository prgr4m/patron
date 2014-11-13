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
    parse_form_fields(form_fields)
    if validators:
        print(u"")
        create_validation_method(form_fields)
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


def parse_form_fields(form_fields):
    form_field_map = {
        'bool': 'BooleanField',
        'date': 'DateTimeField',
        'file': 'FileField',
        'float': 'FloatField',
        'integer': 'IntegerField',
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
    field_def = u"{indent}{field_name} = {wtform_def}"
    wtform_def = u"{field_type}(u'{field_label}'{field_extras})"
    for field in form_fields:
        if ':' not in field:
            continue
        # name:field_type:label|extra*
        field_data = field.split(':')
        field_name = field_data.pop(0)
        field_type = field_data.pop(0)  # check the type
        if field_type not in form_field_map:
            continue
        field_type = form_field_map[field_type]
        if field_data:
            # check if first_element is label; if not create it and parse
            for f_data in field_data:
                pass
        else:  # create the label and close field definition
            field_label = field_name.capitalize()
            wtform_def_data = dict(field_type=field_type,
                                   field_label=field_label, field_extras='')
            wtform_data = wtform_def.format(**wtform_def_data)
            field_def_data = dict(indent=indent, field_name=field_name,
                                  wtform_def=wtform_data)
        print(field_def.format(**field_def_data))


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
