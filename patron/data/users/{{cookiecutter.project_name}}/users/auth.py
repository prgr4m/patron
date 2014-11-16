# -*- coding: utf-8 -*-
from flask.globals import current_app
from flask.helpers import url_for
from flask_login import LoginManager, current_user
from flask_principal import (Principal, Permission, RoleNeed, UserNeed,
                             identity_loaded)
from .models import User


# Login Configuration
# =============================================================================
# Notes:
# If I need to support AnonUsers for some kind of permission I need to provide
# a custom class using the AnonymousUserMixin (ONLY for custom requirements!)
# login_manager.anonymous_user = MyAnonymousUser
#
# If I'm doing an api and want to load a user via headers,
# Look at the section of (Login using Authorization header) for more info
# =============================================================================
login_manager = LoginManager()
login_manager.login_view = "users.login"

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

# Principal Configuration
# =============================================================================
principals = Principal()

# Application Needs and Permissions
# =============================================================================
admin_permission = Permission(RoleNeed('admin'))

@identity_loaded.connect
def on_identity_loaded(sender, identity):
    identity.user = current_user
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))
