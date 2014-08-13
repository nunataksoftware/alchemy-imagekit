#!env/bin/python
# -*- coding: utf-8 -*-


from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from config import DEBUG
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin
from config import UPLOADS_DIR

app = Flask(__name__)

app.config.from_object('config')

app.debug = DEBUG
db = SQLAlchemy(app)

toolbar = DebugToolbarExtension(app)

admin = Admin(app)

from app.views import *

admin.add_view(ContentView(db.session))


if not os.path.exists(UPLOADS_DIR):
    os.mkdir(UPLOADS_DIR)
