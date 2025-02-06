import os
import requests
from flask import Flask, request

app = Flask(__name__)

@app.post('/ocr')
def getOCR():
  allowed = checkOCRUsage()
  if allowed:
    return 'no OCR', 503
  imageData = request.data
  if imageData == '':
    return 'no image data', 400
  return getOCRResponse(imageData)


def checkOCRUsage():
  return True


def getOCRResponse(imageData):
  api_key = os.environ.get("GCP_API_KEY", False)
  res = requests.post(f"https://vision.googleapis.com/v1/images:annotate?key={api_key}", data=imageData)
  return res

app.run(host='0.0.0.0', debug=True)