from flask import Flask, render_template, request, g, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'users.db'  # New database for users

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
    users = query_db('SELECT userid, useremail, username, firstname, lastname, birthdate FROM users')
    return render_template('index.html', users=users)

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

        return redirect(url_for('index'))

    user = query_db('SELECT * FROM users WHERE userid = ?', [userid], one=True)
    return render_template('update.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
