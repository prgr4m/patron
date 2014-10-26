Basic Usage
===========
Patron is command line utility. To view the help at any time run the command 
with `-h` or `--help`::

    patron -h

Also, each respective command group has their own help, so just run a command 
and tack on a `-h` or `--help`:

Example::

    patron addon -h

Initialization and the User Directory
-------------------------------------
With patron you can currently initialize two settings for convenience:

* user template scaffolding
* global node modules used by the front-end work flow addon

The patron user directory on a linux/unix system is located at:

    ~/.patron

On a windows system, it is located at:

    $USERPROFILE/patron

To create the user scaffolding directory::

    patron init templates

As of version 0.2.2, patron uses cookiecutter for scaffolding so you can 
change or use your own cookiecutter flask templates to be used with this tool.
This is for user convenience. If you don't like using jade or the code that is 
being generated, this would be the way to customize the scaffolding.
This directory is hidden by default so you don't delete it on accident.

If you need help in customizing the templates, you can read the 
`cookiecutter documentation`_.

.. _cookiecutter documentation: http://cookiecutter.readthedocs.org/en/latest/

To create global node modules used by the front-end workflow, run::

    patron init frontend

This is used as a convenience in that when dealing with installing anything by 
node, package dependencies can take FOREVER. This command installs global 
commands run by the frontend work flow. When using the front-end addon, patron 
creates a symlink/mklink to the node modules folder in the patron user
directory so you don't have to play the waiting game when you should be 
writing code. This command also generates the user templates in the patron user 
directory but I have separated the commands because the user may not use the 
front-end work flow.

Tasks
-----
Tasks are things done outside of your flask application. There are several 
tools that exist in the python community (paver comes to mind) but I have 
chosen to use fabric (until invoke gets polished) in order to get that `rake` 
functionality for python.

To create a task, run the following command within a generated project::

    patron task name_of_task "description of task"

This will create a stub in the `fabfile.py` file in the project root directory. 
You can view the `fabric documentation`_ for more help.

.. _fabric documentation: http://docs.fabfile.org
