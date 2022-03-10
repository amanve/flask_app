from flask import Flask, render_template, request
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'

login_manager = LoginManager(app)
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(30), unique=True)


@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    user = User.query.filter_by(username=username).first()

    if not user:
      return 'User does not exist'

    login_user(user)
    return '<h1>you are logged in</h1>'

  return render_template('login.html')


@app.route('/home')
@login_required
def home():
  return f'<h1>You are in protected area {current_user.username}</h1>'


@app.route('/logout')
@login_required
def logout():
  logout_user()
  return '<h1>logged out. login again</h1>'


if __name__ == '__main__':
  app.run()
