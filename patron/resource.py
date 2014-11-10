# -*- coding: utf-8 -*-
from __future__ import print_function
from os import path, linesep
import shutil
from cookiecutter.generate import generate_files
from . import config
from .helpers import is_name_valid, get_scaffold, create_context, get_stream
from .injectors import factory_blueprint


def resource_exists(resource_name):
    path_to_check = path.join(config.get_project_name(), resource_name)
    return True if path.exists(path_to_check) else False


def create_blueprint(name, routes=None, templates=True):
    if not is_name_valid(name):
        raise StandardError("'{}' is an invalid name".format(name))
    if resource_exists(name):
        raise OSError("Blueprint '{}' already exists".format(name))
    scaffold = get_scaffold('blueprint')
    context = create_context('blueprint')
    context['cookiecutter']['blueprint_name'] = name
    context['cookiecutter']['project_name'] = config.get_project_name()
    generate_files(repo_dir=scaffold, context=context)
    if routes:
        view_filename = path.join(config.get_project_name(), name, 'views.py')
        route_content = get_stream()
        for route in routes:
            route = route.lower()
            if ':' not in route:
                continue
            route_parts = route.split(':')
            route_methods = route_parts.pop(0)
            route_name = route_parts.pop(0)
            route_vars = route_parts if len(route_parts) > 0 else None
            route_def = build_route_definition(name, route_name, route_methods,
                                               route_vars)
            route_handler = build_route_handler(route_name, route_vars,
                                                templates)
            new_route = "{}".format(linesep).join([route_def, route_handler])
            print(new_route, file=route_content)
            if templates:
                create_route_template(name, route_name)
        with open(view_filename, 'at') as view_file:
            view_file.write(route_content.getvalue())
        route_content.close()
    # if admin addon was added, include admin.py
    factory_blueprint(name.lower())


def build_route_definition(blueprint_name, route_name, methods, variables):
    http_verbs = ('GET', 'POST', 'PUT', 'DELETE')
    variable_types = ('int', 'float', 'path')
    route_stmt = "@{bp_name}.route('/{route_name}{variables}'{methods})"
    variable_prefix = "/{variables}"
    method_prefix = ", methods=[{methods}]"
    route_data = dict(bp_name=blueprint_name, route_name=route_name)
    methods = methods.upper()
    if '-' in methods:
        methods = methods.split('-')
        quote_methods = ",".join(['%s' % m for m in methods if m in http_verbs])
        route_data['methods'] = method_prefix.format(methods=quote_methods)
    elif methods in http_verbs and methods != 'GET':
        quoted_method = "'{}'".format(methods)
        route_data['methods'] = method_prefix.format(methods=quoted_method)
    else:  # just a 'GET' method
        route_data['methods'] = ''
    if variables:
        formatted_variables = []
        for variable in variables:
            if '-' in variable and variable.count('-') == 1:
                var_name, var_type = variable.split('-')
                if var_type in variable_types:
                    formatted_variables.append("<%s:%s>" % (var_type, var_name))
                else:
                    formatted_variables.append("<%s>" % var_name)
            else:
                if '-' in variable:
                    variable = variable.replace('-', '_')
                formatted_variables.append("<%s>" % variable)
        formatted_variable_data = "/".join(formatted_variables)
        route_data['variables'] = variable_prefix \
            .format(variables=formatted_variable_data)
    else:
        route_data['variables'] = ''
    return route_stmt.format(**route_data)


def build_route_handler(route_name, variables, templates):
    indent = " " * 4
    func_def_stmt = "def {route_name}({variables}):"
    func_data = dict(route_name=route_name)
    if variables:
        formatted_variables = []
        for variable in variables:
            if '-' in variable:
                variable = variable.split('-')[0]
            formatted_variables.append(variable)
        func_data['variables'] = ", ".join(formatted_variables)
    else:
        func_data['variables'] = ''
    func_def = func_def_stmt.format(**func_data)
    if templates:
        body_def_stmt = "{indent}return render_template('{route_nm}.jade')"
        body_def = body_def_stmt.format(indent=indent, route_nm=route_name)
    else:
        body_def_stmt = "{indent}pass"
        body_def = body_def_stmt.format(indent=indent)
    return "{}".format(linesep).join([func_def, body_def])


def create_route_template(blueprint_name, route_name):
    scaffold = get_scaffold('blueprint')
    src_file = path.join(scaffold, 'route_template.jade')
    project_name = config.get_project_name()
    target_file = path.join(project_name, blueprint_name, 'templates',
                            "{}.jade".format(route_name))
    shutil.copyfile(src_file, target_file)


def create_package(name, options):
    # options: -m(odel), -f(orms), -a(dmin), -c(ommands)
    # all inclusive unless explicit
    # admin being the exception... has to be added
    pass
