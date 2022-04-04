from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'aman'}
    posts = [{
        'author': {
            'username': 'Aman'
        },
        'body': 'Flask is simple to work with.'
    }, {
        'author': {
            'username': 'John'
        },
        'body': 'Flask is fun to do.'
    }]
    return render_template('index.html', title='Home', user=user, posts=posts)
