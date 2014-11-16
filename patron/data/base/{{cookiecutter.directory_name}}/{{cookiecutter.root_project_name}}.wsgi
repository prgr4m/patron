# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/path/to/the/application')

activate_this = '/path/to/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this)

from {{cookiecutter.project_name}} import create_app
application = create_app('production')
