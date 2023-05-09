import os, sys
from setuptools import find_packages, setup, Command
from src.tools.caching import JsonCachingHandler
from src.tools.caching  import PickleCachingHandler


from src.tools.logger import FingreenLogger
logger = FingreenLogger().logger

from src.sourcing.corporate.sustainability_reports.search import SearchSustainabilityReport
from src.sourcing.wiki import SearchWIKIDATA
from src.sourcing.wiki import SearchWikirate

from src.sourcing.government.sec import SearchSEC
from src.sourcing.government.insee import SearchINSEE
from src.sourcing.government.glei import SearchGLEI


class AlignCommand(Command):
    """Support setup.py align."""

    description = 'align data'
    user_options = [
        ('company=', 'c', 'company'),

    ]

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        self.company = "Apple"

    def finalize_options(self):
        pass

    def run(self):
        output_path = self.get_output_data_path()
        output_dir = output_path + os.sep + self.company.replace(" ","_")
        # print(output_dir)
        os.system("mkdir -p " + output_dir)
        output_file = output_dir + os.sep + "all.pkl"
        print("output_file",output_file)
        cache = PickleCachingHandler(output_file).get()
        if True or  cache is None :
            full_data = dict()
            full_data["corporate"] = self.search_corporate()
            full_data["wikirate"] = self.search_wikirate()
            full_data["wikidata"] = self.search_wikidata()
            full_data["government"] = self.search_gov()
            # full_data["asset_manager"] = self.search_in_am()
            PickleCachingHandler(output_file).store(full_data)

    def search_corporate(self):
        data_path = self.get_data_path()
        # working_path = data_path
        working_path = os.path.join(data_path,"corporate","sustainability")
        logger.info("Search: sustainability reports")
        return SearchSustainabilityReport(working_path).get(company_name = self.company)

    def search_wikirate(self):
        data_path = self.get_data_path()
        working_path = os.path.join(data_path,"wikirate","company")
        logger.info("Search: Wikirate")
        return SearchWikirate(working_path).get(company_name = self.company)

    def search_wikidata(self):

        logger.info("Search: Wikidata")
        data_path = self.get_data_path()
        working_path = os.path.join(data_path,"wikidata")
        return SearchWIKIDATA(working_path).get(company_name = self.company)

    def search_gov(self):
        gov_data = dict()
        data_path = self.get_data_path()

        logger.info("Search: Gov-SEC")
        working_path = os.path.join(data_path,"government","sec")
        gov_data["sec"] =  SearchSEC(data_path).get(company_name = self.company)

        logger.info("Search: Insee")
        working_path = os.path.join(data_path,"government","insee")
        gov_data["sec"] =  SearchINSEE(working_path).get(company_name = self.company)

        logger.info("Search: glei")
        working_path = os.path.join(data_path,"government","glei")
        gov_data["glei"] =  SearchGLEI(working_path).get(company_name = self.company)

        return gov_data

    def search_in_am(self):

        logger.info("Search: Asset managers")
        data_path = self.get_data_path()

        working_path = os.path.join(data_path,"corporate","sustainability")

    def get_data_path(self):
        # here = "/".join(os.path.abspath(os.path.dirname(__file__)).split("/")[:-1])
        # data_path = os.path.join(here, 'data')
        # os.system("mkdir -p " + data_path)
        data_path = "/media/famat/windows/fingreen-ai/alignment/data/"
                # return data_path
        return data_path

    def get_output_data_path(self):
        pass
        data_path = self.get_data_path()
        # here = "/".join(os.path.abspath(os.path.dirname(__file__)).split("/")[:-1])
        data_path = os.path.join(data_path,"alignment")
        os.system("mkdir -p " + data_path)
        return data_path

    # def run(self):
    #     processes = []
    #     processes.append(mp.Process(target=self.get_corporate)) #,args=(data_path)))
    #     processes.append(mp.Process(target=self.get_wikirate)) #,args=(data_path)))
    #     processes.append(mp.Process(target=self.get_wikidata))
    #     processes.append(mp.Process(target=self.get_gov)) #,args=(data_path)))
    #     processes.append(mp.Process(target=self.get_am))
    #     [x.start() for x in processes]
    #     [p.join() for p in processes]
