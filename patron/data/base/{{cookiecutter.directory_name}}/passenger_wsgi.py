#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
# =============================================================================
# script for environments that use mod_passenger for wsgi
# =============================================================================
import os, sys

# Tell Passenger to run our virtualenv python
INTERP = "/path/to/virutalenv/python/bin/python"

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Setup paths and environment variables
sys.path.append(os.getcwd())
# os.environ['{{cookiecutter.project_name}}'] = 'production'

# Set the application up
from {{cookiecutter.project_name}} import create_app
application = create_app('production')

# for debugging, uncomment the next lines
#from werkzeug.debug import DebuggedApplication
#application = DebuggedApplication(application, evalex=True)

