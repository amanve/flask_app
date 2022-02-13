from flask import Flask, jsonify, request, url_for, redirect, session, render_template

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'thisisasecretkey!'


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


@app.route('/home', methods=['POST', 'GET'], defaults={'name': 'John'})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
    session['name'] = name
    return render_template('home.html', name=name)


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
        return render_template('form.html')
    else:
        name = request.form['name']
        # location = request.form['location']

        # return f'Hello {name}, you are from {location}. Form submitted successfully.'
        return redirect(url_for('home', name=name))


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


if __name__ == '__main__':
    app.run()