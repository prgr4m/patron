# -*- coding: utf-8 -*-
# Purpose:
# This is the manager/factory to send the right kind of parser pending on
# conditions and features...
#
# Why:
# I only want to present the user the types of options that are necessary to
# their project since I plan on creating different types of scaffolds for the
# user rather than overloading the main parser when its not necessarily
# appropriate.
#
# Types of parsers:
# - Initial
#   This type of parser is for generating project types and general
#   configuration for the tooling as a whole
# - Main
#   This is the meat and potatoes parser in which is augmented with options only
#   pertaining to the type of project that the user has chosen. The different
#   project types I am choosing are: [tiny | blueprint | mvc]. Tiny would be for
#   a very basic scaffold type with just an project package and an app, model,
#   view and main file structure with the obligatory static and template
#   folders. Blueprint is the current standard and the mvc scaffold would be
#   akin to a padrino scaffold setup but using flask.
#
# Initial logic:
# - is the current working directory a patron project?
# - no: give the initial parser
# - yes: dynamically create the appropriate parser based on patron.json
#
# Initial parser:
# - check external dependencies
# - setup user directory
# - project generation
#   Type: 'tiny', 'blueprint', 'mvc'
#   ORM: alchemy, peewee, mongo
