# -*- coding: utf-8 -*-
import unittest
import tempfile
import textwrap
from stencil.generators import CodeInspector


class TestCodeInspector(unittest.TestCase):
    def setUp(self):
        self.dummy_template = textwrap.fill("""
        from flask import Blueprint, render_template, abort
        from jinja2 import TemplateNotFound

        simple_page = Blueprint('simple_page', __name__,
                                template_folder='templates')

        @simple_page.route('/', defaults={'page': 'index'})
        @simple_page.route('/<page>')
        def show(page):
            try:
                return render_template('pages/%s.html' % page)
            except TemplateNotFound:
                abort(404)

        @blueprint.route('/ninja', methods=['GET','POST'])
        def ninja():
            return render_template('ninja.html')
        """)

    def tearDown(self):
        pass

    def test_checks_if_module_exists(self):
        with tempfile.TemporaryFile() as tmp_file:
            tmp_file.write(self.dummy_template)
            print(tmp_file)
            self.assertEqual(CodeInspector)
