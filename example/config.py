#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
#
basedir = ROOT_DIR = os.path.abspath(os.path.dirname(__file__))


UPLOADS_DIR = os.path.join(basedir, "app/static/uploads")
DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = False
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'database.db'))
CSRF_ENABLED = True
SECRET_KEY = 'example-project-secret-key'

CURRENT_VERSION = "0.1"

try:
    from config_local import *
except ImportError:
    pass
