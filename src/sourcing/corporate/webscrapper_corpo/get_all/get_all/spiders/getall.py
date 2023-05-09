from scrapy.spiders import CrawlSpider
from scrapy import Request
from urllib.parse import urljoin
import json
import os

import configparser
import boto3
from botocore.exceptions import ClientError
# from src.tools.caching import JsonCachingHandler


class GetAllSpider(CrawlSpider):
    name = "getall"
    scrapped_url = []
    start_urls = ["https://famat.me"]
    # allowed_domains = ["famat.me"]
    output_path = "../../../../../data/corporate/webscrapped/famat.me"

    def start_requests(self):
        # self.logger.info('A response from %s just arrived!' + str(self.start_urls))
        urls = self.start_urls
        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        self.logger.info("A response from %s just arrived!", response.url)
        # xpath_href = "a::attr(href)"
        # for link in  response.css('a::attr(href)'):
        xpath_href = "//a[@href]/@href"
        for link in response.xpath(xpath_href).getall():
            if "/" in link:
                url = response.urljoin(link)
                self.add_link(url)

                if link.endswith(".pdf"):
                    yield Request(url=url, callback=self.save_pdf)
                else:
                    yield Request(
                        url=url, callback=self.parse
                    )  # <-- This makes your spider recursiv crawl subsequent pages

    def add_link(self, link):
        self.scrapped_url.append(link)
        self.scrapped_url = list(set(self.scrapped_url))
        store_url = self.output_path + "/" + "url_index.json"
        if len(self.scrapped_url)%100 == 0 :
            JsonCachingHandler(store_url).store(self.scrapped_url)

    def save_pdf(self, response):
        configObj = configparser.ConfigParser()
        configObj.read("config.ini")
        use_aws = configObj.getboolean("aws", "use")
        path = response.url.split("/")[-1]
        with open(self.output_path + "/" + path, "wb") as f:
            f.write(response.body)
        if use_aws:
            path_to_file =path
            bucket = self.configObj["aws"]["aws_bucket_name"]
            s3 = boto3.client('s3',
                              aws_access_key_id=self.configObj["aws"]["aws_access_key_id"],
                              aws_secret_access_key=self.configObj["aws"]["aws_secret_access_key"],
                              )
            try:
                s3.head_object(Bucket=bucket, Key=path_to_file)
            except ClientError:
                s3.upload_file(path_to_file, bucket, path_to_file)



class JsonCachingHandler:
    def __init__(self,filename,config=None):
        if config is None :
            configObj = configparser.ConfigParser()
            configObj.read("config.ini")
            self.use_aws = configObj.getboolean("aws", "use")
        else:
            self.use_aws = config.getboolean("aws", "use")

        self.filename = filename
        if self.use_aws:
            session = boto3.Session(
                aws_access_key_id=configObj["aws"]["aws_access_key_id"],#'<your_access_key_id>',
                aws_secret_access_key=configObj["aws"]["aws_secret_access_key"]
            )

            s3 = session.resource('s3')
            self.aws_obj = s3.Object(configObj["aws"]["aws_bucket_name"],self.filename)

    def get(self,return_if_none=None):
        if not self.use_aws:
            if not os.path.isfile(self.filename):
                return return_if_none
            with open(self.filename,"rb") as f:
                return json.load(f)
        else:
            try:
                return json.loads(self.aws_obj.get()['Body'].read().decode('utf-8'))
            except ClientError as ex:
                return return_if_none
            return return_if_none

    def store(self,data):
        if not  self.use_aws:
            with open(self.filename,"w") as f:
                json.dump(data,f)
        else:
            self.aws_obj.put(Body=json.dumps(data))
