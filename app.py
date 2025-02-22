import os
import requests
import json
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
  api_key = os.environ.get("GCP_API_KEY", '')
  res = requests.post(
    url=f"https://vision.googleapis.com/v1/images:annotate?key={api_key}",
    data=ocrBaseRequest(imageData),
    headers={"Content-Type": "application/json"},
  )
  return res.text, res.status_code


def ocrBaseRequest(imageData):
  return json.dumps({
    "requests": [
      {
        "image": {
          "content": imageData.decode('utf-8')
        },
        "features": [
          {
            "type": "TEXT_DETECTION"
          }
        ]
      }
    ]
  })

app.run(host='0.0.0.0', debug=True)