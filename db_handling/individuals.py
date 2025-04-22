from flask import Blueprint, request
import sqlite3

app = Blueprint('individual', __name__)

# user

fields = [
  'ownerId',
  'name',
  'pstn',
  'paysForSewer'
]

@app.get('/')
def ind():
  with sqlite3.connect('db.db') as conn:
    conn.row_factory = dict_factory
    cur = conn.cursor()
    res = cur.execute('''
                SELECT * FROM individuals
                WHERE ownerId = 1
                ''').fetchall()
    return res

  return 'None'


@app.post('/')
def addIndividual():
  with sqlite3.connect('db.db') as conn:
    cur = conn.cursor()
    dct = {'name': '', 'pstn': None, 'paysForSewer': False}
    dct = {**dct, **request.json}
    dct.update({'ownerId': '1'})

    if not dct['name']:
      return 'Insufficient individual details', 400

    if indivExists({
      'ownerId': dct['ownerId'],
      'name': dct['name']
      }):
      return 'Individual already exists', 400
    
    cur.execute('INSERT INTO individuals (ownerId, name, pstn, paysForSewer) VALUES (:ownerId, :name, :pstn, :paysForSewer)',
      dct)
    return 'ok'
  

@app.patch('/<string:name>')
def updateIndividual(name):
  ownerId = 1
  changes = request.json
  if not changes:
    return 'No changes supplied', 400
  if not all(field in fields for field in changes):
    return 'Inappropriate field names supplied for change', 400

  with sqlite3.connect('db.db') as conn:
    cur = conn.cursor()

    if not indivExists({
      'ownerId': '1',
      'name': name
      }):
      return 'Individual to change not found', 400
    
    identifiers = [ownerId, name]
    flds = []
    values = []
    for key, value in changes.items():
      flds.append(f'{key} = ?')
      values.append(value)
    
    cur.execute(f'UPDATE individuals SET {", ".join(flds)} WHERE ownerId = ? AND name = ?',
                values + identifiers)
    return 'ok', 204


@app.delete('/<string:name>')
def deleteIndividual(name):
  if not name:
    return 'No individual name supplied', 400
  with sqlite3.connect('db.db') as conn:
    if not indivExists({
      'ownerId': '1',
      'name': name
      }):
      return 'Individual to delete not found', 404
    cur = conn.cursor()
    cur.execute('DELETE FROM individuals WHERE ownerId = ? AND name = ?',
                (1, name))
    return 'ok', 204
  

def indivExists(attributes):
  with sqlite3.connect('db.db') as conn:
    cur = conn.cursor()
    query = 'SELECT * FROM individuals WHERE'
    flds = []
    for att, value in attributes.items():
      flds.append(f' {att} = "{value}"')
    print(query+' AND'.join(flds))
    if(len(cur.execute(query+' AND'.join(flds)).fetchall()) == 0):
      return False
    return True
    

def dict_factory(cursor, row):
  fields = [column[0] for column in cursor.description]
  return {key: value for key, value in zip(fields, row)}