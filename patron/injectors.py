# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import re
from . import config

indent = " " * 4


def read_target(target_file):
    with open(target_file) as f:
        for line in f:
            yield line.rstrip()


def get_stream():
    try:
        from io import StringIO
    except ImportError:
        from cStringIO import StringIO
    return StringIO()


def factory(context):
    stream = get_stream()
    content = open(config.get_factory_file(), 'r').read()
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
    with open(config.get_factory_file(), 'w') as new_factory:
        new_factory.write(stream.getvalue().rstrip())
    stream.close()


def factory_blueprint(name):
    context = {
        'import': [
            "from .{bp_name}.views import {bp_name}".format(bp_name=name)
        ],
        'blueprint':
            "{ndnt}app.register_blueprint({bp_name}, url_prefix='/{bp_nm}')"
            .format(ndnt=indent, bp_nm=name)
    }
    factory(context)


def factory_admin():
    context = {
        'import': [
            "from .admin.views import admin",
            "from .admin.auth import login_manager, principals"
        ],
        'extension': [
            "{}principals.init_app(app)".format(indent),
            "{}login_manager.init_app(app)".format(indent),
            "{}admin.init_app(app)".format(indent)
        ]
    }
    factory(context)


def factory_api():
    pass


def factory_users():
    # break out of admin but have to make sure everything works first
    pass


def manage(content):
    stream = get_stream()
    with open('manage.py', 'w') as new_manage:
        new_manage.write(content)
    stream.close()


def manage_users():
    pass


def admin(directive):
    # check to see if admin addon has been added
    if 'admin' in config.addons():
        pass


def settings(content):
    stream = get_stream()
    with open(config.get_settings_file(), 'w') as settings_file:
        settings_file.write(content)
    stream.close()
