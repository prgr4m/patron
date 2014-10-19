# -*- coding: utf-8 -*-
import os.path as path
from flask.blueprints import Blueprint
from flask.templating import render_template

templates_dir = path.join(path.dirname(path.abspath(__file__)), 'templates')
{{cookiecutter.blueprint_name|lower}} = Blueprint('{{cookiecutter.blueprint_name|lower}}', __name__, template_folder=templates_dir)


@{{cookiecutter.blueprint_name|lower}}.context_processor
def processor():
    return dict()


@{{cookiecutter.blueprint_name|lower}}.route('/')
def index():
    return render_template('index.jade')
