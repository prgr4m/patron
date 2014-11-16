# -*- coding: utf-8 -*-
from __future__ import print_function
import codecs
import io
import os
from os import path
from string import Template
import re
from . import config
from .helpers import get_stream, get_scaffold

indent = " " * 4


def read_target(target_file):
    for line in codecs.open(target_file, 'r', encoding='utf-8'):
        yield line.rstrip()


def factory(context):
    stream = get_stream()
    content = io.open(config.get_factory_file(), 'rt').read()
    inject_line = "{linesep}{stmt}"
    separator = u"{linesep}{linesep}".format(linesep=os.linesep)
    for section in re.split(separator, content):
        if re.search(r'import', section) is not None:
            for imp_stmt in context['import']:
                section += inject_line.format(linesep=os.linesep, stmt=imp_stmt)
            print(section, file=stream)
        elif re.search(r'def register_extensions', section) is not None \
                and 'extension' in context:
            for ext_stmt in context['extension']:
                section += inject_line.format(linesep=os.linesep, stmt=ext_stmt)
            print(os.linesep + section, file=stream)
        elif re.search(r'def register_blueprints', section) is not None \
                and 'blueprint' in context:
            section += inject_line.format(linesep=os.linesep,
                                          stmt=context['blueprint'])
            print(os.linesep + section, file=stream)
        else:
            print(os.linesep + section, file=stream)
    with io.open(config.get_factory_file(), 'wt') as new_factory:
        new_factory.write(stream.getvalue().rstrip())
    stream.close()


def factory_blueprint(name):
    context = {
        'import': [
            "from .{bp_name}.views import {bp_name}".format(bp_name=name)
        ],
        'blueprint':
            "{ndnt}app.register_blueprint({bp_name}, url_prefix='/{bp_name}')"
            .format(ndnt=indent, bp_name=name)
    }
    factory(context)
    print(u"Registered {} blueprint with app".format(name))


def factory_admin():
    context = {
        'import': [
            "from .admin.views import admin"
        ],
        'extension': [
            "{}admin.init_app(app)".format(indent)
        ]
    }
    factory(context)
    print(u"Registered admin with app")


def factory_api():
    context = {
        'import': [
            "from .api import api"
        ],
        'blueprint':
            "{}app.register_blueprint(api, url_prefix='/api')".format(indent)

    }
    factory(context)
    print(u"Registered api blueprint with app")


def factory_users():
    context = {
        'import': [
            "from .users.auth import login_manager, principals",
            "from .users.views import users"
        ],
        'extension': [
            "{}principals.init_app(app)".format(indent),
            "{}login_manager.init_app(app)".format(indent),
        ],
        'blueprint':
            "{}app.register_blueprint(users, url_prefix='/users')"
            .format(indent)
    }
    factory(context)
    print(u"Registered users with app")


def manage(stream_in):
    with io.open('manage.py', 'wt') as new_manage:
        new_manage.write(stream_in.getvalue())
    stream_in.close()


def manage_users():
    stream = get_stream()
    match_queue = [r'db, migrate$', r"'db', MigrateCommand\)$"]
    imp_stmt = "from {proj_name}.users.commands import UserAdminCommand"\
        .format(proj_name=config.get_project_name())
    mgr_cmd = "manager.add_command('user', UserAdminCommand)"
    inject_queue = [imp_stmt, mgr_cmd]
    current_search = match_queue.pop(0)
    current_inject = inject_queue.pop(0)
    for line in read_target('manage.py'):
        if current_search is not None:
            if re.search(current_search, line) is not None:
                line = u"{line_in}{linesep}{injected_code}"\
                    .format(line_in=line, linesep=os.linesep,
                            injected_code=current_inject)
                if len(match_queue) > 0:
                    current_search = match_queue.pop(0)
                    current_inject = inject_queue.pop(0)
                else:
                    current_search = None
        print(line, file=stream)
    manage(stream)
    print(u"Injected user commands with manage.py")


