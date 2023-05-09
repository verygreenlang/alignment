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
from src.tools.caching import PickleCachingHandler, FileCachingHandler, JsonCachingHandler


class BNP:
    def __init__(self, data_path):
        self.wait_factor = 2
        self.bnp_url = (
            "https://www.bnpparibas-am.lu/professional-investor/fundexplorer/"
        )
        self.data_path = data_path
        self.basename = "bnp"
        self.bnp_data = self.data_path + os.sep + "am/" + self.basename + os.sep
        self.new_driver()

    def get(self):
        links = self.get_links_index_bnp()
        self.store_links(links)

        for pdf_dir in self.get_data_for_each_link(links):
            PdfExtractor(pdf_dir).get()

    def get_links_index_bnp(self):
        links = self.get_links_from_cache()
        if len(links) > 0:
            return links
        # driver = self.driver
        self.driver.get(self.bnp_url)
        self.accept_cookies_bnp()
        self.scroll_down(30)
        link_templates = [
            "https://www.bnpparibas-am.fr/investisseur-prive/fundsheet/",
            "https://www.bnpparibas-am.lu/private-investor/fundsheet/",
        ]
        return self.get_all_links(link_templates)

    def get_data_for_each_link(self, links):
        pdf_path = []
        for link in tqdm(links, desc="Downloading BNP AM data for each link "):
            # try:
            isin = link.split("-")[-1]
            path_fund_data = self.bnp_data + isin
            os.system("mkdir -p " + path_fund_data)
            pdf_path.append(path_fund_data)
            path_fund_data_link = path_fund_data + os.sep + "index.json"
            if not os.path.isfile(path_fund_data_link):
                try:
                    data = {"path_fund_data": path_fund_data, "isin": isin, "url": link}
                    data = self.get_data_from_link_bnp(data)
                    JsonCachingHandler(path_fund_data_link).store(data)
                #with open(path_fund_data_link, "w") as f:
                #    json.dump(data, f)

                    for pdf_link in data["pdf_links"]:
                        if "blank" not in pdf_link:
                            os.system("wget -P " + path_fund_data + " " + pdf_link)
                            print(path_fund_data +  pdf_link.split("/")[-1])
                            FileCachingHandler(path_fund_data).store(path_fund_data + pdf_link.split("/")[-1])
                except Exception as e:
                    print(e)
        return pdf_path
        # except Exception as e:
        #     print(e, "exception for isin:",isin)
        # except Exception as e:
        # print(e)

    def get_data_from_link_bnp(self, data):
        self.close_driver()
        self.new_driver(data_path=data["path_fund_data"])
        self.driver.get(data["url"])
        self.accept_cookies_bnp()
        today = date.today()
        data["date"] = today.strftime("%d_%m_%Y")
        data["info_fund"] = self.get_data_VL()
        data["pdf_links"] = self.get_documents()
        return data

    def get_documents(self):
        self.driver.find_elements_by_xpath("//*[contains(text(), 'Documents')]")[
            0
        ].click()
        a = ActionChains(self.driver)
        documents = self.driver.find_elements_by_class_name("sc-ciOKUB")
        pdf_links = []
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(1 * self.wait_factor)
        for document in tqdm(documents, desc="Downloading bnp AM documents"):
            m = document
            try:
                a.move_to_element(document).perform()
                m.click()
                window_after = self.driver.window_handles[-1]
                window_before = self.driver.window_handles[0]
                time.sleep(1 * self.wait_factor)
                self.driver.switch_to.window(window_after)
                pdf_url = self.driver.current_url
                self.driver.switch_to.window(window_before)
                pdf_links.append(pdf_url)
            except Exception as e:
                print(e)

        return pdf_links

    def get_data_VL(self):
        try:
            self.driver.find_elements_by_xpath("//*[contains(text(), 'NAV')]")[
                0
            ].click()
            section_VL = self.driver.find_elements_by_tag_name("section")
            info_fund = section_VL[3].text.split("\n")
            return info_fund
        except Exception as e:
            print(e)
            return None

    def accept_cookies_bnp(self):
        driver = self.driver
        time.sleep(10 * self.wait_factor)
        driver.find_element_by_id("onetrust-accept-btn-handler").click()
        try:
            time.sleep(2 * self.wait_factor)
            driver.find_element_by_class_name("bnp-cell-title").click()
            time.sleep(2 * self.wait_factor)
            driver.find_element_by_id("segmentcell_0").click()
            time.sleep(2 * self.wait_factor)
            driver.find_element_by_class_name("bnp-terms-action").click()
        except Exception as e:
            print(e)
        time.sleep(5 * self.wait_factor)

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

        # section_element = driver.find_element_by_class_name("section")
        # classs="sc-ezHeEz"
        # rows = section_element.find_elements_by_class_name(classs)

    def get_links_from_cache(self):
        file_path = self.bnp_data + "links.json"
        PCH = JsonCachingHandler(file_path).get(return_if_none=[])
        return PCH
        # if not os.path.isfile(file_path):
        #     return []
        # with open(file_path,"rb") as f:
        #     return pickle.load(f)

    def store_links(self, links):
        file_path = self.bnp_data + "links.json"
        JsonCachingHandler(file_path).store(links)
        # with open(self.bnp_data +"links.pkl","wb") as f:
        # pickle.dump(links,f)
