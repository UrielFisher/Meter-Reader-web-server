import sqlite3
import json

def indivExists(attributes):
  with sqlite3.connect('./sqlite_db/db.db') as conn:
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


def transform(queryData):
  for record in queryData:
    del record['recordId']
    del record['indivId']

    record['readings'] = json.loads(record['readings'])
    record['rates'] = json.loads(record['rates'])

    for type in record['readings']:
      record[type + ' reading'] = record['readings'][type]
      record[type + ' rate'] = record['rates'][type]
    
    del record['readings']
    del record['rates']
  return