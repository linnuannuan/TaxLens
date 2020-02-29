from flask import Flask
from flask_cors import CORS

STATIC_FOLDER = '../client/dist'
TEMPLATE_FOLDER = '../client/dist'

app = Flask(__name__, static_url_path='', static_folder=STATIC_FOLDER, template_folder=TEMPLATE_FOLDER)
CORS(app)

from server import views
