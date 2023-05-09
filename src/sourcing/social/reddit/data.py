import os
import praw
import configparser
from datetime import datetime
from src.tools.caching import PickleCachingHandler
from src.sourcing.topics.by_company.data import CompanyTopics

class DataReddit:
    def __init__(self,data_path):
        self.data_path = data_path
        self.reddit_path =  data_path + os.sep + "social" + os.sep + "reddit"
        os.system("mkdir -p " + self.reddit_path)
    def get(self,company_name=None):
        if company_name is None : return None
        filename = self.reddit_path + os.sep + datetime.today().strftime("%d-%m-%Y") + ".pkl"
        if PickleCachingHandler(filename).get() is not None :
            return PickleCachingHandler(filename).get()
        submission_total = []
        topics = CompanyTopics(self.data_path).get(company_name=company_name)
        reddit = self.get_reddit_object()
        topics_raw = []
        for el in topics["industry"]:
            topics_raw.append(el)
        for el in topics["product"]:
            topics_raw.append(el)
        query_topic = " OR ".join(topics_raw)
        for submission in reddit.subreddit("all").search(query_topic):
            submission_total.append(submission.__dict__)
            # submission.__dict__
            # print(submission.title)
            # print(submission.subreddit)
            # print( datetime.fromtimestamp(submission.created_utc))
            # print(submission.created_utc)

        return PickleCachingHandler(filename).store(submission_total)

    def get_reddit_object(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        ci =  config["reddit"]["client_id"]
        cs =  config["reddit"]["client_secret"]

        reddit = praw.Reddit(
            client_id=ci,
            client_secret=cs,
            user_agent="default-user-agent",
        )
        return reddit
