Basic Usage
===========
To view the help at any time run the command with `-h` or `--help`::

    patron -h

Also, each respective command group has their own help, so just run a command 
and tack on a `-h` or `--help`:

Example::

    patron addon -h

Initialization
--------------
With patron you can currently initialize 2 settings for convenience:

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
This is just for convenience. If you don't like using jade and prefer to type
more, this would be the way to customize the scaffolding. This directory is
hidden by default so you don't delete it on accident.

To create global node modules used by the front-end workflow, run::

    patron init frontend

This is used as a convenience in that when dealing with installing anything by 
node, package dependencies can take FOREVER. This command installs global 
commands run by the frontend work flow. When using the front-end addon, patron 
creates a symlink/mklink to the node modules folder in the patron user
directory so you don't have to play the waiting game when you should be 
writing code.


Task
----
To create a task (using fabric), run the following command::

    patron task name_of_task "description of task"

This will create a stub in the fabfile.py file in the project root directory.


