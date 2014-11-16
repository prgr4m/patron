# -*- coding: utf-8 -*-
import datetime as dt
import os.path as path
from flask import abort
from flask.blueprints import Blueprint
from flask.globals import current_app
from flask.helpers import make_response
from flask.templating import render_template
from jinja2.exceptions import TemplateNotFound

templates_dir = path.join(path.dirname(path.abspath(__file__)), 'templates')
frontend = Blueprint('frontend', __name__, template_folder=templates_dir)


@frontend.context_processor
def processor():
    return dict()


@frontend.route('/', defaults={'page': 'index'})
@frontend.route('/<page>')
def show(page):
    try:
        return render_template("{}.jade".format(page))
    except TemplateNotFound:
        abort(404)
