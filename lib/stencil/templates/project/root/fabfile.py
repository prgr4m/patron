# -*- coding: utf-8 -*-
from __future__ import print_function
import os
from os import path
from fabric.api import env, hosts, local, run, cd, abort, settings, task


#env.user = 'username_in_here'
#env.hosts = [
#    'server.name.here.com'
#]

#@task
#def init():
#    "initializes front-end workflow for the web app"
#    print("You should add something here if there's something that needs to be done")
#
#@task
#def push():
#    "pushes code to remote server -- not relying on repository hook system"
#    print("This should do some initial housekeeping, hg commit with message prompt, and push to remote server")
#
#
