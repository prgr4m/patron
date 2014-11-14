# -*- coding: utf-8 -*-
from __future__ import print_function
from os import path
import shutil
from cookiecutter.generate import generate_files
from . import config
from .helpers import (get_scaffold, create_context, get_user_directory,
                      setup_user_directory, setup_frontend_symlink)
from .injectors import (factory_blueprint, factory_users, manage_users,
                        factory_admin)


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
    if 'users' not in config.addons():
        print(u"Generating users addon")
        users()
    user_scaffold = get_scaffold('users')
    src_file = path.join(user_scaffold, 'admin.py')
    target_file = path.join(config.get_project_name(), 'users', 'admin.py')
    shutil.copyfile(src_file, target_file)
    admin_scaffold = get_scaffold('admin')
    context = create_context('admin')
    context['cookiecutter']['project_name'] = config.get_project_name()
    generate_files(repo_dir=admin_scaffold, context=context)
    factory_admin()
    # add to requirements file
    config.addons(new_addon='admin')
    # helper
    # ==========================================================================
    # auto generate admin.py file for users addon and register with admin
    # auto generate admin.py files for blueprints
    # scan models; generate admin.py views
    # register with admin.py files for blueprint with admin
    # ==========================================================================
    # end helper
    print(u"Created admin addon")


def api():
    # dependent upon users
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
    scaffold = get_scaffold('users')
    context = create_context('users')
    context['cookiecutter']['project_name'] = config.get_project_name()
    generate_files(repo_dir=scaffold, context=context)
    factory_users()
    manage_users()
    config.addons(new_addon='users')
    # add to requirements file
    print(u"Created user addon")
