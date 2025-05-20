from flask import Blueprint, request, send_file
import sqlite3
# import pandas
# from io import BytesIO

from db_utils import transform, dict_factory

app = Blueprint('records', __name__)

fields = [
  'indivId',
  'date',
  'readings',
  'rates',
  'total'
]


@app.get('/<int:indivId>/')
def getRawRecords(indivId):
  with sqlite3.connect('db.db') as conn:
    cur = conn.cursor()
    res = cur.execute('SELECT * FROM records WHERE indivId = ?', (indivId,)).fetchall()
    return res
  

@app.get('/<int:indivId>/lastRecord')
def getLastRecord(indivId):
  with sqlite3.connect('db.db') as conn:
    conn.row_factory = dict_factory
    cur = conn.cursor()
    res = cur.execute('SELECT * FROM records WHERE indivId = ? ORDER BY date DESC LIMIT 1', (indivId,)).fetchone()
    if res:
      return res
    else:
      return 'No previous records found', 404
  

# @app.get('/<int:indivId>/transformed')
# def getTransformedRecords(indivId):
#   with sqlite3.connect('db.db') as conn:
#     conn.row_factory = dict_factory
#     cur = conn.cursor()
#     res = cur.execute('SELECT * FROM records WHERE indivId = ?', (indivId,)).fetchall()
#     transform(res)
#     return res
  

# @app.get('/<int:indivId>/xlsx')
# def getTransformedRecordsAsXlsx(indivId):
#   with sqlite3.connect('db.db') as conn:
#     conn.row_factory = dict_factory
#     cur = conn.cursor()
#     res = cur.execute('SELECT * FROM records WHERE indivId = ?', (indivId,)).fetchall()
#     transform(res)
#     df = pandas.DataFrame(res)
#     buffer = BytesIO()
#     df.to_excel(buffer, 'export.xlsx')
#     buffer.seek(0)
#     return send_file(buffer, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
  

# @app.get('/averageChanges/<int:indivId>')
# def getAverageChanges(indivId):
#   return
#   with sqlite3.connect('db.db') as conn:
#     cur = conn.cursor()
#     res = cur.execute('')


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