# -*- coding: utf-8 -*-
import os.path as path
from flask.blueprints import Blueprint
from flask.globals import request
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.contrib.atom import AtomFeed
from ..extensions import pages

templates_dir = path.join(path.dirname(path.abspath(__file__)), 'templates')
blog = Blueprint('blog', __name__, template_folder=templates_dir)


@blog.context_processor
def processor():
    return dict()


@blog.route('/')
def index():
    # articles are pages with a publication date
    articles = (p for p in pages if 'published' in p.meta)
    # show the 10 most recent articles, most recent first
    latest = sorted(articles, reverse=True,
                    key=lambda p: p.meta['published'])
    return render_template('articles.jade', articles=latest[:10])


@blog.route('/<path:path>/')
def article(path):
    article = pages.get_or_404(path)
    return render_template('article.jade', article=article)


@blog.route('/tag/<string:tag>/')
def tag(tag):
    tagged = (p for p in pages if tag in p.meta.get('tags', []))
    return render_template('tag.jade', articles=tagged, tag=tag)


@blog.route('/feed.atom')
def feed():
    feed = AtomFeed('Recent Articles',
                    feed_url=request.url, url=request.url_root)
    articles = (p for p in pages if 'published' in p.meta)
    latest = sorted(articles, reverse=True,
                    key=lambda p: p.meta['published'])
    # need to look up specification for 'categories' in atom feeds
    # FeedItem requires list of dictionaries with 'term' being required
    # and (scheme, label) being optional
    # categories = tags
    for article in latest[:10]:
        feed.add(title=unicode(article.meta['title']),
                 content=article.html,
                 url=url_for('blog.article', path=article.path),
                 updated=article.meta['updated'],
                 published=article.meta['published'])
    return feed.get_response()
