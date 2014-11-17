# -*- coding: utf-8 -*-
from __future__ import print_function
import os
from os import path
import shutil
import re
from cookiecutter.generate import generate_files
from . import config
from .helpers import (get_scaffold, create_context, get_user_directory,
                      setup_user_directory, setup_frontend_symlink)
from .injectors import (factory_users, manage_users, factory_admin, factory_api,
                        model_admin_py, requirements)


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
    media_dir = path.join(config.get_project_name(), 'static', 'media')
    os.mkdir(media_dir)
    print(u"Created admin addon")
    factory_admin()
    config.addons(new_addon='admin')
    requirements(u'flask-admin')
    admin_autogen()


def admin_autogen():
    project_name = config.get_project_name()
    scaffold = get_scaffold('blueprint')
    admin_file = path.join(scaffold, 'admin.py')
    exclude_dirs = ('.', '..', 'static', 'templates', 'api', 'users')
    for d in (d for d in os.listdir(project_name) if d not in exclude_dirs):
        if path.exists(path.join(project_name, d, 'models.py')):
            resource_name = path.join(project_name, d)
            target_file = path.join(resource_name, 'admin.py')
            shutil.copyfile(admin_file, target_file)
            admin_model_scanner(d)


def admin_model_scanner(resource_name):
    project_name = config.get_project_name()
    target_scan = path.join(project_name, resource_name, 'models.py')
    model_exp = r'class (?P<model_name>\w+)\(db.Model\)'
    for line in open(target_scan, 'rt'):
        result = re.search(model_exp, line)
        if result is not None:
            model_admin_py(resource_name, result.group('model_name'))


def api():
    scaffold = get_scaffold('api')
    context = create_context('api')
    context['cookiecutter']['project_name'] = config.get_project_name()
    generate_files(repo_dir=scaffold, context=context)
    print(u"Created api addon")
    factory_api()
    config.addons(new_addon='api')


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
    print(u"Created user addon")
    factory_users()
    manage_users()
    requirements(u'flask-login', u'flask-principal')
    config.addons(new_addon='users')
