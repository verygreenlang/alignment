import pandas as pd
from pandas import json_normalize
from SPARQLWrapper import SPARQLWrapper, JSON
from src.tools.caching import PickleCachingHandler

import os 

class RssLinksWikidata:
    def __init__(self,data_path):
        self.folder =data_path + os.sep + "wikidata" + os.sep + "rssfeed" + os.sep
        os.system("mkdir -p " + self.folder)

    def get(self):
        filename = self.folder + "all.pkl"
        cache = PickleCachingHandler(filename).get()
        if cache is not  None : return cache

        sparql_query = """
        SELECT ?item ?itemLabel
        WHERE
        {
          ?a wdt:P1019 ?item .
          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }

        }
        """
        sparql_service_url = "https://query.wikidata.org/sparql"
        result_table = self.query_wikidata(sparql_query, sparql_service_url)
        if len(result_table) > 0 :
            values = self.get_value_list(result_table)
            PickleCachingHandler(filename).store(values)
            return values
        return [ ]

    def get_value_list(self,result_table):
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
