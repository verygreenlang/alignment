from src.tools.caching import PickleCachingHandler
from src.sourcing.wiki import RssLinksWikidata
from src.sourcing.github.rssfeeds.data import GithubRssFeeds

from .data import RssFeedsNews
from urllib.parse import urlparse

import os
import datetime
import feedparser

class SearchRssFeedsNews :
    def __init__(self,data_path):
        self.data_path= data_path


    def get(self,topic=None) :
        if topic is None : return
        self.news_indexed_path = self.data_path + os.sep + "news" + os.sep + topic.replace(" ","_")
        os.system("mkdir -p " + self.news_indexed_path)
        all_news_content = RssFeedsNews(self.data_path).get()

        
