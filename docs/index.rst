.. Patron documentation master file, created by
   sphinx-quickstart on Sat Oct 25 13:46:08 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Patron documentation
====================

**Patron** is a cli generator for `Flask`_ inspired by `Padrino's`_ 
generators but following flask conventions.

.. _Flask: http://flask.pocoo.org
.. _Padrino's: http://www.padrinorb.com/guides/generators

The philosophy behind this cli generator is to provide functionality 
*incrementally* to a project by generating code from prefab scripts into an 
existing (generated) code base. While other scaffolds provide you with a solid
base for your flask projects, this tool is more focused on *speed* of 
development and common patterns generally found in web development so you can 
spend more time writing actual code to solve specific problems.

If you would like to report any issues, please open an issue `here`_.

.. _here: https://bitbucket.org/prgr4m/patron/issues

User Guide
----------

.. toctree::
   :maxdepth: 2

   introduction
   basic_usage
   projects
   blueprints
   model_generator
   addons
   changelog

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
