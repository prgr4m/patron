# -*- coding: utf-8 -*-
from flask_admin.contrib.sqla import ModelView
from wtforms.fields import PasswordField
from ..admin.admin import AdminMixin
from ..extensions import db
from .models import User, Role


class UserModelView(ModelView, AdminMixin):
    column_list = ('username', 'email', 'created_at', 'active', 'roles')
    form_columns = ('username', 'email', 'password', 'active', 'roles')
    form_extra_fields = {
        'password': PasswordField('Password')
    }

    def __init__(self, **kwargs):
        super(UserModelView, self).__init__(User, db.session, **kwargs)

    def create_model(self, form):
        try:
            new_user = User()
            form.populate_obj(new_user)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            return True
        except Exception:
            return False

    def update_model(self, form, model):
        try:
            old_password = model.password
            form.populate_obj(model)
            if form.password.data != old_password:
                if not len(form.password.data) > 0:
                    model.password = old_password
                else:
                    model.set_password(form.password.data)
            db.session.commit()
            return True
        except Exception:
            return False


class RoleModelView(ModelView, AdminMixin):
    def __init__(self, **kwargs):
        super(RoleModelView, self).__init__(Role, db.session, **kwargs)
