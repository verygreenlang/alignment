import textdistance
import os
from src.tools.caching.pickle_handler import PickleCachingHandler

class SearchSEC:
    def __init__(self,data_path):
        self.data_path = data_path
        # self.entity_list = os.listdir(data_path)
        # sec_data_path = os.path.join(data_path, "government", "sec")
        data_path = os.path.join(data_path,"government","sec")

        self.cik_to_name_url_filename = data_path + os.sep + "all.pkl"
        self.name_index =PickleCachingHandler( self.cik_to_name_url_filename).get()["name_to_cik"]
        # print(self.name_index)
        #["name_to_cik"]

    def get(self,company_name = None):
        if company_name in self.name_index.keys():
            return self.name_index["company_name"]
        return None
