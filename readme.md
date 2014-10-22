# Patron

## Overview

Patron is a cli generator for [Flask](http://flask.pocoo.org) modeled after 
[Padrino’s](http://www.padrinorb.com/guides/generators) generators but 
following flask conventions.

The philosophy behind this cli generator is to provide functionality 
incrementally to a project by generating code from prefab scripts into an 
existing (generated) code base. While other scaffolds provide you with a solid 
base for your flask projects, this tool is more focused on speed of 
development and common patterns generally found in web development so you can 
spend more time writing actual code to solve specific problems.

## Documentation

Can be found on [pythonhosted](http://pythonhosted.org/patron/).

This tooling was originally created for my own personal use and now has been 
open sourced.

## Repository details
Main repo on [bitbucket](https://bitbucket.org/prgr4m/patron) and a mirror 
on [github](https://github.com/prgr4m/patron).

## Todo

- form generator similar to model generator
- addons (at a minimum matching padrino's set but adding on other patterns)
- argcompletion for cli (linux)
- python 3.x support
- create list of packages being used by each addon and why
- revise static site generator
- revisit admin addon and move registration into public via injection
- patron logo
- revise model generator
    - shorter commands without losing meaning
    - update cli documentation for models
    - create modular orm support so people can just plug in their own
- update docs to have feature matrix and road map
- multi page public docs for easier navigation on users

## Change Log

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

## Thanks goes to...
- @audreyr for making cookiecutter
- @mitsuhiko for creating flask
- the flask community for being awesome
- the padrino [team](http://www.padrinorb.com/team).

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
