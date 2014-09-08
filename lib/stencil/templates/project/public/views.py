# -*- coding: utf-8 -*-
import os.path as path
from flask.blueprints import Blueprint
from flask.templating import render_template

templates_dir = path.join(path.dirname(path.abspath(__file__)), 'templates')
frontend = Blueprint('frontend', __name__, template_folder=templates_dir)


@frontend.context_processor
def processor():
    return dict()


@frontend.route('/')
def index():
    return render_template('index.jade')
