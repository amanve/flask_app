from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

app = Flask(__name__)
app.config['SECRETKEY'] = 'secretkey!'


class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')


if __name__ == '__main__':
    app.run()