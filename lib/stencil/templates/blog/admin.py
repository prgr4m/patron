# -*- coding: utf-8 -*-
import datetime as dt
from flask_admin.contrib.sqla import ModelView
from wtforms.fields import BooleanField
from ..extensions import db
from .models import BlogPost, Tag
from .forms import CKTextAreaField


def date_fmt():
    return '%a %b %d, %Y - %I:%M:%S %p'


class BlogPostView(ModelView):
    form_overrides = dict(text=CKTextAreaField, published=BooleanField)
    column_list = ('title', 'created', 'published', 'updated')
    column_formatters = {
        'created': lambda v, c, m, n: m.created.strftime(date_fmt()),
        'published': lambda v, c, m, n: m.published.strftime(date_fmt()),
        'updated': lambda v, c, m, n: m.updated.strftime(date_fmt())
    }
    form_excluded_columns = ('created', 'updated')
    create_template = "admin/blog_create.jade"
    edit_template = "admin/blog_edit.jade"

    def __init__(self, **kwargs):
        super(BlogPostView, self).__init__(BlogPost, db.session, **kwargs)

    def create_model(self, form):
        try:
            new_blog_post = BlogPost()
            form.populate_obj(new_blog_post)
            now = dt.datetime.now()
            if form.published.data:
                new_blog_post.published = now
            else:
                new_blog_post.published = None
            new_blog_post.updated = now
            db.session.add(new_blog_post)
            db.session.commit()
            return True
        except Exception:
            return False

    def update_model(self, form, model):
        try:
            published = model.published
            form.populate_obj(model)
            now = dt.datetime.now()
            model.updated = now
            if form.published.data:
                if not published:
                    model.published = now
            else:
                model.published = None
            db.session.commit()
            return True
        except Exception:
            return False


class TagView(ModelView):
    def __init__(self, **kwargs):
        super(TagView, self).__init__(Tag, db.session, **kwargs)
