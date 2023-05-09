import os
import string
import requests
import time
import pickle

from bs4 import BeautifulSoup
from tqdm import tqdm
from src.tools.logger import FingreenLogger
logger = FingreenLogger().logger
from src.tools.caching import PickleCachingHandler
from src.tools.caching import  PdfCachingHandler

class IndexSustainabilityReport:
    def __init__(self,data_path):
        self.sustainability_report_path = data_path +os.sep + "corporate" + os.sep +"sustainability"
        os.system("mkdir -p " + self.sustainability_report_path)
        self.base_url = "https://www.responsibilityreports.com/"

    def get(self):
        total_files = []
        companies_url = list(set(self.get_companies()))
        for url in tqdm(companies_url,desc="Downloading sustainability reports"):
            total_files.append(self.get_hosted_data_from_companies_url(url))
        return total_files

    def get_companies(self):
        companies = []
        cache = PickleCachingHandler(self.sustainability_report_path +os.sep + "company_index.pkl").get()
        if cache is not None : return cache
        # if os.path.isfile(self.sustainability_report_path + "/" + "index_companies.pkl"):
        #     with open(self.sustainability_report_path + "/" + "index_companies.pkl",'rb') as f:
        #         return pickle.load(f)
        letters = self.get_all_letter_index()
        for letter in tqdm(letters,desc="Downloading sustainability reports Index"):
            time.sleep(0.2)
            req = requests.get(self.base_url + "Companies?a=" + letters[0])
            html_doc = req.content.decode("utf8")
            soup = BeautifulSoup(html_doc, 'html.parser')
            for el in soup.find_all("a") :
                href = el["href"]
                if "Company" in href:
                    companies.append(self.base_url + href)
        PickleCachingHandler(self.sustainability_report_path+os.sep + "company_index.pkl").store(companies)
        # with open(self.sustainability_report_path + "/" + "index_companies.pkl","wb") as f:
        #     pickle.dump(companies,f)
        return companies

    def get_hosted_data_from_companies_url(self, company):
        files = []
        req = requests.get(company)
        clean_company = company.split("/")[-1]
        html_doc = req.content.decode("utf8")
        soup = BeautifulSoup(html_doc, 'html.parser')
        output_dir = self.sustainability_report_path + os.sep +clean_company
        if os.path.isdir(output_dir): return
        os.system("mkdir -p "+ output_dir)
        logger.info("Getting data for company," + company)
        for el in soup.find_all("a") :
            try:
                href = el["href"]
                file = href.split("/")[-1]
                filename = output_dir  + os.sep +  file
                files.append(filename)
                if "HostedData" in href:
                    PCH = PdfCachingHandler(filename)
                    cache = PCH.get()
                    if cache is None:
                        response = requests.get(self.base_url + href)
                        PCH.store(response.content)
                    # if not os.path.isfile(filename):
                        time.sleep(0.2)
                        # response = requests.get(self.base_url + href)
                        # with open(filename, "wb") as file :
                        #     file.write(response.content)
            except Exception as e:
                print(e)
        return files

    def get_all_letter_index(self):
        letters = ["#"]
        for e in string.ascii_lowercase:
            letters.append(e.upper())
        return letters
