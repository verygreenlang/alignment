import os, json
import camelot.io as camelot
from tika import parser
import PyPDF2
from tqdm import tqdm
from src.sourcing.wiki import CountriesWikidata
from src.sourcing.wiki import CO2WIKIDATA
from src.tools.caching import JsonCachingHandler
class PdfExtractor:
    def __init__(self,path):
        self.sep_page_str = "\n___page_sep___\n"
        self.path = path
        self.pdf_files = [path + os.sep + el for el in os.listdir(path) if ".pdf" in el  ]
        self.pdf_files = [el for el in self.pdf_files if os.path.isfile(el)]

        self.index_by_keywords = dict()
        self.index_by_keywords["country"] = dict()
        self.index_by_keywords["co2"] = dict()
        self.index_by_keywords["isin"] = dict()

        self.text_files = [ document+"-dir" + "/text.txt" for document in self.pdf_files ]

    def get(self):
        try:
            self.create_folder()
            self.extract_text()
            self.extract_tables()
            self.index()
        except Exception as e :
            print("error  - ", e)

    def extract_text(self):
        for document in self.pdf_files:
            csv_path = document+"-dir" + "/text.txt"
            text = ""
            with open( document, 'rb') as f :
                pdfReader = PyPDF2.PdfFileReader(f)
                for page in range(pdfReader.getNumPages()):
                    try:
                        pagehandle = pdfReader.getPage(page)
                        new_text = pagehandle.extractText()
                        text += new_text+ self.sep_page_str
                    except Exception as e:
                        print(e,"page skipped")
                        text += new_text+ self.sep_page_str
            with open(csv_path, "w") as f:
                f.write(text)

    def extract_tables(self):
        for document in self.pdf_files:
            data_store_path =  document+"-dir"
            tables = camelot.read_pdf(document)
            with open( document, 'rb') as f :
                pdfReader = PyPDF2.PdfFileReader(f)
                page_count = pdfReader.getNumPages()
            for i in range(page_count):
                try:
                    tables = camelot.read_pdf(document,pages = str(i), flavor = 'stream')
                    tables.export(data_store_path + "/"+str(i)+'.csv', f='csv')
                except Exception as e:
                    print(e)


    def index(self):
        self.index_by_isin()
        self.index_by_country()
        self.index_by_esg()
        self.index_by_industry()
        self.store_index_by_keywords()

    def index_by_isin(self):
        isin = self.path.split("/")[-1]
        for file in self.text_files:
            if file not in self.index_by_keywords["isin"].keys():
                self.index_by_keywords["isin"][file] = dict()
            if isin not in self.index_by_keywords["isin"][file].keys():
                self.index_by_keywords["isin"][file][isin] = []
            with open(file, "r") as f:
                content = f.read().upper()
            content_by_pages = content.split(self.sep_page_str)
            for i in range(len(content_by_pages)):
                if isin.upper() in content_by_pages[i]:
                    self.index_by_keywords["isin"][file][isin].append(i)

    def index_by_country(self):
        countries = CountriesWikidata().get()
        countries.append("russia")
        for file in self.text_files:
            if file not in self.index_by_keywords["country"].keys():
                self.index_by_keywords["country"][file] = dict()
            with open(file, "r") as f:
                content = f.read().upper()
            content_by_pages = content.split(self.sep_page_str)
            for country in countries :
                if country.upper() not in self.index_by_keywords["country"][file].keys():
                    self.index_by_keywords["country"][file][country.upper()] = []

                for i in range(len(content_by_pages)):
                    if country.upper() in content_by_pages[i]:
                        self.index_by_keywords["country"][file][country.upper()].append(i)

    def index_by_esg(self):
        co2 = CO2WIKIDATA().get()
        for file in self.text_files:
            if file not in self.index_by_keywords["co2"].keys():
                self.index_by_keywords["co2"][file] = dict()
            with open(file, "r") as f:
                content = f.read().upper()
            content_by_pages = content.split(self.sep_page_str)

            for key in co2 :
                if key.upper() not in self.index_by_keywords["co2"][file].keys():
                    self.index_by_keywords["co2"][file][key.upper()] = []

                for i in range(len(content_by_pages)):
                    if key.upper() in content_by_pages[i]:
                        self.index_by_keywords["co2"][file][key.upper()].append(i)

    def index_by_industry(self):
        pass

    def extract_lines(self):
        pass

    def store_index_by_keywords(self):
        filename = self.path + "/index_by_keywords.json"
        data = self.index_by_keywords
        JsonCachingHandler(filename).store(data)
        # with open(self.path + "/index_by_keywords.json","w") as f:
        #     json.dump(self.index_by_keywords,f)
    def create_folder(self):
        for el in self.pdf_files:
            os.system("mkdir -p " + el + "-dir")
