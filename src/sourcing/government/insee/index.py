from api_insee import ApiInsee
import configparser
import pandas as pd
import pickle
import json
from src.tools.caching import TextCachingHandler
import os

config = configparser.ConfigParser()
config.read("config.ini")
api = ApiInsee(key=config["insee"]["key"], secret=config["insee"]["secret"])


class IndexINSEE:
    def __init__(self, data_path):
        self.data_path = data_path
        self.output_dir = os.path.join(data_path, "government", "insee")
        os.system("mkdir -p " + self.output_dir)

    def get(self, company_name=None):
        if company_name is None:
            return
        filename = self.output_dir + os.sep + company_name
        cache = TextCachingHandler(filename).get()
        if cache is None:
            data = self.get_data_from_name(company_name)
            TextCachingHandler(filename).store(json.dumps(data))

    def get_data_from_name(self, name):
        data = api.siret(q={"denominationUniteLegale": name}).get()
        history = []
        for et in range(len(data["etablissements"])):
            naf_history = []
            for periode in data["etablissements"][et]["periodesEtablissement"]:
                naf_history.append(periode["activitePrincipaleEtablissement"])
            # data["etablissements"][et]["periodesEtablissement_type"]=\
            #                     get_activities_from_history(naf_history,df)
        return data

    # def get_first_el_if_possible(self,arr):
    #     if len(arr) > 0 :
    #         return arr[0]
    #     else:
    #         return None

    # def get_activities_from_history(history,df):
    #     index_sub_and_nace = []
    #     for el in history:
    #         if el != el : break
    #         if el is None : break
    #         candidate_level5 =  el
    #         candidate_level4 = el[:-2]+"0"
    #         candidate_level3 = float(el[:-2])
    #         candidate_level2 = int(el[:2])
    #         u5 = df[df["id_5"] == candidate_level5]["label_5"].unique()
    #         u4 = df[df["id_4"] == candidate_level4]["label_5"].unique()
    #         u3 = df[df["id_3"] == candidate_level3]["label_5"].unique()
    #         u2 = df[df["id_2"] == candidate_level2]["label_5"].unique()
    #         candidates = {"level_5":get_first_el_if_possible(u5),
    #                       "level_4":get_first_el_if_possible(u4),
    #                       "level_3":get_first_el_if_possible(u3),
    #                       "level_2":get_first_el_if_possible(u2)}
    #         index_sub_and_nace.append(candidates)
    #     return index_sub_and_nace
