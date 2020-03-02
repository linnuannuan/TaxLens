import json
import pandas as pd
import numpy as np
import networkx as nx


PATH_APIRN = './server/data/APIRN_data.json'
PATH_APIRN_ALL = './server/data/APIRN_data_all.json'


class Model:
    def __init__(self):
        with open(PATH_APIRN, "r", encoding='utf-8') as file:
            self.APIRN = json.load(file)
        with open(PATH_APIRN_ALL, "r", encoding='utf-8') as file:
            self.APIRN_all = json.load(file)

    def algorithm(self):
        return
