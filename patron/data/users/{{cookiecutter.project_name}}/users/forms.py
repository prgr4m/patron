# -*- coding: utf-8 -*-
from flask_wtf.form import Form
from wtforms.fields import StringField, PasswordField, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms import validators as val
from ..extensions import db
from .models import User, Role


def available_roles():
    return Roles.query.all()


class UserAdminForm(Form):
    username = StringField(
        'Username',
        validators=[
            val.DataRequired(),
            val.Length(4, 80, "The minimum length for username is 4 characters")
        ])
    email = StringField(
        'Email',
        validators=[
            val.DataRequired(),
            val.Length(
                4, 16,
                "The password length needs to be between 4-16 characters")
        ])
    password = PasswordField(
        'Password',
        validators=[
            val.DataRequired(),
            val.Length(
                4, 16,
                "The password length needs to be between 4 - 16 characters")
        ])
    confirm = PasswordField('Confirm Password', validators=[val.DataRequired()])
    active = BooleanField('Active', [val.Optional()])
    roles = QuerySelectMultipleField('Roles',
                                     query_factory=available_roles,
                                     allow_blank=True)

    def validate_confirm(self, field):
        if field.data != self.password.data:
            raise val.ValidationError("Passwords do not match!")


class LoginForm(Form):
    username = StringField(
        'Username',
        validators=[val.InputRequired("Username is needed to login")])
    password = PasswordField(
        'Password',
        validators=[val.InputRequired("Password is needed to login")])

    def get_user(self):
        return db.session.query(User)\
            .filter_by(username=self.username.data).first()

    def validate_username(self, field):
        user = self.get_user()
        if user is None:
            raise val.ValidationError("Invalid user")
        if not user.check_password(self.password.data):
            raise val.ValidationError("Invalid password")


class UserRegistrationForm(Form):
    username = StringField(
        'Username',
        validators=[val.InputRequired("A Username is need to create a user")])
    email = StringField(
        'Email',
        validators=[
            val.InputRequired(
                "An email address is needed to confirm user registration"),
            val.Email("Please supply a valid email address")
        ])
    password = PasswordField(
        'Password',
        validators=[
            val.InputRequired("A password is needed for user creation"),
            val.Length(
                4, 16,
                "Password length needs to be between 4-16 characters long")
        ])
    confirm = PasswordField('Confirm Password')

    def validate_username(self, field):
        if db.session.query(User)\
                .filter_by(username=self.username.data).count() > 0:
            raise val.ValidationError('Username already taken')

    def validate_confirm(self, field):
        if field.data != self.password.data:
            raise val.ValidationError('Passwords do not match')