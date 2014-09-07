#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
# =============================================================================
# This script is tailored for deployment under a2hosting servers
# =============================================================================
import os, sys

# Tell Passenger to run our virtualenv python
INTERP = "/path/to/virutalenv/python/bin/python"

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Setup paths and environment variables
sys.path.append(os.getcwd())
# os.environ['$project_name_env'] = 'production'

# Set the application up
#from $project_name import create_app as application
from $project_name import create_app
application = create_app('production')

# for debugging, uncomment the next lines
#from werkzeug.debug import DebuggedApplication
#application = DebuggedApplication(application, evalex=True)

