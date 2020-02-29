from server import app
from server.models import Model
import json


APIRN = Model()


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/APIRN')
def retrieve_networks():
    return json.dumps(APIRN.APIRN, ensure_ascii=False)


@app.route('/APIRN_all')
def retrieve_all_networks():
    return json.dumps(APIRN.APIRN_all, ensure_ascii=False)
