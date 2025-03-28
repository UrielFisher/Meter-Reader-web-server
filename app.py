from flask import Flask, request
from flask_cors import CORS

from db_handling import initDB
from db_handling.individuals import app as individuals
from readingExtraction import app as extraction

app = Flask(__name__)

cors = CORS(app, resources={'*': {'origins':"http://localhost:5173"}})

app.register_blueprint(blueprint=individuals, url_prefix='/individuals')
app.register_blueprint(blueprint=extraction, url_prefix='/ocr')

app.run(host='0.0.0.0', debug=True)