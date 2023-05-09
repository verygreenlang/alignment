import os
from src.tools.caching import PickleCachingHandler

from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner

from .get_all.get_all.spiders.getall import GetAllSpider
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

# import multiprocessing as mp


class DataWebscrapperCorpo:
    def __init__(self, data_path):
        self.data_path = data_path
        self.web_data_path = (
            data_path + os.sep + "corporate" + os.sep + "WebscrapperCorpo"
        )
        os.system("mkdir -p " + self.web_data_path)
        # self.runner = CrawlerProcess(get_project_settings())
        # self.runner = CrawlerRunner(get_project_settings())
        # self.runner = CrawlerProcess(get_project_settings())

    def get(self, company_url):
        self.company_url = company_url
        domain = (
            company_url.replace("http://", "").replace("https://", "").split("/")[0]
        )
        output_path = self.web_data_path + os.sep + domain
        #print(output_path)
        if not os.path.isdir(output_path):
            os.system("mkdir -p " + output_path)
            os.system(
                "python src/sourcing/corporate/webscrapper_corpo/launch.py -c"
                + company_url
                + " "
                + "-o "
                + output_path
            )  # + "> /dev/null 2>&1")
        # https://famat.me -o data " + )

        # runner = CrawlerRunner(get_project_settings())
        # self.runner.crawl(GetAllSpider,start_urls=[company_url],
        # allowed_domains=[domain],
        # output_path = self.web_data_path)
        # self.runner.start()
        # d = self.runner.crawl(GetAllSpider)#,start_urls=[company_url],allowed_domains=[domain],output_path = "data/")
        # d.addBoth(lambda _: reactor.stop())
        # processes = []
        # processes.append(mp.Process(target=self.execute_spider)) #,args=(data_path)))
        # [x.start() for x in processes]
        # [p.join() for p in processes]

    def execute_spider(self):
        # reactor.run()
        pass
        # runner.start()

        # d.addBoth(lambda _: reactor.stop())
        # reactor.run()
        # reactor.stop()
