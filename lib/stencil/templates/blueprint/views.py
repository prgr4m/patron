# -*- coding: utf-8 -*-
import os.path as path
from flask.blueprints import Blueprint
from flask.templating import render_template

templates_dir = path.join(path.dirname(path.abspath(__file__)), 'templates')
${blueprint_name_lower} = Blueprint('${blueprint_name}', __name__, template_folder=templates_dir)


@${blueprint_name_lower}.context_processor
def processor():
    return dict()


@${blueprint_name_lower}.route('/')
def index():
    return render_template('index.jade')
