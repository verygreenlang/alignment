import textdistance
import os
from src.tools.caching import PickleCachingHandler
class SearchWIKIDATA:
    def __init__(self,data_path):
        self.data_path = data_path
        self.entity_list = os.listdir(data_path)

    def get(self,company_name = None):
        company_name = company_name.replace(" ","_").replace("-","_")
        target_filename = os.path.join(self.data_path,company_name,"all.pkl")
        return  PickleCachingHandler(target_filename).get()
