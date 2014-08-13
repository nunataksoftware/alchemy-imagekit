#!env/bin/python
# -*- coding: utf-8 -*-

from config import SQLALCHEMY_DATABASE_URI

from app import app

from app import db

import os.path

print "Creating database on: " + SQLALCHEMY_DATABASE_URI

db.create_all()
