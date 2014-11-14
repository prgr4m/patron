# -*- coding: utf-8 -*-
from __future__ import print_function
import codecs
import io
import os
import re
import sys
from . import config
from .helpers import get_stream

indent = " " * 4


def read_target(target_file):
    with open(target_file, 'rt') as f:
        for line in f:
            yield line.rstrip().encode('utf-8')


def factory(context):
    stream = get_stream()
    content = io.open(config.get_factory_file(), 'rt').read()
    inject_line = "{linesep}{stmt}"
    for section in re.split(r'\n\n', content):
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
            "from .admin.views import admin",
        ],
        'extension': [
            "{}admin.init_app(app)".format(indent)
        ]
    }
    factory(context)


def factory_api():
    pass


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
    for line in codecs.open('manage.py', 'r', encoding='utf-8'):
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
    # check to see if admin addon has been added
    if 'admin' in config.addons():
        pass


def settings(content):
    stream = get_stream()
    with io.open(config.get_settings_file(), 'wt') as settings_file:
        settings_file.write(content)
    stream.close()
