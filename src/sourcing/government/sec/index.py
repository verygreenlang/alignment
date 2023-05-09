
import pickle, os
import edgar
import contextlib
from src.tools.logger import FingreenLogger
from src.tools.caching import JsonCachingHandler
from src.tools.caching.pickle_handler import PickleCachingHandler

logger = FingreenLogger().logger

class IndexSEC:
    def __init__(self, data_path ):
        self.cik_to_name_url_index =  "https://www.sec.gov/Archives/edgar/cik-lookup-data.txt"
        # self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"
        # self.user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        self.user_agent = "famat v Contact@famat.me"
        sec_data_path = os.path.join(data_path, "government", "sec")
        os.system("mkdir -p " + sec_data_path )
        self.cik_to_name_url_filename = sec_data_path + os.sep + "all.pkl"
        self.cik_to_name_url_filename_raw = sec_data_path + os.sep + "raw.txt"
        self.sec_data_path = sec_data_path
        self.data_path_index_data_by_cik = sec_data_path + os.sep + "index_documents/"
    def get(self):
        self.get_index_cik_to_data()
        return self.get_index_cik_name()


    def get_index_cik_to_data(self):
        download_directory = self.data_path_index_data_by_cik #"data_index_from_edgar_python"
        since_year=2021
        user_agent =" FAMAT  François Amat  francois@famat.me"
        with contextlib.redirect_stdout(None):
            edgar.download_index(download_directory, since_year, user_agent, skip_all_present_except_last=True)

    def get_index_cik_name(self):
        cache = self.get_from_cache(self.cik_to_name_url_filename)
        if cache is not None : return cache
        CMD = """  wget --user-agent=""" +'"'+ self.user_agent+'"'+""" "https://www.sec.gov/Archives/edgar/cik-lookup-data.txt" """
        os.system(CMD)
        os.system("mv cik-lookup-data.txt " +  self.cik_to_name_url_filename_raw)
        with open(self.cik_to_name_url_filename_raw, encoding="latin-1",mode="r") as f:
            content = f.readlines()
        index = dict()
        index["cik_to_name"] = dict()
        index["name_to_cik"] = dict()
        for line in content :
            name,cik = line.split(":")[0], line.split(":")[1]
            index["cik_to_name"][cik]  = name.lower()
            index["name_to_cik"][name.lower()] = cik
        self.store_cache(index,self.cik_to_name_url_filename)
        return index

    def get_from_cache(self,filename):
        return PickleCachingHandler(filename).get()


    def store_cache(self,content,filename):
        return PickleCachingHandler(filename).store(content)

