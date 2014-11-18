# -*- coding: utf-8 -*-
from flask import redirect
from flask.helpers import url_for
import flask_login as login
from flask_admin.base import AdminIndexView, BaseView, expose
from flask_admin.contrib.fileadmin import FileAdmin
from ..users.auth import admin_permission


class AdminMixin(object):
    def is_accessible(self):
        if login.current_user.is_authenticated() and admin_permission.can():
            return True
        return False


class MyAdminIndexView(AdminMixin, AdminIndexView):
    @expose('/')
    def index(self):
        return super(MyAdminIndexView, self).index()


class MyView(AdminMixin, BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/index.jade')


class MediaFileAdmin(AdminMixin, FileAdmin):
    pass
