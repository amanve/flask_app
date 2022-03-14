from enum import unique
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from flask_admin.contrib.fileadmin import FileAdmin

from os.path import dirname, join

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admin_app.db'
app.config['SECRET_KEY'] = 'mysecret!'

db = SQLAlchemy(app)
admin = Admin(app, template_mode='bootstrap4')


class User(db.Model):
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


class UserView(ModelView):
  column_exclude_list = []
  column_display_pk = True
  can_create = True
  can_edit = True
  can_delete = True
  can_export = True

  def on_model_change(self, form, model, is_current):
    model.password = generate_password_hash(model.password, method='sha256')


class CommentView(ModelView):
  create_modal = True


admin.add_view(UserView(User, db.session))
admin.add_view(ModelView(Comment, db.session))

path = join(dirname(__file__), 'uploads')
admin.add_view(FileAdmin(path, '/uploads/', name='Uploads'))

if __name__ == '__main__':
  app.run()
