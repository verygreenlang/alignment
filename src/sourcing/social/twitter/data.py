import os
import tweepy
import configparser
from datetime import datetime
from src.tools.caching import PickleCachingHandler
from src.sourcing.topics.by_company.data import CompanyTopics


class DataTwitter:
    def __init__(self, data_path):
        self.data_path = data_path

        self.twitter_path = data_path + os.sep + "social" + os.sep + "twitter"

        os.system("mkdir -p " + self.twitter_path)

    def get(self, company_name=None):
        if company_name is None:
            return None
        date = datetime.today().strftime("%d-%m-%Y")
        company_name_no_space = company_name.replace(" ", "")
        self.company_twitter_path = (
            self.twitter_path + os.sep + company_name_no_space + os.sep + date
        )
        os.system("mkdir -p " + self.company_twitter_path)
        topics = CompanyTopics(self.data_path).get(company_name=company_name)
        client = self.get_twitter_object()
        full_data = []
        for topic in self.get_all_topics_in_one_array(topics):
            filename = self.company_twitter_path + os.sep + topic + ".pkl"
            query = topic
            tweets = client.search_recent_tweets(
                query=query,
                tweet_fields=["context_annotations", "created_at"],
                max_results=100,
            )
            topic_data = []

            for tweet in tweets.data:
                data_to_store = dict()
                for key in tweet.keys():
                    data_to_store[key] = tweet[key]

                topic_data.append(data_to_store)
            PickleCachingHandler(filename).store(topic_data)
            full_data.append(topic_data)
        return full_data

    def get_twitter_object(self):
        config = configparser.ConfigParser(interpolation=None)
        config.read("config.ini")
        bt = config["twitter"]["bearer_token"]
        client = tweepy.Client(bearer_token=bt)

        return client

    def get_all_topics_in_one_array(self, topics):
        topics_raw = []
        for el in topics["industry"]:
            topics_raw.append(el)
        for el in topics["product"]:
            topics_raw.append(el)
        return topics_raw
