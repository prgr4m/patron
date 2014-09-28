# -*- coding: utf-8 -*-
from __future__ import print_function
import cStringIO
import os
import os.path as path
import re
from . import StencilConfig, get_templates_dir


class InjectorBase(object):
    """The base object for injecting code into an existing code base"""
    indent = " " * 4

    def __init__(self):
        """
        Initializing the common base for code injection

        :param str target:
            the path of the target file to inject code to (safely)
        """
        self.config = StencilConfig()
        self.stream = cStringIO.StringIO()

    def __del__(self):
        self.stream.close()

    def inject(self):
        raise NotImplementedError("InjectorBase::inject must be overridden")

    def read_target(self):
        with open(self.target_file) as f:
            for line in f:
                yield line.rstrip()


class ManageInjector(InjectorBase):
    """
    Responsible for injecting admin management hooks into manage.py
    """
    def __init__(self):
        super(ManageInjector, self).__init__()
        self.target_file = "manage.py"

    def inject(self, directive):
        """
        The method responsible for injecting code snippets into a (flask-script)
        manage.py file.

        :param str directive:
            a known key to perform associated script injections
        """
        known_directives = ['admin']  # livereload, etc, will come later
        if directive not in known_directives:
            raise ValueError("ManageInjector:Unknown directive value")
        getattr(self, "_{}".format(directive))()

    def _admin(self):
        match_queue = [r'db, migrate$', r"'db', MigrateCommand\)$"]
        imp_stmnt = "from {proj_name}.admin.commands import UserAdminCommand"\
            .format(proj_name=self.config.project_name)
        mgr_cmd = "manager.add_command('user', UserAdminCommand)"
        inject_queue = [imp_stmnt, mgr_cmd]
        current_search = match_queue.pop(0)
        current_inject = inject_queue.pop(0)
        for line in self.read_target():
            if current_search is not None:
                if re.search(current_search, line) is not None:
                    line = "{line_in}{linesep}{injected_code}"\
                        .format(line_in=line, linesep=os.linesep,
                                injected_code=current_inject)
                    if len(match_queue) > 0:
                        current_search = match_queue.pop(0)
                        current_inject = inject_queue.pop(0)
                    else:
                        current_search = None
            print(line, file=self.stream)
        with open(self.target_file, 'w') as new_manage:
            new_manage.write(self.stream.getvalue())


class FactoryInjector(InjectorBase):
    """
    Responsible for registering extensions and blueprints with an app factory
    """
    def __init__(self):
        super(FactoryInjector, self).__init__()
        self.target_file = self.config.factory_path

    def inject(self, directive, name=None):
        """
        The method responsible for injecting code snippets into the app factory
        file.

        :param str directive:
            a key that is used to look up known directives on how to inject code
            into an app factory. I decided to keep file hacks contained rather
            than dynamically through the method.
        """
        known_directives = ['admin', 'blueprint', 'api']
        if directive not in known_directives:
            raise ValueError("FactoryInjector:Unknown value for directive")
        if directive == 'blueprint' and name is not None:
            injection_context = self._blueprint(name)
        else:
            injection_context = getattr(self, "_{}".format(directive))()
        content = open(self.target_file, 'r').read()
        inject_line = "{linesep}{stmt}"
        for section in re.split(r'\n\n', content):
            if re.search(r'import', section) is not None:
                for imp_stmt in injection_context['import']:
                    section += inject_line.format(linesep=os.linesep,
                                                  stmt=imp_stmt)
                print(section, file=self.stream)
            elif re.search(r'def register_extensions', section) is not None \
                    and 'extension' in injection_context:
                for ext_stmt in injection_context['extension']:
                    section += inject_line.format(linesep=os.linesep,
                                                  stmt=ext_stmt)
                print(os.linesep + section, file=self.stream)
            elif re.search(r'def register_blueprints', section) is not None \
                    and 'blueprint' in injection_context:
                section += inject_line\
                    .format(linesep=os.linesep,
                            stmt=injection_context['blueprint'])
                print(os.linesep + section, file=self.stream)
            else:
                print(os.linesep + section, file=self.stream)
        with open(self.target_file, 'w') as init_file:
            init_file.write(self.stream.getvalue().rstrip())

    def _admin(self):
        project_name = self.config.project_name
        injection_directive = {
            'import': [
                "from {proj_name}.admin.views import admin"
                .format(proj_name=project_name),
                "from {proj_name}.admin.auth import login_manager, principals"
                .format(proj_name=project_name)
            ],
            'extension': [
                "{}principals.init_app(app)".format(self.indent),
                "{}login_manager.init_app(app)".format(self.indent),
                "{}admin.init_app(app)".format(self.indent)
            ]
        }
        return injection_directive

    def _blueprint(self, name):
        project_name = self.config.project_name
        injection_directive = {
            'import': [
                "from {proj_name}.{bp_name}.views import {bp_name}"
                .format(proj_name=project_name, bp_name=name)
            ],
            'blueprint':
                "{ndnt}app.register_blueprint({bp_nm}, url_prefix='/{bp_nm}')"
                .format(ndnt=self.indent, bp_nm=name)
        }
        return injection_directive

    def _api(self):
        # only responsible for including api
        pass


