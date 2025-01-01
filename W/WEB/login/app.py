from flask import Flask, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a more secure secret key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    
    # Check if user already exists
    existing_user = session.query(User).filter_by(email=email).first()
    if existing_user:
        flash('Email already registered.')
        return redirect('/')
    
    # Hash the password before storing it using a valid method
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    
    # Create new user and add to the database
    new_user = User(email=email, username=username, password=hashed_password)
    session.add(new_user)
    session.commit()
    
    flash('Registration successful! Please log in.')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
