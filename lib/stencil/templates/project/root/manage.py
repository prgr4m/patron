#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import os.path as path
import sys
from flask_script import Manager
from flask_script.commands import Shell
#from flask_script.cli import prompt, prompt_pass, prompt_bool
from flask_migrate import MigrateCommand
from werkzeug.datastructures import MultiDict
from $project_name import create_app
from $project_name.extensions import db, migrate
from $project_name.admin.commands import UserAdminCommand

env = os.environ.get('$proj_env', 'default')
app = create_app(env)

migrate.init_app(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('admin', UserAdminCommand)

@manager.command
def test():
    "Run unit tests"
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

def make_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_context))

@manager.option('-p', '--port', dest='port', default=5000)
def liveserver(port):
    "Run LiveReload Server with Flask"
    static_dir = path.join(os.getcwd(), "$project_name", "static")
    sass_globs = ['*.sass', 'base/*.sass', 'modules/*.sass']
    sass_conf = {
        'sass': path.join(static_dir,'sass'),
        'css': path.join(static_dir,'css')
    }
    sass_cmd = "sass --trace -I {sass} {sass}/main.sass {css}/main.css".format(**sass_conf)
    os.system(sass_cmd)
    coffee_globs = ['*.coffee', '**/*.coffee', '**/**/*.coffee'] # 3 levels deep
    coffee_conf = {
        'src': path.join(static_dir, 'coffee'),
        'out': path.join(static_dir, 'js')
    }
    coffee_cmd = "coffee -c -b --no-header -o {out} {src}".format(**coffee_conf)
    from livereload import Server
    server = Server(app.wsgi_app)
    for coffee_glob in coffee_globs:
        dir_glob = path.join(static_dir, 'coffee', coffee_glob)
        server.watch(dir_glob, coffee_cmd)
    for sass_glob in sass_globs:
        dir_glob = path.join(static_dir, 'sass', sass_glob)
        server.watch(dir_glob, sass_cmd)
    server.serve(port=port)

#@manager.command
#def create_superuser():
#    "Create an account for application administration"
#    try:
#        u_name = prompt("Username")
#        u_email = prompt("Email Address")
#        u_pass = prompt_pass("Password")
#        u_conf = prompt_pass("Confirm Password")
#        vals = {
#            'username': u_name,
#            'email': u_email,
#            'password': u_pass,
#            'confirm': u_conf
#        }
#        reg_form = UserRegistrationForm(MultiDict(vals), csrf_enabled=False)
#        if reg_form.validate():
#            admin_role = Role('admin', 'admistrator role')
#            db.session.add(admin_role)
#            admin_user = User(u_name, u_email, u_pass, True)
#            admin_user.roles.append(admin_role)
#            db.session.add(admin_user)
#            db.session.commit()
#            print("Done creating superuser")
#        else:
#            print("Errors were encountered when validating user input:")
#            for k, v in reg_form.errors:
#                print("Input: {key}{linesep}{msg}".format(key=k,linesep=os.linesep,msg=v))
#            print("Aborting superuser creation")
#    except KeyboardInterrupt:
#        print("Aborting superuser creation")
#        sys.exit()

if __name__ == '__main__':
    manager.run()

