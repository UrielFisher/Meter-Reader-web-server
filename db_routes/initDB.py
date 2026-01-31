import sqlite3

conn = sqlite3.connect('./sqlite_db/db.db')

cur = conn.cursor()

# def attemptDropAllTables():
#   cur.execute('DROP TABLE IF EXISTS users')
#   cur.execute('DROP TABLE IF EXISTS individuals')
#   cur.execute('DROP TABLE IF EXISTS records')

def attemptInitAllTables():
  cur.execute('''
              CREATE TABLE IF NOT EXISTS users (
              userId INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              settings TEXT CHECK(json_valid(settings)) NOT NULL
  )''')

  cur.execute('''
              CREATE TABLE IF NOT EXISTS individuals (
              indivId INTEGER PRIMARY KEY AUTOINCREMENT,
              userId INTEGER NOT NULL,
              name TEXT,
              pstn TEXT,
              paysForSewer BOOLEAN DEFAULT FALSE
  )''')

  cur.execute('''
              CREATE TABLE IF NOT EXISTS records (
              recordId INTEGER PRIMARY KEY AUTOINCREMENT,
              indivId INTEGER NOT NULL,
              date INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
              readings TEXT CHECK(json_valid(readings)),
              rates TEXT CHECK(json_valid(rates)),
              total NUMBER
  )''')