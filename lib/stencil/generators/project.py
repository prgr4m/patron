# -*- coding: utf-8 -*-
import os
import os.path as path
import shutil
from string import Template
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
            tpl_files = {
                'fcgi_template.txt': [
                    dict(project_name=self.name),
                    "{}.fcgi".format(self.name.lower())
                ],
                'manage.py': [
                    dict(project_name=self.name,
                         proj_env="%s_ENV" % self.name.upper())
                ],
                'passenger_wsgi.py': [
                    dict(project_name=self.name,
                         project_name_env=self.name.upper())
                ],
                'wsgi_template.txt': [
                    dict(project_name=self.name),
                    "{}.wsgi".format(self.name.lower())
                ]
            }
            for tpl_file, data in tpl_files.items():
                dest_file = data[1] if len(data) > 1 else tpl_file
                with open(dest_file, 'w') as f:
                    src_file = path.join(tpl_dir, tpl_file)
                    tpl = Template(open(src_file, 'r').read())
                    f.write(tpl.safe_substitute(**data[0]))
            shutil.copyfile(path.join(tpl_dir, 'fabfile.py'), 'fabfile.py')
            shutil.copyfile(path.join(tpl_dir, 'htaccess.txt'), 'htaccess')

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
