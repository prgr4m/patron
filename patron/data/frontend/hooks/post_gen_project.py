#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
from os import path
import shutil
import sys
import subprocess
import platform
from string import Template

USER = '~user' if platform.system() == 'Windows' else '~'
NODE_MODULES_DIR = path.join(path.expanduser(USER), 'Projects', '.node_modules')

ROOT_DIR = os.getcwd()
APP_DIR = path.join(ROOT_DIR, 'frontend', 'app')
FONT_DIR = path.join(ROOT_DIR, 'frontend', 'assets', 'fonts')
SASS_DIR = path.join(ROOT_DIR, 'frontend', 'sass', 'lib')
VENDOR_DIR = path.join(ROOT_DIR, 'frontend', 'coffee', 'vendor')
BOWER_DIR = path.join(ROOT_DIR, 'bower_components')
JS_LIBS = []


def command_available(command):
    ret_value = False
    try:
        devnull = open(os.devnull)
        subprocess.Popen([command], stdout=devnull, stderr=devnull)\
            .communicate()
        ret_value = True
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            print("'{}' doesn't exist on the path!".format(command))
        else:
            print("OSError when running {}: {}".format(e, command))
    finally:
        devnull.close()
        return ret_value


def check_external_commands():
    commands = ('bower', 'npm', 'coffeegulp')
    for cmd in commands:
        val = command_available(cmd)
        if not val:
            err_msg = "{} does not exist on path!"
            print(err_msg.format(cmd))
            sys.exit()


def setup_node_modules():
    if not path.exists(NODE_MODULES_DIR):
        npm_pkgs = ['browser-sync', 'coffee-script', 'coffeegulp', 'gulp',
                    'gulp-coffee', 'gulp-imagemin', 'gulp-jade', 'gulp-notify',
                    'gulp-requirejs', 'gulp-ruby-sass', 'gulp-uglify']
        for pkg in npm_pkgs:
            subprocess.call(['npm', 'install', pkg])
        node_root_path = path.dirname(NODE_MODULES_DIR)
        if not path.exists(node_root_path):
            os.mkdir(node_root_path)
        shutil.move('node_modules', NODE_MODULES_DIR)
    if platform.system() == 'Windows' and sys.version_info.major == 2:
        os.system("mklink \d node_modules {}".format(NODE_MODULES_DIR))
    else:
        os.symlink(NODE_MODULES_DIR, 'node_modules')
    print("Created symlink at: {}".format(NODE_MODULES_DIR))


def install_default_css():
    subprocess.call(['bower', 'install', 'normalize.css'])
    normalize_root = path.join(BOWER_DIR, 'normalize.css')
    shutil.copyfile(path.join(normalize_root, 'normalize.css'),
                    path.join(SASS_DIR, '_normalize.scss'))
    subprocess.call(['bower', 'install', 'font-awesome'])
    font_awesome_root = path.join(BOWER_DIR, 'font-awesome')
    font_awesome_scss = path.join(font_awesome_root, 'scss')
    font_awesome_fonts = path.join(font_awesome_root, 'fonts')
    for f in [x for x in os.listdir(font_awesome_fonts)
              if x not in ('.', '..')]:
        shutil.copyfile(path.join(font_awesome_fonts, f),
                        path.join(FONT_DIR, f))
    shutil.copytree(font_awesome_scss, path.join(SASS_DIR, 'font-awesome'))


def install_bnb():
    bnb_commands = ('bourbon', 'neat', 'bitters')
    ret_vals = []
    for cmd in bnb_commands:
        ret_vals.append(command_available(cmd))
    if False in ret_vals:
        for cmd in bnb_commands:
            subprocess.call(['bower', 'install', cmd])
        bourbon_path = path.join(BOWER_DIR, 'bourbon', 'dist')
        neat_path = path.join(BOWER_DIR, 'neat', 'app', 'assets', 'stylesheets')
        bitters_path = path.join(BOWER_DIR, 'bitters', 'app', 'assets',
                                 'stylesheets')
        shutil.copytree(bourbon_path, path.join(SASS_DIR, 'bourbon'))
        shutil.copytree(neat_path, path.join(SASS_DIR, 'neat'))
        shutil.copytree(bitters_path, path.join(SASS_DIR, 'base'))
    else:
        os.chdir(SASS_DIR)
        for cmd in bnb_commands:
            subprocess.call([cmd, 'install'])
        os.chdir(ROOT_DIR)
    grid_file = path.join(SASS_DIR, 'base/_grid-settings.scss')
    orig_contents = open(grid_file).readlines()
    fixed_import = '@import "../neat/neat-helpers";{}'.format(os.linesep)
    with open(grid_file, 'w') as new_grid_file:
        for index, line in enumerate(orig_contents):
            if index == 0:
                line = fixed_import
            new_grid_file.write(line)


def install_bootstrap():
    bootstrap_cmd = ['bower', 'install', 'bootstrap-sass']
    subprocess.call(bootstrap_cmd)
    bootstrap_root = path.join(BOWER_DIR, 'bootstrap-sass')
    fonts = path.join(bootstrap_root, 'fonts')
    scss = path.join(bootstrap_root, 'lib')
    js = path.join(bootstrap_root, 'dist', 'js', 'bootstrap.js')
    for f in [x for x in os.listdir(fonts) if x not in ('.', '..')]:
        shutil.copyfile(path.join(fonts, f), path.join(FONT_DIR, f))
    shutil.copytree(scss, path.join(SASS_DIR, 'bootstrap'))
    shutil.copyfile(js, path.join(VENDOR_DIR, 'bootstrap.js'))
    JS_LIBS.append('bootstrap')
    jquery = path.join(BOWER_DIR, 'jquery', 'dist', 'jquery.js')
    shutil.copyfile(jquery, path.join(VENDOR_DIR, 'jquery.js'))
    JS_LIBS.append('jquery')


