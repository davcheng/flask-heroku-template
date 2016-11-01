from flask import Flask, g, render_template, request, url_for, jsonify
import sqlite3


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
    # create db connection and store the widget
    conn = get_db()
    # execute query to store widget data from the request form from index.html
    conn.execute('INSERT INTO widgets (WIDGET_NAME) VALUES (?)', [request.form['widget_name']])
    # save changes
    conn.commit()
    return redirect(url_for('index'))


# basic API
@app.route('/api/widget', methods=['GET'])
def list_widgets():
    # create db connection
    conn = get_db()
    # create cursor object with squawk query
    cursor_object = conn.execute('SELECT * FROM widgets ORDER BY id DESC')
    # iterate over all widgets and store
    widgets = cursor_object.fetchall()
    return jsonify(widgets)


if __name__ == '__main__':
    app.run()
