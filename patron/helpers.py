# -*- coding: utf-8 -*-
from __future__ import print_function
import platform
import io
import os
from os import path
import shutil
import subprocess
import sys
import re
from string import Template
from cookiecutter.generate import generate_context

PKG_SCAFFOLDS = path.join(path.dirname(path.abspath(__file__)), 'data')


def command_available(cmd):
    ret_val = None
    try:
        print("Checking command: {}".format(cmd))
        devnull = open(os.devnull)
        if cmd == 'sass':
            subprocess.Popen(['sass', '-h'], stdout=devnull, stderr=devnull)\
                .communicate()
        else:
            subprocess.Popen([cmd], stdout=devnull, stderr=devnull)\
                .communicate()
        ret_val = True
    except OSError:
        ret_val = False
    finally:
        devnull.close()
    return ret_val


def check_dependencies():
    cmd_help = {
        'npm': "Please make nodejs is installed.",
        'gem': "A ruby environment is required for using sass."
    }
    root_cmds = ('npm', 'gem')
    node_based = ('bower', 'coffeegulp')
    for cmd in root_cmds:
        if not command_available(cmd):
            print(cmd_help[cmd])
            sys.exit()
    for cmd in node_based:
        if not command_available(cmd):
            print("Installing: {}".format(cmd))
            subprocess.call(['npm', 'install', '-g', cmd])
    if not command_available('sass'):
        print("Installing ruby-sass")
        subprocess.call(['gem', 'install', 'sass'])
    print("All external dependencies are installed.")


def get_user_directory():
    user_platform = platform.system()
    user = '~user' if user_platform == 'Windows' else '~'
    patron_dir = 'patron' if user_platform == 'Windows' else '.patron'
    return path.join(path.expanduser(user), patron_dir)


def setup_frontend():
    user_dir = get_user_directory()
    target_dir = path.join(user_dir, 'frontend')
    if not path.exists(target_dir):
        packages = ('browser-sync', 'coffee-script', 'coffeegulp', 'gulp',
                    'gulp-coffee', 'gulp-imagemin', 'gulp-jade', 'gulp-notify',
                    'gulp-requirejs', 'gulp-ruby-sass', 'gulp-uglify')
        for pkg in packages:
            subprocess.call(['npm', 'install', pkg])
        shutil.move('node_modules', target_dir)


def setup_frontend_symlink():
    user_dir = get_user_directory()
    target_dir = path.join(user_dir, 'frontend')
    if sys.version_info.major == 2:
        if platform.system() == 'Windows':
            subprocess.call(['mklink', '/d', 'node_modules', target_dir])
        else:
            os.symlink(target_dir, 'node_modules')
    else:
        os.symlink(target_dir, 'node_modules', target_is_directory=True)


def setup_user_scaffolds():
    user_dir = get_user_directory()
    template_dir = path.join(user_dir, 'templates')
    os.makedirs(template_dir)
    for d in [x for x in os.listdir(PKG_SCAFFOLDS) if x not in ('.', '..')]:
        shutil.copytree(path.join(PKG_SCAFFOLDS, d),
                        path.join(template_dir, d))


def setup_user_directory():
    user_dir = get_user_directory()
    if not path.exists(user_dir):
        os.makedirs(path.join(user_dir, 'templates'))
        if platform.system() == 'Windows':
            subprocess.call(['attrib', '+h', user_dir])
        setup_user_scaffolds()
        setup_frontend()
        print("Create patron user directory at: {}".format(user_dir))
    else:
        print("Patron user directory already exists: {}".format(user_dir))


def is_name_valid(name_in):
    if len(name_in) < 3:
        return False
    if re.search(r'[^\w]', name_in):
        return False
    return True


def get_templates_dir():
    user_dir = get_user_directory()
    if path.exists(path.join(user_dir, 'templates')):
        templates_dir = path.join(user_dir, 'templates')
    else:
        templates_dir = PKG_SCAFFOLDS
    return templates_dir


def scaffold_dir_exists(scaffold_name):
    scaffold_dir = path.join(get_templates_dir(), scaffold_name)
    return True if path.exists(scaffold_dir) else False


def get_default_scaffold_list():
    return [x for x in os.listdir(PKG_SCAFFOLDS) if x not in ['.', '..']]


def get_scaffold(scaffold_name):
    if scaffold_name not in get_default_scaffold_list():
        raise NameError("Unknown scaffold provided: '{}'".format(scaffold_name))
    if scaffold_dir_exists(scaffold_name):
        scaffold_dir = path.join(get_templates_dir(), scaffold_name)
    else:
        scaffold_dir = path.join(PKG_SCAFFOLDS, scaffold_name)
    return scaffold_dir


def create_context(scaffold_name):
    config_dict = dict(default_context=dict())
    context_file = path.join(get_scaffold(scaffold_name), 'cookiecutter.json')
    context = generate_context(
        context_file=context_file,
        default_context=config_dict['default_context'])
    return context


def get_stream():
    try:
        from io import StringIO
    except ImportError:
        from cStringIO import StringIO
    return StringIO()


def create_unittest(name, test_type='blueprint'):
    pass


def create_task(name, description):
    if not is_name_valid(name):
        raise StandardError("Name supplied is invalid")
    name = name.lower()
    scaffold = get_scaffold('task')
    task_template_file = path.join(scaffold, 'task_template.txt')
    template = Template(io.open(task_template_file, 'rt').read())
    template_data = dict(task_name=name, task_description=description)
    task_contents = u"{}{}".format(os.linesep,
                                   template.safe_substitute(**template_data))
    with io.open('fabfile.py', 'at')as fabfile:
        fabfile.write(task_contents)
