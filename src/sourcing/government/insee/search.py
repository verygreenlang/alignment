import textdistance
import os
from src.tools.caching import PickleCachingHandler
class SearchINSEE:
    def __init__(self,data_path):
        self.data_path = data_path
        self.entity_list = os.listdir(data_path)

    def get(self,company_name = None):
        pass
