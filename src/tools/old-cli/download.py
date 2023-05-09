import os, sys
from src.tools.logger import FingreenLogger
logger = FingreenLogger().logger

from setuptools import find_packages, setup, Command
from shutil import rmtree
from src.sourcing.asset_manager.asset_manager import AssetManagerData

from src.sourcing.government.sec.data import DataSEC
from src.sourcing.government.insee.index import IndexINSEE
from src.sourcing.government.glei.index import IndexGLEI

from src.sourcing.wiki import CompanyWikirate
from src.sourcing.wiki import CompanyWikidata, RssLinksWikidata
from src.sourcing.topics.by_company.data import CompanyTopics

from src.sourcing.social.reddit.data import DataReddit
from src.sourcing.social.twitter.data import DataTwitter

from src.sourcing.github.rssfeeds.data import GithubRssFeeds
from src.sourcing.news.rssfeeds.data import RssFeedsNews
from src.sourcing.corporate.sustainability_reports.index import IndexSustainabilityReport
from src.sourcing.corporate import IndexWebscrapperCorpo

from src.sourcing.academia import DataAcademia


import multiprocessing as mp


import configparser




class DownloadCommand(Command):
    """Support setup.py download."""

    description = 'Download data'
    user_options = [
        ('data=', 'i', 'data type'),
        ('company=', 'c', 'company'),

    ]

    def initialize_options(self):
        self.data = None
        self.company = None #"Apple"

    def finalize_options(self):
        pass

    def get_corporate(self):
        if self.company is None :
            logger.info("Dl: sustainability reports")
            IndexSustainabilityReport(self.get_data_path()).get()
            logger.info("Done: sustainability reports")

            logger.info("Dl: web scrapping")
            IndexWebscrapperCorpo(self.get_data_path()).get_all()
            logger.info("Done: web scrapping")

        else:
            logger.info("Dl: web scrapping for :" + str(self.company))
            IndexWebscrapperCorpo(self.get_data_path()).get(company_name=self.company)
            logger.info("Done: web scrapping")

    def get_wikirate(self):
        if self.company is not None :
            logger.info("Dl: Wikirate")
            CompanyWikirate(self.get_data_path()).get(company_name=self.company)
            logger.info("Done: Wikirate")
        else:
            logger.info("Dl: Wikirate")
            CompanyWikirate(self.get_data_path()).get_all_companies()
            logger.info("Done: Wikirate")
            
    def get_wikidata(self):
        if self.company is not None :
            logger.info("Dl: Wikidata")
            CompanyWikidata(self.get_data_path()).get(company_name=self.company)
            logger.info("Done: Wikidata")
        else:
            logger.info("Dl: Wikidata")
            RssLinksWikidata(self.get_data_path()).get()
            logger.info("Done: Wikidata")

    def get_social(self):
        logger.info("Dl: social")
        if self.company is not None :
            DataReddit(self.get_data_path()).get(company_name=self.company)
            DataTwitter(self.get_data_path()).get(company_name=self.company)
        logger.info("Dl: end-social")

    def get_github(self):
        if self.company is  None :
            logger.info("Dl: github")

            GithubRssFeeds(self.get_data_path()).get()
            logger.info("Done: github")

    def get_news(self):
        if self.company is None :
            logger.info("DL: news")
            RssFeedsNews(self.get_data_path()).get()
            logger.info("Done: news")
    def get_topics(self):
        logger.info("Dl: topics")

        if self.company is not None :
            CompanyTopics(self.get_data_path()).get(company_name=self.company)
            #0 get company wikidata id
            # industry_topics = []
            # company_topics = []
            # product_topics = []
            #
            # wikidata_company_ids = CompanyWikidata(self.get_data_path()).get_entity_by_name(company_name=self.company)
            # for company_id in wikidata_company_ids:
            #     #2 get topics on company industry
            #     for topicIndus in  IndustriesWikidata.get(company_wikid=company_id):
            #         industry_topics.append(topicIndus)
            #     #3 get company product topics
            #     for topicProduct in ProductWikidata.get(company_wikid=company_id):
            #         product_topics.append(topicProduct)

        else:

            #1 get all industry (manual / wikidata )
            #2 get topic coverage
            #3 get new topics based on news
            #4 get esg topics from specific text + nlp

            pass
        logger.info("Done: Topics")
    def get_gov(self):
        if self.company is None :
            logger.info("Dl: Gov-SEC")
            DataSEC(self.get_data_path()).get(company_name=self.company)
            logger.info("Done: Gov-SEC")
        else:
            logger.info("Dl: Insee")
            IndexINSEE(self.get_data_path()).get(company_name=self.company)
            logger.info("Done: Insee")

            logger.info("Dl: glei")
            IndexGLEI(self.get_data_path()).get(company_name=self.company)
            logger.info("Done: glei")

    def get_am(self):
        if self.company is None :
            logger.info("Dl: Asset managers")
            AssetManagerData(self.get_data_path()).get()
            logger.info("Done: Asset managers")

    def get_academia(self):
        if self.company is None :
            logger.info("Dl: Academia")
            DataAcademia(self.get_data_path()).get()
            logger.info("Done:  Academia")
    def get_data_path(self):
        # here = "/".join(os.path.abspath(os.path.dirname(__file__)).split("/")[:-1])
        # data_path = os.path.join(here, 'data')
        # os.system("mkdir -p " + data_path)
        config = configparser.ConfigParser()
        config.read('config.ini')
        data_path =  config["data"]["path"]
        #TODO add option in config file
        # data_path = "/media/famat/windows/fingreen-ai/alignment/data/"
        return data_path
    def run(self):
        # create folder
        logger.info(self.get_data_path())
        processes = []
        config = configparser.ConfigParser()
        config.read('download_config.ini')
        sourcing_config =  config["sourcing"]
        if sourcing_config.getboolean("corporate"):
            processes.append(mp.Process(target=self.get_corporate))
        if sourcing_config.getboolean("social"):
            processes.append(mp.Process(target=self.get_social))
        if sourcing_config.getboolean("academia"):
            processes.append(mp.Process(target=self.get_academia))
        if sourcing_config.getboolean("asset_manager"):
            processes.append(mp.Process(target=self.get_am))
        if sourcing_config.getboolean("github"):
            processes.append(mp.Process(target=self.get_github))
        if sourcing_config.getboolean("wiki"):
             processes.append(mp.Process(target=self.get_wikirate))
             processes.append(mp.Process(target=self.get_wikidata))
        if sourcing_config.getboolean("news"):
            processes.append(mp.Process(target=self.get_news))
        if sourcing_config.getboolean("government"):
            processes.append(mp.Process(target=self.get_gov))
        if sourcing_config.getboolean("topics"):
            processes.append(mp.Process(target=self.get_topics))
        [x.start() for x in processes]
        [p.join() for p in processes]
