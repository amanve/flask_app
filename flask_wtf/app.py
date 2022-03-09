from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config[
    'SECRET_KEY'] = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'


class LoginForm(FlaskForm):
  username = StringField(label=('username:'),
                         validators=[DataRequired(message='*Required')])
  password = PasswordField(label=('password:'),
                           validators=[DataRequired('*Required')])
  submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
  this_form = LoginForm()
  if this_form.validate_on_submit():
    return f'<h1>Username:{this_form.username.data} Password:{this_form.password.data}</h1>'

  return render_template('index.html', form=this_form)


if __name__ == '__main__':
  app.run()