def configure_requirejs():
    indent = " " * 2
    paths, shims = [], []
    client_indent, gulp_indent = 2, 3
    gulp_config = path.join(ROOT_DIR, 'gulp', 'config.coffee')
    client_config = path.join(APP_DIR, 'main.coffee')
    known_js_libs = {
        'jquery': {
            'paths': 'jquery: "vendor/jquery"',
            'shim': 'jquery: exports: "$"'
        },
        'bootstrap': {
            'paths': 'bootstrap: "vendor/bootstrap"',
            'shim': 'bootstrap: deps: ["jquery"]'
        },
        'angular': {
            'paths': 'angular: "vendor/angular"',
            'shim': 'angular: exports: "angular"'
        },
        'angular-route': {
            'paths': '"angular-route": "vendor/angular-route"',
            'shim': '"angular-route": deps: ["angular"]'
        }
    }
    for js_lib in JS_LIBS:
        if js_lib in known_js_libs:
            paths.append(known_js_libs[js_lib]['paths'])
            shims.append(known_js_libs[js_lib]['shim'])
    gulp_content = Template(open(gulp_config).read())
    with open(gulp_config, 'w') as gulp_file:
        if len(paths) > 0:
            pth = "{}{}".format(os.linesep, indent * gulp_indent).join(paths)
            shim = "{}{}".format(os.linesep, indent * gulp_indent).join(shims)
            gulp_data = dict(paths=pth, shims=shim)
        else:
            gulp_data = dict(paths='', shims='')
        gulp_file.write(gulp_content.safe_substitute(**gulp_data))
    client_content = Template(open(client_config).read())
    with open(client_config, 'w') as client_file:
        if len(paths) > 0:
            pth = "{}{}".format(os.linesep, indent * client_indent).join(paths)
            shim = "{}{}".format(os.linesep, indent * client_indent).join(shims)
            client_data = dict(paths=pth, shims=shim)
        else:
            client_data = dict(paths='', shims='')
        client_file.write(client_content.safe_substitute(**client_data))


def install_css_libs():
    os.chdir(ROOT_DIR)
    prompt_user = True
    available_choices = ('bnb', 'bootstrap', 'none')
    user_choice = None
    input_prompt = "CSS choice [bnb|bootstrap|none]: "
    default_css = ('font-awesome', 'normalize.css')
    note_msg = "Note: {} and {} will be installed either way"
    base_file = path.join(path.dirname(SASS_DIR), 'base', '_base.sass')
    tpl = Template(open(base_file).read())
    while prompt_user:
        print("Install CSS libraries:")
        print("\tbnb: bourbon, neat, bitters")
        print("\tbootstrap: twitter bootstrap")
        print("\tnone: no css library to install")
        print(note_msg.format(*default_css))
        if sys.version_info.major == 2:
            choice = raw_input(input_prompt)
        else:
            choice = input(input_prompt)
        choice = choice.lower()
        if choice in available_choices:
            user_choice = choice
            prompt_user = False
        else:
            print("Invalid choice. Try again.")
    install_default_css()
    if user_choice == 'bnb':
        install_bnb()
        bnb = [
            '@import "../lib/bourbon/bourbon"',
            '@import "../lib/base/grid-settings"',
            '@import "../lib/neat/neat"',
            '@import "../lib/base/base"'
        ]
        tpl_data = dict(css_imports="{}".format(os.linesep).join(bnb))
    elif user_choice == 'bootstrap':
        install_bootstrap()
        import_line = '@import ../lib/bootstrap/bootstrap'
        tpl_data = dict(css_imports="{}{}".format(import_line, os.linesep))
    else:
        tpl_data = dict(css_imports="")
    with open(base_file, 'w') as new_base:
        new_base.write(tpl.safe_substitute(tpl_data))
    hgkeep_file = path.join(SASS_DIR, '.hgkeep')
    os.remove(hgkeep_file)


def install_js_libs():
    os.chdir(ROOT_DIR)
    prompt_user = True
    input_prompt = "Would you like to install angularjs? [yes|no]: "
    while prompt_user:
        if sys.version_info.major == 2:
            choice = raw_input(input_prompt)
        else:
            choice = input(input_prompt)
        choice = choice.lower()
        if choice in ('yes', 'no'):
            if choice == 'yes':
                subprocess.call(['bower', 'install', 'angular',
                                 'angular-route'])
                angular = path.join(BOWER_DIR, 'angular', 'angular.js')
                angular_route = path.join(BOWER_DIR, 'angular-route',
                                          'angular-route.js')
                shutil.copyfile(angular, path.join(VENDOR_DIR, 'angular.js'))
                shutil.copyfile(angular_route, path.join(VENDOR_DIR,
                                                         'angular-route.js'))
                JS_LIBS.extend(['angular', 'angular-route'])
            prompt_user = False
    if 'jquery' not in JS_LIBS:
        subprocess.call(['bower', 'install', 'jquery'])
    subprocess.call(['bower', 'install', 'requirejs'])
    jquery = path.join(BOWER_DIR, 'jquery', 'dist', 'jquery.js')
    shutil.copyfile(jquery, path.join(VENDOR_DIR, 'jquery.js'))
    JS_LIBS.append('jquery')
    rjs = path.join(BOWER_DIR, 'requirejs', 'require.js')
    shutil.copyfile(rjs, path.join(VENDOR_DIR, 'require.js'))
    hgkeep_file = path.join(VENDOR_DIR, '.hgkeep')
    os.remove(hgkeep_file)
    configure_requirejs()


check_external_commands()
setup_node_modules()
install_css_libs()
install_js_libs()
