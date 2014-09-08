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
        if isinstance(directory, str):
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
            template_root = path.join(self.tpl_root, 'root')
            template_files = {
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
            generate_templates(template_root, template_files)
            shutil.copyfile(path.join(template_root, 'fabfile.py'),
                            'fabfile.py')
            shutil.copyfile(path.join(template_root, 'htaccess.txt'),
                            'htaccess')

        def setup_tests_directory():
            os.mkdir('tests')
            open(path.join('tests', '__init__.py'), 'w').close()
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
            template_root = path.join(self.tpl_root, 'package')
            def create_app_templates():
                os.makedirs(path.join('templates', 'includes'))
                template_root = path.join(self.tpl_root, 'templates')
                for f in [x for x in os.listdir(template_root) \
                          if x not in ['.', '..', 'includes']]:
                    shutil.copyfile(path.join(template_root, f),
                                    path.join('templates', f))
                template_root = path.join(template_root, 'includes')
                for f in [x for x in os.listdir(template_root) \
                          if x not in ['.', '..', 'meta.jade']]:
                    shutil.copyfile(path.join(template_root, f),
                                    path.join('templates', 'includes', f))
                template_file = {
                    'meta.jade': [
                        dict(project_name=self.name),
                        path.join('templates', 'includes', 'meta.jade')
                    ]
                }
                generate_templates(template_root, template_file)

            def create_public_package():
                template_root = path.join(self.tpl_root, 'public')
                def create_templates():
                    nonlocal template_root
                    os.mkdir('templates')
                    os.chdir('templates')
                    template_root = path.join(template_root, 'templates')
                    template_file = {
                        'public_base.jade': [dict(project_name=self.name)]
                    }
                    generate_templates(template_root, template_file)
                    shutil.copyfile(path.join(template_root, 'index.jade'),
                                    'index.jade')

                os.mkdir('public')
                os.chdir('public')
                open('__init__.py', 'w').close()
                for f in [x for x in os.listdir(template_root) \
                          if x not in ['.', '..', 'templates']]:
                    shutil.copyfile(path.join(template_root, f), f)
                create_templates()

            def create_static_directory():
                template_root = path.join(self.tpl_root, 'static')
                os.mkdir('static')
                for f in [x for x in os.listdir(template_root) \
                          if x not in ['.', '..']]:
                    shutil.copyfile(path.join(template_root, f),
                                    path.join('static', f))

            os.mkdir(self.name)
            os.chdir(self.name)
            template_files = {
                '__init__.py': [dict(project_name=self.name)],
                'settings.py': [
                    dict(project_name=self.name,
                         project_key="{}_KEY".format(self.name.upper()))
                ]
            }
            generate_templates(template_root, template_files)
            shutil.copyfile(path.join(template_root, 'extensions.py'),
                            'extensions.py')
            create_app_templates()
            create_static_directory()
            create_public_package()

        setup_root_directory()
        setup_tests_directory()
        setup_tmp_directory()
        setup_package_directory()
