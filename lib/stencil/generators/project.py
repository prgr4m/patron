# -*- coding: utf-8 -*-
import os
import os.path as path
import shutil
from . import is_name_valid, get_templates_dir


class FlaskProject(object):
    def __init__(self, name, directory=None):
        if is_name_valid(name):
            self.name = name
        else:
            raise StandardError("Name supplied to FlaskProject is not valid")
        if directory != None and isinstance(directory, str):
            if path.exists(directory):
                raise OSError("Directory already exists")
            self.root_path = directory
        else:
            self.root_path = name
        self.tpl_root = path.join(get_templates_dir(), 'project')

    def create(self):
        os.mkdir(self.root_path)
        os.chdir(self.root_path)
        def setup_root_directory():
            tpl_dir = path.join(self.tpl_root, 'root')
            # need the following:
            # fabfile.py
            # ${project_name}.fcgi
            # ${project_name}-requirements.txt
            # ${project_name|lower}.wsgi
            # htaccess
            # manage.py
            # passenger_wsgi.py (but minus some things...)
            pass

        def setup_tests_directory():
            # this is a package directory
            # has a template (test_basic.py) that is a unit test
            pass

        def setup_tmp_directory():
            # needed for deployment on a2 servers
            pass

        def setup_package_directory():
            # uses self.name
            pass

        setup_root_directory()
        setup_tests_directory()
        setup_tmp_directory()
        setup_package_directory()
