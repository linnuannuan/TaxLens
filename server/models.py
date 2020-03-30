import pyarrow
import pandas as pd
import numpy as np
import networkx as nx
from functools import reduce
import random

PATH_TPIIN = './server/data/TPIIN.gpickle'
PATH_TPIIN_AP_TXN = './server/data/TPIIN_ap_txn.ftr'
PATH_TPIIN_INVOICE = './server/data/TPIIN_invoice.ftr'
PATH_TPIIN_INVESTOR = './server/data/TPIIN_investor.ftr'
PATH_TPIIN_TAXPAYER = './server/data/TPIIN_taxpayer.ftr'
# PATH_TPIIN_TAX_EVADER = './server/data/TPIIN_tax_evader.ftr'

PATH_TPIIN_TAXINDEX = './server/data/TPIIN_tax_index.pkl'

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
        self.TPIIN_tax_index = nx.read_gpickle(PATH_TPIIN_TAXINDEX)
        # self.TPIIN_tax_evader = pd.read_feather(PATH_TPIIN_TAX_EVADER)

        # declare class variables
        self.AP_list = []
        self.APIRN = nx.DiGraph()

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
        self.APIRN = nx.DiGraph()
        # validate edges by requiring buyer to reach seller within an arbitrary steps in the TPIIN
        for src, tar in zip(self.TPIIN_ap_txn['seller_id'], self.TPIIN_ap_txn['buyer_id']):
            if nx.has_path(tpiin_undirected, src, tar):
                if nx.shortest_path_length(tpiin_undirected, src, tar) <= max_transaction_length:
                    self.APIRN.add_edge(src, tar)
        # remove isolated nodes
        self.APIRN.remove_nodes_from(list(nx.isolates(self.APIRN)))
        # remove affiliated parties that have not involved in any invoices
        apirn_node = list(self.APIRN.nodes())
        apirn_ap = tpiin_ap.query('tp_id in @apirn_node')['ap_id'].drop_duplicates()
        self.TPIIN.remove_nodes_from(tpiin_ap.query('ap_id not in @apirn_ap')['tp_id'])

        # obtain the control chain using BFS
        control_chain = set()
        for node in self.APIRN.nodes():
            control_chain.add(node)
            control_chain |= {v for _, v in nx.bfs_edges(tpiin_undirected, source=node, depth_limit=max_control_length)}

        # remove the nodes that are out of reach
        self.TPIIN.remove_nodes_from([n for n in self.TPIIN.nodes() if n not in control_chain])
        tpiin_ap = get_ap_df(tpiin_undirected)

        # build the APIRN once again to index AP because a large AP might break into smaller ones
        self.APIRN = nx.DiGraph()
        # validate edges by requiring buyer to reach seller within an arbitrary steps in the TPIIN
        for src, tar in zip(self.TPIIN_ap_txn['seller_id'], self.TPIIN_ap_txn['buyer_id']):
            if src in self.TPIIN and tar in self.TPIIN and nx.has_path(tpiin_undirected, src, tar):
                if nx.shortest_path_length(tpiin_undirected, src, tar) <= max_transaction_length:
                    self.APIRN.add_edge(src, tar)
        # remove isolated nodes
        self.APIRN.remove_nodes_from(list(nx.isolates(self.APIRN)))
        # remove affiliated parties that have not involved in any invoices
        apirn_node = list(self.APIRN.nodes())
        apirn_ap = tpiin_ap.query('tp_id in @apirn_node')['ap_id'].drop_duplicates()
        self.TPIIN.remove_nodes_from(tpiin_ap.query('ap_id not in @apirn_ap')['tp_id'])

        # augment the TPIIN with affiliated transactions
        self.TPIIN.add_edges_from(list(self.APIRN.edges()), ap_txn=True)
        # assign an id for each affiliated party
        self.AP_list = sorted(list(nx.connected_components(tpiin_undirected)), key=lambda _ap: len(_ap))

    def get_affiliated_party_list(self):
        """
        Get the list for affiliated parties with their id, number of inner transactions and nodes.
        The ap_id is for internal use only because the topology of affiliated parties differ
        based on the TPIIN parameter settings.
        :return: json-ready list of affiliated parties
        """
        ap_list_json = []

        ap_id = 0
        for ap in self.AP_list:
            ap_graph = self.TPIIN.subgraph(ap)
            num_nodes = nx.number_of_nodes(ap_graph)
            num_ap_txn = sum([txn for _, _, txn in ap_graph.edges.data('ap_txn', default=False)])
            ap_list_json.append({'ap_id': ap_id, 'num_nodes': num_nodes, 'num_ap_txn': num_ap_txn})
            ap_id += 1

        return ap_list_json


    def get_ap_txn_time_list(self):
        """
        Get the temporal data of ap_transaction_amount to draw the time slider.
        :return:  list of transaction by time
        """
        # https://observablehq.com/@mbrownshoes/multiline-time-series-chart
        # {'date':[], 'ap_txn_amount_data':[], }
        # date: A list of time []
        # ap_txn_amount_data: A list of
        # affiliated party transaction: -124.7927
        # 按照日期
        # TPIIN_ap_txn 对应到 TPIIN_invoice
        # print(self.TPIIN_ap_txn)
        ap_txn_by_time = pd.merge(self.TPIIN_ap_txn, self.TPIIN_invoice, on=['seller_id', 'buyer_id'], how='left').groupby('date').sum().reset_index()
        # ap_txn_by_time.groupby('date').sum('txn')
        ap_txn_by_time['date'] = ap_txn_by_time['date'].dt.strftime("%Y-%m-%d")
        # .strftime("%Y-%m-%d")

        return {
            'date': list(ap_txn_by_time['date']),
            'ap_txn_amount': list(ap_txn_by_time['txn'])
        }

        # print(self.TPIIN_ap_txn)






    def get_affiliated_party_by_time(self, start_time,end_time):
        """
        Get the matched affiliated_party list based on start time , end time of ap transaction.
        :return:  list of ap id
        """






    def get_affiliated_party_topo_list(self):
        """
        Get the topology list for affiliated parties with their id, inner taxpayer, trade links with sum transaction amount.
        The ap_id is for internal use only because the topology of affiliated parties differ
        based on the TPIIN parameter settings.
        :return: json-ready list of affiliated parties
        """
        ap_topo_json = []

        ap_id = 0
        for ap in self.AP_list:
            ap_graph = self.TPIIN.subgraph(ap)
            tp_list = [n for n, tp in list(ap_graph.nodes(data='tp')) if tp]
            tp_graph = ap_graph.subgraph(tp_list).copy()
            # remove invest info
            tp_graph.remove_edges_from([(u, v) for u, v, iv in tp_graph.edges(data='in_ratio') if iv])

            # retrive transaction info
            ap_invoice = self.TPIIN_invoice.query('seller_id in @tp_list').query('buyer_id in @tp_list')


            # calculate the transaction amount of each ap_txn
            for u, v, data in list(tp_graph.edges(data=True)):
                if 'ap_txn' in data:
                    txn = ap_invoice.query('seller_id == @u').query('buyer_id == @v')['txn']
                    ap_txn_amount = np.sum(txn)
                    tp_graph.add_edge(u, v, ap_txn_amount=ap_txn_amount)

            ap_topo_json.append({'ap_id': ap_id, 'tax_gap': 100*random.random(), 'nodes': nx.node_link_data(tp_graph)['nodes'], 'links': nx.node_link_data(tp_graph)['links']})
            # get only 10 group for test
            if ap_id >= 19:
                break;
            ap_id += 1

        return ap_topo_json


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
        # tax_df = self.TPIIN_tax_index.query('tp_id in @tp_list').set_index('tp_id', drop=True)
        # retrieve taxpayer index info (12 months as 12 dimension)
        # ti_df =  self.TPIIN_tax_index.query('tp_id in @tp_list').set_index('tp_id', drop=True)

        for n in tp_list:
            ap_graph.add_node(n, **dict(tp_df.loc[n]))
            # if len(self.TPIIN_tax_index.query('tp_id == @n'))>0:
            #     print('get node info: ', tax_df.loc[n])
            #     ap_graph.add_node(n, **dict(tax_df.loc[n]))

            # print('get info of ', n, ' the answer is:',)

            # tax_evader = self.TPIIN_tax_evader.query('tp_id == @n')
            # if not tax_evader.empty:
            #     ap_graph.add_node(n, tax_evader=True)  # will be fix to the actual rule number later

        # retrieve investor information
        in_list = [n for n, inv in list(ap_graph.nodes(data='in')) if inv]
        in_df = self.TPIIN_investor.query('in_id in @in_list').set_index('in_id', drop=True)
        for n in in_list:
            ap_graph.add_node(n, **dict(in_df.loc[n]))

        # Calculate suspicious value
        for in_node in in_list:
            # 根据每个investor，求她到关联交易的距离和路径数
            # node的嫌疑值 = 多条路径上的比例的相乘 的加和
            # check if ap_node conducted affiliated party transactions
            node_suspect_value = 0
            for ap_node in tp_list:  # every taxpayer
                weight = 0
                if ap_node in self.APIRN:  # if taxpayer conducted related party transaction
                    weight = 1
                    paths = list(nx.all_simple_paths(ap_graph, source=in_node, target=ap_node))

                    # 获取每一个path的invest ratio ,如果是多步就invest ratio相乘
                    for path in paths:
                        for i in range(len(path)-1):
                            e_dict = ap_graph.get_edge_data(path[i], path[i+1], default=None)
                            if (e_dict is not None) & ('in_ratio' in e_dict):
                                weight *= e_dict['in_ratio']
                node_suspect_value += weight
            ap_graph.add_node(in_node, suspect_value=node_suspect_value)

        # retrieve invoice information
        # narrow down search space
        ap_invoice = self.TPIIN_invoice.query('seller_id in @tp_list').query('buyer_id in @tp_list')
        ap_graph_undirected = ap_graph.to_undirected()
        ap_graph_undirected.remove_edges_from([(src, dst) for src, dst, data in ap_graph_undirected.edges.data() if ('ap_txn' in data)])
        for u, v, data in list(ap_graph.edges(data=True)):
            if 'ap_txn' in data:
                # calculate the related strength of each ap_txn
                related_strength = 0
                txn = ap_invoice.query('seller_id == @u').query('buyer_id == @v')['txn']
                # add all simple path of each ap_txn into the graph to be highlighted
                self.list = list(nx.all_simple_paths(ap_graph_undirected, source=u, target=v))
                paths = self.list
                for path in paths:
                    path_strength = 1
                    for i in range(0, len(path)-1):
                        path_strength *= ap_graph_undirected.get_edge_data(path[i], path[i+1])['in_ratio']
                    related_strength += path_strength
                ap_graph.add_edge(u, v, ap_txn_amount=np.sum(txn), ap_txn_count=len(txn), path=paths, related_strength=related_strength)

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
                break
        ap_graph = self.TPIIN.subgraph(self.AP_list[ap_id]).copy()
        return self.get_detail_by_ap_id(ap_id) if ap_id != -1 else "{}"

    # def get_ap_id_by_tp_id(self, tp_id):
    #     # get ap_id
    #     ap_id = -1
    #     for ap in range(len(self.AP_list)):
    #         if tp_id in self.AP_list[ap]:
    #             ap_id = ap
    #     ap_graph = self.TPIIN.subgraph(self.AP_list[ap_id]).copy()



    def get_detail_ap_txn(self, source, target):
        """
        get the detail ap_txn
        """

        print('get source,target', source, target)
        ap_id = -1
        for ap in range(len(self.AP_list)):
            if source in self.AP_list[ap]:
                ap_id = ap
                break
        ap_graph = self.TPIIN.subgraph(self.AP_list[ap_id]).copy()

        ap_graph_undirected = ap_graph.to_undirected(as_view=True)


        paths = list(nx.all_simple_paths(ap_graph_undirected, source=source, target=target))


        # 获取所有path的node list
        node_list = list(set(reduce(lambda x, y: x+y, paths)))


        # 获取对应node list的subgraph
        detail_ap_txn_graph = nx.DiGraph(ap_graph.subgraph(node_list))

        # for n, iv in detail_ap_txn_graph.nodes():
        #     print(n,iv)


        # 去除非source和target的 tp节点
        # detail_ap_txn_graph.remove_nodes_from([n for n, iv in detail_ap_txn_graph.nodes(data='in') if ((not iv) & (n != source) & (n != target))])
        # detail_ap_txn_graph.remove_nodes_from([n for n, iv in detail_ap_txn_graph.nodes(data='in') if ((not iv) & (n != source) & (n != target))])

        # 去除transaction的link
        # print('detail edges:', detail_ap_txn_graph.edges())
        # print('remove edges:', [(src, dst) for src, dst, data in detail_ap_txn_graph.edges.data() if (('ap_txn' in data) & ((src != source) | (dst != target)))])

        # remove_edges = [(src, dst) for src, dst, data in detail_ap_txn_graph.edges.data() if (('ap_txn' in data) & ((src != source) | (dst != target)))]
        # if len(remove_edges)>0:
        detail_ap_txn_graph.remove_edges_from([(src, dst) for src, dst, data in detail_ap_txn_graph.edges.data() if (('ap_txn' in data) & ((src != source) | (dst != target)))])


        tp_list = [n for n, tp in list(detail_ap_txn_graph.nodes(data='tp')) if tp]
        tp_df = self.TPIIN_taxpayer.query('tp_id in @tp_list').set_index('tp_id', drop=True)

        for n in tp_list:
            detail_ap_txn_graph.add_node(n, **dict(tp_df.loc[n]))

        in_list = [n for n, inv in list(detail_ap_txn_graph.nodes(data='in')) if inv]
        in_df = self.TPIIN_investor.query('in_id in @in_list').set_index('in_id', drop=True)

        for n in in_list:
            detail_ap_txn_graph.add_node(n, **dict(in_df.loc[n]))


        graph_data = nx.node_link_data(detail_ap_txn_graph)
        return graph_data


