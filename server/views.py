from server import app
from server.models import Model
from flask import request
import simplejson
from datetime import date
import random

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
            start_time=post_data['start_time'],
            end_time=post_data['end_time'],
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


@app.route('/profit_detail', methods=['POST'])
def get_profit_detail():
    post_data = request.data.decode()
    # const cyear = 2014
    # function
    # getVirtulOData(year)
    # {
    #     year = year | | cyear;
    # var
    # date = +echarts.number.parseDate(year + '-01-01');
    # var
    # end = +echarts.number.parseDate((+year + 1) + '-01-01');
    # var
    # dayTime = 3600 * 24 * 1000;
    # var
    # data = ['Date', 'Profit', 'Normal Transaction', 'Ap Transaction'];
    # for (var time = date; time < end; time += dayTime) {
    #     let random_txn = Math.random() * 1000
    # data.push([
    # echarts.format.formatTime('yyyy-MM-dd', time),
    # date.fromisoformat('2019-12-04')
    # Math.floor(Math.random() * 1000) - 500,
    # random_txn - 500,
    # random_txn > 800 ? random_txn * Math.random():0
    # ]);
    # }
    # return data;
    # }
    # if post_data != "":
    print('post_data', post_data)

    post_data = simplejson.loads(post_data)
    start_time = post_data['start_time'],
    end_time = post_data['end_time'],
    detail_ap_data = {
        'source': [['Date', 'Profit', 'Normal Transaction', 'Ap Transaction']],
        'target': [['Date', 'Profit', 'Normal Transaction', 'Ap Transaction']]
    }
    for time in range(start_time, end_time):
        print('time is: ', time)
        random_txn_src = random.random() * 1000 - 500
        random_txn_dst = random.random() * 1000 - 500
        detail_ap_data.source.append[
            time,
            random.random()*1000 - 500,
            random_txn_src,
            0 if random_txn_src > 300 else random*0.3,
        ],
        detail_ap_data.target.append[
            time,
            random.random() * 1000 - 500,
            random_txn_dst,
            0 if random_txn_dst > 300 else random * 0.3,
        ]
    # else:
    #     detail_ap_data = TPIIN.get_detail_ap_txn('610201694932047', '610198671502546')  # default case
    return json_dump(detail_ap_data)