# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from flask_script import Manager
from flask_script.cli import prompt, prompt_pass, prompt_bool
from werkzeug.datastructures import MultiDict
from ..extensions import db
from .models import User, Role
from .forms import UserRegistrationForm

roles_col_fmt = "{:<3} {:<20} {:<37}"
roles_col_heading = ('id', 'role name', 'description')
users_col_fmt = "{:<3} {:<20} {:<20} {:<6} {:<20}"
users_col_heading = ('id', 'username', 'email', 'active', 'roles')

UserAdminCommand = Manager(usage="Perform user and roles management")

@UserAdminCommand.command
def create_user(auto_activate=False):
    "create a new user interactively"
    username = prompt("Username")
    email = prompt("Email")
    password = prompt_pass("Password")
    confirm = prompt_pass("Confirm")
    active = False
    if password != confirm:
        print("Passwords do not match!", file=sys.stderr)
        sys.exit()
    if not auto_activate:
        if prompt_bool("Activate the user"):
            active = True
    else:
        active = True
    user_instance = User(username, email, password, active)
    db.session.add(user_instance)
    db.session.commit()
    return user_instance

@UserAdminCommand.option('--name', dest='name', default=None, help='role name')
@UserAdminCommand.option('--desc', dest='desc', default=None, help='role description')
def create_role(name, desc):
    "create a new application role"
    if name == None and desc == None:
        print("Both role name and description are required", file=sys.stderr)
        sys.exit()
    role_instance = Role(name, desc)
    db.session.add(role_instance)
    db.session.commit()
    return role_instance

@UserAdminCommand.command
def add_role():
    "add a role to the specified user interactively"
    list_users()
    print("")
    user_id = prompt("'id' of the user")
    print("")
    user_instance = User.query.get(int(user_id))
    if user_instance is None:
        print("Invalid user -- User does not exist")
        sys.exit()
    list_roles()
    print("")
    if len(user_instance.roles) > 0:
        role_list = []
        for role in user_instance.roles:
            role_list.append(role.name)
        print("User: {username} has the following roles already: {roles}".format(username=user_instance.username, roles=",".join(role_list)))
    else:
        print("User: {username} does not have any roles assigned to them.".format(username=user_instance.username))
    print("")
    input_role_to_apply = prompt("Id of the role to apply to {}".format(user_instance.username))
    print("")
    # get role to see if it exists
    role_to_apply = Role.query.get(int(input_role_to_apply))
    if role_to_apply is None:
        print("Role does not exist -- aborting operation", file=sys.stderr)
        sys.exit()
    user_instance.roles.append(role_to_apply)
    db.session.commit()

@UserAdminCommand.command
def remove_role():
    "removes a role from the specified user interactively"
    list_users()
    print("")
    input_user_id = prompt("'id' of the user")
    user_instance = User.query.get(int(input_user_id))
    if user_instance is None:
        print("User does not exist!")
        sys.exit()
    if len(user_instance.roles) > 0:
        roles_list = []
        for role in user_instance.roles:
            roles_list.append(role.name)
        print("{username} has the following roles applied: {roles}".format(username=user_instance.username, roles=",".join(roles_list)))
    else:
        print("{} does not have any roles to remove".format(user_instance.username))
        sys.exit()
    print("")
    input_role_name = prompt("Name of role to remove")
    role_to_remove = Role.query.filter_by(name=input_role_name).first()
    if role_to_remove is None:
        print("Role doesn't exist!", file=sys.stderr)
        sys.exit()
    role_index = None
    for index, role in enumerate(user_instance.roles):
        if role_to_remove.name == role.name:
            role_index = index
            break
    try:
        del user_instance.roles[role_index]
    except TypeError:
        print("Invalid role given -- does not belong to user", file=sys.stderr)
        sys.exit()
    db.session.commit()

@UserAdminCommand.command
def list_roles():
    "lists all user roles in the application"
    roles = Role.query.all()
    if roles:
        print(roles_col_fmt.format(*roles_col_heading))
        print("=" * 80)
        for role in roles:
            print(roles_col_fmt.format(role.id, role.name, role.description))
    else:
        print("There are no user roles in the system. Please add one.")
        sys.exit()

@UserAdminCommand.command
def list_users():
    "lists all users in the application"
    users = User.query.all()
    if users:
        print(users_col_fmt.format(*users_col_heading))
        print("=" * 80)
        for user in users:
            role_list = [role.name for role in user.roles]
            print(users_col_fmt.format(user.id, user.username, user.email, user.active, ",".join(role_list)))
    else:
        print("There are no users in the system. Please add one.")
        sys.exit()

