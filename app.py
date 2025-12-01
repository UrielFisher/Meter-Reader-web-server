from flask import Flask, request
from flask_cors import CORS

from db_routes import initDB
from db_routes.users import app as users
from db_routes.individuals import app as individuals
from db_routes.records import app as records
from readingExtraction import app as extraction

app = Flask(__name__)

cors = CORS(app, resources={'*': {'origins':"http://localhost:5173"}})

app.register_blueprint(blueprint=users, url_prefix='/users')
app.register_blueprint(blueprint=individuals, url_prefix='/individuals')
app.register_blueprint(blueprint=records, url_prefix='/records')
app.register_blueprint(blueprint=extraction, url_prefix='/ocr')