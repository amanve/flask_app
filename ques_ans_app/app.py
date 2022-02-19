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
    user_result = None

    if 'user' in session:
        user = session['user']

        db = get_db()
        user_cur = db.execute(
            'select id, name, password, expert, admin from users where name = ?',
            [user])
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

        session['user'] = request.form['name']
        return redirect(url_for('index'))
        # return f'<h1>Name: {request.form["name"]}, Password: {request.form["password"]}</h1>'
        """ return '<h1>Name: {}, Password: {}</h1>'.format(
            request.form["name"], request.form["password"]) """

    return render_template('register.html', user=user)


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
            return redirect(url_for('index'))
        else:
            return '<h1>The password is incorrect</h1>'

    return render_template('login.html', user=user)


@app.route('/question')
def question():
    user = get_current_user()
    return render_template('question.html', user=user)


@app.route('/answer')
def answer():
    user = get_current_user()
    return render_template('answer.html', user=user)


@app.route('/ask')
def ask():
    user = get_current_user()
    return render_template('ask.html', user=user)


@app.route('/unanswered')
def unanswered():
    user = get_current_user()
    return render_template('unanswered.html', user=user)


@app.route('/users')
def users():
    user = get_current_user()
    return render_template('users.html', user=user)


@app.route('/logout')
def logout():
    # return render_template('home.html')
    session.pop('user', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()