from server import app
from server.models import Model
from flask import request
import simplejson

# initialize the model
TPIIN = Model()
TPIIN.get_TPIIN()


@app.route('/ap_list')
def get_ap_list():
    return simplejson.dumps(TPIIN.get_affiliated_party_list(), ensure_ascii=False, ignore_nan=True)

@app.route('/ap_time_list')
def get_ap_time_list():
    return simplejson.dumps(TPIIN.get_ap_txn_time_list(), ensure_ascii=False, ignore_nan=True)


@app.route('/ap_topo_list')
def get_topo_list():
    return simplejson.dumps(TPIIN.get_affiliated_party_topo_list(), ensure_ascii=False, ignore_nan=True)



@app.route('/ap_detail', methods=['POST'])
def get_ap_by_ap_id():
    post_data = request.data.decode()
    if post_data != "":
        post_data = simplejson.loads(post_data)
        ap_data = TPIIN.get_detail_by_ap_id(post_data['ap_id'])
    else:
        ap_data = TPIIN.get_detail_by_tp_id('610198671502546')  # default case
        # ap_data = TPIIN.get_detail_by_tp_id('610402196912020326')
    return simplejson.dumps(ap_data, ensure_ascii=False, ignore_nan=True)


@app.route('/tp_detail', methods=['POST'])
def get_ap_by_tp_id():
    post_data = request.data.decode()
    if post_data != "":
        post_data = simplejson.loads(post_data)
        ap_data = TPIIN.get_detail_by_tp_id(post_data['tp_id'])
    else:
        ap_data = TPIIN.get_detail_by_tp_id('610198671502546')  # default case
        # ap_data = TPIIN.get_detail_by_tp_id('610402196912020326')
    return simplejson.dumps(ap_data, ensure_ascii=False, ignore_nan=True)


@app.route('/set_model', methods=['POST'])
def set_model_parameter():
    post_data = request.data.decode()
    if post_data != "":
        post_data = simplejson.loads(post_data)
        TPIIN.get_TPIIN(post_data['max_transaction_length'], post_data['max_control_length'])
    return simplejson.dumps(TPIIN.get_affiliated_party_list(), ensure_ascii=False, ignore_nan=True)


@app.route('/ap_txn_detail', methods=['POST'])
def get_ap_txn_detail():
    post_data = request.data.decode()
    # print('view: get ap_txn_detail  post data:', post_data)
    if post_data != "":
        post_data = simplejson.loads(post_data)
        detail_ap_data = TPIIN.get_detail_ap_txn(post_data['source'], post_data['target'])
    else:
        detail_ap_data = TPIIN.get_detail_ap_txn('610201694932047', '610198671502546')  # default case

    # print('detail_ap_data:', detail_ap_data)
    return simplejson.dumps(detail_ap_data, ensure_ascii=False, ignore_nan=True)