from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

app = Flask(__name__)
app.config['SECRET_KEY'] = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'


class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')

@app.route('/',methods=['GET','POST'])
def index():
    form=LoginForm()

    return render_template('index.html',form=form)


if __name__ == '__main__':
    app.run()