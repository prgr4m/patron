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


def factory_api():
    context = {
        'import': [
            "from .api import api"
        ],
        'blueprint':
            "{}app.register_blueprint(api, url_prefix='/api')".format(indent)

    }
    factory(context)


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


def admin(directive):
    # for adding and registering model views
    pass


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
        if re.search(r'api = Blueprint', section):
            section += os.linesep
        if section.rstrip() == '':
            continue
        print(section, file=stream, sep=separator)
    print(template.safe_substitute(**tpl_data), file=stream)
    with io.open(target_file, 'wt') as new_target_file:
        new_target_file.write(stream.getvalue())
    stream.close()


def settings(content):
    stream = get_stream()
    with io.open(config.get_settings_file(), 'wt') as settings_file:
        settings_file.write(content)
    stream.close()