def admin(context):
    stream = get_stream()
    target_file = path.join(config.get_project_name(), 'admin', 'views.py')
    contents = io.open(target_file, 'rt').read()
    separator = u"{linesep}{linesep}".format(linesep=os.linesep)
    import_stmt = u"from ..{}.admin import".format(context['resource_name'])
    watch_import = True
    for section in re.split(separator, contents):
        if re.search(import_stmt, section) is not None and watch_import:
            sep = os.linesep
            imports = section.split(sep)
            for index, line in enumerate(imports):
                if import_stmt in line:
                    model_name = context['modelview']
                    imports[index] = line + ", %sModelView" % model_name
            section = u"{}".format(sep).join(imports)
            watch_import = False
        elif re.search(r'import', section) and watch_import:
            new_import = "{linesep}{import_stmt} {name}ModelView"
            import_data = dict(linesep=os.linesep, import_stmt=import_stmt,
                               name=context['modelview'])
            section += new_import.format(**import_data)
            watch_import = False
        elif section.rstrip() == '':
            continue
        else:
            section = os.linesep + section
        print(section, file=stream)
    add_view_stmt = u"admin.add_view(%sModelView())" % context['modelview']
    print(add_view_stmt, file=stream)
    with io.open(target_file, 'wt') as new_admin:
        new_admin.write(stream.getvalue().rstrip())
    stream.close()
    print(u"{}ModelView was registered with the admin"
          .format(context['modelview']))


def model_admin_py(resource_name, model_name):
    context = {
        'resource_name': resource_name,
        'modelview': model_name
    }
    admin_py = path.join(config.get_project_name(), resource_name, 'admin.py')
    scaffold = get_scaffold('model')
    tpl_file = path.join(scaffold, 'admin_inject.txt')
    tpl_data = dict(model_name=model_name)
    template = Template(io.open(tpl_file, 'rt').read())
    stream = get_stream()
    separator = u"{linesep}{linesep}".format(linesep=os.linesep)
    admin_py_contents = io.open(admin_py, 'rt').read()
    import_statement = r'from .models import'
    watch_import = True
    for section in re.split(separator, admin_py_contents):
        if re.search(import_statement, section) is not None and watch_import:
            model_append = ", %s" % model_name
            section += model_append
            watch_import = False
        elif re.search(r'import', section) is not None and watch_import:
            section += "{linesep}from .models import {name}{linesep}"\
                .format(linesep=os.linesep, name=model_name)
            watch_import = False
        if section.rstrip() == '':
            continue
        else:
            section += os.linesep
        print(section, file=stream, sep=separator)
    print(template.safe_substitute(**tpl_data), file=stream)
    with io.open(admin_py, 'wt') as new_admin_py:
        new_admin_py.write(stream.getvalue())
    stream.close()
    print(u"Auto generated {}ModelView for model".format(model_name))
    admin(context)


def api_injector(name):
    stream = get_stream()
    import_def = u"{linesep}from .{name_lower} import {name}Resource{linesep}"\
        .format(linesep=os.linesep, name=name, name_lower=name.lower())
    tpl_data = dict(name=name, name_lower=name.lower())
    scaffold = get_scaffold('api')
    tpl_file = path.join(scaffold, 'api_inject.txt')
    template = Template(io.open(tpl_file, 'rt').read())
    target_file = path.join(config.get_project_name(), 'api', '__init__.py')
    watch_import = True
    contents = io.open(target_file, 'rt').read()
    separator = u"{linesep}{linesep}".format(linesep=os.linesep)
    for section in re.split(separator, contents):
        if re.search(r'import', section) is not None and watch_import:
            section += import_def
            watch_import = False
        if section.rstrip() == '':
            continue
        else:
            section += os.linesep
        print(section, file=stream, sep=separator)
    print(template.safe_substitute(**tpl_data), file=stream)
    with io.open(target_file, 'wt') as new_target_file:
        new_target_file.write(stream.getvalue())
    stream.close()
    print(u"Added {} Resource with api".format(name))


def requirements(*packages):
    project_name = config.get_project_name().lower()
    target_file = u"{}-requirements.txt".format(project_name)
    with io.open(target_file, 'at') as reqs_file:
        for pkg in packages:
            reqs_file.write(u"{}{}".format(pkg, os.linesep))
    feedback = u"The following packages were added to the requirements file: {}"
    feedback_data = ", ".join(packages)
    print(feedback.format(feedback_data))
