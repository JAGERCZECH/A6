import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('subscribers.db')
c = conn.cursor()

# Create a table to store subscriber information
c.execute('''
    CREATE TABLE IF NOT EXISTS subscribers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        plan TEXT NOT NULL,
        card_number TEXT NOT NULL,
        expiry_date TEXT NOT NULL,
        cvv TEXT NOT NULL
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
