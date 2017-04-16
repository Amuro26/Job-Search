# -*- coding: utf-8 -*-

from app import app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)



