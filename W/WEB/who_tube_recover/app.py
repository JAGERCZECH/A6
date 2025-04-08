from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from routes.auth import auth_bp
from routes.content import content_bp
from routes.subscription import subscription_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use PostgreSQL in production

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(content_bp, url_prefix='/content')
app.register_blueprint(subscription_bp, url_prefix='/subscribe')

# Load User Model
from models.user import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Homepage Route
@app.route('/')
def home():
    return "Welcome to the Streaming & Photography Platform!"

if __name__ == '__main__':
    app.run(debug=True)
