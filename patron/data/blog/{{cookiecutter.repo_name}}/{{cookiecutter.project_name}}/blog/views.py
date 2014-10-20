# -*- coding: utf-8 -*-
import os.path as path
from flask.blueprints import Blueprint
from flask.globals import request
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.contrib.atom import AtomFeed
from .models import BlogPost, Tag

templates_dir = path.join(path.dirname(path.abspath(__file__)), 'templates')
blog = Blueprint('blog', __name__, template_folder=templates_dir)


@blog.context_processor
def processor():
    return dict()


@blog.route('/')
def index():
    articles = BlogPost.query.filter(BlogPost.published)\
        .order_by(BlogPost.published).limit(10).all()
    return render_template('articles.jade', articles=articles)


@blog.route('/<path:path>/')
def article(path):
    article = BlogPost.query.filter(BlogPost.slug == path).first_or_404()
    return render_template('article.jade', article=article)


@blog.route('/tag/<string:tag>/')
def tag(tag):
    articles = Tag.filter(name=tag).all().posts
    return render_template('tag.jade', articles=articles, tag=tag)


@blog.route('/feed.atom')
def feed():
    feed = AtomFeed('Recent Articles',
                    feed_url=request.url, url=request.url_root)
    articles = BlogPost.query.filter(BlogPost.published)\
        .order_by(BlogPost.published).all()
    # need to look up specification for 'categories' in atom feeds
    # FeedItem requires list of dictionaries with 'term' being required
    # and (scheme, label) being optional
    # categories = tags
    for article in articles:
        feed.add(title=unicode(article.title),
                 content=article.content,
                 url=url_for('blog.article', path=article.slugify()),
                 updated=article.updated,
                 published=article.published)
    return feed.get_response()
