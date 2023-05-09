import os, sys
from src.tools.caching  import  PickleCachingHandler


from src.tools.logger import FingreenLogger
logger = FingreenLogger().logger

from src.sourcing.corporate.sustainability_reports.search import SearchSustainabilityReport
from src.sourcing.wiki import SearchWIKIDATA
from src.sourcing.wiki import SearchWikirate

from src.sourcing.government.sec import SearchSEC
from src.sourcing.government.insee import SearchINSEE
from src.sourcing.government.glei import SearchGLEI


class Align:
    def __init__(self,asset,config):
        self.asset = asset
        configObj = configparser.ConfigParser()
        configObj.read(config)
        self.config = configObj
        self.classify_asset(asset)


    def classify_asset(self,asset):
        if self.mostly_integer(asset):
            self.fund = asset
        else:
            self.company = asset

    def mostly_integer(self,asset):
        count = 0
        for i in asset :
            if i.isdigit():
                count += 1
        if count > 4 :
            return True
        return False


    def run(self):
        output_path = self.get_output_data_path()
        output_dir = output_path + os.sep + self.company.replace(" ","_")
        # print(output_dir)
        os.system("mkdir -p " + output_dir)
        output_file = output_dir + os.sep + "all.pkl"
        print("output_file",output_file)
        cache = PickleCachingHandler(output_file).get()
        if True or  cache is None :
            full_data = dict()
            full_data["corporate"] = self.search_corporate()
            full_data["wikirate"] = self.search_wikirate()
            full_data["wikidata"] = self.search_wikidata()
            full_data["government"] = self.search_gov()
            # full_data["asset_manager"] = self.search_in_am()
            PickleCachingHandler(output_file).store(full_data)

    def search_corporate(self):
        data_path = self.get_data_path()
        # working_path = data_path
        working_path = os.path.join(data_path,"corporate","sustainability")
        logger.info("Search: sustainability reports")
        return SearchSustainabilityReport(working_path).get(company_name = self.company)

    def search_wikirate(self):
        data_path = self.get_data_path()
        working_path = os.path.join(data_path,"wikirate","company")
        logger.info("Search: Wikirate")
        return SearchWikirate(working_path).get(company_name = self.company)

    def search_wikidata(self):

        logger.info("Search: Wikidata")
        data_path = self.get_data_path()
        working_path = os.path.join(data_path,"wikidata")
        return SearchWIKIDATA(working_path).get(company_name = self.company)

    def search_gov(self):
        gov_data = dict()
        data_path = self.get_data_path()

        logger.info("Search: Gov-SEC")
        working_path = os.path.join(data_path,"government","sec")
        gov_data["sec"] =  SearchSEC(data_path).get(company_name = self.company)

        logger.info("Search: Insee")
        working_path = os.path.join(data_path,"government","insee")
        gov_data["sec"] =  SearchINSEE(working_path).get(company_name = self.company)

        logger.info("Search: glei")
        working_path = os.path.join(data_path,"government","glei")
        gov_data["glei"] =  SearchGLEI(working_path).get(company_name = self.company)

        return gov_data

    def search_in_am(self):
        logger.info("Search: Asset managers")
        data_path = self.get_data_path()

        working_path = os.path.join(data_path,"corporate","sustainability")
    def get_data_path(self):
        if self.config.getboolean("aws","use"):
            return "fingreen"
        else:
            data_path = self.config["data"]["path"]
            return data_path

    def get_output_data_path(self):
        pass
        data_path = self.get_data_path()
        # here = "/".join(os.path.abspath(os.path.dirname(__file__)).split("/")[:-1])
        data_path = os.path.join(data_path,"alignment")
        os.system("mkdir -p " + data_path)
        return data_path

    # def run(self):
    #     processes = []
    #     processes.append(mp.Process(target=self.get_corporate)) #,args=(data_path)))
    #     processes.append(mp.Process(target=self.get_wikirate)) #,args=(data_path)))
    #     processes.append(mp.Process(target=self.get_wikidata))
    #     processes.append(mp.Process(target=self.get_gov)) #,args=(data_path)))
    #     processes.append(mp.Process(target=self.get_am))
    #     [x.start() for x in processes]
    #     [p.join() for p in processes]



















class AlignCore():
    pass
