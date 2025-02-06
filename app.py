import os
from flask import Flask

app = Flask(__name__)

@app.route('/ocr')
def getOCR():
  allowed = checkOCRUsage()
  if(allowed):
    return '<h1>no OCR</h1>'
  return getOCRResponse()


def checkOCRUsage():
  return True


def getOCRResponse():
  api_key = os.environ.get("GCP_API_KEY", False)
  return 'pass'

app.run(host='0.0.0.0', debug=True)