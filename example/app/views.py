#!env/bin/python
# -*- coding: utf-8 -*-

from flask import render_template

from app import app
from app.models import Content
from wtforms import FileField
from config import UPLOADS_DIR

from flask.ext.admin.contrib.sqla import ModelView

import os

@app.route('/')
@app.route('/index')
def index():
    """ Main view """
    contents = Content.query.all()
    return render_template("index.html", contents=contents)



class MyFileField(FileField):

    def populate_obj(self, obj, name):
        if self.data:
            setattr(obj, name, self.data.filename)


class ContentView(ModelView):

    column_list = ("title", "image")

    form_overrides = dict(
        image=MyFileField
    )


    def __init__(self, session, **kwargs):
        super(ContentView, self).__init__(Content, session, **kwargs)

    def on_model_change(self, form, model, is_created):
        if form.image.data:
            filename = form.image.data.filename
            form.image.data.save(os.path.join(UPLOADS_DIR, filename))
