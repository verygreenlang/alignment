import os
from src.sourcing.wiki import CompanyWikidata
from .data import DataWebscrapperCorpo
from src.tools.logger import FingreenLogger
logger = FingreenLogger().logger

class IndexWebscrapperCorpo:
    def __init__(self,data_path):
        self.data_path = data_path
        self.web_data_path = data_path +os.sep + "corporate" + os.sep +"WebscrapperCorpo"
        os.system("mkdir -p " + self.web_data_path)
        self.wikiName = CompanyWikidata( self.data_path)

    def get_all(self):
        company_wikidata_names = self.wikiName.get_all()
        for company_name in company_wikidata_names:
            self.get(company_name = company_name)

    def get(self,company_name = None):
        if company_name is None : return
        logger.info("company_name "+str(company_name))
        url_candidates = self.get_index_from_wikidata(company_name)
        logger.info("url_candidates "+str(url_candidates))
        data_web_scrapper = DataWebscrapperCorpo(self.data_path)
        for url in url_candidates:
            logger.info("scraping url: "+ str(url))
            data_web_scrapper.get(url)

        # data_web_scrapper.execute_spider()

    def get_index_from_wikidata(self,company_name):
        data = self.wikiName.get(company_name)
        #print(data)
        # logger.info("wikidata_data "+str(data))
        url_candidates = []
        for candidate in data :
            candidate_df = data[candidate]
            url_prop =  "http://www.wikidata.org/prop/direct/P856"
            new_url_candidates = candidate_df[candidate_df["b.value"] == url_prop]["c.value"].unique()
            if len(new_url_candidates) > 0 :
                for new_url in new_url_candidates:
                    url_candidates.append(new_url)
            # new_url = candidate_df[candidate_df["b.value"] ==url_prop]["c.value"].unique()[0]
        logger.info(url_candidates)

        return url_candidates
