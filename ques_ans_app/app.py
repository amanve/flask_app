from flask import Flask, redirect, render_template, g, request, session, url_for
from db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def get_current_user():
    # user = None
    user_result = None
    if 'user' in session:
        user = session['user']

        db = get_db()
        user_cur = db.execute(
            'select id,name,password from users where name= ?', [user])
        user_result = user_cur.fetchone()

    return user_result


@app.route('/')
def index():
    """ user = None
    if 'user' in session:
        user = session['user'] """

    user = get_current_user()

    return render_template('home.html', user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    user = get_current_user()
    if request.method == 'POST':
        db = get_db()
        hashed_password = generate_password_hash(request.form['password'],
                                                 method='sha256')
        db.execute(
            'insert into users ( name, password,expert,admin) values(?,?,?,?)',
            [request.form['name'], hashed_password, '0', '0'])
        db.commit()
        return '<h1>User created!</h1>'
        # return f'<h1>Name: {request.form["name"]}, Password: {request.form["password"]}</h1>'
        """ return '<h1>Name: {}, Password: {}</h1>'.format(
            request.form["name"], request.form["password"]) """

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    user = get_current_user()
    if request.method == 'POST':
        # return f'<h1>Username: {request.form["name"]} Password: {request.form["password"]}'
        db = get_db()

        name = request.form["name"]
        password = request.form["password"]

        user_cur = db.execute(
            'select id,name,password from users where name= ?', [name])
        user_result = user_cur.fetchone()

        # return f'<h1>{user_result["password"]}</h1>'
        if check_password_hash(user_result['password'], password):
            session['user'] = user_result['name']
            return '<h1>The password is correct</h1>'
        else:
            return '<h1>The password is incorrect</h1>'
    return render_template('login.html')


@app.route('/question')
def question():
    user = get_current_user()
    return render_template('question.html')


@app.route('/answer')
def answer():
    user = get_current_user()
    return render_template('answer.html')


@app.route('/ask')
def ask():
    user = get_current_user()
    return render_template('ask.html')


@app.route('/unanswered')
def unanswered():
    user = get_current_user()
    return render_template('unanswered.html')


@app.route('/users')
def users():
    user = get_current_user()
    return render_template('users.html')


@app.route('/logout')
def logout():
    user = get_current_user()
    # return render_template('home.html')
    session.pop('user', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()