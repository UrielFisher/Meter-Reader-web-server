import sqlite3

conn = sqlite3.connect('db.db')

cur = conn.cursor()

# cur.execute('DROP TABLE IF EXISTS individuals')

cur.execute('''
            CREATE TABLE IF NOT EXISTS individuals (
            owner INTEGER NOT NULL,
            name TEXT NOT NULL,
            pstn INTEGER
)''')