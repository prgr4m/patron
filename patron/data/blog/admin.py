# -*- coding: utf-8 -*-
import datetime as dt
from markupsafe import Markup
from flask_admin.contrib.sqla import ModelView
from wtforms.fields import BooleanField
from ..extensions import db
from .models import BlogPost, Tag
from .forms import CKTextAreaField


class BlogPostView(ModelView):
    form_overrides = dict(text=CKTextAreaField, published=BooleanField)
    column_list = ('title', 'created', 'published', 'updated', 'tags')
    form_excluded_columns = ('created', 'updated', 'slug')
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
            new_blog_post.slug = new_blog_post.slugify()
            new_blog_post.content = Markup.escape(form.content.data)
            new_blog_post.updated = now
            db.session.add(new_blog_post)
            db.session.commit()
            return True
        except Exception:
            return False

    def update_model(self, form, model):
        try:
            published = model.published
            title = model.title
            form.populate_obj(model)
            now = dt.datetime.now()
            model.content = Markup.escape(form.content.data)
            model.updated = now
            if form.published.data:
                if not published:
                    model.published = now
            else:
                model.published = None
            if form.title.data != title:
                model.slug = model.slugify()
            db.session.commit()
            return True
        except Exception:
            return False


class TagView(ModelView):
    def __init__(self, **kwargs):
        super(TagView, self).__init__(Tag, db.session, **kwargs)
