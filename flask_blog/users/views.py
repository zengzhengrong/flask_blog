from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_blog.users.forms import (RegistrationForm,LoginForm,AccounForm,
                            RequestResetPasswordForm,ResetPasswordForm)
from flask_blog.models import User,Post,Account
from flask_blog import bcrypt,db
from flask_login import current_user,login_user,logout_user,login_required
from flask_blog.utils import save_img_as,send_reset_email
from datetime import datetime

users = Blueprint('users',__name__)

@users.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        flash(f'无效操作：{current_user.username} 请退出当前账号再进行操作','danger')
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hash_password)
        account = Account()
        user.account = account
        db.session.add(user)
        db.session.commit()
        flash(f'注册成功 - { form.username.data } 请用邮箱登陆','primary')
        return redirect(url_for('users.login'))
    return render_template('register.html',form=form,title='注册')

@users.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        flash(f'无效操作：{current_user.username} 你已在登陆状态','danger')
        return redirect(url_for('main.home'))
    form = LoginForm()
    rest_password_form = RequestResetPasswordForm() # modal from 
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            flash(f'登陆成功','primary')
            # print(dict(request.args)) # 转dict显示
            next_page = request.args.get('next')
            return redirect(url_for('users.account')) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'登陆失败 ： 邮箱或密码错误','danger')
    return render_template('login.html',form=form,title='登陆',rest_form=rest_password_form)

@users.route('/logout')
def logout():
    flash(f'{current_user.username} 已退出登陆','primary')
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = AccounForm()
    user_account = current_user.account
    if form.validate_on_submit():
        if form.avatar.data: # save as avatar
            avatar = save_img_as(form.avatar.data)
            current_user.image_file = avatar
        user_account.biography = form.biography.data
        user_account.location = form.location.data
        user_account.qq = form.qq.data
        user_account.phone = form.phone.data
        user_account.sex = form.sex.data
        db.session.commit()
        flash('更新成功','primary')
        return redirect(url_for('users.account'))
    if request.method == 'GET':
        form.sex.data = user_account.sex
        form.biography.data = user_account.biography
        form.location.data = user_account.location
        form.qq.data = user_account.qq
        form.phone.data = user_account.phone
    avatar = url_for('static',filename='account/avatar/' + current_user.image_file)
    return render_template('account.html',title='账户',avatar=avatar,form=form)

@users.route('/user/<string:username>/detail')
def user_detail(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    # print(datetime.now())
    posts = Post.query.filter_by(author=user).order_by(Post.created_time.desc()).paginate(page=page,per_page=10)
    avatar = url_for('static',filename='account/avatar/' + user.image_file)
    return render_template('user_detail.html',title=f'用户详情:{user.username}',user=user,avatar=avatar,posts=posts)

@users.route('/user/request/reset_password',methods=['GET','POST'])
def request_reset_password():
    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        token = user.generate_rest_token()
        link = url_for('users.resetpassword_by_token',token=token,_external=True) # full path
        send_reset_email(user.email,token,link)
        flash(f'已发送重置链接到{form.email.data}','info')
        return redirect(url_for('users.login'))
    return render_template('reqeust_resetpw.html',title=f'请求重置密码',form=form)

@users.route('/user/request/reset_password/<token>',methods=['GET','POST'])
def resetpassword_by_token(token):
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.verify_rest_token(token) # return User object
        if user is None:
            flash('异常:用户验证失败或操作超时','danger')
            return redirect(url_for('users.login'))
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hash_password
        db.session.commit()
        flash(f'{user.username} 密码重置成功，请重新登陆','primary')
        return redirect(url_for('users.login'))
    return render_template('resetpassword.html',title=f'重置密码',form=form)

@users.route('/user/request/reset_password_moadl',methods=['POST'])
def request_reset_password_modal():
    # request rest passwrod from with modal
    form = LoginForm()
    rest_password_form = RequestResetPasswordForm()
    # print(rest_password_form.email.data)
    user = User.query.filter_by(email=rest_password_form.email.data).first()
    if user is None:
        flash('不存在这个邮箱','danger')
    if rest_password_form.validate_on_submit():
        user = User.query.filter_by(email=rest_password_form.email.data).first()
        token = user.generate_rest_token()
        link = url_for('users.resetpassword_by_token',token=token,_external=True) # full path
        send_reset_email(user.email,token,link)
        flash(f'已发送重置链接到{rest_password_form.email.data}','info')
        return redirect(url_for('users.login'))
    return redirect(url_for('users.login'))