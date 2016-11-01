from flask import Flask, g, jsonify
import sqlite3
from flask import render_template, request, redirect, url_for, abort
from math import ceil

app = Flask(__name__)

#--------------------------------

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

# url generator
def url_for_pages(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_pages'] = url_for_pages

# ------------------------------


# def get_widgets():



# index router
@app.route('/')
def index():
    # create db connection
    conn = get_db()
    # create cursor object with squawk query
    cursor_object = conn.execute('SELECT ID, WIDGET_NAME FROM widgets ORDER BY id DESC')
    # iterate over all squawks and store
    widgets = cursor_object.fetchall()
    return render_template('index.html', widgets=widgets)


# add a widget to the database
@app.route('/add_widget', methods=['POST'])
def add_widget():
    # server side validation of squawk length
    if len(request.form['squawk_text']) > 140:
        abort(400)
    # create db connection and store the squawk
    conn = get_db()
    conn.execute('INSERT INTO squawks (squawk_text) VALUES (?)', [request.form['squawk_text']])
    conn.commit()
    return redirect(url_for('index'))


# Basic API
@app.route('/api/widget', methods=['GET'])
def list_widgets():
    # create db connection
    conn = get_db()
    # create cursor object with squawk query
    cursor_object = conn.execute('SELECT * from widget order by id desc')
    # iterate over all widgets and store
    widgets = cursor_object.fetchall()
    return jsonify(widgets)


if __name__ == '__main__':
    app.run()
