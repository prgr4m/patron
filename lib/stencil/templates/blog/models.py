# -*- coding: utf-8 -*-
import datetime as dt
from ..extensions import db


tags_posts = db.Table(
    'tags_posts',
    db.Column('blog_id', db.Integer, db.ForeignKey('blog_posts.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)


class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    summary = db.Column(db.String(100))
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=dt.datetime.now)
    date_published = db.Column(db.DateTime)
    date_updated = db.Column(db.DateTime)
    tags = db.relationship('Tag', secondary=tags_posts,
                           backref=db.backref('posts', lazy='dynamic'))

    def slugify(self):
        return self.title.lower().replace(' ', '-')

    def __str__(self):
        return self.title

    def __repr__(self):
        return "<BlogPost: %s>" % self.title


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Tag: %s>" % self.name
