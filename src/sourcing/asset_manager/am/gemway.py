import os
import json
import time
import pickle
from tqdm import tqdm
from datetime import date
from selenium import webdriver
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

from src.tools.pdf import PdfExtractor
from src.tools.caching import PickleCachingHandler
from src.tools.logger import FingreenLogger
from src.tools.caching import PickleCachingHandler, FileCachingHandler, JsonCachingHandler

logger = FingreenLogger().logger


class GEMWAY:
    def __init__(self, data_path):
        self.wait_factor = 2
        self._url = "https://www.gemway.com/fr/gamme-fonds"
        self.data_path = data_path
        self.basename = "gemway"
        self._data = self.data_path + os.sep + "am/"+self.basename + os.sep
        self.link_templates = ["https://www.gemway.com/e/fr/docs/funds/gemequity/",
                            "/e/fr/docs/funds/"]
        self.new_driver()

    def get(self):
        links = self.get_links_index()
        for pdf_dir in self.get_data_for_each_link(links):
            PdfExtractor(pdf_dir).get()

    def get_links_index(self):
        links = self.get_links_from_cache()
        if len(links) > 0: return links
        self.driver.get(self._url)
        self.accept_cookies()
        logger.debug("accepting cookies")
        link_templates = self.link_templates
        links = self.get_all_links(link_templates)
        self.store_links(links)
        return links

    def get_data_for_each_link(self, links):
        pdf_path = []
        desc = "Downloading "+self.basename+" AM data for each link"
        for link in tqdm(links, desc=""):
            path_fund_data = self._data  + link[-1]
            os.system("mkdir -p " + path_fund_data)
            pdf_path.append(path_fund_data)
            path_fund_data_link = path_fund_data + os.sep + "index.json"
            if not os.path.isfile(path_fund_data_link):
                data = {"path_fund_data": path_fund_data,
                        "isin": None,
                        "url": link}
                data = self.get_data_from_link(data)
                with open(path_fund_data_link, "w") as f:
                    json.dump(data, f)
                for l in data["pdf_links"]:
                    if "blank" not in l:
                        os.system("wget -P " + path_fund_data + " " + l)
                        FileCachingHandler(path_fund_data).store(path_fund_data + l.split("/")[-1])

        return pdf_path
        # except Exception as e:
        #     print(e, "exception for isin:",isin)
        # except Exception as e:
        # print(e)

    def get_data_from_link(self, data):
        self.close_driver()
        self.new_driver(data_path=data["path_fund_data"])
        self.driver.get(data["url"])
        self.accept_cookies()
        today = date.today()
        data["date"] = today.strftime("%d_%m_%Y")
        data["info_fund"] = None #self.get_data_VL()
        data["pdf_links"] = self.get_documents()
        return data

    def get_documents(self):
        document_cdn = self.link_templates
        documents_links = self.get_all_links(filter=document_cdn)
        return documents_links

    def accept_cookies(self):
        driver = self.driver
        time.sleep(3 * self.wait_factor)
        if  len(driver.find_elements_by_xpath("//button[text()='en']")) > 0:
            driver.find_elements_by_xpath("//button[text()='en']")[0].click()
            driver.find_elements_by_xpath("//button[text()='Retail']")[0].click()
            d = driver.find_elements_by_xpath("//*[contains(text(), 'I have read and I confirm the legal notices.')]")
            d[0].click()
            driver.find_elements_by_xpath("//button[text()='Validate']")[0].click()
            time.sleep(1 * self.wait_factor)

            driver.get(self._url)
        # driver.find_element_by_id("choixProfilModal").click()


    def get_all_links(self, filter=[]):
        links, filtered_link = [], []
        elems = self.driver.find_elements_by_xpath("//a[@href]")
        for elem in elems:
            links.append(elem.get_attribute("href"))
        for el in links:
            for template in filter:
                if template in el:
                    filtered_link.append(el)
        return filtered_link

    def scroll_down(self, iterations):
        for e in tqdm(range(iterations), desc="Scrolling down"):
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(5 * self.wait_factor)
            # self.driver.implicitly_wait(2)

    def close_driver(self):
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            self.driver.close()

    def new_driver(self, data_path=os.getcwd() + "/data/"):
        options = Options()
        options.headless = True
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.helperApps.alwaysAsk.force", False)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.download.dir", data_path)
        profile.set_preference(
            "browser.helperApps.neverAsk.saveToDisk", ("application/vnd.ms-excel")
        )
        profile.set_preference("general.warnOnAboutConfig", False)
        self.driver = webdriver.Firefox(firefox_profile=profile, options=options)

    def get_links_from_cache(self):
        file_path = self._data + "links.pkl"
        PCH = PickleCachingHandler(file_path).get(return_if_none=[])
        return PCH

    def store_links(self, links):
        file_path = self._data + "links.pkl"
        PickleCachingHandler(file_path).store(links)
