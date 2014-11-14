# -*- coding: utf-8 -*-
from __future__ import print_function
from os import path
from cookiecutter.generate import generate_files
from . import config
from .helpers import (get_scaffold, create_context, get_user_directory,
                      setup_user_directory, setup_frontend_symlink)


def get_known_addons():
    return ['admin', 'api', 'frontend', 'users']


def install_addon(addon_name):
    addon_map = {
        'admin': admin,
        'api': api,
        'frontend': frontend,
        'users': users
    }
    if addon_name not in addon_map:
        raise KeyError("Unknown addon to install")
    addon_map[addon_name]()


def admin():
    print(u"Installing admin addon")


def api():
    print(u"Installing api addon")


def frontend():
    user_dir = get_user_directory()
    if not path.exists(user_dir):
        setup_user_directory()
    scaffold = get_scaffold('frontend')
    context = create_context('frontend')
    context['cookiecutter']['project_name'] = config.get_project_name()
    context['cookiecutter']['directory_name'] = 'frontend'
    generate_files(repo_dir=scaffold, context=context)
    setup_frontend_symlink()
    config.addons(new_addon='frontend')
    print(u"Created frontend workflow")


def users():
    print(u"Installing user addon")
