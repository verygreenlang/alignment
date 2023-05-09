import pandas as pd
from pandas import json_normalize
from SPARQLWrapper import SPARQLWrapper, JSON
from src.tools.caching import PickleCachingHandler



class LeiWikidata:
    def __init__(self):
        pass

    def get(self,company_wikid = None):
        if company_wikid is None : return
        sparql_query = """
        SELECT ?item ?itemLabel
        WHERE
        {
          """ +company_wikid + """ wdt:P1278 ?item .
          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }

        }
        """
        sparql_service_url = "https://query.wikidata.org/sparql"
        result_table = self.query_wikidata(sparql_query, sparql_service_url)
        if len(result_table) > 0 :
            return self.get_name_list(result_table)
        return  [ ]
    def get_name_list(self,result_table):
        return list(result_table["itemLabel.value"].unique())

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
