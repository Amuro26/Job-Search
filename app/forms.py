# -*- coding: utf-8 -*-
# 本部分处理html上面的表单数据

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import ValidationError
from .models import User, Company, Job


class UserRegisterForm(FlaskForm):  # in templates, add a blank for age
    username = StringField('username', validators=[DataRequired(), Length(min=0, max=20)])
    age = StringField('age', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('re_password', '输入的密码必须一致。')])
    re_password = PasswordField('re_password', validators=[DataRequired()])
    submit = SubmitField('注册')
    # 以上是用户注册表单的内容，可以用UserRegisterForm

    # 在验证表单的eamil时候会同时调用自定义的validate_email方法
    def validate_eamil(self, field):
        if User.query.filter_by(email=field.data).first() or Company.query.filter_by(email=field.data).first():
            raise ValidationError('此邮箱已被注册')


class CompanyRegisterForm(FlaskForm):  # bug = username 不能重复的问题！
    company_name = StringField('company_name', validators=[DataRequired()])
    # industry = StringField('industry', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    contact = StringField('contact', validators=[DataRequired()])
    telephone = StringField('telephone', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired(), Length(min=0, max=20)])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('re_password', '输入的密码必须一致。')])
    re_password = PasswordField('re_password', validators=[DataRequired()])
    submit = SubmitField('注册')

    # 在验证表单的eamil时候会同时调用自定义的validate_email方法
    def validate_eamil(self, field):
        if User.query.filter_by(email=field.data).first() or Company.query.filter_by(email=field.data).first():
            raise ValidationError('此邮箱已被注册')


class JobRegisterForm(FlaskForm):  # 有较大不同，和晨桥讨论一下
    # user_name = StringField('user_name', validators=[DataRequired()])
    company_name = StringField('company_name', validators=[DataRequired()])
    job_name = StringField('job_name', validators=[DataRequired()])
    industry = StringField('industry', validators=[DataRequired()])
    salary = StringField('salary', validators=[DataRequired()])
    welfare = TextAreaField('welfare', validators=[DataRequired()])
    work_place = StringField('work_place', validators=[DataRequired()])
    requirement = TextAreaField('edu_req', validators=[DataRequired()])   # 诸如时间、额外要求之类的，通过网页的展示要求发布者放在这一格
    job_detail = TextAreaField('job_detail', validators=[DataRequired()])
    PS = TextAreaField('ps', validators=[DataRequired()])  # 提供给信息发布者发布附加的一些杂项信息
    email = StringField('eamil', validators=[DataRequired(), Email()])
    submit = SubmitField('发布')


class SearchForm(FlaskForm):
    key_words = StringField('key_words', validators=[DataRequired()])
    search = SubmitField('搜索')


class UserLoginForm(FlaskForm):
    email = StringField('account', validators=[DataRequired()])  # 用email作为登录的账号，注意数据库端的处理
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    submit_user = SubmitField('立即登录')


class CompanyLoginForm(FlaskForm):
    email = StringField('account', validators=[DataRequired()])  # 用email作为登录的账号，注意数据库端的处理
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    submit_company = SubmitField('立即登录')


class UserEditForm(FlaskForm):  # 个人用户在 /user/<username> 页面修改自己的信息, 第一版使用一键修改所有的信息，以后看条件再提供单项信息，没有修改时，使用之前存在数据库里的信息
    age = StringField('age', validators=[Length(min=0, max=40)])
    phone = StringField('phone', validators=[Length(min=0, max=120)])
    email = StringField('email', validators=[Email(), Length(min=0, max=120)])
    password = PasswordField('password', validators=[EqualTo('re_password', '输入的密码必须一致。')])
    re_password = PasswordField('re_password', validators=[])
    education = TextAreaField('education', validators=[Length(min=0, max=400)])
    working_experience = TextAreaField('work_experience', validators=[Length(min=0, max=600)])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=600)])
    avatar = FileField('avatar')
    submit = SubmitField('提交')


class CompanyEditForm(FlaskForm):  # 公司用户在profile页面修改自己的信息
    password = PasswordField('password', validators=[EqualTo('re_password', '输入的秘密码必须一致。')])
    re_password = PasswordField('re_password', validators=[])
    company_name = StringField('company_name', validators=[])
    address = StringField('address', validators=[Length(min=0, max=120)])
    industry = StringField('industry', validators=[Length(min=0, max=60)])
    type = StringField('type', validators=[Length(min=0, max=60)])
    contact = StringField('contact', validators=[Length(min=0, max=40)])
    telephone = StringField('telephone', validators=[Length(min=0, max=120)])
    email = StringField('email', validators=[Length(min=0, max=120), Email()])
    found_year = StringField('found_year', validators=[Length(min=0, max=20)])
    introduction = TextAreaField('introduction', validators=[])
    logo = FileField('logo', validators=[])
    submit = SubmitField('提交')



