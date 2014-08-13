#!env/bin/python
# -*- coding: utf-8 -*-

from flask import *
from config import SQLALCHEMY_DATABASE_URI, CURRENT_VERSION

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager, Command, Server
from app import app, db



class InfoCommand(Command):
    "prints app info"

    def run(self):
        print "Current site version: " + CURRENT_VERSION
        print "Database URI: " + SQLALCHEMY_DATABASE_URI
        print "Satabase engine: " + db.engine.dialect.name

manager = Manager(app)
#manager.add_command('db', MigrateCommand)

manager.add_command('info', InfoCommand)

manager.add_command('runserver', Server())

if __name__ == '__main__':
    manager.run()