# -*- coding: utf-8 -*-
import os.path as path
from flask import redirect
from flask.blueprints import Blueprint
from flask.globals import current_app, request, session
from flask.helpers import url_for, flash
from flask.templating import render_template
from flask_login import login_user, logout_user, login_required
from flask_principal import Identity, AnonymousIdentity, identity_changed
from ..extensions import db
from .forms import LoginForm, UserRegistrationForm
from .models import User

templates_dir = path.join(path.dirname(path.abspath(__file__)), 'templates')
users = Blueprint('users', __name__, template_folder=templates_dir)


@users.context_processor
def processor():
    return dict()


@users.route('/')
@login_required
def index():
    return render_template('index.jade')


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.get_user()
        login_user(user)
        identity_changed.send(current_app._get_current_object(),
                              identity=Identity(user.id))
        flash("Logged in successfully")
        return redirect(request.args.get("next") or url_for('.index'))
    return render_template('login.jade', form=form)


@users.route('/registration', methods=['GET', 'POST'])
def registration():
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
    return render_template('registration.jade', form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    flash("You are now logged out")
    return redirect(url_for('.index'))
