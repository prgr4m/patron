# -*- coding: utf-8 -*-
from flask import Flask
from flask.templating import render_template
from .settings import config
from .extensions import db, flask_bcrypt, cache, toolbar
from .public.views import frontend


def create_app(config_obj='default'):
    app = Flask(__name__, static_url_path='')
    if config_obj in config.keys():
        app.config.from_object(config[config_obj])
    else:
        app.config.from_object(config['default'])
    app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app


def register_extensions(app):
    db.init_app(app)
    flask_bcrypt.init_app(app)
    toolbar.init_app(app)
    cache.init_app(app)


def register_blueprints(app):
    app.register_blueprint(frontend)


def register_errorhandlers(app):
    def render_error_page(error):
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.jade".format(error_code)), error_code
    for err in (401, 403, 404, 500):
        app.errorhandler(err)(render_error_page)


__all__ = [create_app]
