# Hatsudenki - 発電機 - (generator)

---

# Overview
Stencil is a generator for [Flask](http://flask.pocoo.org) modeled after 
[Padrino](http://padrinorb.com)'s generators particular to my workflow. I 
originally wrote [Stencil](https://bitbucket.org/prgr4m/stencil-original) 
but have changed my workflow since then and have separated a web based project 
into client and server workflows since they are 2 different problems to be 
solved.

There are a couple of things that will be kept in from the original stencil 
codebase:

- livereload for the development server
- app factory creation
- admin and user models (with slight modifications)

Significant changes will be made:

- Transitioning to flask-classy
- Possible integration with flask-bouncer
- Add-ons with piecemeal features
- Underlying codebase as a whole
- argcomplete
- model scaffolding
- form scaffolding
- admin interface customization
- fabric scripts generation rather than an empty stub
- cms
- blog
- sitemap
- banning interface
- ecommerce addon
- jade templates
- transition script for node workflow to flask (using jade)

Stencil's multiple project creation and asset management has been broken off 
into another project (still to be written) as my focus is making this tool 
solely for flask and only flask. You know, the whole Unix philosophy...

I still have yet to find a tool for flask that'll give me the flexibility and 
speed of development such as rails, padrino and django. Yeah, I'm a python 
coder but I don't use django... and I write code in ruby but I don't use rails 
either. I just don't care for too much fluff when I don't need it in a project.
But then again, flask doesn't assume anything, and you can build things 
particular to your needs, which is why I love it! Hence the reason for creating 
this tooling.

## Copyright
Copyright (c) 2014 John Boisselle. MIT Licensed.

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
