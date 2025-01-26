import sqlite3

conn = sqlite3.connect('users.db')  # New database for users
c = conn.cursor()

# Create table
c.execute('''
CREATE TABLE users (
    userid INTEGER PRIMARY KEY,
    useremail TEXT NOT NULL,
    username TEXT NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    birthdate TEXT NOT NULL
)
''')

# Insert sample data
sample_users = [
    ('user1@example.com', 'user1', 'First1', 'Last1', '2000-01-01'),
    ('user2@example.com', 'user2', 'First2', 'Last2', '1999-02-02'),
    # Add more users as needed
]

c.executemany('''
INSERT INTO users (useremail, username, firstname, lastname, birthdate)
VALUES (?, ?, ?, ?, ?)
''', sample_users)

conn.commit()
conn.close()
