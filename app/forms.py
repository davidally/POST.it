from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    user = StringField('Username',
                       validators=[DataRequired(),
                                   Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    verify_pass = PasswordField(
        'Confirm Password', validators=[DataRequired(),
                                        EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_user(self, user):
        user = User.query.filter_by(username=user.data).first()
        if user:
            raise ValidationError(
                'Username is not available. Choose a different name.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is not available.')


class LoginsForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    stay_on = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccount(FlaskForm):
    user = StringField('Username',
                       validators=[DataRequired(),
                                   Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_img = FileField('Change profile picture',
                            validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_user(self, user):
        if user.data != current_user.username:
            user = User.query.filter_by(username=user.data).first()
            if user:
                raise ValidationError(
                    'Username is not available. Choose a different name.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is not available.')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')