# -*- coding: utf-8 -*-
from __future__ import print_function
from . import config

indent = " " * 4
stream = StringIO()
factory_file = config.get_factory_path()
manage_file = 'manage.py'


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


def factory(contents):
    with open(factory_file, 'w') as new_factory:
        new_factory.write(contents)


def factory_blueprint(name):
    pass


def factory_admin():
    pass


def factory_api():
    pass


def manage(contents):
    with open(manage_file, 'w') as new_manage:
        new_manage.write(contents)


def manage_users():
    pass


def admin(contents):
    # check to see if admin addon has been added
    if 'admin' in config.addons():
        pass
