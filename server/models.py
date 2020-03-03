import json
import pyarrow
import pandas as pd
import numpy as np
import networkx as nx
from functools import reduce

PATH_TPIIN = './server/data/TPIIN.gpickle'
PATH_TPIIN_AP_TXN = './server/data/TPIIN_ap_txn.ftr'
PATH_TPIIN_INVOICE = './server/data/TPIIN_invoice.ftr'
PATH_TPIIN_INVESTOR = './server/data/TPIIN_investor.ftr'
PATH_TPIIN_TAXPAYER = './server/data/TPIIN_taxpayer.ftr'

# legacy path
PATH_APIRN_ALL = './server/data/APIRN_data_all.json'


def get_ap_df(undirected_graph):
    """
    A helper function to index the affiliated parties
    :param undirected_graph: an undirected graph
    :return: DataFrame with [['tp_id', 'ap_id']]
    """
    _ap = []
    num = 0
    for component in nx.connected_components(undirected_graph):
        _ap.extend([dict(tp_id=node, ap_id=num) for node in component])
        num += 1
    return pd.DataFrame(_ap)


class Model:
    def __init__(self):
        # initialize TPIIN
        self.TPIIN = nx.read_gpickle(PATH_TPIIN)
        # load supplementary data
        self.TPIIN_ap_txn = pd.read_feather(PATH_TPIIN_AP_TXN)
        self.TPIIN_invoice = pd.read_feather(PATH_TPIIN_INVOICE)
        self.TPIIN_investor = pd.read_feather(PATH_TPIIN_INVESTOR)
        self.TPIIN_taxpayer = pd.read_feather(PATH_TPIIN_TAXPAYER)
        # declare class variables
        self.AP_list = []

        # legacy data
        with open(PATH_APIRN_ALL, "r", encoding='utf-8') as file:
            self.APIRN_all = json.load(file)

    def get_TPIIN(self, max_transaction_length=5, max_control_length=5):
        """
        Remove affiliated parties who have affiliated transactions taken place exceeding a step limit
        :param max_transaction_length: a TPIIN, if left empty, the unmodified original version will be used
        :param max_control_length: maximum steps for a transaction to be considered affiliated
        :return: the resulted TPIIN and a corresponding affiliated transaction network
        """
        # initialize TPIIN
        self.TPIIN = nx.read_gpickle(PATH_TPIIN)  # loading pickle is about 4 times faster than deep copy
        tpiin_undirected = self.TPIIN.to_undirected(as_view=True)
        tpiin_ap = get_ap_df(tpiin_undirected)

        # build the APIRN with invoice data
        apirn = nx.DiGraph()
        # validate edges by requiring buyer to reach seller within an arbitrary steps in the TPIIN
        for src, tar in zip(self.TPIIN_ap_txn['seller_id'], self.TPIIN_ap_txn['buyer_id']):
            if nx.has_path(tpiin_undirected, src, tar):
                if nx.shortest_path_length(tpiin_undirected, src, tar) <= max_transaction_length:
                    apirn.add_edge(src, tar)
        # remove isolated nodes
        apirn.remove_nodes_from(list(nx.isolates(apirn)))
        # remove affiliated parties that have not involved in any invoices
        apirn_node = list(apirn.nodes())
        apirn_ap = tpiin_ap.query('tp_id in @apirn_node')['ap_id'].drop_duplicates()
        self.TPIIN.remove_nodes_from(tpiin_ap.query('ap_id not in @apirn_ap')['tp_id'])

        # obtain the control chain using BFS
        control_chain = set()
        for node in apirn.nodes():
            control_chain.add(node)
            control_chain |= {v for _, v in nx.bfs_edges(tpiin_undirected, source=node, depth_limit=max_control_length)}

        # remove the nodes that are out of reach
        self.TPIIN.remove_nodes_from([n for n in self.TPIIN.nodes() if n not in control_chain])
        tpiin_ap = get_ap_df(tpiin_undirected)

        # build the APIRN once again to index AP because a large AP might break into smaller ones
        apirn = nx.DiGraph()
        # validate edges by requiring buyer to reach seller within an arbitrary steps in the TPIIN
        for src, tar in zip(self.TPIIN_ap_txn['seller_id'], self.TPIIN_ap_txn['buyer_id']):
            if src in self.TPIIN and tar in self.TPIIN and nx.has_path(tpiin_undirected, src, tar):
                if nx.shortest_path_length(tpiin_undirected, src, tar) <= max_transaction_length:
                    apirn.add_edge(src, tar)
        # remove isolated nodes
        apirn.remove_nodes_from(list(nx.isolates(apirn)))
        # remove affiliated parties that have not involved in any invoices
        apirn_node = list(apirn.nodes())
        apirn_ap = tpiin_ap.query('tp_id in @apirn_node')['ap_id'].drop_duplicates()
        self.TPIIN.remove_nodes_from(tpiin_ap.query('ap_id not in @apirn_ap')['tp_id'])

        # augment the TPIIN with affiliated transactions
        self.TPIIN.add_edges_from(list(apirn.edges()), ap_txn=True)
        # assign an id for each affiliated party
        self.AP_list = sorted(list(nx.connected_components(tpiin_undirected)), key=lambda _ap: len(_ap))

    def get_affiliated_party_list(self):
        """
        Get the list for affiliated parties with their id, number of inner transactions and nodes.
        The ap_id is for internal use only because the topology of affiliated parties differ
        based on the TPIIN parameter settings.
        :return: json-ready list of affiliated parties
        """
        tpiin_undirected = self.TPIIN.to_undirected(as_view=True)
        ap_list_json = []

        ap_id = 0
        for ap in self.AP_list:
            ap_graph = self.TPIIN.subgraph(ap)
            num_nodes = nx.number_of_nodes(ap_graph)
            num_ap_txn = sum([txn for _, _, txn in ap_graph.edges.data('ap_txn', default=False)])
            ap_list_json.append({'ap_id': ap_id, 'num_nodes': num_nodes, 'num_ap_txn': num_ap_txn})
            ap_id += 1

        return ap_list_json

    def get_detail_by_ap_id(self, ap_id):
        """
        Prepare the affiliated party sub-graph with additional node information
        :param ap_id: the requested affiliate party id
        :return: the sub-graph json
        """
        # extract the requested sub-graph
        ap_graph = self.TPIIN.subgraph(self.AP_list[ap_id]).copy()
        # retrieve taxpayer information
        tp_list = [n for n, tp in list(ap_graph.nodes(data='tp')) if tp]
        tp_df = self.TPIIN_taxpayer.query('tp_id in @tp_list').set_index('tp_id', drop=True)

        for n in tp_list:
            ap_graph.add_node(n, **dict(tp_df.loc[n]))

        # retrieve investor information
        in_list = [n for n, inv in list(ap_graph.nodes(data='in')) if inv]
        in_df = self.TPIIN_investor.query('in_id in @in_list').set_index('in_id', drop=True)
        for n in in_list:
            ap_graph.add_node(n, **dict(in_df.loc[n]))
        for n in in_list:
            # 根据每个invester，求她到关联交易的距离和路径数
            # node的嫌疑值 = 多条路径上的比例的相乘 的加和
            node_suspect_value = 0
            for node in self.AP_list[ap_id]:
                paths = list(nx.all_simple_paths(ap_graph, source=n, target=node))
                for path in list(paths):
                    # 获取每一个path的invest ratio ,如果是多步就invest ratio相乘
                    weight = 1
                    for i in range(len(path)):
                        if i+1 >= len(path): break;
                        else:
                            curr_edge_data = ap_graph.get_edge_data(path[i], path[i+1])
                            if 'in_ratio' in curr_edge_data:
                                weight = weight*curr_edge_data['in_ratio']
            node_suspect_value += weight
            ap_graph.add_node(n, suspect_value=node_suspect_value)



        # retrieve invoice information
        # narrow down search space
        ap_invoice = self.TPIIN_invoice.query('seller_id in @tp_list').query('buyer_id in @tp_list')
        for u, v, data in list(ap_graph.edges(data=True)):
            if 'ap_txn' in data:
                txn = ap_invoice.query('seller_id == @u').query('buyer_id == @v')['txn']
                ap_graph.add_edge(u, v, ap_txn_amount=np.sum(txn), ap_txn_count=len(txn))

        return nx.node_link_data(ap_graph)

    def get_detail_by_tp_id(self, tp_id):
        """
        Prepare the affiliated party sub-graph with additional node information
        :param tp_id: the requested taxpayer id
        :return: the sub-graph json
        """
        # extract the requested sub-graph
        ap_id = -1
        for ap in range(len(self.AP_list)):
            if tp_id in self.AP_list[ap]:
                ap_id = ap

        return self.get_detail_by_ap_id(ap_id) if ap_id != -1 else "{}"
