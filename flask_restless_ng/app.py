from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restless_api.db'
db = SQLAlchemy(app)


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(20), unique=True)
  items = db.relationship('Item', backref='user')


class Item(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(20), unique=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


manager = APIManager(app, session=db.session)

manager.create_api(User, methods=['GET', 'POST'])
manager.create_api(Item, methods=['GET'])

if __name__ == '__main__':
  app.run()
