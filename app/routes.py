from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginsForm
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [{
    'author': 'Admin',
    'title': 'Post One',
    'content': 'First post content.',
    'date': 'April 20, 2018'
}, {
    'author': 'Admin Two',
    'title': 'Post Two',
    'content': 'Second post content.',
    'date': 'April 20, 2018'
}]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        hash_pass = bcrypt.generate_password_hash(
            reg_form.password.data).decode('utf-8')
        new_user = User(username=reg_form.user.data,
                        email=reg_form.email.data,
                        password=hash_pass)
        db.session.add(new_user)
        db.session.commit()
        flash('Account successfully created.', 'Success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up', form=reg_form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    log_form = LoginsForm()
    if log_form.validate_on_submit():
        user = User.query.filter_by(email=log_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               log_form.password.data):
            login_user(user, remember=log_form.stay_on.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(
                url_for('home'))
        else:
            flash('Error: Check email and password.')
    return render_template('login.html',
                           title='Log Into Your Account',
                           form=log_form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Your Account')
