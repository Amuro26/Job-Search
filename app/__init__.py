# -*- coding: utf-8 -*-
# 本部分完成项目的初始化


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand
import flask_whooshalchemyplus

app = Flask(__name__)  # 启动app
app.config.from_object('config')  # 加载设置

db = SQLAlchemy(app)  # 链接数据库

manager = Manager(app)
lm = LoginManager()  # 启动login第三方模块
lm.session_protection = 'basic'
lm.login_view = 'login'  # 登记login的html文件
lm.init_app(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

flask_whooshalchemyplus.init_app(app)
flask_whooshalchemyplus.index_all(app)
from app import views  # 加载主逻辑views


