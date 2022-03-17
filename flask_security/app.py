from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore,\
  UserMixin, RoleMixin, login_required, current_user, \
  roles_accepted

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///security.db'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_SALT'] = 'salty'
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_RECOVERABLE'] = True
app.config['SECURITY_CHANGEABLE'] = True

db = SQLAlchemy(app)

roles_users = db.Table(
    'roles_users', \
  db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),\
  db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(80), unique=True)
  description = db.Column(db.String(255))


class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(255), unique=True)
  password = db.Column(db.String(255))
  active = db.Column(db.Boolean())
  confirmed_at = db.Column(db.DateTime())
  roles = db.relationship('Role',
                          secondary=roles_users,
                          backref=db.backref('users', lazy='dynamic'))


@app.route('/')
def index():
  admin_role = user_datastore.find_or_create_role('admin')
  user_datastore.add_role_to_user(current_user, admin_role)
  db.session.commit()
  return '<h1>Home page</h1>'


@app.route('/protected')
@login_required
def protected():
  email = current_user.email
  return f'<h1>This is a protected page. Your email is {current_user.email}</h1>'


@app.route('/roleprotected')
@roles_accepted('admin')
def roleprotected():
  return '<h1>this is for admin only.</h1>'


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

if __name__ == '__main__':
  app.run()
