#!env/bin/python
# -*- coding: utf-8 -*-

from app import db

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255))

    def __unicode__(self):
        return self.title

