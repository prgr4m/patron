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

if __name__ == '__main__':
    manager.run()

