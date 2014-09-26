from flask_admin.contrib.sqla import ModelView
from .models import BlogPost, Tag
from .forms import CKTextAreaField


# ckeditor for content field
# should be able to create tags dynamically from blog post creation
# do not display dates and just have a checkbox for publishing or not
class BlogPostView(ModelView):
    form_overrides = dict(text=CKTextAreaField)
    create_template = "admin/blog_create.jade"
    edit_template = "admin/blog_edit.jade"

    def __init__(self, session, **kwargs):
        super(BlogPostView, self).__init__(BlogPost, session, **kwargs)


class TagView(ModelView):
    def __init__(self, session, **kwargs):
        super(TagView, self).__init__(Tag, session, **kwargs)
