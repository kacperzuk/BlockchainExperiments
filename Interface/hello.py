import os
import sqlite3
from flask import Flask, render_template, request, url_for, session, g, redirect, abort, flash


app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
def hello(name=None):
    return render_template('main.html', name=name)

@app.route("/main.html")
def main():
    return render_template('main.html', method=['POST'])

@app.route('/contact_form.html')
def client():
	return render_template('contact_form.html')

@app.route('/rcv_form.html')
def recive():
	return render_template('rcv_form.html')

@app.route('/snd_form.html')
def send():
	return render_template('snd_form.html')



		#DATABASE
app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'contacts.db'),
	SECRET_KEY='development key',
	USERNAME='admin',
	PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
#	Connects to the specific database.
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

#initialize database from hello.py   #nie dziala
#def init_db():
#	db = get_db()
#	with app.open_resource('contacts', mode='r') as f:
#		db.cursor().executescript(f.read())
#	db.commit()

#@app.cli.command('initdb')
#def initdb_command():
#Initializes the database.
#	init_db()
#	print 'Initialized the database.'

def get_db():
#Opens a new database connection if there is none yet for the current application context.
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
#	Closes the database again at the end of the request.
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

@app.route('/')
def show_names():
	db = get_db()
	cur = db.execute('select names')
	names = cur.fetchall()
	return render_template('snd_form.html', names=names)

@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	db = get_db()
	db.execute('insert into entries (title, text) values (?, ?)',
				[request.form['title'], request.form['text']])
	db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))

if __name__ == "__main__":
    app.run()