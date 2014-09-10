# -*- coding: utf-8 -*-
import os.path as path
from flask.blueprints import Blueprint
from flask.templating import render_template

templates_dir = path.join(path.dirname(path.abspath(__file__)), 'templates')
${blueprint_name} = Blueprint('${blueprint_name}', __name__, template_folder=templates_dir)


@${blueprint_name}.context_processor
def processor():
    return dict()


@${blueprint_name}.route('/')
def index():
    return render_template('index.jade')
