# -*- coding: utf-8 -*-
import os
import os.path as path


class Config(object):
    SECRET_KEY = os.environ.get('{{cookiecutter.project_name}}_ENV',
                                "super-secret-key-here")
    APP_DIR = path.abspath(path.dirname(__file__))  # This directory
    PROJECT_ROOT = path.abspath(path.join(APP_DIR, os.pardir))
    BCRYPT_LEVEL = 13
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = "simple"
    DEBUG = False
    TESTING = False


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgres://username:password@host:port/database'


class DevConfig(Config):
    DEBUG = True
    DB_NAME = "{{cookiecutter.project_name|lower}}.db"
    DB_PATH = path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = "sqlite:///{0}".format(DB_PATH)
    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True
    CACHE_TYPE = "simple"


class TestConfig(Config):
    TESTING = True
    DB_NAME = "{{cookiecutter.project_name|lower}}-testing.db"
    DB_PATH = path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = "sqlite:///{0}".format(DB_PATH)


config = {
    'development': DevConfig,
    'testing': TestConfig,
    'production': ProdConfig,
    'default': DevConfig
}
