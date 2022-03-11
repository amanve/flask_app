from enum import unique
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

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
  column_exclude_list = ['password']
  column_display_pk = True
  can_create = False
  can_edit = True
  can_delete = False


admin.add_view(UserView(User, db.session))
admin.add_view(ModelView(Comment, db.session))

if __name__ == '__main__':
  app.run()
