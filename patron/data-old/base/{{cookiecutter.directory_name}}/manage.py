#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import os.path as path
import sys
from flask_script import Manager
from flask_script.commands import Shell
from flask_migrate import MigrateCommand
from {{cookiecutter.project_name}} import create_app
from {{cookiecutter.project_name}}.extensions import db, migrate

env = os.environ.get('{{cookiecutter.project_name}}_ENV', 'default')
app = create_app(env)

migrate.init_app(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    "Run unit tests"
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

def make_context():
    return dict(app=app, db=db)

manager.add_command("shell", Shell(make_context=make_context))

if __name__ == '__main__':
    manager.run()

