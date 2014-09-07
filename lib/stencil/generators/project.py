# -*- coding: utf-8 -*-
import os
import os.path as path
import shutil
from . import is_name_valid, get_templates_dir, generate_templates


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
            generate_templates(tpl_dir, tpl_files)
            shutil.copyfile(path.join(tpl_dir, 'fabfile.py'), 'fabfile.py')
            shutil.copyfile(path.join(tpl_dir, 'htaccess.txt'), 'htaccess')

        def setup_tests_directory():
            os.mkdir('tests')
            open(path.join('tests','__init__.py'), 'w').close()
            tpl_dir = path.join(self.tpl_root, 'tests')
            tpl_file = {
                'test_basic.py': [
                    dict(project_name=self.name),
                    path.join('tests', 'test_basic.py')
                ]
            }
            generate_templates(tpl_dir, tpl_file)

        def setup_tmp_directory():
            os.mkdir('tmp')
            open(path.join('tmp', 'restart.txt'), 'w').close()

        def setup_package_directory():
            # uses self.name
            pass

        setup_root_directory()
        setup_tests_directory()
        setup_tmp_directory()
        setup_package_directory()
