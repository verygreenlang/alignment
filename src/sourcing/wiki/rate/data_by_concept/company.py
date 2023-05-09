import configparser
import os
import json
import pickle
from wikirate4py import API, models
from .metrics import MetricsWikirate
from src.tools.caching import PickleCachingHandler
from tqdm import tqdm


class CompanyWikirate:
    def __init__(self, data_path):
        config = configparser.ConfigParser()
        config.read("config.ini")
        api_key = config["wikirate"]["api_key"]
        self.api = API(api_key)
        self.metrics = MetricsWikirate(data_path).get()
        self.wikirate_path = data_path + os.sep + "wikirate"
        self.wikirate_company_path = self.wikirate_path + "/company"
        os.system("mkdir -p " + self.wikirate_company_path)
        # print("metrics", self.metrics)

    def get(self, company_name=None):
        self.company_name_path = (
            self.wikirate_company_path + os.sep + company_name.replace(" ", "_")
        )
        self.company_name_file = self.company_name_path + os.sep + "all.pkl"
        os.system("mkdir -p " + self.company_name_path)
        if self.get_from_cache() is None:
            metrics_values = {}
            company_ids = self.api.search_by_name(models.Company, name=company_name)
            for company_id in company_ids:
                metrics_values[company_id] = {}
                for id in self.metrics:
                    id_clean = id.raw_json().get("id")
                    company_id_clean = company_id.raw_json().get("id")
                    metrics_values[company_id][
                        id_clean
                    ] = self.api.get_answers_by_metric_id(
                        id_clean, company_id=company_id_clean
                    )
            self.store_cache(metrics_values)
            return metrics_values
        else:
            return self.get_from_cache()

    def get_all_companies(self):
        self.company_name_path = self.wikirate_company_path + os.sep + "all_companies"
        os.system("mkdir -p " + self.company_name_path)
        batch = 0
        for batch in tqdm(range(0, 6000), desc="company"):
            self.company_name_file = (
                self.company_name_path + os.sep + "all" + str(batch) + ".pkl"
            )
            if self.get_from_cache() is None:
                offset = batch * 20
                metrics_values = {}
                company_ids = self.api.get_companies(
                    offset=offset
                )  # self.api.search_by_name(models.Company,name=company_name)
                for company_id in company_ids:
                    metrics_values[company_id] = {}
                    for id in tqdm(self.metrics, desc=" metric "):
                        id_clean = id.raw_json().get("id")
                        company_id_clean = company_id.raw_json().get("id")
                        metrics_values[company_id][
                            id_clean
                        ] = self.api.get_answers_by_metric_id(
                            id_clean, company_id=company_id_clean
                        )
                self.store_cache(metrics_values)

    def store_cache(self, content):
        PickleCachingHandler(self.company_name_file).store(content)
        # # print(self.company_name_file)
        # with open(self.company_name_file,"wb") as f:
        #     pickle.dump(content,f)

    def get_from_cache(self):
        return PickleCachingHandler(self.company_name_file).get()
        # if os.path.isfile(self.company_name_file):
        #     with open(self.company_name_file,"rb") as f:
        #         return pickle.load(f)
        # return None
