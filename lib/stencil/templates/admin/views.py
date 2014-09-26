# -*- coding: utf-8 -*-
import os
from flask import abort, redirect
from flask.globals import current_app, request, session
from flask.helpers import url_for, flash
from flask_login import login_required, login_user, logout_user
import flask_login as login
from flask_principal import Identity, AnonymousIdentity, identity_changed
from flask_admin.base import Admin, AdminIndexView, BaseView, MenuLink, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from wtforms.fields import PasswordField
from ..extensions import db
from .auth import admin_permission
from .models import User, Role
from .forms import UserAdminForm, LoginForm, UserRegistrationForm

media_path = os.path.join(os.path.dirname(__file__),
                          os.pardir, 'static', 'media')

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect(url_for('.login'))
        return super(MyAdminIndexView, self).index()

    @expose('/login', methods=['GET', 'POST'])
    def login(self):
        form = LoginForm()
        if form.validate_on_submit():
            user = form.get_user()
            login_user(user)
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))
            flash("Logged in successfully")
            return redirect(request.args.get("next") or url_for('.index'))
        return self.render('admin/login.jade', form=form)

    @expose('/registration', methods=['GET', 'POST'])
    def registration(self):
        form = UserRegistrationForm()
        if form.validate_on_submit():
            # change user activation pending on application needs
            new_user = User()
            form.populate_obj(new_user)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash("Successfully created new user")
            return redirect(request.args.get("next") or url_for('.index'))
        return self.render('admin/registration.jade', form=form)

    @expose('/logout')
    def logout(self):
        logout_user()
        for key in ('identity.name', 'identity.auth_type'):
            session.pop(key, None)
        identity_changed.send(current_app._get_current_object(),
                              identity=AnonymousIdentity())
        flash("You are now logged out")
        return redirect(url_for('.index'))

class MyView(BaseView):
    @expose('/')
    def index(self):
        if admin_permission.can():
            return self.render('admin/index.jade')
        abort(403)

    def is_accessible(self):
        return login.current_user.is_authenticated()

class UserModelView(ModelView):
    column_list = ('username', 'email', 'created_at', 'active', 'roles')
    form_columns = ('username', 'email', 'password', 'active', 'roles')
    form_extra_fields = {
        'password': PasswordField('Password')
    }

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

    def is_accessible(self):
        if admin_permission.can():
            return True
        return False

class RoleModelView(ModelView):
    def is_accessible(self):
        if admin_permission.can():
            return True
        return False

class MediaFileAdmin(FileAdmin):
    def is_accessible(self):
        return login.current_user.is_authenticated()

admin = Admin(name="$project_name",
              index_view=MyAdminIndexView(template='admin/index.jade'),
              template_mode='bootstrap3')

#admin.add_view(MyView(name='Hello'))
admin.add_view(UserModelView(User, db.session))
admin.add_view(RoleModelView(Role, db.session))
admin.add_view(MediaFileAdmin(media_path, '/media/', name="Media Files",
                              endpoint="media"))

logout_link = MenuLink(name="Logout", url="/admin/logout")
admin.add_link(logout_link)
