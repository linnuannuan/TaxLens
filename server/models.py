import pandas as pd
import numpy as np
import networkx as nx
from functools import reduce
import random

PATH_TP_NETWORK = './server/data/tp_network.pkl'
PATH_AP_TXN = './server/data/ap_txn.ftr'
PATH_AP_TXN_TIME = './server/data/ap_txn_time.ftr'
PATH_INVOICE = './server/data/invoice.ftr'
PATH_INVESTOR = './server/data/investor.ftr'
PATH_TAXPAYER = './server/data/taxpayer.ftr'
PATH_FINANCE = './server/data/finance.ftr'


class Model:
    def __init__(self):
        # initialize TPIIN
        self.tp_network = nx.read_gpickle(PATH_TP_NETWORK)
        # load supplementary data
        self.ap_txn = pd.read_feather(PATH_AP_TXN)
        self.ap_txn_time = pd.read_feather(PATH_AP_TXN_TIME)
        self.invoice = pd.read_feather(PATH_INVOICE)
        self.investor = pd.read_feather(PATH_INVESTOR)
        self.taxpayer = pd.read_feather(PATH_TAXPAYER)
        self.finance = pd.read_feather(PATH_FINANCE)

        # declare class variables
        self.ap_list = []
        self.ap_network = None

        # initialization
        self.ap_txn_time['date'] = self.ap_txn_time['date'].dt.strftime("%Y-%m-%d")
        self.get_tp_network()

    def get_temporal_overview(self):
        """
        Get the temporal data of ap_transaction_amount to draw the time slider.
        Notice that the data used here is independent, for the sake of having consistent visualization
        :return:    date: A list of time
                    ap_txn_amount_data: A list of affiliated party transaction
        """
        return {
            'date': list(self.ap_txn_time['date']),
            'ap_txn_amount': list(self.ap_txn_time['txn_sum'])
        }

    def get_tp_network(self, max_txn_length=5, max_control_length=5, start_time='2014-01-01', end_time='2015-12-31'):
        """
        Remove affiliated parties who have affiliated transactions taken place exceeding a step limit
        :param max_txn_length: maximum steps for a transaction to be considered affiliated
        :param max_control_length: maximum steps for a taxpayer to be considered related to the suspect
        :param start_time: the start time of query
        :param end_time: the end time of query
        :return: the resulted TPIIN and a corresponding affiliated transaction network
        """
        # initialize taxpayer network
        self.tp_network = nx.read_gpickle(PATH_TP_NETWORK)  # loading pickle is about 4 times faster than deep copy
        tp_network_undirected = self.tp_network.to_undirected(as_view=True)

        # build the trade network with invoice data
        self.ap_network = nx.DiGraph()
        ap_txn = self.ap_txn.query('@start_time <= date <= @end_time')
        # validate edges by requiring buyer to reach seller within an arbitrary steps in the TPIIN
        for src, tar in zip(ap_txn['seller_id'], ap_txn['buyer_id']):
            if nx.shortest_path_length(tp_network_undirected, src, tar) <= max_txn_length:
                self.ap_network.add_edge(src, tar)
        # remove isolated nodes
        self.ap_network.remove_nodes_from(list(nx.isolates(self.ap_network)))

        # create a mapping for affiliated parties
        ap_df = []
        for num, component in enumerate(nx.connected_components(tp_network_undirected), 0):
            ap_df.extend([dict(tp_id=node, ap_id=num) for node in component])
        ap_df = pd.DataFrame(ap_df)

        # remove affiliated parties that have not appeared in ap_network
        ap_node = list(self.ap_network.nodes())
        ap_exist = ap_df.query('tp_id in @ap_node')['ap_id'].drop_duplicates()
        self.tp_network.remove_nodes_from(ap_df.query('ap_id not in @ap_exist')['tp_id'])

        # obtain the control chain using BFS
        control_chain = set()
        for node in self.ap_network.nodes():
            control_chain.add(node)
            control_chain |= {v for _, v in
                              nx.bfs_edges(tp_network_undirected, source=node, depth_limit=max_control_length)}
        # remove the nodes that are out of reach
        self.tp_network.remove_nodes_from([n for n in self.tp_network.nodes() if n not in control_chain])

        # augment the taxpayer network with affiliated transactions
        self.tp_network.add_edges_from(list(self.tp_network.edges()), ap_txn=False)  # initialize
        self.tp_network.add_edges_from(list(self.ap_network.edges()), ap_txn=True)
        # assign an id for each affiliated party
        self.ap_list = sorted(list(nx.connected_components(tp_network_undirected)), key=lambda _ap: len(_ap))

    def get_affiliated_party_list(self):
        """
        Get the list for affiliated parties with their id, number of inner transactions and nodes.
        The ap_id is for internal use only because the topology of affiliated parties differ
        based on the TPIIN parameter settings.
        :return: json-ready list of affiliated parties
        """
        ap_list_json = []
        for ap_id, ap in enumerate(self.ap_list, 0):
            ap_graph = self.tp_network.subgraph(ap)
            num_nodes = nx.number_of_nodes(ap_graph)
            num_ap_txn = sum([txn for _, _, txn in ap_graph.edges.data('ap_txn')])
            ap_list_json.append({'ap_id': ap_id, 'num_nodes': num_nodes, 'num_ap_txn': num_ap_txn})
        return ap_list_json

    def get_affiliated_party_topo_list(self):
        """
        Get the topology list for affiliated parties with their id, inner taxpayer, trade links with sum transaction
        amount. The ap_id is for internal use only because the topology of affiliated parties differ based on
        the TPIIN parameter settings.
        :return: json-ready list of affiliated parties
        """
        ap_topo_json = []

        # for i, ap in enumerate(reversed(self.ap_list), 0):
        for num in range(20):
            ap_id = int(len(self.ap_list)*random.random())
            # Find all taxpayers in the affiliated party
            tp_graph = self.tp_network.subgraph(self.ap_list[ap_id])
            tp_list = [n for n, tp in list(tp_graph.nodes(data='tp')) if tp]
            # Find only the nodes involved the the related party transactions
            tp_graph = self.ap_network.subgraph(tp_list).copy()

            # retrieve transaction info
            ap_invoice = self.ap_txn.query('seller_id in @tp_list').query('buyer_id in @tp_list')
            # calculate the transaction amount of each ap_txn
            for u, v in tp_graph.edges():
                txn = ap_invoice.query('seller_id == @u').query('buyer_id == @v')['txn_sum']
                ap_txn_amount = np.sum(txn)
                tp_graph.add_edge(u, v, ap_txn_amount=ap_txn_amount)

            ap_topo_json.append({
                'ap_id': ap_id,
                'tax_gap': 100*random.random(),
                'nodes': nx.node_link_data(tp_graph)['nodes'],
                'links': nx.node_link_data(tp_graph)['links']
            })

        return ap_topo_json

    def get_ap_id(self, tp_id):
        """
        Retrieve the corresponding ap_id with tp_id
        :param tp_id: the taxpayer id
        :return: ap_id
        """
        ap_id = -1
        for i, ap in enumerate(self.ap_list, 0):
            if tp_id in ap:
                ap_id = i
                break
        return ap_id

    def get_taxpayer_detail(self, ap_graph):
        tp_list = [n for n, tp in list(ap_graph.nodes(data='tp')) if tp]
        tp_df = self.taxpayer.query('tp_id in @tp_list').set_index('tp_id', drop=True)
        for n in tp_list:
            ap_graph.add_node(n, **dict(tp_df.loc[n]))
        return tp_list

    def get_investor_detail(self, ap_graph):
        in_list = [n for n, inv in list(ap_graph.nodes(data='in')) if inv]
        in_df = self.investor.query('in_id in @in_list').set_index('in_id', drop=True)
        for n in in_list:
            ap_graph.add_node(n, **dict(in_df.loc[n]))
        return in_list

    def get_detail_by_tp_id(self, tp_id):
        """
        Prepare the affiliated party sub-graph with additional node information
        :param tp_id: the requested taxpayer id
        :return: the sub-graph json
        """
        # extract the requested sub-graph
        ap_id = self.get_ap_id(tp_id)
        return self.get_detail_by_ap_id(ap_id) if ap_id != -1 else '{}'

    def get_detail_by_ap_id(self, ap_id):
        """
        Prepare the affiliated party sub-graph with additional node information
        :param ap_id: the requested affiliate party id
        :return: the sub-graph json
        """
        # extract the requested sub-graph
        ap_graph = self.tp_network.subgraph(self.ap_list[ap_id]).copy()
        # retrieve taxpayer information
        tp_list = self.get_taxpayer_detail(ap_graph)
        # retrieve investor information
        in_list = self.get_investor_detail(ap_graph)

        # Calculate suspicious value
        for in_node in in_list:
            # 根据每个investor，求她到关联交易的距离和路径数
            # node的嫌疑值 = 多条路径上的比例的相乘 的加和
            # check if ap_node conducted affiliated party transactions
            node_suspect_value = 0
            for ap_node in tp_list:  # every taxpayer
                if ap_node in self.ap_network:  # if taxpayer conducted related party transaction
                    # 获取每一个path的invest ratio ,如果是多步就invest ratio相乘
                    for path in list(nx.all_simple_paths(ap_graph, source=in_node, target=ap_node)):
                        weight = 1
                        for i in range(len(path)-1):
                            e_dict = ap_graph.get_edge_data(path[i], path[i+1])
                            weight = weight * e_dict['in_ratio'] if 'in_ratio' in e_dict else 0
                        node_suspect_value += weight
            ap_graph.add_node(in_node, suspect_value=node_suspect_value)

        # retrieve invoice information
        ap_invoice = self.ap_txn.query('seller_id in @tp_list').query('buyer_id in @tp_list')
        # obtain an undirected investment network
        ap_graph_undirected = ap_graph.to_undirected()
        ap_graph_undirected.remove_edges_from(
            [(u, v) for u, v, ap in ap_graph_undirected.edges(data='ap_txn') if ap]
        )
        for u, v, ap_txn in ap_graph.edges(data='ap_txn'):
            if ap_txn:
                # calculate the related strength of each ap_txn
                related_strength = 0
                txn = ap_invoice.query('seller_id == @u').query('buyer_id == @v')['txn_sum']
                # add all simple path of each ap_txn into the graph to be highlighted
                paths = list(nx.all_simple_paths(ap_graph_undirected, source=u, target=v))
                for path in paths:
                    path_strength = 1
                    for i in range(0, len(path)-1):
                        path_strength *= ap_graph_undirected.get_edge_data(path[i], path[i+1])['in_ratio']
                    related_strength += path_strength
                ap_graph.add_edge(
                    u,
                    v,
                    ap_txn_amount=np.sum(txn),
                    ap_txn_count=len(txn),
                    path=paths,
                    related_strength=related_strength
                )

        return nx.node_link_data(ap_graph)

    def get_detail_ap_txn(self, source, target):
        """
        Get the details of affiliated party transactions from source to target
        :param source: seller tp_id
        :param target: buyer tp_id
        :return:
        """
        # find the corresponding ap_graph
        ap_id = self.get_ap_id(source)
        if ap_id == -1:
            return '{}'
        ap_graph = self.tp_network.subgraph(self.ap_list[ap_id])
        ap_graph_undirected = ap_graph.to_undirected(as_view=True)

        # 获取所有path的node list
        paths = list(nx.all_simple_paths(ap_graph_undirected, source=source, target=target))
        node_list = list(set(reduce(lambda x, y: x+y, paths)))

        # 获取对应node list的sub-graph
        detail_ap_txn_graph = ap_graph.subgraph(node_list).copy()
        detail_ap_txn_graph.remove_edges_from(
            [(src, dst) for src, dst, ap_txn in detail_ap_txn_graph.edges(data='ap_txn')
             if (ap_txn & ((src != source) | (dst != target)))])
        self.get_taxpayer_detail(detail_ap_txn_graph)
        self.get_investor_detail(detail_ap_txn_graph)
        return nx.node_link_data(detail_ap_txn_graph)
