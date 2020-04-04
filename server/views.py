from server import app
from server.models import Model
from flask import request
import simplejson

# initialize the model
TPIIN = Model()


def json_dump(data):
    return simplejson.dumps(data, ensure_ascii=False, ignore_nan=True)


@app.route('/ap_list')
def get_ap_list():
    return json_dump(TPIIN.get_affiliated_party_list())


@app.route('/ap_time_list')
def get_temporal_overview():
    return json_dump(TPIIN.get_temporal_overview())


@app.route('/ap_topo_list')
def get_topo_list():
    return json_dump(TPIIN.get_affiliated_party_topo_list())


@app.route('/ap_detail', methods=['POST', 'OPTIONS'])
def get_ap_by_ap_id():
    post_data = request.data.decode()
    if post_data != "":
        post_data = simplejson.loads(post_data)
        ap_data = TPIIN.get_detail_by_ap_id(post_data['ap_id'])
    else:
        ap_data = TPIIN.get_detail_by_tp_id('610198671502546')  # default case
        # ap_data = TPIIN.get_detail_by_tp_id('610402196912020326')
    return json_dump(ap_data)


@app.route('/tp_detail', methods=['POST'])
def get_ap_by_tp_id():
    post_data = request.data.decode()
    if post_data != "":
        post_data = simplejson.loads(post_data)
        ap_data = TPIIN.get_detail_by_tp_id(post_data['tp_id'])
    else:
        ap_data = TPIIN.get_detail_by_tp_id('610198671502546')  # default case
        # ap_data = TPIIN.get_detail_by_tp_id('610402196912020326')
    return json_dump(ap_data)


@app.route('/set_model', methods=['POST'])
def set_model_parameter():
    post_data = request.data.decode()
    if post_data != "":
        post_data = simplejson.loads(post_data)
        TPIIN.get_tp_network(
            max_txn_length=post_data['max_transaction_length'],
            max_control_length=post_data['max_control_length']
        )
    return json_dump(TPIIN.get_affiliated_party_list())


@app.route('/ap_txn_detail', methods=['POST'])
def get_ap_txn_detail():
    post_data = request.data.decode()
    if post_data != "":
        post_data = simplejson.loads(post_data)
        detail_ap_data = TPIIN.get_detail_ap_txn(post_data['source'], post_data['target'])
    else:
        detail_ap_data = TPIIN.get_detail_ap_txn('610201694932047', '610198671502546')  # default case
    return json_dump(detail_ap_data)
