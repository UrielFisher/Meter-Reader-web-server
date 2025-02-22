import os
import requests
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app, resources={'*': {'origins':"http://localhost:5173"}})

@app.post('/ocr')
def getOCR():
  if not ocrAllowed():
    return 'no OCR', 503
  imageData = request.data
  if imageData == '':
    return 'no image data', 400
  return getOCRResponse(imageData)


def ocrAllowed():
  return True


def getOCRResponse(imageData):
  api_key = os.environ.get("GCP_API_KEY", False)
  res = requests.post(
    url=f"https://vision.googleapis.com/v1/images:annotate?key={api_key}",
    data=imageData,
    headers={"Content-Type": "application/json"},
  )
  return res.text, res.status_code

app.run(host='0.0.0.0', debug=True)