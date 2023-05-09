import os
import sys

import multiprocessing as mp
import configparser

from src.tools.logger import FingreenLogger


from setuptools import find_packages
from setuptools import setup
from setuptools import Command
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
from src.sourcing.corporate.sustainability_reports.index import (
    IndexSustainabilityReport,
)
from src.sourcing.corporate import IndexWebscrapperCorpo

from src.sourcing.academia import DataAcademia

from src.sourcing.news import NewsGraphs

logger = FingreenLogger().logger


class SourceCore:
    def __init__(self, asset, config, dconfig):
        self.asset = asset
        configObj = configparser.ConfigParser()
        configObj.read(config)
        self.config = configObj
        dconfigobj = configparser.ConfigParser()
        dconfigobj.read(dconfig)
        self.dconfig = dconfigobj
        self.classify_asset(asset)

    def get_academia(self):
        logger.info("DL: Academia")
        DataAcademia(self.get_data_path()).get()
        logger.info("Done: Academia")

    def get_am(self):
        logger.info("Dl: Asset managers")
        AssetManagerData(self.get_data_path()).get()
        logger.info("Done: Asset managers")

    def get_corporate(self):

        logger.info("Dl: web scrapping for :" + str(self.company))
        IndexWebscrapperCorpo(self.get_data_path()).get(company_name=self.company)
        logger.info("Done: web scrapping")

    def get_wikirate(self):
        logger.info("Dl: Wikirate")
        CompanyWikirate(self.get_data_path()).get(company_name=self.company)
        logger.info("Done: Wikirate")

    def get_wikidata(self):

        logger.info("Dl: Wikidata")
        RssLinksWikidata(self.get_data_path()).get()
        logger.info("Done: Wikidata")

    def get_social(self):
        logger.info("Dl: social")
        DataReddit(self.get_data_path()).get(company_name=self.company)
        DataTwitter(self.get_data_path()).get(company_name=self.company)
        logger.info("Dl: end-social")

    def get_github(self):
        if self.company is None:
            logger.info("Dl: github")

            GithubRssFeeds(self.get_data_path()).get()
            logger.info("Done: github")

    def get_news(self):
        logger.info("DL: news")
        RssFeedsNews(self.get_data_path()).get()
        logger.info("Done: news")

    def get_topics(self):
        logger.info("Dl: topics")
        CompanyTopics(self.get_data_path()).get(company_name=self.company)
        logger.info("Done: Topics")

    def get_gov(self):

        logger.info("Dl: Insee")
        IndexINSEE(self.get_data_path()).get(company_name=self.company)
        logger.info("Done: Insee")

        logger.info("Dl: glei")
        IndexGLEI(self.get_data_path()).get(company_name=self.company)
        logger.info("Done: glei")

        logger.info("Dl: Gov-SEC")
        DataSEC(self.get_data_path()).get(company_name=self.company)
        logger.info("Done: Gov-SEC")

    def render_graphs(self):
        pass
	    #self.render_topic_graphs()
	    #self.render_topic_graphs_from_config()

    def render_topic_graphs(self):
        topics = CompanyTopics(self.get_data_path()).get(company_name=self.company)
        with open(self.get_data_path() + "/esg_keywords.txt") as f:
            esg_topics = f.readlines()
        esg_topics = [e.strip() for e in esg_topics]
        esg_topics = [e.strip() for e in esg_topics if len(e) > 1]
        logger.info("GEN: industry graphs")

        NewsGraphs(
            self.get_data_path(),
            topics["industry"],
            esg_topics,
            company_name=self.company,
        ).generate()
        logger.info("GEN: products graphs")

        NewsGraphs(
            self.get_data_path(),
            topics["product"],
            esg_topics,
            company_name=self.company,
        ).generate()
        # NewsGraphs(self.get_data_path(), topics["product"],esg_topics).generate
        logger.info("GEN: people graphs")

        NewsGraphs(
            self.get_data_path(),
            topics["people"],
            esg_topics,
            company_name=self.company,
        ).generate()
        logger.info("GEN: company_topics graphs")

        NewsGraphs(
            self.get_data_path(),
            topics["company_topics"],
            esg_topics,
            company_name=self.company,
        ).generate()

    def render_topic_graphs_from_config(self):
        import json

        with open(self.get_data_path() + "/esg_keywords.txt") as f:
            esg_topics = f.readlines()
        esg_topics = [e.strip() for e in esg_topics]
        esg_topics = [e.strip() for e in esg_topics if len(e) > 1]
        logger.info("GEN: industry graphs")
        with open(self.get_data_path() + "/topics_keywords.json") as f:
            topics = json.load(f)
        NewsGraphs(
            self.get_data_path(),
            topics["industry"],
            esg_topics,
            company_name=self.company,
        ).generate()
        logger.info("GEN: products graphs")

        NewsGraphs(
            self.get_data_path(),
            topics["product"],
            esg_topics,
            company_name=self.company,
        ).generate()
        # NewsGraphs(self.get_data_path(), topics["product"],esg_topics).generate
        logger.info("GEN: people graphs")

        NewsGraphs(
            self.get_data_path(),
            topics["people"],
            esg_topics,
            company_name=self.company,
        ).generate()
        logger.info("GEN: company_topics graphs")

        NewsGraphs(
            self.get_data_path(),
            topics["company_topics"],
            esg_topics,
            company_name=self.company,
        ).generate()

    def render_esg_metrics_graphs(self):
        pass

    def get_data_path(self):
        if self.config.getboolean("aws","use"):
            return "fingreen"
        else:
            data_path = self.config["data"]["path"]
            return data_path

    def run(self):
        # create folder
        logger.info(self.get_data_path())
        processes = []
        sourcing_config = self.dconfig["sourcing"]
        if sourcing_config.getboolean("corporate"):
            processes.append(mp.Process(target=self.get_corporate))
        if sourcing_config.getboolean("academia"):
            processes.append(mp.Process(target=self.get_academia))
        if sourcing_config.getboolean("social"):
            processes.append(mp.Process(target=self.get_social))
        if sourcing_config.getboolean("wiki"):
            processes.append(mp.Process(target=self.get_wikirate))
            processes.append(mp.Process(target=self.get_wikidata))
        if sourcing_config.getboolean("news"):
            processes.append(mp.Process(target=self.get_news))
        if sourcing_config.getboolean("government"):
            processes.append(mp.Process(target=self.get_gov))
        if sourcing_config.getboolean("topics"):
            processes.append(mp.Process(target=self.get_topics))
        if sourcing_config.getboolean("asset_manager"):
            processes.append(mp.Process(target=self.get_am))
        [x.start() for x in processes]
        [p.join() for p in processes]
        logger.info("render_graphs")

        self.render_graphs()
        logger.info("thx bye")

    def classify_asset(self, asset):
        if self.mostly_integer(asset):
            self.fund = asset
        else:
            self.company = asset

    def mostly_integer(self, asset):
        count = 0
        for i in asset:
            if i.isdigit():
                count += 1
        if count > 4:
            return True
        return False
