# -*- coding: utf-8 -*-
import os
import os.path as path
import shutil
import fnmatch
from . import is_name_valid, get_templates_dir, generate_templates


class StaticProject(object):
    """
    Very similar to a standard flask project minus the database dependencies
    and includes Flask-FlatPages and Frozen-Flask.
    """
    def __init__(self, name, directory=None):
        if is_name_valid(name):
            self.name = name
        else:
            raise StandardError("Name supplied to StaticProject is not valid")
        root_path = directory if isinstance(directory, str) else name
        self.root_path = path.join(os.getcwd(), root_path)
        if path.exists(self.root_path):
            raise OSError("Directory already exists")
        self.tpl_root = path.join(get_templates_dir(), 'static')

    def create(self):
        os.mkdir(self.root_path)
        os.chdir(self.root_path)

        self.__setup_root_directory()
        self.__setup_package_directory()
        self.__setup_blog_directory()

    def __setup_root_directory(self):
        template_root = path.join(self.tpl_root, 'root')
        template_files = {
            'manage.py': [
                dict(project_name=self.name,
                     proj_env="%s_ENV" % self.name.upper())
            ]
        }
        generate_templates(template_root, template_files)
        shutil.copyfile(path.join(template_root, 'fabfile.py'),
                        'fabfile.py')
        shutil.copyfile(path.join(template_root, 'htaccess.txt'),
                        'htaccess')
        shutil.copyfile(path.join(template_root, 'requirements.txt'),
                        "{}-requirements.txt".format(self.name.lower()))

    def __setup_package_directory(self):
        template_root = path.join(self.tpl_root, 'package')

        def create_app_templates():
            os.makedirs(path.join('templates', 'includes'))
            template_root = path.join(self.tpl_root, 'templates')
            for f in [x for x in os.listdir(template_root)
                      if x not in ['.', '..', 'includes']]:
                shutil.copyfile(path.join(template_root, f),
                                path.join('templates', f))
            template_root = path.join(template_root, 'includes')
            for f in [x for x in os.listdir(template_root)
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
                os.mkdir('templates')
                os.chdir('templates')
                template_root = path.join(self.tpl_root, 'public', 'templates')
                template_file = {
                    'public_base.jade': [dict(project_name=self.name)]
                }
                generate_templates(template_root, template_file)
                shutil.copyfile(path.join(template_root, 'index.jade'),
                                'index.jade')
                shutil.copyfile(path.join(template_root,
                                          'sitemap_template.xml'),
                                'sitemap_template.xml')

            os.mkdir('public')
            os.chdir('public')
            open('__init__.py', 'w').close()
            for f in [x for x in os.listdir(template_root)
                      if x not in ['.', '..', 'templates']]:
                shutil.copyfile(path.join(template_root, f), f)
            create_templates()

        def create_static_directory():
            template_root = path.join(self.tpl_root, 'static')
            os.mkdir('static')
            for f in [x for x in os.listdir(template_root)
                      if x not in ['.', '..', 'sass']]:
                shutil.copyfile(path.join(template_root, f),
                                path.join('static', f))

            def make_sass_dir():
                template_root = path.join(self.tpl_root, 'static', 'sass')
                sass_root = path.join('static', 'sass')
                sass_dirs = [path.join(sass_root, d)
                             for d in ['base', 'lib', 'modules']]
                for d in sass_dirs:
                    os.makedirs(d)

                base_files = ['_base.sass', '_mixins.sass', '_variables.sass']

                for f in os.listdir(template_root):
                    if f not in ['.', '..']:
                        if fnmatch.fnmatch(f, '_*.sass'):
                            if f in base_files:
                                target_dir = path.join(sass_root, 'base')
                            else:
                                target_dir = path.join(sass_root, 'modules')
                        else:
                            target_dir = sass_root

                        shutil.copyfile(path.join(template_root, f),
                                        path.join(target_dir, f))

            static_dirs = [path.join('static', d)
                           for d in ['css', 'coffee', 'img', 'fonts',
                                     path.join('js', 'vendor')]]
            for d in static_dirs:
                os.makedirs(d)

            make_sass_dir()

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

    def __setup_blog_directory(self):
        os.chdir(path.join(self.root_path, self.name))
        os.mkdir('blog')
        template_root = path.join(self.tpl_root, 'blog')
        open(path.join('blog', '__init__.py'), 'w').close()
        shutil.copyfile(path.join(template_root, 'commands.py'),
                        path.join('blog', 'commands.py'))
        template_files = {
            'views.py': [
                dict(project_name=self.name),
                path.join('blog', 'views.py')
            ]
        }
        generate_templates(template_root, template_files)
        shutil.copytree(path.join(template_root, 'templates'),
                        path.join('blog', 'templates'))

