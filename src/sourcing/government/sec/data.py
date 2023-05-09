from .index import IndexSEC
import os
import requests
import json
from tqdm import tqdm
import time
from src.sourcing.wiki import CikWikidata,CompanyWikidata
from src.tools.caching import JsonCachingHandler

from bs4 import BeautifulSoup
class DataSEC:

    def  __init__(self,data_path) :
        self.data_path = data_path
        self.index = IndexSEC(data_path).get()
        self.user_agent = "famat contact@famat.me"
        self.headers = {"User-Agent":self.user_agent}
        self.output_dir = os.path.join(self.data_path , "government", "sec","documents")
        os.system("mkdir -p " + self.output_dir)
    def get(self,company_name=None):
        #self.get_data_from_index()
        company_name = company_name.lower()
        ciks = []
        ciks.append(self.get_cik_from_edgar_index(company_name))
        for el in self.get_cik_from_partial_match_edgar_index(company_name):
            ciks.append(el)
        for el in self.get_cik_from_wikidata(company_name):
            ciks.append(el)
        for cik in tqdm( ciks,desc="Downloading gov sec docs"):
        # for cik in ciks:
            if cik is not None :
                self.get_data_from_cik(cik)
        return ciks

    def get_cik_from_edgar_index(self,company_name):
        if company_name in self.index["name_to_cik"]:
            company_cik = self.index["name_to_cik"].get(company_name)
            return company_cik

    def get_cik_from_partial_match_edgar_index(self,company_name):
        candidates = dict()
        for value in self.index["name_to_cik"].keys():
            if company_name in value :
                candidates[value] = self.index["name_to_cik"].get(value)
        return candidates.values()

    def get_cik_from_wikidata(self,company_name):
        wikidata_company_ids = CompanyWikidata(self.data_path).get_entity_by_name(company_name=company_name)
        ciks = []
        for company_wikid in wikidata_company_ids:
            cand = CikWikidata().get(company_wikid=company_wikid)
            if len(cand)> 0:
                ciks.append(cand[0])
        return ciks



    def get_data_from_cik(self,cik):
        #path = "https://www.sec.gov/Archives/edgar/data/" + cik
        #    ACCESSION_NUMBER_WITHOUT_DASHES>/<ACCESSION_NUMBER>
        total_hrefs = []
        for doc_path in  self.get_ACCESSION_NUMBER_WITHOUT_DASHES(cik):
            try:
                for final_doc in self.get_ACCESSION_NUMBER(cik,doc_path):
                    total_hrefs.append(final_doc)
            except Exception as e:
                print(e)

        # for url in tqdm( total_hrefs,desc="Downloading gov sec docs"):
        for url in total_hrefs:
            if ".htm" in url or ".txt" in url :
                time.sleep(0.5)
                self.download_file(url,self.output_dir,cik)

    def get_ACCESSION_NUMBER_WITHOUT_DASHES(self,cik):
        url = "https://www.sec.gov/Archives/edgar/data/" +cik
        time.sleep(0.5)
        data = requests.get(url,headers=self.headers).content.decode()
        soup = BeautifulSoup(data, 'html.parser')
        return soup.table.find_all("a")

    def get_ACCESSION_NUMBER(self,cik,anwd):
        # print(anwd.get('href'))
        url = "https://www.sec.gov/" + anwd.get('href')
        time.sleep(0.5)
        data = requests.get(url,headers=self.headers).content.decode()
        soup = BeautifulSoup(data, 'html.parser')
        hrefs = []
        for link in soup.table.find_all("a"):
            hrefs.append("https://www.sec.gov/" + link.get('href'))
        return hrefs

    def get_cik_bin(self,cik):
        cik_bins = range(0,10000000,1000000)
        for el in cik_bins:
            if int(cik) < el:
                return str(el)

    def download_file(self,url,path,cik):
        local_filename = url.split('/')[-1]
        if not os.path.isfile(local_filename):
            content = requests.get(url,headers=self.headers).content.decode()
            os.system("mkdir -p " + path + "/"+ cik + "/")
            with open(path + "/"+ cik + "/" + local_filename,"w") as f:
                f.write(content)

    def get_data_from_index(self):
        output_dir = os.path.join(self.data_path , "government", "sec","documents")
        # full_data = dict()
        data_path_index = os.path.join(self.data_path , "government", "sec","index_documents")
        documents = os.listdir(data_path_index)
        documents_full_path = [data_path_index + os.sep + el for el in documents ]
        for document in tqdm( documents_full_path,desc="Downloading gov sec docs"):
            with open(document,"r")  as f:
                content = f.readlines()
            for line in tqdm(content,desc="for each line in sec index file") :
                splitted = line.split("|")
                year = splitted[3].split("-")[0]
                cik = splitted[0]
                cik_bin = self.get_cik_bin(cik)
                os.system("mkdir -p " + output_dir + os.sep + year + os.sep + str(cik_bin))
                output_file =  output_dir + os.sep + year + os.sep + str(cik_bin) + os.sep + splitted[0].split("/")[-1] +".json"
                if not os.path.isfile(output_file):
                    new_data = dict()
                    new_data["cik"] = splitted[0]
                    new_data["date"] = splitted[3]
                    new_data["doc_type"] = splitted[2]
                    new_data["data_url_path"] ="https://www.sec.gov/Archives/"+ splitted[4]
                    time.sleep(0.3)
                    headers = {"User-Agent":self.user_agent}
                    new_data["data_url_content"] = requests.get(new_data["data_url_path"],headers=headers).content.decode("utf8")
                    os.system("mkdir -p " + output_dir + os.sep + year )
                    JsonCachingHandler(output_file).store(new_data)

        #         else:
        #             with open(output_file,'r') as f:
        #                 new_data = json.load(f)
        #
        #         if year not in full_data.keys() :
        #             full_data[year] = dict()
        #         if new_data["cik"] not in full_data[year].keys():
        #             full_data[year][new_data["cik"]] = dict()
        #         full_data[year][new_data["cik"]] = new_data
        #
        # with open( output_dir + os.sep + "all.pkl",'w') as f :
        #     json.dumps(full_data,f)
