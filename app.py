from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginsForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'f9bf78b9a18ce6d46a0cd2b0b86df9da'

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


if __name__ == "__main__":
    app.run(debug=True)