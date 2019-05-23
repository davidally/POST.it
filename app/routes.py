from flask import render_template, url_for, flash, redirect
from app import app
from app.forms import RegistrationForm, LoginsForm
from app.models import User, Post

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
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        flash('Account created for {}'.format(reg_form.user.data), 'Success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Sign Up', form=reg_form)


# Add POST validation
@app.route("/login")
def login():
    log_form = LoginsForm()
    return render_template('login.html',
                           title='Log Into Your Account',
                           form=log_form)