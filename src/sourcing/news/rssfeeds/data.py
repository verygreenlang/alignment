# from src.tools.caching import PickleCachingHandler
from src.tools.caching import JsonCachingHandler
from src.sourcing.wiki import RssLinksWikidata
from src.sourcing.github.rssfeeds.data import GithubRssFeeds
from urllib.parse import urlparse
from src.tools.logger import FingreenLogger
logger = FingreenLogger().logger

import os
import datetime
import feedparser
class RssFeedsNews :
    def __init__(self,data_path):
        self.data_path= data_path
        self.news_path = data_path + os.sep + "news" + os.sep + "rssfeeds"
        os.system("mkdir -p " + self.news_path)

    def get(self) :
        self.get_rss_data_from_github()
        self.get_rss_data_from_wikidata()

    def get_rss_data_from_wikidata(self):
        path = self.news_path + os.sep + "wikidata"
        rss_links_wikidata = RssLinksWikidata(self.data_path).get()
        for link in rss_links_wikidata:
            new_path = path + os.sep + self.get_domain_from_url(link)
            os.system("mkdir -p " + new_path )
            filename = new_path + os.sep + datetime.datetime.today().strftime('%d-%m-%Y') + ".json"
            try:
                content = self.get_or_store_from_url(link,filename)
            except Exception as e :
                logger.error(e)

    def get_rss_data_from_github(self) :
        rss_links_github = GithubRssFeeds(self.data_path).get()
        path = self.news_path + os.sep + "github"
        for file in rss_links_github:
            annotation = file.get("annotation","no_annotation")
            for feed in file.get("data_links",[]):
                feed_url = feed["xmlurl"]
                new_path = path + os.sep + self.get_domain_from_url(feed_url)
                os.system("mkdir -p " + new_path )
                filename = new_path + os.sep + datetime.datetime.today().strftime('%d-%m-%Y') + ".json"
                try:
                    content = self.get_or_store_from_url(feed_url,filename)
                except Exception as e :
                    logger.error(e)

    def get_or_store_from_url(self,url,filename):
        logger.info("mining : " + url)
        logger.info("storing in: " + filename)
        PH = JsonCachingHandler(filename)
        cache = PH.get()
        if cache is not None : return cache
        content = self.get_content_rss(url)
        content = content.copy()
        JsonCachingHandler(filename).store(content)
        return content

    def get_content_rss(self,url):
        try:
            content = feedparser.parse(url)
            content = dict(content)
            return content
        except Exception as e :
            logger.error("error rss feed empty: " +  url  )
            logger.error(e)
        return dict()

    def get_domain_from_url(self,url):
        return urlparse(url ).netloc
