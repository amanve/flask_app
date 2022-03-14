from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from flask_admin.contrib.fileadmin import FileAdmin
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user

from os.path import dirname, join

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admin_app.db'
app.config['SECRET_KEY'] = 'mysecret!'

db = SQLAlchemy(app)
admin = Admin(app, template_mode='bootstrap4')
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
  return User.query.filter_by(id=int(user_id)).first()


class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String, unique=True)
  password = db.Column(db.String)
  age = db.Column(db.Integer)
  birthday = db.Column(db.DateTime)

  comments = db.relationship('Comment', backref='User', lazy='dynamic')

  def __repr__(self):
    return f'<User {self.username}>'


class Comment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  commentText = db.Column(db.String(200))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __repr__(self):
    return f'<Comment {self.commentText}>'


class NotificationView(BaseView):

  @expose('/')
  def index(self):
    return self.render('admin/notification.html')
    # return 'Hello World'


class UserView(ModelView):
  column_exclude_list = []
  column_display_pk = True
  can_create = True
  can_edit = True
  can_delete = True
  can_export = True

  def on_model_change(self, form, model, is_current):
    model.password = generate_password_hash(model.password, method='sha256')

  inline_models = [Comment]

  def is_accessible(self):
    return current_user.is_authenticated
    # set false to disable /admin/user view

  def inaccessible_callback(self, name, **kwargs):
    return '<h1>you are not loggedin</h1>'


class CommentView(ModelView):
  create_modal = True


admin.add_view(UserView(User, db.session))
admin.add_view(ModelView(Comment, db.session))

path = join(dirname(__file__), 'uploads')
admin.add_view(FileAdmin(path, '/uploads/', name='Uploads'))

admin.add_view(NotificationView(name='Notification', endpoint='notify'))


@app.route('/login')
def login():
  user = User.query.filter_by(id=1).first()
  # user = User.get(1)
  login_user(user)
  return redirect(url_for('admin.index'))


@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('admin.index'))


if __name__ == '__main__':
  app.run()
