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


def create_blueprint(name, routes=None, templates=True):
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
            # print to route_content
            # if templates:
            #     create_route_template(route_name)
            # route_stmt = "{}{}".format(linesep, )
        print(route_content.getvalue())
        # with open(view_filename, 'at') as view_file:
        #     view_file.write(route_content.getvalue())
        route_content.close()
    # if admin addon was added, include admin.py
    # factory_blueprint(name.lower())


def build_route_definition(blueprint_name, route_name, methods, variables):
    # @bp_name.route('/route_name', methods=['GET','POST'])
    route_stmt = "@{bp_name}.route('/{route_name}{variables}'{methods})"
    route_data = dict(bp_name=blueprint_name)
    # validate each part


def build_route_handler(route_parts, variables, templates):
    indent = " " * 4
    # def route_name():
    #     pass|return render_template('{route_name}.jade')
    if templates:
        body_def_stmt = "{indent}return render_template('{route_nm}.jade')"
        body_def = body_def_stmt.format(indent=indent, route_nm=route_name)
    else:
        body_def_stmt = "{indent}pass"
        body_def = body_def_stmt.format(indent=indent)
    return [route_def, body_def]


def create_route_template(route_name):
    # get scaffold directory
    # fetch route_template
    # copy over to templates directory as 'route_name'.jade
    pass


def create_package(name, options):
    # options: -m(odel), -f(orms), -a(dmin), -c(ommands)
    # all inclusive unless explicit
    # admin being the exception... has to be added
    pass
