from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Create a string
    def __repr__(self):
        return '<Test %r>' % self.name


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    email = db.Column(db.String(30))
    join_date = db.Column(db.DateTime)

    # Create a string
    """ Returns representation of the object in Database """

    def __repr__(self):
        return '<Member %r>' % self.name


if __name__ == '__main__':
    app.run()