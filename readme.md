# Patron

## Overview

Patron is a cli generator for [Flask](http://flask.pocoo.org) inspired by 
[Padrino’s](http://www.padrinorb.com/guides/generators) generators but 
following flask conventions.

The philosophy behind this cli generator is to provide functionality 
incrementally to a project by generating code into an existing (generated) 
code base. While other scaffolds provide you with a solid base for your flask 
projects, this tool is more focused on speed of development so you can spend 
more time writing actual code to solve specific problems.

## Documentation

Can be found on [pythonhosted](http://pythonhosted.org/patron/).

This tooling was originally created for my own personal use and now has been 
open sourced.

## Repository details
Main repo on [bitbucket](https://bitbucket.org/prgr4m/patron) and a mirror 
on [github](https://github.com/prgr4m/patron).

## Patron Changelog

#### 0.2.3
- rewrite of project so it doesn't smell like java
- added python 3 support
- multi-page documentation format for easier organization and navigation
- rewrite of parser to show only relevant options when dealing with a project or not
- added check of minimal external dependencies
- removed '|' in cookiecutter filenames in case of users running Windows
- removal of static site generator as a project scaffold
- removal of blog addon
- added packages generation to flask projects
- added cli option to open official docs in browser
- ability to add extra routes to blueprint scaffolding along with option to exclude templates generated
- revised sqlalchemy model generator to have relations as an option along with fields without mixing the two
- added wtforms generator
- revised frontend addon workflow
- revised admin addon to have cleaner structure and moved users out into its own addon/blueprint
- added api parser for creating Resource/MethodView based api rather than just using function based routes

#### 0.2.2
- conversion to cookiecutter for users to be able to override scaffolds
- changed patron project configuration implementation from ini to json format
- added option in cli to create user template directory
- fixed minor bugs in code being generated
- added front-end work flow to addons
- added public facing documentation

#### 0.2.1
- published python package

#### 0.2.0 and below
- model generators functionality
- blog addon functionality
- admin addon functionality
- static site generator functionality
- blueprint registration functionality
- initial project creation with scaffolding ripped out of stencil


## Copyright
Copyright (c) 2014 John Boisselle

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
of the Software, and to permit persons to whom the Software is furnished to do 
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.
