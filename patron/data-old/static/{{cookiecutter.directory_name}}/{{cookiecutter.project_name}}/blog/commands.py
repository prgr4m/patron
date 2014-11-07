# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime as dt
import os
import os.path as path
import sys
from flask_script.commands import Command, Option
from flask_script.cli import prompt

article_dir = path.join(path.dirname(path.realpath(__file__)), 'articles')


class Article(Command):
    "Create new article entry stubs"
    option_list = (
        Option('--title', '-t', dest='title', default=None),
    )

    def run(self, title):
        if not title:
            title = prompt('Title of article')
        filename = "{}.md".format(title.lower().replace(' ', '-'))
        if filename in os.listdir(article_dir):
            print("Article already exists!")
            sys.exit()
        file_path = path.join(article_dir, filename)
        with open(file_path, 'w') as article:
            lines = [
                "title: {}".format(title),
                "date: {}".format(dt.datetime.now().strftime('%Y-%m-%d')),
                "tags: []",
                "# author: Your name here...",
                "# published: YEAR-MO-DA",
                "# updated: YEAR-MO-DA",
                "# summary: ",
                "",
                "#{}".format(title),
                "---",
                "Place content below"
            ]
            article.writelines(["%s%s" % (line, os.linesep) for line in lines])
        print("Created article at:{}".format(file_path))
