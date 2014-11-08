# -*- coding: utf-8 -*-
from __future__ import print_function
import platform
import os
from os import path
import shutil
import subprocess
import sys


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


def setup_user_directory():
    user_dir = get_user_directory()
    if not path.exists(user_dir):
        os.makedirs(path.join(user_dir, 'templates'))
        if platform.system() == 'Windows':
            subprocess.call(['attrib', '+h', user_dir])
        # copy over data directory
        setup_frontend()
        print("Create patron user directory at: {}".format(user_dir))
    else:
        print("Patron user directory already exists: {}".format(user_dir))
