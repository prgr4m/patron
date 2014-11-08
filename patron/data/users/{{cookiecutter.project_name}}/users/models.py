# -*- coding: utf-8 -*-
import sys
import datetime as dt
from flask_login import UserMixin
from ..extensions import db, flask_bcrypt

# =============================================================================
# Users and Roles
# Check flask_security docs if need to add user tracking or account 
# confirmation via email
# =============================================================================
roles_users = db.Table('roles_users',
    db.Column('id', db.Integer(), primary_key=True),
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))

    def __init__(self, name='', description=''):
        self.name = name
        self.description = description

    def __eq__(self, other):
        return (self.name == other or
                self.name == getattr(other, 'name', None))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Role %s>" % self.name


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    active = db.Column(db.Boolean, nullable=False, default=True)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, username=None, email=None, password=None, active=False):
        self.username = username
        self.email = email
        if password:
            self.set_password(password)
        self.created_at = dt.datetime.utcnow()
        self.active = active

    def set_password(self, password):
        self.password = flask_bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password, password)

    # UserMixin (methods with default return values):
    # - is_active: returns True
    # - is_authenticated: returns True
    # - is_anonymous: returns False
    # - get_id
    def is_active(self):
        # override UserMixin
        return self.active

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def has_role(self, role):
        string_types = basestring if sys.version_info[0] == 3 else str
        if isinstance(role, sting_types):
            return role in (role.name for role in self.roles)
        else:
            return role in self.roles

    def __str__(self):
        return self.username

    def __repr__(self):
        return "<User username: %s, email: %s, active: %s>" % (self.username, self.email, self.active)

