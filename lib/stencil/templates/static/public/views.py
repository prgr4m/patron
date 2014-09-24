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
        return render_template("%s.jade")
    except TemplateNotFound:
        abort(404)


@frontend.route('/sitemap.xml', methods=['GET'])
def sitemap():
    # also need to add priority and changefreq to all urls
    pages = []
    ten_days_ago = dt.datetime.now() - dt.timedelta(days=10)
    for rule in current_app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            if not (rule.rule.startswith('/admin') or
                    rule.rule.startswith('/_debug')):
                pages.append([rule.rule, ten_days_ago])
    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers['Content-Type'] = 'application/xml'
    return response
