from flask import Flask, render_template, request, g, redirect, url_for, flash, session
import os
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename  # Correct import

# Create Flask app instance
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for flashing messages and sessions
DATABASE = 'users.db'  # Database for users

# Configuration for file uploads
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max size

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/display')
def display():
    users = query_db('SELECT userid, useremail, username, firstname, lastname, birthdate FROM users')
    return render_template('display.html', users=users)

@app.route('/update/<int:userid>', methods=['GET', 'POST'])
def update(userid):
    if request.method == 'POST':
        useremail = request.form.get('useremail')
        username = request.form.get('username')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        birthdate = request.form.get('birthdate')

        updates = []
        if useremail:
            updates.append(f"useremail = '{useremail}'")
        if username:
            updates.append(f"username = '{username}'")
        if firstname:
            updates.append(f"firstname = '{firstname}'")
        if lastname:
            updates.append(f"lastname = '{lastname}'")
        if birthdate:
            updates.append(f"birthdate = '{birthdate}'")

        if updates:
            update_query = f"UPDATE users SET {', '.join(updates)} WHERE userid = {userid}"
            db = get_db()
            db.execute(update_query)
            db.commit()

        return redirect(url_for('display'))

    user = query_db('SELECT * FROM users WHERE userid = ?', [userid], one=True)
    return render_template('update.html', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        useremail = request.form.get('useremail')
        username = request.form.get('username')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        birthdate = request.form.get('birthdate')
        password = request.form.get('password')

        # Check if email or username already exists
        email_exists = query_db('SELECT * FROM users WHERE useremail = ?', [useremail], one=True)
        username_exists = query_db('SELECT * FROM users WHERE username = ?', [username], one=True)

        if email_exists:
            flash('Email already registered. Please use a different email.')
            return redirect(url_for('register'))
        if username_exists:
            flash('Username already taken. Please choose a different username.')
            return redirect(url_for('register'))

        # Calculate age and check if user is at least 13 years old
        birthdate_dt = datetime.strptime(birthdate, '%Y-%m-%d')
        age = (datetime.now() - birthdate_dt).days // 365
        if age < 13:
            flash('You must be at least 13 years old to register.')
            return redirect(url_for('register'))

        # Hash the password for security
        hashed_password = generate_password_hash(password, method='sha256')

        # Insert new user if checks pass
        db = get_db()
        db.execute('''
            INSERT INTO users (useremail, username, firstname, lastname, birthdate, password)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', [useremail, username, firstname, lastname, birthdate, hashed_password])
        db.commit()

        flash('Registration successful!')
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        useremail = request.form.get('useremail')
        password = request.form.get('password')
        user = query_db('SELECT * FROM users WHERE useremail = ?', [useremail], one=True)

        if user and check_password_hash(user[6], password):
            session['userid'] = user[0]
            session['username'] = user[2]
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'userid' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))

    return render_template('dashboard.html', username=session.get('username'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.')
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'userid' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))

    userid = session['userid']

    if request.method == 'POST':
        username = request.form.get('username')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        birthdate = request.form.get('birthdate')

        db = get_db()
        db.execute('''
            UPDATE users SET username = ?, firstname = ?, lastname = ?, birthdate = ?
            WHERE userid = ?
        ''', (username, firstname, lastname, birthdate, userid))
        db.commit()
        flash('Profile updated successfully!')

    user = query_db('SELECT userid, useremail, username, firstname, lastname, birthdate FROM users WHERE userid = ?', [userid], one=True)
    return render_template('profile.html', user=user)

@app.route('/home')
def home():
    if 'userid' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))

    userid = session['userid']
    user = query_db('SELECT userid, useremail, username, profile_picture FROM users WHERE userid = ?', [userid], one=True)
    return render_template('home.html', user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'userid' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))

    userid = session['userid']

    if request.method == 'POST':
        username = request.form.get('username')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        birthdate = request.form.get('birthdate')
        bio = request.form.get('bio')
        twitter = request.form.get('twitter')
        linkedin = request.form.get('linkedin')

        # Handle file upload
        if 'profile_picture' in request.files:
            profile_picture = request.files['profile_picture']
            if profile_picture.filename != '':
                filename = secure_filename(profile_picture.filename)
                profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                profile_picture_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # Updated path
            else:
                profile_picture_url = None
        else:
            profile_picture_url = None

        db = get_db()
        if profile_picture_url:
            db.execute('''
                UPDATE users SET username = ?, firstname = ?, lastname = ?, birthdate = ?, profile_picture = ?, bio = ?, twitter = ?, linkedin = ?
                WHERE userid = ?
            ''', (username, firstname, lastname, birthdate, profile_picture_url, bio, twitter, linkedin, userid))
        else:
            db.execute('''
                UPDATE users SET username = ?, firstname = ?, lastname = ?, birthdate = ?, bio = ?, twitter = ?, linkedin = ?
                WHERE userid = ?
            ''', (username, firstname, lastname, birthdate, bio, twitter, linkedin, userid))
        db.commit()
        flash('Profile updated successfully!')

    user = query_db('SELECT userid, useremail, username, firstname, lastname, birthdate, profile_picture, bio, twitter, linkedin FROM users WHERE userid = ?', [userid], one=True)
    return render_template('edit_profile.html', user=user)

@app.route('/profile/<username>')
def public_profile(username):
    user = query_db('SELECT username, firstname, lastname, birthdate, profile_picture, bio, twitter, linkedin FROM users WHERE username = ?', [username], one=True)
    if user is None:
        flash('User not found.')
        return redirect(url_for('index'))
    return render_template('public_profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
