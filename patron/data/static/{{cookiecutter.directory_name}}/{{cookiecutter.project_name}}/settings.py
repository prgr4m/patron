# -*- coding: utf-8 -*-
import os
import os.path as path


class Config(object):
    APP_DIR = path.abspath(path.dirname(__file__)) # This directory
    PROJECT_ROOT = path.abspath(path.join(APP_DIR, os.pardir))
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    DEBUG = True
    FLATPAGES_ROOT = path.join('blog', 'articles')
    FLATPAGES_AUTO_RELOAD = DEBUG
    FLATPAGES_EXTENSION = '.md'
    FLATPAGES_ENCODING = 'utf8'

config = {
    'development': DevConfig,
    'default': DevConfig
}