class SettingsInjector(InjectorBase):
    """Injects attributes into the Config object"""
    def __init__(self):
        super(SettingsInjector, self).__init__()
        self.target_file = self.config.settings

    def inject(self, directive, section='DevConfig'):
        known_directives = ['mail', 'flat_pages']
        if directive not in known_directives:
            raise ValueError('SettingsInjector:Uknown directive for injection')
        injection_context = getattr(self, "_{}".format(directive))()
        # make sure that there is 2 spaces between each class!
        watching, linesep = False, os.linesep
        for src_line in self.read_target():
            if watching:
                if src_line == '':
                    self.stream.writelines(["{}{}{}".format(self.indent,
                                                            line,
                                                            linesep)
                                            for line in injection_context])
            if re.search(section, src_line):
                watching = True
            self.stream.write("{}{linesep}".format(src_line, linesep))

    def _mail(self):
        """
        This targets the general Config object
        """
        pass


class AdminInjector(InjectorBase):
    def __init__(self):
        super(AdminInjector, self).__init__()
        admin_items = self.config.get_blueprint_info('admin')
        for item in admin_items:
            if item[0] == 'views':
                self.target_file = item[1]
                break

    def inject(self, directive):
        known_directives = ['blog']
        if directive not in known_directives:
            raise ValueError("AdminInjector:Unknown directive given to inject.")
        injection_context = getattr(self, "_{}".format(directive))()
        watching_imports, watching_views = True, False
        for line in self.read_target():
            if watching_imports:
                if line == "":
                    for import_directive in injection_context['import']:
                        print(import_directive, file=self.stream)
                    watching_imports = False
            if re.search(r'^admin.add_view', line):
                watching_views = True
            if watching_views:
                if line == "":
                    for view_addition in injection_context['views']:
                        print(view_addition, file=self.stream)
                    watching_views = False
            print(line, file=self.stream)
        with open(self.target_file, 'w') as new_admin:
            new_admin.write(self.stream.getvalue())

    def _blog(self):
        injection_context = {
            'import': ['from ..blog.admin import BlogPostView, TagView'],
            'views': [
                'admin.add_view(BlogPostView())',
                'admin.add_view(TagView())'
            ]
        }
        return injection_context


class SitemapInjector(InjectorBase):
    def __init__(self):
        super(SitemapInjector, self).__init__()
        public_items = self.config.get_blueprint_info('public')
        for item in public_items:
            if item[0] == 'views':
                self.target_file = item[1]
                break

    def inject(self, directive):
        known_directives = ['blog']
        if directive not in known_directives:
            raise ValueError("SitemapInjector:Unknown directive given")
        injection = getattr(self, "_{}".format(directive))()
        watch_helpers, watch_import, watch_page_append = True, False, False
        for line in self.read_target():
            if watch_helpers:
                if re.search(r'from flask.helpers', line):
                    if not re.search(r'url_for', line):
                        line = line.rstrip()
                        line = "{}, url_for".format(line)
                        watch_helpers = False
                        watch_import = True
            if watch_import:
                if line == '':
                    print(injection['import'], file=self.stream)
                    watch_import = False
            if re.search(r'sitemap.xml', line):
                watch_page_append = True
            if watch_page_append and re.search(r'sitemap_xml =', line):
                print(injection['code'], file=self.stream)
                watch_page_append = False
            print(line, file=self.stream)
        with open(self.target_file, 'w') as pub_view:
            pub_view.write(self.stream.getvalue())

    def _blog(self):
        template = path.join(get_templates_dir(), 'injectors', 'sitemap.txt')
        code = open(template, 'r').read()
        code = code.format(indent=self.indent)
        injection = {
            'import': "from ..blog.models import BlogPost, Tag",
            'code': code
        }
        return injection
