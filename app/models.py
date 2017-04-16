# -*- coding: utf-8 -*-
# 本部分是数据库模型


from app import db, app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import flask_whooshalchemyplus as whooshalchemyplus
from sqlalchemy.sql import func


def num_gen():
    s = str(datetime.utcnow())
    num = s[6] + s[8] + s[9] + s[11] + s[12] + s[14] + s[15] + s[17] + s[18]
    print(num)
    return int(num)


# User数据模型
class User(db.Model):  # 实例名称自动登记为user
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    password = db.Column(db.String(40), index=True)
    password_hash = db.Column(db.String(40), index=True)
    age = db.Column(db.Integer, index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(20), index=True, unique=True)
    education = db.Column(db.Text, index=True)
    working_experience = db.Column(db.Text, index=True)
    about_me = db.Column(db.Text, index=True)
    last_seen = db.Column(db.DateTime, index=True) #, default=datetime.utcnow())
    avatar = db.Column(db.String(120), index=True, unique=True, default='/static/avatar/default.jpg')
    # 以上的部分是数据库内部的数据，可以用user.id , user.password之类的方法在渲染模板里调用调用
    jobs = db.relationship('Job', backref='i_provider', lazy='dynamic')

    @property  # 密码不可直接获取
    def password(self):
        raise AttributeError('For security reason, password is not visible.')

    @password.setter  # 定义密码加密的方法和验证密码的方法（反加密）
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_authenticated(self):  # 是否已经登陆
        return True

    @property
    def is_active(self):  # 是否有登陆权限
        return True

    @property
    def is_anonymous(self):  # 是否允许匿名访问
        return False

    def get_id(self):
        try:
            return self.id
        except NameError:
            return 'Failed to get id.'

    def __repr__(self):
        return '<User %s>' % self.username


# Company数据模型
class Company(db.Model):  # 实例名称自动登记为company

    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(40), index=True, unique=True)
    username = db.Column(db.String(40), index=True, unique=True)
    password = db.Column(db.String(40), index=True)
    password_hash = db.Column(db.String(40), index=True)
    address = db.Column(db.String(40), index=True)
    contact = db.Column(db.String(20), index=True)
    telephone = db.Column(db.String(20), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    industry = db.Column(db.String(20), index=True)
    type = db.Column(db.String(20), index=True)
    found_year = db.Column(db.String(20), index=True)
    introduction = db.Column(db.Text, index=True)
    last_seen = db.Column(db.DateTime, index=True) #, default=datetime.utcnow())
    logo = db.Column(db.String(40), index=True, default='/static/avatar/default.jpg')

    jobs = db.relationship('Job', backref='c_provider', lazy='dynamic')


    @property  # 密码不可直接获取
    def password(self):
        raise AttributeError('For security reason, password is not visible.')

    @password.setter  # 定义密码加密的方法和验证密码的方法（反加密）
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_authenticated(self):  # 是否已经登陆
        return True

    @property
    def is_active(self):  # 是否有登陆权限
        return True

    @property
    def is_anonymous(self):  # 是否允许匿名访问
        return False

    def get_id(self):
        try:
            return self.id
        except NameError:
            return 'Failed to get id.'

    def __repr__(self):
        return '<Company %s>' % self.company_name


# Job数据模型
class Job(db.Model):
    __tablename__ = 'jobs'
    __searchable__ = ['job_name', 'company_name', 'job_detail', 'requirement', 'industry']
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    company_name = db.Column(db.String(20), index=True)
    job_name = db.Column(db.String(20), index=True)
    email = db.Column(db.String(40), index=True)
    industry = db.Column(db.String(20), index=True)
    salary = db.Column(db.String(10), index=True)  # 用string 还是 integer 存疑
    welfare = db.Column(db.Text, index=True)
    work_place = db.Column(db.String(20), index=True)
    requirement = db.Column(db.Text, index=True)
    job_detail = db.Column(db.Text, index=True)
    PS = db.Column(db.Text, index=True)
    avatar = db.Column(db.String(20), index=True, )
    timestamp = db.Column(db.DateTime, index=True) #, default=datetime.utcnow())

    def __repr__(self):
        return '<Job %s from %s>' % (self.job_name, self.company_name)


whooshalchemyplus.whoosh_index(app, Job)





