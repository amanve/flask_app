from flask import Flask, jsonify, request, url_for, redirect, session, g, render_template
import sqlite3

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'thisisasecretkey!'


def connect_db():
    sql = sqlite3.connect('data.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    session.pop('name', None)
    return '<h1>Hello, World!</h1>'


# @app.route('/home')
# def home():
#     return '<h1>Home Page</h1>'
""" 
string
(default) accepts any text without a slash

int
accepts positive integers

float
accepts positive floating point values

path
like string but also accepts slashes

uuid
accepts UUID strings """
""" @app.route('/home', methods=['POST', 'GET'], defaults={'name': 'John'})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
    session['name'] = name
    return f'<h1>{name} is on Home Page</h1>' """


@app.route('/home', methods=['POST', 'GET'], defaults={'name': 'John'})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
    session['name'] = name
    db = get_db()
    cur = db.execute('select id,name, location from users')
    results = cur.fetchall()

    return render_template('home.html',
                           name=name,
                           display=False,
                           myList=['one', 'two', 'three', 'four'],
                           Listofdict=[{
                               'name': 'Aman'
                           }, {
                               'name': 'John'
                           }],
                           results=results)


@app.route('/json')
def json():
    if 'name' in session:
        name = session['name']
    else:
        name = 'NotinSession!'
    return jsonify({'key': 'value', 'key2': [1, 2, 3], 'name': name})


@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return f'<h1>Hi {name}. u r from {location}. You are on the query page</h1>'


# @app.route('/form')
# def form():
#     return '''<form method="POST" action="/process">
#     <input type="text" name="name">
#     <input type="text" name="location">
#     <input type="submit" value="Submit">
#     </form>'''
""" @app.route('/form', methods=['GET', 'POST'])
def form():

    if request.method == 'GET':
        return '''<form method="POST" action="/form">
    <input type="text" name="name">
    <input type="text" name="location">
    <input type="submit" value="Submit">
    </form>'''
    else:
        name = request.form['name']
        location = request.form['location']

        return f'Hello {name}, you are from {location}. Form submitted successfully.' """
""" Either of the methods to handle form requests """
""" @app.route('/form')
def form():
    return '''<form method="POST" action="/form">
    <input type="text" name="name">
    <input type="text" name="location">
    <input type="submit" value="Submit">
    </form>'''


@app.route('/form', methods=['POST'])
def process():
    name = request.form['name']
    location = request.form['location']

    return f'Hello {name}, you are from {location}. Form submitted successfully.' """


# URL redirect and form
@app.route('/form', methods=['GET', 'POST'])
def form():

    if request.method == 'GET':
        return '''<form method="POST" action="/form">
    <input type="text" name="name">
    <input type="text" name="location">
    <input type="submit" value="Submit">
    </form>'''
    else:
        name = request.form['name']
        location = request.form['location']

        db = get_db()
        db.execute('insert into users (name, location) values(?,?)',
                   [name, location])
        db.commit()

        # return f'Hello {name}, you are from {location}. Form submitted successfully.'
        return redirect(url_for('home', name=name, location=location))


@app.route('/processjson', methods=['POST'])
def processjson():
    data = request.get_json()
    name = data['name']
    location = data['location']
    randomList = data['randomList']
    return jsonify({
        'result': 'Success',
        'name': name,
        'location': location,
        'randomKeyList': randomList[0]
    })


@app.route('/viewresults')
def viewresults():
    db = get_db()
    cur = db.execute('select id,name,location from users')
    results = cur.fetchall()
    return f'<h2>The ID is {results[0]["id"]}. The name is {results[0]["name"]}. The location is {results[0]["location"]}.</h2>'


if __name__ == '__main__':
    app.run()