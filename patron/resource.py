# -*- coding: utf-8 -*-
from __future__ import print_function
from os import path, linesep
import sys
from cookiecutter.generate import generate_files
from . import config
from .helpers import is_name_valid, get_scaffold, create_context, get_stream
from .injectors import factory_blueprint


def resource_exists(resource_name):
    path_to_check = path.join(config.get_project_name(), resource_name)
    return True if path.exists(path_to_check) else False


def create_blueprint(name, routes=None):
    # if not is_name_valid(name):
    #     raise StandardError("'{}' is an invalid name".format(name))
    # if resource_exists(name):
    #     raise OSError("Blueprint '{}' already exists".format(name))
    # scaffold = get_scaffold('blueprint')
    # context = create_context('blueprint')
    # context['cookiecutter']['blueprint_name'] = name
    # context['cookiecutter']['project_name'] = config.get_project_name()
    # generate_files(repo_dir=scaffold, context=context)
    if routes:
        # create templates along with extra routes?
        # view_filename = path.join(config.get_project_name(), name, 'views.py')
        content = parse_blueprint_routes(name, routes)
        print(content)
        # with open(view_filename, 'at') as view_file:
        #     view_file.write(content)
    # if admin addon was added, include admin.py
    # factory_blueprint(name.lower())


def parse_blueprint_routes(blueprint_name, routes):
    # route_name:methods:variable-type
    # ex: should be able to work with just the name
    # @name.route('/route_name/<type:variable>', methods=[])
    # def name(variable):
    #     return render_template
    stream = get_stream()
    for route in routes:
        route = route.lower()
        print(linesep, file=stream)
        route_statement = build_route_statement(blueprint_name, route)
        handler_def, handler_body = build_route_handler(route)
        for stmt in (route_statement, handler_def, handler_body):
            print(stmt, file=stream)
        print(linesep, file=stream)
    content = stream.getvalue()
    stream.close()
    return content


def build_route_statement(blueprint_name, route):
    def get_variable_format(variable=None):
        if '-' in variable:
            var, var_type = variable.split('-')
            if var_type in ('int', 'float', 'path'):
                var_format = "<{}:{}>".format(var_type, var)
        else:
            var_format = "<{}>".format(variable)
        return var_format

    def get_methods_format(method=None):
        route_methods = ('GET', 'POST', 'PUT', 'DELETE')
        if '-' in method:
            method = method.split('-')

    if ':' in route:
        route_stmt = "@{bp_nm}.route('/{route_name}{variables}'{methods})"
    else:  # just the name was supplied
        route_data = dict(bp_nm=blueprint_name, route)
        route_stmt = "@{bp_nm}.route('/{route_name}')"
    return route_stmt.format(**route_data)


def build_route_handler(route):
    # need to return (definition, body)
    # func_stmt = "def {route_name}({variables}):{linesep}"
    #     return render_template('{route_name}.jade')
    # does not care about methods
    body_stmt = "{indent}return render_template('{route_name}.jade')"
    if ':' in route:
        rt = route.split(':')
        # need route_name
        # need variable names only
        # ignore methods
        pass
    else:  # just the name was supplied
        def_stmt = "def {route_name}():".format(route_name=route)
        def_data = dict(route_name=route)
        body_data = dict(route_name=route, indent=" " * 4)
    return (def_stmt.format(**def_data), body_stmt.format(**body_data))


def create_package(name, options):
    # options: -m(odel), -f(orms), -a(dmin), -c(ommands)
    # all inclusive unless explicit
    # admin being the exception... has to be added
    pass
