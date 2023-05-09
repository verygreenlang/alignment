import os
from selenium import webdriver
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
from .am.bnp import BNP
from .am.amundi import AMUNDI
from .am.echiquier import ECHIQUIER
from .am.gemway import GEMWAY
from .am.carmignac import CARMIGNAC
from .am.jpmorgan import JPMORGAN
from .am.pictet import PICTET


class AssetManagerData:
    def __init__(self, data_path):
        # self.data_path = data_path
        self.BNP = BNP(data_path)
        self.ECHIQUIER = ECHIQUIER(data_path)
        self.GEMWAY = GEMWAY(data_path)
        self.CARMIGNAC = CARMIGNAC(data_path)
        self.JPMORGAN = JPMORGAN(data_path)
        self.PICTET = PICTET(data_path)

    def get(self):
        self.BNP.get()
        self.ECHIQUIER.get()
        self.GEMWAY.get()
        self.CARMIGNAC.get()
        self.JPMORGAN.get()
        self.PICTET.get()
