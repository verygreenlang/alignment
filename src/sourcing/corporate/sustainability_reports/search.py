from textdistance.algorithms import levenshtein
import os

class SearchSustainabilityReport:
    def __init__(self,data_path):
        self.data_path = data_path
        self.entity_list = os.listdir(data_path)
        # print(data_path)
        # print(len(        self.entity_list),"entity_list")
    def get(self,company_name = None):
        return_template = {"pdf":None}
        company_name = company_name.replace(" ","-").replace("_","-")
        if company_name is None : return return_template
        if not self.get_entity_exact_match(company_name):
            company_name = self.get_most_resemblant(company_name)
            if company_name is None : return return_template
        pdf_reports = os.listdir(self.data_path + os.sep + company_name)
        return {"pdf":pdf_reports}

    def get_entity_exact_match(self,company):
        return company in self.entity_list

    def get_most_resemblant(self,company):
        max = 0
        entity_max = None
        for entity in self.entity_list:
            if levenshtein.distance(company, entity) > max :
                max = levenshtein.distance(company, entity)
                entity_max = entity
        return entity_max
