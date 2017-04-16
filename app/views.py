# -*- coding: utf-8 -*-
# 本部分处理视图和网站的逻辑


from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import UserRegisterForm, CompanyRegisterForm, JobRegisterForm, SearchForm, UserLoginForm, CompanyLoginForm, \
    UserEditForm, CompanyEditForm
from .models import User, Company, Job
from datetime import datetime
from config import MAX_SEARCH_RESULTS, UPLOAD_FOLDER
from sqlalchemy.sql.expression import func


# 每个试图访问网页的request都会先执行before_request函数
# 把当前的user或者company存到全局变量g里面
@app.before_request
def before_request():
    if 'phone' in dir(current_user):
        g.user = current_user
        if g.user.is_authenticated:
            g.user.last_seen = datetime.utcnow()
            db.session.add(g.user)
            db.session.commit()
    else:
        pass
    if 'telephone' in dir(current_user):
        g.company = current_user
        if g.company.is_authenticated:
            g.company.last_seen = datetime.utcnow()
            db.session.add(g.company)
            db.session.commit()
    else:
        pass
    g.search_form = SearchForm()


# login部分，需要一个加载用户的方法，和验证用户的方法
@lm.user_loader
def load_user(id):
    if User.query.get(int(id)):
        print('load user')
        return User.query.get(int(id))  # 在数据表User里面按id调取用户

    if Company.query.get(int(id)):
        print('load company')
        return Company.query.get(int(id))  # 在数据表Company里面按id调取用户


