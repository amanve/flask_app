from unittest import result
from flask import Flask, render_template, g, request
import sqlite3

app = Flask(__name__)
""" Database connection to 
sqlite3 """


def connect_db():
    sql = sqlite3.connect('food_log.db')
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
    return render_template('home.html')


@app.route('/view/<date>')  #date is 20170520
def view(date):
    db = get_db()

    cur = db.execute('select entry_date from log_date where entry_date= ?',
                     [date])
    result = cur.fetchone()
    return '<h1>The date is {}</h1>'.format(result)
    # return render_template('day.html')


@app.route('/add_food', methods=['GET', 'POST'])
def add_food():
    if request.method == 'POST':
        return '<h1>Name: {} Protein:{} Carbs: {} Fat:{}</h1>'.format(
            request.form['food-name'], request.form['protein'],
            request.form['carbohydrates'], request.form['fat'])
    return render_template('add_food.html')


if __name__ == '__main__':
    app.run()