@UserAdminCommand.option('--username', dest='username', default=None, help='username of the user to deactivate')
@UserAdminCommand.option('--userid', dest='user_id', default=None, help='user id of the user to deactivate')
def deactivate_user(username, user_id):
    "deactivates the specified user account"
    if username == None and user_id == None:
        # interactive mode
        active_users = User.query.filter_by(active=True)
        if active_users is None:
            print("There are no users that are active")
            sys.exit()
        # print active users
        print(users_col_fmt.format(*users_col_heading))
        print("=" * 80)
        for user in active_users:
            role_list = [role.name for role in user.roles]
            print(users_col_fmt.format(user.id, user.username, user.email, user.active, ",".join(role_list)))
        user_id = prompt("'Id' of user to deactivate")
        user_instance = User.query.get(int(user_id))
    else:
        if username != None:
            user_instance = User.query.filter_by(username=username, active=True).first()
        else:
            user_instance = User.query.get(id=int(user_id))
    if user_instance is None:
        print("User does not exist or is already deactivated!", file=sys.stderr)
        sys.exit()
    user_instance.active = False
    db.session.commit()

@UserAdminCommand.option('--username', dest='username', default=None, help='username of the user to activate')
@UserAdminCommand.option('--userid', dest='user_id', default=None, help='user id of the user to activate')
def activate_user(username, user_id):
    "activates the specified user account"
    if username == None and user_id == None:
        # interactive mode
        inactive_users = User.query.filter_by(active=False)
        if inactive_users is None:
            print("There are no users that are inactive")
            sys.exit()
        # print inactive users
        print(users_col_fmt.format(*users_col_heading))
        print("=" * 80)
        for user in inactive_users:
            role_list = [role.name for role in user.roles]
            print(users_col_fmt.format(user.id, user.username, user.email, user.active, ",".join(role_list)))
        print("")
        user_id = prompt("'Id' of user to activate")
        print("")
        user_instance = User.query.get(int(user_id))
    else:
        if username != None:
            user_instance = User.query.filter_by(username=username, active=False).first()
        else:
            user_instance = User.query.get(int(user_id))
    if user_instance is None:
        print("User does not exist or is already active!", file=sys.stderr)
        sys.exit()
    user_instance.active = True
    db.session.commit()

@UserAdminCommand.option('--username', dest='username', default=None, help='username of the user to delete')
@UserAdminCommand.option('--userid', dest='user_id', default=None, help='user id of the user to delete')
def delete_user(username, user_id):
    "deletes the specified user account"
    if username == None and user_id == None:
        # interactive mode
        users = User.query.all()
        if users is None:
            print("There are no users to remove!")
            sys.exit()
        print(users_col_fmt.format(*users_col_heading))
        print("=" * 80)
        for user in users:
            role_list = [role.name for role in user.roles]
            print(users_col_fmt.format(user.id, user.username, user.email, user.active, ",".join(role_list)))
        print("")
        user_id = prompt("'Id' of user to delete")
        print("")
        user_instance = User.query.get(int(user_id))
    else:
        if username != None:
            user_instance = User.query.filter_by(username=username).first()
        else:
            user_instance = User.query.get(int(user_id))
    if user_instance is None:
        print("User does not exist!", file=sys.stderr)
        sys.exit()
    db.session.delete(user_instance)
    db.session.commit()

@UserAdminCommand.option('--rolename', dest='role_name', default=None, help='name of role to delete')
@UserAdminCommand.option('--roleid', dest='role_id', default=None, help='id of the role to delete')
def delete_user(role_name, role_id):
    "deletes the specified role from the application"
    if role_name == None and role_id == None:
        # interactive mode
        roles = Role.query.all()
        if roles is None:
            print("There are no roles to remove!")
            sys.exit()
        print(roles_col_fmt.format(*roles_col_heading))
        print("=" * 80)
        for role in roles:
            print(roles_col_fmt.format(role.id, role.name, role.description))
        role_id = prompt("'Id' of user to delete")
        role_instance = Role.query.get(int(role_id))
    else:
        if role_name != None:
            role_instance = Role.query.filter_by(name=role_name).first()
        else:
            role_instance = Role.query.get(int(role_id))
    if role_instance is None:
        print("Role does not exist!", file=sys.stderr)
        sys.exit()
    db.session.delete(role_instance)
    db.session.commit()

@UserAdminCommand.command
def create_superuser():
    "creates super user for administrative purposes"
    admin_role = create_role("admin", "application administrative role")
    user = create_user(True)
    user.roles.append(admin_role)
    db.session.commit()

