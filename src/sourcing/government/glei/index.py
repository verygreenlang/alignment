import json
import os
import requests
from src.tools.caching import JsonCachingHandler
from src.sourcing.wiki import LeiWikidata
from src.sourcing.wiki import CompanyWikidata

class IndexGLEI:
    def __init__(self,data_path):
        self.data_path = data_path
        self.output_dir = os.path.join(data_path,"government","glei")
        os.system("mkdir -p " + self.output_dir)
        self.api_base_url ="https://api.gleif.org/api/v1/"

    def get(self,company_name=None):
        if company_name is None : return
        filename = self.output_dir + os.sep + company_name.replace(" ","_") + ".json"
        cache = JsonCachingHandler(filename).get()
        if cache: return cache
        company_data = {}
        company_data["by_name"] = self.get_by_name(company_name)
        company_data["by_lei"] = self.get_by_lei(company_name)
        JsonCachingHandler(filename).store(company_data)

    def get_by_lei(self,company_name):
        company_data = {}
        wikidata_company_ids = CompanyWikidata(self.data_path).get_entity_by_name(company_name=company_name)
        for company_id in wikidata_company_ids:
            leis = LeiWikidata().get(company_wikid=company_id)
            for lei in leis :
                for child in self.get_companies_by_lei(lei):
                    parent = self.get_highest_parent_company(lei)
                    if parent is not None :
                        company_data[parent["id"]] = dict()
                        company_data[parent["id"]]["entity"] = parent
                        company_data[parent["id"]]["children"] = self.get_children(lei)
                    else:
                        company_data[child["id"]] = dict()
                        company_data[child["id"]]["entity"] = parent
                        company_data[child["id"]]["children"] = self.get_children(lei)
        return company_data

    def get_by_name(self,company_name):
        company_data = {}
        candidates =  self.get_companies_by_name(company_name)
        candidates_lei = [el["id"] for el in candidates]
        for lei in candidates_lei:
            parent = self.get_highest_parent_company(lei)
            if parent is not None :
                company_data[parent["id"]] = dict()
                company_data[parent["id"]]["entity"] = parent
                company_data[parent["id"]]["children"] = self.get_children(lei)
            else:
                company_data[lei] = dict()
                company_data[lei]["entity"] = parent
                company_data[lei]["children"] = self.get_children(lei)
        return company_data

    def get_companies_by_lei(self,lei):
        search_options = "?filter[lei]="+lei
        data =  json.loads(requests.get(self.api_base_url + "lei-records" + search_options).content.decode("utf8"))
        return data["data"]

    def get_companies_by_name(self,name):
        search_options = "?filter%5Bentity.legalName%5D="+name+"&page%5Bnumber%5D=1&page%5Bsize%5D=50"
        data =  json.loads(requests.get(self.api_base_url + "lei-records" + search_options).content.decode("utf8"))
        return data["data"]

    def get_highest_parent_company(self,lei):
        data = json.loads(requests.get(self.api_base_url + "lei-records/"+lei+"/ultimate-parent-relationship").content.decode("utf8"))
        if "errors" in data.keys():
            return None
        return data["data"]

    def get_children(self,lei):
        first_rep = json.loads(requests.get(self.api_base_url  + "lei-records/"+lei+"/direct-child-relationships/").content.decode("utf8"))
        number_of_pages = first_rep["meta"]["pagination"]["to"]
        if number_of_pages is None : number_of_pages = 0

        children = [ ]
        for i in range(1,number_of_pages+1):
            children.append(json.loads(requests.get(self.api_base_url  + "lei-records/"+lei+"/direct-child-relationships/" +"?page%5Bnumber%5D="+str(i) ).content.decode("utf8")))
        return children
