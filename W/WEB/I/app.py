from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    # Here, you can add logic to store the user information securely
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
