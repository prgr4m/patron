# -*- coding: utf-8 -*-
import unittest
from flask.globals import current_app
from ${project_name} import create_app
from ${project_name}.extensions import db


class ${blueprint_name}TestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # write tests specifically for the ${blueprint_name} here
