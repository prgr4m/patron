.. _Projects:

Projects
========

Creating a Project
------------------
Generate a project::

    patron project NameOfProject

Generate a project under a different directory name::

    patron project -d server NameOfProject

The project layout is fairly standard within the flask community but I tried 
not to make any assumptions (ex: everybody uses bootstrap). If you prefer to 
make any changes or would like to use another scaffold, you should look under 
the 'templates/base' subdirectory that is generated in the patron user 
directory.

Creating Tasks
--------------
Tasks are things done outside of your flask application. There are several 
tools that exist in the python community (paver comes to mind) but I have 
chosen to use fabric in order to get that `rake` functionality for python. 
This is the only python 2.x project dependency and will be switching over to 
invoke some time in the future.

To create a task, run the following command within a generated project::

    patron task name_of_task "description of task"

This will create a stub in the `fabfile.py` file in the project root directory. 
You can view the `fabric documentation`_ for more help.

.. _fabric documentation: http://docs.fabfile.org

