# -*- coding: utf-8 -*-
from __future__ import print_function


def get_addons():
    return ('admin', 'api', 'frontend', 'users')


def admin():
    print("Installing admin addon")


def api():
    print("Installing api addon")


def frontend():
    # run scaffold
    # make symlink
    # add to addons
    print("Installing frontend addon")


def users():
    print("Installing user addon")
