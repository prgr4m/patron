# -*- coding: utf-8 -*-
import unittest
from flask.globals import current_app
from FlaskBase import create_app
from FlaskBase.extensions import db


class AdminTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

# Write tests specific to admin here...
