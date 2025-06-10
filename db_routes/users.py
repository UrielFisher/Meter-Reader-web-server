from flask import Blueprint, request
import sqlite3

from db_utils import dict_factory

app = Blueprint('users', __name__)

fields = [
  'userId',
  'name',
  'settings'
]

@app.get('/settings')
def getUserSettings():
  userId = 1
  with sqlite3.connect('db.db') as conn:
    conn.row_factory = dict_factory
    cur = conn.cursor()
    res = cur.execute('SELECT settings FROM users WHERE userId = ?', (userId,)).fetchone()
    return res['settings']
  

@app.put('/settings')
def editUserSettings():
  userId = 1
  changes = request.data
  with sqlite3.connect('db.db') as conn:
    cur = conn.cursor()
    cur.execute(f'UPDATE users SET settings = ? WHERE userId = ?', (changes,userId))
    return '', 204