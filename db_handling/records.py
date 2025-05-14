from flask import Blueprint, request
import sqlite3

app = Blueprint('records', __name__)

fields = [
  'indivId',
  'date',
  'readings',
  'rates',
  'total'
]


@app.get('/<int:indivId>')
def getRecords(indivId):
  with sqlite3.connect('db.db') as conn:
    cur = conn.cursor()
    res = cur.execute('SELECT * FROM records WHERE indivId = ?', (indivId,)).fetchall()
    return res
  

@app.get('/averageChanges/<int:indivId>')
def getAverageChanges(indivId):
  return
  with sqlite3.connect('db.db') as conn:
    cur = conn.cursor()
    res = cur.execute('')


@app.post('/')
def addRecord():
  with sqlite3.connect('db.db') as conn:
    cur = conn.cursor()
    dct = request.json
    fldsInDct = [field for field in dct.keys() if field in fields]
    if not dct.get('indivId', ''):
      return 'No individual specified', 400
    cur.execute(f'INSERT INTO records ({', '.join(fldsInDct)}) VALUES ({':' + ', :'.join(fldsInDct)})',
                dct)
    return 'ok'