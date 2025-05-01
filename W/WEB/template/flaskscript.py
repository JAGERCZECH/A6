from flask import Flask
from flask_script import Manager

# Create the Flask app instance
app = Flask(__name__)

# Initialize the Manager with the app
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
