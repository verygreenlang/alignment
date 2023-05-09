import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import configparser
import boto3
from botocore.exceptions import ClientError

from src.tools.logger import FingreenLogger
logger = FingreenLogger().logger
class DataAcademia:
    def __init__(self,data_path):
        self.data_path = data_path
        self.academia_path = data_path + os.sep + "academia"
        self.configObj = configparser.ConfigParser()
        self.configObj.read("config.ini")
        self.use_aws = self.configObj.getboolean("aws", "use")
        os.system("mkdir -p " + self.academia_path)

    def get(self):
        self.get_data_aminer()

    def get_data_aminer(self):
        self.get_data_aminer_citation()
        self.get_data_aminer_collaboration()
        self.get_data_aminer_socialtieacross()
        self.get_data_aminer_soinf()
        self.get_data_aminer_kernelcommunity()
        self.get_data_aminer_knowledge_graph()
        self.get_data_aminer_dynamic_coauthor()
        self.get_data_aminer_arnetminer()
        self.get_data_aminer_panther()
        self.get_data_aminer_disambiguation()
        self.get_data_aminer_open_academic_graph()
        self.get_data_aminer_scikg()
        self.get_data_aminer_knowledge_graph()
        url = "https://www.aminer.org/data/"


    def get_data_aminer_citation(self):
        logger.info("Getting aminer citation data")
        url ="https://www.aminer.org/citation"
        urls = self.get_links_from_url(url)
        data_path = self.academia_path + os.sep + "aminer" + os.sep + "citation" + os.sep
        os.system("mkdir -p " + data_path)
        for new_url in urls:
            self.download_files(new_url,data_path)


    def get_data_aminer_socialtieacross(self):
        logger.info("Getting aminer socialtieacross data")
        url = "https://www.aminer.org/socialtieacross"
        urls = self.get_links_from_url(url)
        data_path = self.academia_path + os.sep + "aminer" + os.sep + "socialtieacross" + os.sep
        os.system("mkdir -p " + data_path)
        for new_url in urls:
            self.download_files(new_url,data_path)


    def get_data_aminer_soinf(self):
        logger.info("Getting aminer soinf data")
        url = "https://lfs.aminer.cn/lab-datasets/soinf/"
        urls = self.get_links_from_url(url)
        data_path = self.academia_path + os.sep + "aminer" + os.sep + "soinf" + os.sep
        os.system("mkdir -p " + data_path)
        for new_url in urls:
            self.download_files(new_url,data_path)

    def get_data_aminer_collaboration(self):
        logger.info("Getting aminer collaboration data")
        url = "https://www.aminer.cn/collaboration"
        urls = self.get_links_from_url(url)
        data_path = self.academia_path + os.sep + "aminer" + os.sep + "collaboration" + os.sep
        os.system("mkdir -p " + data_path)
        for new_url in urls:
            self.download_files(new_url,data_path)


    def get_data_aminer_kernelcommunity(self):
        logger.info("Getting aminer kernelcommunity data")
        url = "https://www.aminer.cn/kernelcommunity"
        urls = self.get_links_from_url(url)
        data_path = self.academia_path + os.sep + "aminer" + os.sep + "kernelcommunity" + os.sep
        os.system("mkdir -p " + data_path)
        for new_url in urls:
            self.download_files(new_url,data_path)

    def get_data_aminer_dynamic_coauthor(self):
        logger.info("Getting aminer dynamic_coauthor data")
        url = "https://www.aminer.cn/dynamic_coauthor"
        urls = self.get_links_from_url(url)
        data_path = self.academia_path + os.sep + "aminer" + os.sep + "dynamic_coauthor" + os.sep
        os.system("mkdir -p " + data_path)
        for new_url in urls:
            self.download_files(new_url,data_path)

    def get_data_aminer_arnetminer(self):
        logger.info("Getting aminer arnetminer data")
        url = "https://www.aminer.cn/arnetminer"
        urls = self.get_links_from_url(url)
        data_path = self.academia_path + os.sep + "aminer" + os.sep + "arnetminer" + os.sep
        os.system("mkdir -p " + data_path)
        for new_url in urls:
            self.download_files(new_url,data_path)

    def get_data_aminer_panther(self):
        logger.info("Getting aminer panther data")
        url = "https://www.aminer.cn/panther"
        urls = self.get_links_from_url(url)
        data_path = self.academia_path + os.sep + "aminer" + os.sep + "panther" + os.sep
        os.system("mkdir -p " + data_path)
        for new_url in urls:
            self.download_files(new_url,data_path)
    def get_data_aminer_disambiguation(self):
        logger.info("Getting aminer disambiguation data")
        url = "https://www.aminer.cn/disambiguation"
        urls = self.get_links_from_url(url)
        data_path = self.academia_path + os.sep + "aminer" + os.sep + "disambiguation" + os.sep
        os.system("mkdir -p " + data_path)
        for new_url in urls:
            self.download_files(new_url,data_path)
    def get_data_aminer_open_academic_graph(self):
        logger.info("Getting aminer open-academic-graph data")
        url = "https://www.aminer.cn/open-academic-graph"
        urls = self.get_links_from_url(url)
        data_path = self.academia_path + os.sep + "aminer" + os.sep + "open-academic-graph" + os.sep
        os.system("mkdir -p " + data_path)
        for new_url in urls:
            self.download_files(new_url,data_path)
    def get_data_aminer_scikg(self):
        logger.info("Getting aminer scikg data")
        url = "https://www.aminer.cn/scikg"
        urls = self.get_links_from_url(url)
        data_path = self.academia_path + os.sep + "aminer" + os.sep + "scikg" + os.sep
        os.system("mkdir -p " + data_path)
        for new_url in urls:
            self.download_files(new_url,data_path)

    def get_data_aminer_knowledge_graph(self):
        logger.info("Getting aminer knowledge_graph data")
        url = "https://www.aminer.cn/knowledge_graph"
        urls = self.get_links_from_url(url)
        data_path = self.academia_path + os.sep + "aminer" + os.sep + "knowledge_graph" + os.sep
        os.system("mkdir -p " + data_path)
        for new_url in urls:
            self.download_files(new_url,data_path)

    def get_links_from_url(self,link):
        total_links = []
        parser = 'html.parser'
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.get(link)
        soup =  BeautifulSoup(driver.page_source, parser)
        for l in soup.find_all('a', href=True):
            new_url = l['href']
            if self.get_data_link(new_url):
                total_links.append(new_url)
        return total_links


    def get_data_link(self,link):
        if "http" not in link: return False
        filename = link.split("/")[-1]
        extensions = [".zip",".rar",".gz",".tar",".json",".pdf",".bz2",".tar",".tgz",".ppt"]
        for ext in extensions :
            if ext in filename :
                return True
        return False


    def download_files(self,url,data_path):
        filename = url.split("/")[-1]
        cmd = "wget " + url + " -O " + data_path + filename
        if not os.path.isfile(data_path+filename):
            logger.info(cmd)
            os.system(cmd)
        if os.path.isfile(data_path+filename) and self.use_aws :
            path_to_file = data_path + filename
            bucket = self.configObj["aws"]["aws_bucket_name"]
            s3 = boto3.client('s3',
                              aws_access_key_id=self.configObj["aws"]["aws_access_key_id"],
                              aws_secret_access_key=self.configObj["aws"]["aws_secret_access_key"],
                              )
            try:
                s3.head_object(Bucket=bucket, Key=path_to_file)
            except ClientError:
                logger.info("uploading academia data to s3")
                s3.upload_file(path_to_file,bucket,path_to_file)
                logger.info("done: academia data to s3")
