from flask import Blueprint, request
import sqlite3

from db_utils import dict_factory, indivExists

app = Blueprint('individuals', __name__)

fields = [
  'userId',
  'name',
  'pstn',
  'paysForSewer'
]


@app.get('/')
def getIndividual():
  with sqlite3.connect('db.db') as conn:
    conn.row_factory = dict_factory
    cur = conn.cursor()
    res = cur.execute('''
                SELECT * FROM individuals
                WHERE userId = 1
                ''').fetchall()
    return res

  return 'None'


@app.post('/')
def addIndividual():
  with sqlite3.connect('db.db') as conn:
    cur = conn.cursor()
    dct = {'name': '', 'pstn': None, 'paysForSewer': False}
    dct = {**dct, **request.json}
    dct.update({'userId': '1'})

    if not dct['name']:
      return 'Insufficient individual details', 400

    if indivExists({
      'userId': dct['userId'],
      'name': dct['name']
      }):
      return 'Individual already exists', 400
    
    cur.execute('INSERT INTO individuals (userId, name, pstn, paysForSewer) VALUES (:userId, :name, :pstn, :paysForSewer)',
      dct)
    
    res = cur.execute('SELECT * FROM individuals WHERE userId = ? AND name = ?',
                      (dct['userId'], dct['name'])).fetchone()
    return str(res[0])
  

@app.patch('/<string:name>')
def updateIndividual(name):
  userId = 1
  changes = request.json
  if not changes:
    return 'No changes supplied', 400
  if not all(field in fields for field in changes):
    return 'Inappropriate field names supplied for change', 400

  with sqlite3.connect('db.db') as conn:
    cur = conn.cursor()

    if not indivExists({
      'userId': '1',
      'name': name
      }):
      return 'Individual to change not found', 400
    
    identifiers = [userId, name]
    flds = []
    values = []
    for key, value in changes.items():
      flds.append(f'{key} = ?')
      values.append(value)
    
    cur.execute(f'UPDATE individuals SET {", ".join(flds)} WHERE userId = ? AND name = ?',
                values + identifiers)
    return 'ok', 204


@app.delete('/<string:name>')
def deleteIndividual(name):
  if not name:
    return 'No individual name supplied', 400
  with sqlite3.connect('db.db') as conn:
    if not indivExists({
      'userId': '1',
      'name': name
      }):
      return 'Individual to delete not found', 404
    cur = conn.cursor()
    cur.execute('DELETE FROM individuals WHERE userId = ? AND name = ?',
                (1, name))
    return 'ok', 204