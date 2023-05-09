import pandas as pd
import os, pickle
from pandas import json_normalize
from SPARQLWrapper import SPARQLWrapper, JSON
from src.tools.caching import PickleCachingHandler, JsonCachingHandler
import json, requests


class CompanyWikidata:
    def __init__(self,data_path):
        self.folder =data_path + os.sep + "wikidata"
        os.system("mkdir -p " + self.folder)

    def get(self,company_name):
        self.company_name = company_name
        self.folder = self.folder +os.sep + company_name.replace(" ","_")
        os.system("mkdir -p " + self.folder)
        #self.filename = self.folder +os.sep + "all.json"
        res_dict = dict()
        #if os.path.isfile(self.filename):
        #    dfs =  self.get_from_cache()
        #    dfs = [pd.DataFrame(el) for el in dfs]
        #    return dfs
        entities =  self.get_entity_by_name()
        if len(entities) > 0  :
            for entity in entities:
                res_dict[entity] = self.get_data_by_entity(entity)
        return res_dict

    def get_all(self):
        query = """
        SELECT ?item ?itemLabel
        WHERE
        {
          ?item wdt:P31 wd:Q783794.
          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
        }
        """
        sparql_service_url = "https://query.wikidata.org/sparql"
        result_table = self.query_wikidata(query, sparql_service_url)
        if len(result_table) > 0 :
            return self.get_name_list(result_table)


    def get_entity_by_name(self,company_name = None):
        if company_name is None :
            candidate_name = [self.company_name.lower(), self.company_name.upper(), self.company_name.title(), self.company_name]
        else:
            candidate_name = [company_name]
        candidates = []
        for name in candidate_name:
            query_url = """https://www.wikidata.org/w/api.php?action=wbsearchentities&search="""+ name+"""&language=en&format=json"""
            data = requests.get(query_url)
            for id in  ["wd:" + str(el["id"]) for el in json.loads(data.content)["search"]]:
                candidates.append(id)
        return candidates

    def get_data_by_entity(self,company_wiki_id):
        sparql_query = """
        SELECT ?b ?c ?bLabel ?cLabel
        WHERE
        {
        """+company_wiki_id.replace("http://www.wikidata.org/entity/","wd:")+""" ?b ?c
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }

        }
        """


        sparql_service_url = "https://query.wikidata.org/sparql"
        return self.query_wikidata(sparql_query, sparql_service_url)

    def get_name_list(self,result_table):
        return list(result_table["itemLabel.value"].unique())
    def get_entity_list(self,result_table):
        return list(result_table["item.value"].unique())

    def query_wikidata(self,sparql_query, sparql_service_url):
        """
        Query the endpoint with the given query string and return the results as a pandas Dataframe.
        """
        # create the connection to the endpoint
        # Wikidata enforces now a strict User-Agent policy, we need to specify the agent
        # See here https://www.wikidata.org/wiki/Wikidata:Project_chat/Archive/2019/07#problems_with_query_API
        # https://meta.wikimedia.org/wiki/User-Agent_policy
        sparql = SPARQLWrapper(sparql_service_url, agent="Sparql Wrapper on Jupyter example")

        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(JSON)

        # ask for the result
        result = sparql.query().convert()
        return json_normalize(result["results"]["bindings"])
    def get_from_cache(self):
        return JsonCachingHandler(self.filename).get()
        # if os.path.isfile(self.filename):
        #     with open(self.filename,"rb") as f:
        #         return pickle.load(f)
        # return None

    def store_cache(self,content):
        JsonCachingHandler(self.filename).store(content)

        # # print(self.wikirate_metric_file)
        # with open(self.filename,"wb") as f:
        #     pickle.dump(content,f)
