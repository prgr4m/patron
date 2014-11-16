Basic Usage
===========
Patron is command line utility and has an adaptive parser. It basically 
switches modes when you are working with a patron project or not.

To view the help at any time run the command with `-h` or `--help`::

    patron -h

Each respective command group has their own help, so just run a command 
and tack on a `-h` or `--help`:

Example::

    patron project -h

Initialization
--------------
When using the patron command outside of a patron project you only have 2 
options available to you:

* init
* project

Anything dealing with patron itself is done through the `init` command group 
and has the following actions:

check
  Patron checks to see if the (minimal) external commands are present on your 
  path for running the front-end work flow.

user
  Patron will create a user directory that contains user templates that
  can be overridden to the user's liking. It will also install the necessary 
  packages for the front-end work flow as a convenience so the user won't 
  have to wait FOREVER whenever using the `frontend` addon with multiple 
  projects as they are symlink'd/mklink'd to this directory.

docs
  This option will open up the documentation that you are reading within a 
  web browser for easier lookups on what types a generator supports.

.. note::

    The patron user directory on a linux/unix system is located at:

        ~/.patron

    On a windows system, it is located at:

        $USERPROFILE/patron

    As of version 0.2.2, patron uses cookiecutter for scaffolding so you can 
    change or use your own cookiecutter flask templates to be used with this tool.
    This is for user convenience. If you don't like using jade or the code that is 
    being generated, this would be the way to customize the scaffolding.
    This directory is hidden by default so you don't delete it on accident.

    If you need help in customizing the templates, you can read the 
    `cookiecutter documentation`_.

    .. _cookiecutter documentation: http://cookiecutter.readthedocs.org/en/latest/

The next thing to do is learn how to create several types of 
:ref:`projects <Projects>`.