# 欢迎页的逻辑
@app.route('/', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
def index():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        g.key_words = search_form.key_words.data
        return redirect(url_for('search_result', query=g.key_words))
    return render_template('index.html', search_form=search_form)


# 主页
@app.route('/home', methods=['GET', 'POST'])
def home():
    page = request.args.get('page', 1, type=int)
    pagination = Job.query.order_by(Job.timestamp.desc()).paginate(page, per_page=6, error_out=False)
    jobs = pagination.items

    recommend = Job.query.order_by(func.random()).limit(6)
    # print(recommend)

    search_form = SearchForm()
    if search_form.validate_on_submit():
        g.key_words = search_form.key_words.data
        return redirect(url_for('search_result', query=g.key_words))
    return render_template('home.html', jobs=jobs, recommend=recommend, search_form=search_form, pagination=pagination)


@app.route('/register', methods=['GET', 'POST'])
def register():  # 发邮件进行注册验证的方法，可以考虑附加进来
    user_form = UserRegisterForm()
    company_form = CompanyRegisterForm()
    s = str(datetime.utcnow())
    num = s[6] + s[8] + s[9] + s[11] + s[12] + s[14] + s[15] + s[17] + s[18]
    # print(user_form.validate_on_submit())
    if user_form.validate_on_submit():
        user = User()
        user.username = user_form.username.data
        user.password = user_form.password.data
        user.age = user_form.age.data
        user.phone = user_form.phone.data
        user.email = user_form.email.data
        g.user = user
        db.session.add(g.user)
        db.session.commit()
        # flash('恭喜您，注册成功！')
        session.username = g.user.username
        print('register success.')
        return redirect(url_for('success1'))

    # 两类用户，是不是下面的所有方法都得分两类？
    if company_form.validate_on_submit():
        company = Company()
        company.id = int(num)
        company.company_name = company_form.company_name.data
        company.address = company_form.address.data
        company.contact = company_form.contact.data
        company.telephone = company_form.telephone.data
        company.username = company_form.username.data
        company.email = company_form.email.data
        company.password = company_form.password.data
        g.company = company
        db.session.add(g.company)
        db.session.commit()
        # flash('恭喜您，您的公司已经注册成功！')
        session.company_name = g.company.company_name
        return redirect(url_for('success2'))

    return render_template('register.html',
                           user_form=user_form,
                           company_form=company_form)


# search页面key_words表单
@app.route('/search', methods=['GET', 'POST'])
def search():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        g.key_words = search_form.key_words.data
        return redirect(url_for('search_result', query=g.key_words))
    return render_template('search.html',
                           search_form=search_form)


@app.route('/search_result/<query>', methods=['GET', 'POST'])
def search_result(query):
    results = Job.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    '''
    for result in results:
        print(result)
        print(type(result))
        print(result.work_place)
    '''
    search_form = SearchForm()
    if search_form.validate_on_submit():
        g.key_words = search_form.key_words.data
        return redirect(url_for('search_result', query=g.key_words))
    return render_template('search.html',
                           query=query,
                           results=results,
                           search_form=search_form)


# login 功能
@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('myhome1'))
    if g.company is not None and g.company.is_authenticated:
        return redirect(url_for('myhome2'))
    '''
    user_form = UserLoginForm(request.form)
    company_form = CompanyLoginForm(request.form)
    if user_form.validate_on_submit():
        print('submitted user')
        g.user = User.query.filter_by(email=user_form.email.data).first()  # 从数据库中查询当前登录表单的eamil
        if g.user is None:
            pass
        else:
            print(g.user.verify_password(user_form.password.data))
            if g.user is not None and g.user.verify_password(user_form.password.data):
                login_user(g.user)
                g.company = None
                return redirect(request.args.get('next') or '/user/%s' % g.user.email)
            flash('邮箱或密码错误。')

    if company_form.validate_on_submit():
        print('submitted company')
        g.company = Company.query.filter_by(email=company_form.email.data).first()
        print(g.company.verify_password(company_form.password.data))
        if g.company is not None and g.company.verify_password(company_form.password.data):
            login_user(g.company)
            print(type(g.company))
            g.user = None
            print('login_user success')
            return redirect(request.args.get('next') or '/company/%s' % g.company.email)
        flash('邮箱或密码错误。')

    return render_template('login.html',
                           user_form=user_form,
                           company_form=company_form)


# 登出 部分
@app.route('/logout')
@login_required
def logout():
    logout_user()
    # flash('您已经登出！')
    return redirect(url_for('index'))


# 个人用户资料展示部分
@app.route('/user/<email>')
@login_required
def user_detail(email):
    user = User.query.filter_by(email=email).first()
    search_form = SearchForm()
    if search_form.validate_on_submit():
        g.key_words = search_form.key_words.data
        return redirect(url_for('search_result', query=g.key_words))
    if user is None:
        redirect(url_for('404'))
    jobs = user.jobs.order_by(Job.timestamp.desc()).all()
    return render_template('showinfo1.html',
                           user=user,
                           jobs=jobs,
                           search_form=search_form)


# 个人资料修改部分
@app.route('/myhome1', methods=['GET', 'POST'])
@login_required
def myhome1():
    form = UserEditForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        if form.password.data is not '':
            current_user.password = form.password.data
        print('validate success')
        current_user.age = form.age.data
        current_user.phone = form.phone.data
        current_user.email = form.email.data
        current_user.password = form.password.data
        current_user.education = form.education.data
        current_user.working_experience = form.working_experience.data
        current_user.about_me = form.about_me.data
        # 新增头像部分
        avatar = request.files['avatar']
        fname = avatar.filename
        ALLOWED_EXTENTIONS = ['png', 'jpg', 'jpeg', 'gif']
        flag = '.' in fname and fname.rsplit('.', 1)[1] in ALLOWED_EXTENTIONS
        if not flag:
            flash('文件类型错误。')
            return redirect(url_for('myhome1'))
        print('avatar success')
        avatar.save('{}/{}_{}'.format(UPLOAD_FOLDER, current_user.username, fname))
        current_user.avatar = '/static/avatar/{}_{}'.format(current_user.username, fname)
        db.session.add(current_user)
        db.session.commit()
        return redirect('/user/%s' % current_user.email)
    form.age.data = current_user.age
    form.phone.data = current_user.phone
    form.email.data = current_user.email
    # form.password.data = current_user.password
    form.education.data = current_user.education
    form.working_experience.data = current_user.working_experience
    form.about_me.data = current_user.about_me
    return render_template('myhome1.html', form=form, user=current_user)


# 公司用户资料展示部分
@app.route('/company/<email>')
@login_required
def company_detail(email):
    print('company_detail success')
    search_form = SearchForm()
    if search_form.validate_on_submit():
        g.key_words = search_form.key_words.data
        return redirect(url_for('search_result', query=g.key_words))
    company = Company.query.filter_by(email=email).first()
    if company is None:
        redirect(url_for('404'))
    jobs = Job.query.filter_by(company_id=company.id).limit(6)
    return render_template('showinfo2.html',
                           company=company,
                           jobs=jobs,
                           search_form=search_form)


# 公司资料的修改部分
@app.route('/myhome2', methods=['GET', 'POST'])
@login_required
def myhome2():
    form = CompanyEditForm()
    if form.validate_on_submit():
        if form.password.data is not '':
            g.company.password = form.password.data
        g.company.address = form.address.data
        g.company.contact = form.contact.data
        g.company.telephone = form.telephone.data
        g.company.eamil = form.email.data
        g.company.introduction = form.introduction.data
        # 新增头像部分
        avatar = request.files['logo']
        fname = avatar.filename
        ALLOWED_EXTENTIONS = ['png', 'jpg', 'jpeg', 'gif']
        flag = '.' in fname and fname.rsplit('.', 1)[1] in ALLOWED_EXTENTIONS
        if not flag:
            flash('文件类型错误。')
            return redirect(url_for('myhome2'))
        avatar.save('{}/{}_{}'.format(UPLOAD_FOLDER, g.company.company_name, fname))
        g.company.logo = '/static/avatar/{}_{}'.format(g.company.company_name, fname)
        db.session.add(g.company)
        db.session.commit()
        return redirect('/company/%s' % g.company.email)
    form.company_name.data = g.company.company_name
    form.address.data = g.company.address
    form.contact.data = g.company.contact
    form.telephone.data = g.company.telephone
    form.email.data = g.company.email
    form.introduction.data = g.company.introduction
    form.logo.data = g.company.logo
    return render_template('myhome2.html', form=form, company=g.company)


# 公司信息展示部分
@app.route('/<company_name>/information')
def company_inf(company_name):
    search_form = SearchForm()
    if search_form.validate_on_submit():
        g.key_words = search_form.key_words.data
        return redirect(url_for('search_result', query=g.key_words))
    company = Company.query.filter_by(company_name=company_name).first()
    if company is None:
        redirect(url_for('404'))
    return render_template('companydetail.html',
                           company=company,
                           search_form=search_form)


# 招聘信息发布部分
@app.route('/newjob', methods=['GET', 'POST'])
@login_required
def newjob():
    form = JobRegisterForm()
    job = Job()
    try:
        if g.user is not None:
            if form.validate_on_submit():
                job.user_id = g.user.id
                # print('user_id 设置成功')
                job.username = g.user.username
                job.avatar = g.user.avatar
                job.company_name = form.company_name.data
                job.job_name = form.job_name.data
                job.salary = form.salary.data
                job.industry = form.industry.data
                job.work_place = form.work_place.data
                job.requirement = form.requirement.data
                job.job_detail = form.job_detail.data
                job.PS = form.PS.data
                job.email = form.email.data
                job.i_provider = current_user._get_current_object()
                db.session.add(job)
                db.session.commit()
                return redirect(url_for('success3'))
            else:
                flash('提交失败, 您可以重新提交。')
    except:
        if g.company is not None:
            if form.validate_on_submit():
                job.company_id = g.company.id
                print('company_id success.')
                # job.username = g.user.username
                job.company_name = form.company_name.data
                job.avatar = g.company.logo
                job.job_name = form.job_name.data
                job.salary = form.salary.data
                job.industry = form.industry.data
                job.work_place = form.work_place.data
                job.requirement = form.requirement.data
                job.job_detail = form.job_detail.data
                job.PS = form.PS.data
                job.c_provider = current_user._get_current_object()
                db.session.add(job)
                db.session.commit()
                return redirect(url_for('success3'))
            else:
                flash('提交失败, 您可以重新提交。')

    return render_template('newjob.html', form=form)


# 招聘信息详细展示
@app.route('/job_detail/<job_id>')
def job_detail(job_id):
    job = Job.query.filter_by(id=job_id).first()
    company_job = None
    if job.company_id:
        company_job = Job.query.filter_by(company_id=job.company_id).limit(3)
    jobs = Job.query.order_by(func.random()).limit(6)

    search_form = SearchForm()
    if search_form.validate_on_submit():
        g.key_words = search_form.key_words.data
        return redirect(url_for('search_result', query=g.key_words))

    return render_template('jobdetail.html', job=job, company_job=company_job, jobs=jobs, search_form=search_form)


# 两个success页面
@app.route('/success1')
def success1():
    return render_template('success1.html')


@app.route('/success2')
def success2():
    return render_template('success2.html')


@app.route('/success3')
def success3():
    return render_template('success3.html')



