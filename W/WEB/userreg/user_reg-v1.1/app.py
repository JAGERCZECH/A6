from flask import Flask, render_template, request, redirect, url_for, g, session as flask_session
import sqlite3
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

# Database configuration
DATABASE_USERS = 'users.db'
DATABASE_SESSIONS = 'sessions.db'
DATABASE_PRODUCTS = 'products.db'

# Functions to connect to the databases
def get_db(db_name):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_name)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Function to update the session counter
def update_session_counter():
    db = get_db(DATABASE_SESSIONS)
    cursor = db.execute('SELECT value FROM session_counter WHERE id = 1')
    current_value = cursor.fetchone()[0]
    new_value = current_value + 1
    db.execute('UPDATE session_counter SET value = ? WHERE id = 1', (new_value,))
    db.commit()
    return new_value

# Routes
@app.route('/')
def index():
    if 'unique_id' not in flask_session:
        flask_session['unique_id'] = random.randint(100000, 999999)  # Assign a unique random number
    flask_session['last_visit'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session_id = update_session_counter()
    store_session_data(flask_session['unique_id'], flask_session['last_visit'])
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        session_value = request.form['session_value']
        flask_session['username'] = username  # Store the username in session
        db = get_db(DATABASE_USERS)
        db.execute('INSERT INTO users (username, email, session_value) VALUES (?, ?, ?)', (username, email, session_value))
        db.commit()
        return redirect(url_for('index'))  # Redirect to index page after registration
    return render_template('register.html')

@app.route('/users')
def users():
    db = get_db(DATABASE_USERS)
    cursor = db.execute('SELECT * FROM users')
    users_data = cursor.fetchall()
    return render_template('user.html', users=users_data)

@app.route('/sessions')
def sessions():
    db = get_db(DATABASE_SESSIONS)
    cursor = db.execute('SELECT * FROM sessions')
    sessions_data = cursor.fetchall()
    return render_template('session.html', sessions=sessions_data)

@app.route('/products')
def products():
    db = get_db(DATABASE_PRODUCTS)
    cursor = db.execute('SELECT * FROM products')
    products_data = cursor.fetchall()
    return render_template('product.html', products=products_data)

def store_session_data(session_value, last_visit):
    db = get_db(DATABASE_SESSIONS)
    db.execute('INSERT INTO sessions (sessions, datetime) VALUES (?, ?)', (session_value, last_visit))
    db.commit()

if __name__ == '__main__':
    app.run(debug=True)
