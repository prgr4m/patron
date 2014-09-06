# -*- coding: utf-8 -*-
import unittest
import tempfile
import textwrap
from stencil.generators import CodeInspector


class TestCodeInspector(unittest.TestCase):
    def setUp(self):
        self.dummy_template = textwrap.fill("""
        import os
        from flask import abort, redirect

        # you do realize this isn't supposed to be real...

        @blueprint.route('/', methods=['GET'])
        def index():
            return render_template('index.html')
        """)

    def tearDown(self):
        pass

    def test_checks_if_module_exists(self):
        with tempfile.TemporaryFile() as tmp_file:
            tmp_file.write(self.dummy_template)
            print(tmp_file)
            self.assertEqual(CodeInspector)
