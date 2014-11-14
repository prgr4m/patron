# -*- coding: utf-8 -*-
from flask import redirect
from flask.helpers import url_for
import flask_login as login
from flask_admin.base import AdminIndexView, BaseView, expose
from flask_admin.contrib.fileadmin import FileAdmin
from ..users.auth import admin_permission


class AdminMixin(object):
    def is_accessible(self):
        if admin_permission.can():
            return True
        return False


class MyAdminIndexView(AdminIndexView, AdminMixin):
    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect(url_for('users.login'))
        return super(MyAdminIndexView, self).index()


class MyView(BaseView, AdminMixin):
    @expose('/')
    def index(self):
        return self.render('admin/index.jade')


class MediaFileAdmin(FileAdmin, AdminMixin):
    pass
