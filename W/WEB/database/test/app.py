from flask import Flask, render_template, request, redirect, url_for, g, session
import sqlite3
from datetime import datetime

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

# Routes
@app.route('/')
def index():
    session['last_visit'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    store_session_data(session['last_visit'])
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        db = get_db(DATABASE_USERS)
        db.execute('INSERT INTO users (username, email) VALUES (?, ?)', (username, email))
        db.commit()
        return redirect(url_for('users'))
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

def store_session_data(timestamp):
    db = get_db(DATABASE_SESSIONS)
    db.execute('INSERT INTO sessions (timestamp) VALUES (?)', (timestamp,))
    db.commit()

if __name__ == '__main__':
    app.run(debug=True)
