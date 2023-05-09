from src.tools.caching import JsonCachingHandler
from src.sourcing.wiki import CompanyWikidata
from src.sourcing.wiki import IndustriesWikidata
from src.sourcing.wiki import ProductWikidata
from src.sourcing.wiki import PeopleWikidata

import os


class CompanyTopics:
    def __init__(self, data_path):
        self.data_path = data_path
        self.topic_path = self.data_path + os.sep + "topics"
        os.system("mkdir -p " + self.topic_path)

    def get(self, company_name=None):
        if company_name is None:
            return
        topic_path = (
            self.topic_path
            + os.sep
            + company_name.replace(" ", "_")
            + os.sep
            + "all.json"
        )
        os.system(
            "mkdir -p "
            + self.topic_path
            + os.sep
            + company_name.replace(" ", "_")
            + os.sep
        )
        cache = JsonCachingHandler(topic_path).get()
        if cache is None:
            industry_topics = []
            company_topics = []
            product_topics = []
            people_topics = []
            wikidata_company_ids = CompanyWikidata(self.data_path).get_entity_by_name(
                company_name=company_name
            )
            for company_id in wikidata_company_ids:
                for topicIndus in IndustriesWikidata().get(company_wikid=company_id):
                    industry_topics.append(topicIndus)
                # 3 get company product topics
                for topicProduct in ProductWikidata().get(company_wikid=company_id):
                    product_topics.append(topicProduct)
                for topicPeople in PeopleWikidata().get(company_wikid=company_id):
                    people_topics.append(topicPeople)
            topics = {}
            topics["industry"] = industry_topics
            topics["product"] = product_topics
            topics["people"] = people_topics
            topics["company_topics"] = company_topics
            JsonCachingHandler(topic_path).store(topics)
            return topics
        else:
            return cache
