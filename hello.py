from flask import Flask, g, jsonify
import sqlite3
from flask import render_template, request, redirect, url_for, abort
from math import ceil

app = Flask(__name__)

# set number of squawks per page
PER_PAGE = 20


# Set up and initialize db
def get_db():
    if not hasattr(g, 'sqlite_db'):
        db_name = app.config.get('DATABASE', 'squawker.db')
        g.sqlite_db = sqlite3.connect(db_name)

    return g.sqlite_db


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'sqlite_db', None)
    if db is not None:
        db.close()
# ------------------------------

@app.route('/')
def index():
    data = get_data()
    return render_template('index.html', data=data)

def get_time():
    milli = time.time() * 1000
    # format to un-scientific notation it
    unsci_milli = '{:.0f}'.format(milli)
    return unsci_milli


# add to database
@app.route('/add_data', methods=['POST'])
def add_data():
    # server side validation of squawk length
    if len(request.form['squawk_text']) > 140:
        abort(400)
    # create db connection and store the squawk
    conn = get_db()
    conn.execute('INSERT INTO squawks (squawk_text) VALUES (?)', [request.form['squawk_text']])
    conn.commit()
    return redirect(url_for('root'))


# TODO create a JSON API that lists all possible squawks
@app.route('/api/squawks', methods=['GET'])
def list_squawks():
    # create db connection
    conn = get_db()
    # create cursor object with squawk query
    cursor_object = conn.execute('SELECT * from squawks order by id desc')
    # iterate over all squawks and store
    squawks = cursor_object.fetchall()
    return jsonify(squawks)


if __name__ == '__main__':
    app.run()
