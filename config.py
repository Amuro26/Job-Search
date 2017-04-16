# -*- coding: utf-8 -*-

import os

CSRF_ENABLED = True  # 注意在html里面都加上{{ form.hidden_tag() }}来满足安全保护验证
SECRET_KEY = 'lijianpku15@163.com'
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
WHOOSH_BASE = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS = 40

UPLOAD_FOLDER = os.getcwd() + '/app/static/avatar'





