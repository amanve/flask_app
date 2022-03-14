from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_restless

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restless_api.db'
db = SQLAlchemy(app)
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(20), unique=True)
  items = db.relationship('Item', backref='user', lazy='dynamic')


class Item(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(20), unique=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


manager.create_api(User, methods=['GET'])
manager.create_api(Item)

if __name__ == '__main__':
  app.run()
