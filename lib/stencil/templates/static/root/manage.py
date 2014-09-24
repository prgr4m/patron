#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import os.path as path
from livereload import Server
from flask_script import Manager
from flask_migrate import MigrateCommand
from $project_name import create_app
from $project_name.blog.commands import Article
from $project_name.freezer import freezer

env = os.environ.get('$proj_env', 'default')
app = create_app(env)

manager = Manager(app)
manager.add_command('article', Article())


@manager.option('-p', '--port', dest='port', default=5000)
def liveserver(port):
    "Run LiveReload Server with Flask"
    static_dir = path.join(os.getcwd(), "Portfolio", "static")
    sass_globs = ['*.sass', 'base/*.sass', 'modules/*.sass']
    sass_conf = {
        'sass': path.join(static_dir, 'sass'),
        'css': path.join(static_dir, 'css')
    }
    sass_cmd = "sass --trace -I {sass} {sass}/main.sass {css}/main.css"\
        .format(**sass_conf)
    os.system(sass_cmd)

    coffee_globs = ['*.coffee', '**/*.coffee', '**/**/*.coffee']
    coffee_conf = {
        'src': path.join(static_dir, 'coffee'),
        'out': path.join(static_dir, 'js')
    }
    coffee_cmd = "coffee -c -b --no-header -o {out} {src}".format(**coffee_conf)

    template_dirs = ['public', 'blog']
    jade_dirs = [path.join("Portfolio", d, "templates") for d in template_dirs]
    jade_dirs.append(path.join("Portfolio", "templates", "admin"))

    def jade_alert():
        print("jade template has been modified!")

    def blog_alert():
        print("change in a blog page!")

    server = Server(app.wsgi_app)
    for coffee_glob in coffee_globs:
        dir_glob = path.join(static_dir, 'coffee', coffee_glob)
        server.watch(dir_glob, coffee_cmd)

    for sass_glob in sass_globs:
        dir_glob = path.join(static_dir, 'sass', sass_glob)
        server.watch(dir_glob, sass_cmd)

    for jade_dir in jade_dirs:
        dir_glob = path.join(jade_dir, '*.jade')
        server.watch(dir_glob, jade_alert)

    blog_glob = path.join('Portfolio', 'blog', 'articles', '*.md')
    server.watch(blog_glob, blog_alert)

    server.serve(port=port)


@manager.command
def build():
    "Build static version of website"
    freezer.init_app(app)
    print("Do something here...")

if __name__ == '__main__':
    manager.run()
