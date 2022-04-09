from flask import Flask, request, make_response, redirect

app = Flask(__name__)


@app.route('/')
def index():
    """
    user_agent = request.headers.get('User-Agent')
    return f'<h1>Hello World! Your browser is {user_agent}</h1>'
    """
    """
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('aman', '42')
    return response
    """
    return redirect('www.google.com')


@app.route('/user/<name>')
def user(name):
    return f'Hello {name}'
