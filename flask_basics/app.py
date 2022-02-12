from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def index():
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
    return '<h1>{} is on Home Page</h1>'.format(name)


@app.route('/json')
def json():
    return jsonify({'key': 'value', 'key2': [1, 2, 3]})


@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return '<h1>Hi {}. u r from {}. You are on the query page</h1>'.format(
        name, location)


@app.route('/form')
def form():
    return '''<form method="POST" action="/process">
    <input type="text" name="name">
    <input type="text" name="location">
    <input type="submit" value="Submit">
    </form>'''


@app.route('/process', methods=['POST'])
def process():
    name = request.form['name']
    location = request.form['location']

    return 'Hello {}, you are from {}. Form submitted successfully.'.format(
        name, location)


if __name__ == '__main__':
    app.run()