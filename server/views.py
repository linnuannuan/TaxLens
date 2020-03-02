from server import app
from server.models import Model
from flask import request
import simplejson

# initialize the model
TPIIN = Model()
TPIIN.get_TPIIN()
TPIIN.get_affiliated_party_list()


@app.route('/ap_list')
def get_ap_list():
    return simplejson.dumps(TPIIN.get_affiliated_party_list(), ensure_ascii=False, ignore_nan=True)


@app.route('/ap_detail', methods=['POST'])
def get_ap_by_id():
    post_data = request.data.decode()
    if post_data != "":
        post_data = simplejson.loads(request.data.decode())
        ap_data = TPIIN.get_detail_by_ap_id(post_data['ap_id'])
    else:
        ap_data = TPIIN.get_detail_by_tp_id('610198671502546')  # default case
    return simplejson.dumps(ap_data, ensure_ascii=False, ignore_nan=True)


# legacy
@app.route('/APIRN_all')
def retrieve_all_networks():
    return simplejson.dumps(TPIIN.APIRN_all, ensure_ascii=False, ignore_nan=True)
