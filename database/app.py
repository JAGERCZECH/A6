from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)

# Database configuration
DATABASE_USERS = 'maindatabase/users.db'
DATABASE_PRODUCTS = 'maindatabase/products.db'

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
    return render_template('index.html')

@app.route('/users')
def users():
    db = get_db(DATABASE_USERS)
    cursor = db.execute('SELECT * FROM users')
    users_data = cursor.fetchall()
    return render_template('user.html', users=users_data)

@app.route('/sessions')
def sessions():
    return render_template('session.html')

@app.route('/products')
def products():
    db = get_db(DATABASE_PRODUCTS)
    cursor = db.execute('SELECT * FROM products')
    products_data = cursor.fetchall()
    return render_template('product.html', products=products_data)

if __name__ == '__main__':
    app.run(debug=True)
