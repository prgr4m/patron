from flask_admin.contrib.sqla import ModelView
from .models import BlogPost, Tag


class BlogPostView(ModelView):
    def __init__(self, session, **kwargs):
        super(BlogPostView, self).__init__(BlogPost, session, **kwargs)

