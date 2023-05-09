import configparser
import os
import pickle
from wikirate4py import API, models
from src.tools.caching import PickleCachingHandler


class MetricsWikirate:
    def __init__(self, data_path):
        config = configparser.ConfigParser()
        config.read("config.ini")
        api_key = config["wikirate"]["api_key"]
        self.api = API(api_key)
        self.wikirate_path = data_path + os.sep + "wikirate"
        self.wikirate_metric_path = self.wikirate_path + "/metrics"
        os.system("mkdir -p " + self.wikirate_metric_path)
        self.wikirate_metric_file = self.wikirate_metric_path + os.sep + "all.pkl"

    def get(self):
        cache = self.get_from_cache()
        if cache:
            return cache

        print("getting from api")
        content = self.get_from_api()
        self.store_cache(content)
        return content
        # if cache is not  None:
        #     return cache
        # else:
        #     content = self.get_from_api()
        #     self.store_cache(content)
        #     return content

    def get_from_cache(self):
        return PickleCachingHandler(self.wikirate_metric_file).get()
        # if os.path.isfile(self.wikirate_metric_file):
        #     with open(self.wikirate_metric_file,"rb") as f:
        #         return pickle.load(f)
        # return None

    def store_cache(self, content):
        PickleCachingHandler(self.wikirate_metric_file).store(content)
        # print(self.wikirate_metric_file)
        # with open(self.wikirate_metric_file,"wb") as f:
        #     pickle.dump(content,f)

    def get_from_api(self):
        metrics_total = []
        offset = 0
        limit = 20
        hard_limit = 5000
        while offset < hard_limit:
            try:
                new_metrics = self.api.get_metrics(offset=offset, limit=limit)
                for new_metric in new_metrics:
                    metrics_total.append(new_metric)
                offset += limit
            except Exception as e:
                print("metrics download wikirate", e)
                return metrics_total
            self.store_cache(metrics_total)
            with open(
                self.wikirate_metric_file.replace(".pkl", str(offset) + "_.pkl"), "wb"
            ) as f:
                pickle.dump(metrics_total, f)
