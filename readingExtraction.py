import os
import requests
import json
from flask import Blueprint, request

app = Blueprint('readingExtraction', __name__)

@app.get('/')
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
    data=ocrRequest(imageData),
    headers={"Content-Type": "application/json"},
  )
  return res.text, res.status_code


def ocrRequest(imageData):
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