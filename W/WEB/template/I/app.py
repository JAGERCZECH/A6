from flask import Flask, request, make_response
import random

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>MCMXCII</h1>'

@app.route('/user/<gamertag>')
def user(gamertag):
    return f'<h1>yo! {gamertag}</h1>'

@app.route('/useragent')
def testing():
    useragent = request.headers.get('User-Agent')
    return f'<p>Your browser is {useragent}</p>'

@app.route('/pastry')
def randnum():
    length = request.args.get('length', default=10, type=int)
    if length < 1:
        return "<p>Error: Length must be at least 1.</p>", 400
    lower = 10**(length - 1)
    upper = 10**length - 1
    number = random.randint(lower, upper)
    
    response = make_response(f'<h1>Random number: {number}</h1>')
    response.set_cookie('hexagonal', str(number))
    return response

if __name__ == '__main__':
    app.run(debug=True)
