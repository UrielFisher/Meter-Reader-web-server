from flask import Blueprint, request
import sqlite3

app = Blueprint('individual', __name__)

# user

@app.get('/')
def ind():
  with sqlite3.connect('db.db') as conn:
    cur = conn.cursor()
    res = cur.execute('''
                SELECT * FROM individuals
                WHERE owner = 1
                ''').fetchall()
    return res

  return 'None'


@app.post('/')
def addIndividual():
  with sqlite3.connect('db.db') as conn:
    cur = conn.cursor()
    dct = {'name': '', 'pstn': None}
    dct = {**dct, **request.json}
    dct.update({'owner': '1'})

    if indivExists({
      'owner': dct['owner'],
      'name': dct['name']
      }):
      return 'Individual already exists', 400
    
    cur.execute('INSERT INTO individuals (owner, name) VALUES (:owner, :name)',
      dct)
    return 'ok'
  

@app.patch('/')
def updateIndividual():
  if(len(request.args) == 0):
    return 'No changes supplied', 400
  with sqlite3.connect('db.db') as conn:
    cur = conn.cursor()

    if not indivExists({
      'owner': '1',
      'name': request.args.get('name', '')
      }):
      return 'Individual to change not found', 400
    
    cur.execute('UPDATE individuals SET name = ? WHERE owner = ?',
                (request.args.get('name', ''), 1))
    return 'ok'


@app.delete('/')
def deleteIndividual():
  if(not request.args.get('name', None)):
    return 'No individual name supplied', 400
  with sqlite3.connect('db.db') as conn:
    cur = conn.cursor()
    cur.execute('DELETE FROM individuals WHERE owner = ? AND name = ?',
                (1, request.args['name']))
    return 'ok'
  

def indivExists(attributes):
  with sqlite3.connect('db.db') as conn:
    cur = conn.cursor()
    query = 'SELECT * FROM individuals WHERE'
    for att, value in attributes:
      query += f' {att} = {value}'
    if(len(cur.execute(query).fetchone()) == 0):
      return False
    return True
    