# -*- coding: utf-8 -*-
import os
from os import path
from flask_admin.base import Admin, MenuLink
from .admin import MyAdminIndexView, MediaFileAdmin
from ..users.admin import UserModelView, RoleModelView


media_path = path.join(path.dirname(__file__), os.pardir, 'static', 'media')

admin = Admin(name="{{cookiecutter.project_name}}",
              index_view=MyAdminIndexView(template='admin/index.jade'))

admin.add_view(UserModelView())
admin.add_view(RoleModelView())
admin.add_view(MediaFileAdmin(media_path, '/media/', name="Media Files",
                              endpoint="media"))

logout_link = MenuLink(name="Logout", url='/users/logout')
admin.add_link(logout_link)
