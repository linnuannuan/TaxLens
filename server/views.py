from server import app
from server.models import Model
from flask import request
import simplejson

# initialize the model
TPIIN = Model()


def json_dump(data):
    return simplejson.dumps(data, ensure_ascii=False, ignore_nan=True)


@app.route('/temporal_overview')
def get_temporal_overview():
    return json_dump(TPIIN.get_temporal_overview())


@app.route('/ap_list', methods=['POST'])
def get_ap_list():
    post_data = request.data.decode()
    if post_data != "":
        post_data = simplejson.loads(post_data)
        TPIIN.get_tp_network(
            _start_time=post_data['start_time'],
            _end_time=post_data['end_time'],
            max_txn_length=post_data['max_txn_length'],
            max_control_length=post_data['max_control_length']
        )
    else:
        TPIIN.get_tp_network()
    return json_dump(TPIIN.get_affiliated_party_list())


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


@app.route('/ap_txn_detail', methods=['POST'])
def get_ap_txn_detail():
    post_data = request.data.decode()
    if post_data != "":
        post_data = simplejson.loads(post_data)
        detail_ap_data = TPIIN.get_detail_ap_txn(post_data['source'], post_data['target'])
    else:
        detail_ap_data = TPIIN.get_detail_ap_txn('610201694932047', '610198671502546')  # default case
    return json_dump(detail_ap_data)


@app.route('/calendar', methods=['POST'])
def get_calendar():
    post_data = request.data.decode()
    if post_data != "":
        post_data = simplejson.loads(post_data)
        detail_ap_data = TPIIN.get_calendar_data(
            post_data['seller_id'],
            post_data['buyer_id'],
            post_data['start_time'],
            post_data['end_time']
        )
    else:
        detail_ap_data = TPIIN.get_calendar_data(
            '610198748609852',
            '610198684755147',
            '2014-01-01',
            '2014-03-31'
        )
    return json_dump(detail_ap_data)
