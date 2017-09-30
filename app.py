# coding=utf-8
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mako import MakoTemplates, render_template
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__, template_folder='./templates',
            static_folder='./static')
app.config.from_object('config')

db = SQLAlchemy(app)

bootstrap = Bootstrap(app)

mako = MakoTemplates(app)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

migration = Migrate(app, db)

# mako.init_app(app)
db.init_app(app)
