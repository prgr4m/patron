.. _Projects:

Projects
========

Creating a project
------------------
Generate a project::

    patron project NameOfProject

Generate a project under a different directory name::

    patron project -d server NameOfProject

The project layout is fairly common within the flask community but I tried 
not to make any assumptions (ex: everybody uses bootstrap). 

The base directory structure is as follows::

    project_root/
      |-- fabfile.py
      |-- project_name.fcgi
      |-- project_name-requirements.txt
      |-- project_name.wsgi
      |-- htaccess
      |-- manage.py
      |-- passenger_wsgi.py
      |-- patron.json
      |-- tests/
      |-- tmp/
      `-- project_name/                       <-- flask project
            |-- __init__.py                   <-- contains app factory
            |-- extensions.py
            |-- settings.py
            |-- public/
            |     |-- __init__.py
            |     |-- forms.py
            |     |-- models.py
            |     |-- views.py
            |     `-- templates/
            |           |-- index.jade
            |           `-- public_base.jade
            |-- static/
            `-- templates/
                  |-- 401.jade
                  |-- 403.jade
                  |-- 404.jade
                  |-- 500.jade
                  |-- base.jade
                  `-- includes/
                        |-- footer.jade
                        |-- meta.jade
                        `-- navigation.jade

The project scaffold does not provide anything extra other than what it needs.
The requirements file already contains the minimum for installation of all 
dependencies (excluding add-ons). Just pip install the requirements file with a 
virtualenv already activated. Whenever you use an add-on, patron will tell you 
what it added to the requirements file and then just pip install the 
requirements file again to use the add-on.

If you prefer to make any changes or would like to use another scaffold, you 
should look under the 'templates/base' subdirectory that is generated in the 
patron user directory.

Creating tasks
--------------
Tasks are things done outside of your flask application. There are several 
tools that exist in the python community (paver comes to mind) but I have 
chosen to use fabric in order to get that `rake` functionality for python. 
This is the only python 2.x project dependency and will be switching over to 
invoke+patchwork some time in the future.

To create a task, run the following command within a generated project::

    patron task name_of_task "description of task"

This will create a stub in the `fabfile.py` file in the project root directory. 
You can view the `fabric documentation`_ for more help.

.. _fabric documentation: http://docs.fabfile.org

So, what's next? :ref:`Resources <Resources>`.
