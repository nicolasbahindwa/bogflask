from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
 
from blog.users.forms import (RegistrationForm, LoginForm, UpdadeAccountForm,
                              ResetPasswordForm, RequestResetFrom)
from blog import db, bcrypt
# from blog.users.models import User
# from blog.posts.models import Post
from blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from blog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
                        form.password.data).decode('utf--8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created, Your username:{form.username.data} !',
              'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login",  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                    user.password, form.password.data):
            next_page = request.args.get('next')
            login_user(user, remember=form.remember.data)
            flash('welcome to our blog', 'success')
            return redirect(
                   next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. check email and password', 'danger')
    return render_template('login.html', title='Register', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdadeAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.image_file = picture_file
        db.session.commit()
        flash('You have upated your account', 'success')
        return redirect(url_for('users.account'))
    else:
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',
                         filename='profile/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date.desc())\
        .paginate(page=page, per_page=2)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetFrom()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An password reset email have been sent to your account', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',
                           title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
                        form.password.data).decode('utf--8')
        user.password = hashed_password
        db.session.commit()
        flash('Your Password have been reset', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_token.html',
                           title='Reset Password', form=form)

