# -*- coding: utf-8 -*-
from flask_bcrypt import Bcrypt
flask_bcrypt = Bcrypt()

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_migrate import Migrate
migrate = Migrate()

from flask_cache import Cache
cache = Cache()

from flask_debugtoolbar import DebugToolbarExtension
toolbar = DebugToolbarExtension()

