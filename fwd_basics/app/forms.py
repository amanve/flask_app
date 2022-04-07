from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField,
                     TextAreaField)
from wtforms.validators import (InputRequired, Email, EqualTo, ValidationError,
                                Length)
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    password2 = PasswordField('Retype Password',
                              validators=[InputRequired(),
                                          EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter(User.username == username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter(User.email == email.data).first()
        if user is not None:
            raise ValidationError('Email already registered.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    about_me = TextAreaField('About Me', validators=[Length(min=0, max=150)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter(User.username == username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')
