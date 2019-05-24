import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginsForm, UpdateAccount, PostForm
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About', legend='About')


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


def save_img(form_img):
    r_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_img.filename)
    img_fn = r_hex + f_ext
    img_path = os.path.join(app.root_path, 'static/imgs', img_fn)

    out_size = (150, 150)
    i = Image.open(form_img)
    i.thumbnail(out_size)
    i.save(img_path)
    return img_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    upd_form = UpdateAccount()
    if upd_form.validate_on_submit():
        if upd_form.profile_img.data:
            img_file = save_img(upd_form.profile_img.data)
            current_user.img = img_file
        current_user.username = upd_form.user.data
        current_user.email = upd_form.email.data
        db.session.commit()
        flash('Your account has been updated.', 'Success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        upd_form.user.data = current_user.username
        upd_form.email.data = current_user.email
    account_img = url_for('static', filename='imgs/' + current_user.img)
    return render_template('account.html',
                           title='Your Account',
                           img=account_img,
                           form=upd_form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def create_post():
    post_form = PostForm()
    if post_form.validate_on_submit():
        post = Post(title=post_form.title.data,
                    content=post_form.content.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created.', 'Success')
        return redirect(url_for('home'))
    return render_template('new_post.html',
                           title='New Post',
                           form=post_form,
                           legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    post_form = PostForm()
    if post_form.validate_on_submit():
        post.title = post_form.title.data
        post.content = post_form.content.data
        db.session.commit()
        flash('Your post has been updated.', 'Success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        post_form.title.data = post.title
        post_form.content.data = post.content
    return render_template('new_post.html',
                           title='Update Post',
                           form=post_form,
                           legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def del_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.', 'Success')
    return redirect(url_for('home'))