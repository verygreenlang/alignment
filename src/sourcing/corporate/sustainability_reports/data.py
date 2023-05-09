import os
import string
import requests
import time
import pickle
from bs4 import BeautifulSoup
from tqdm import tqdm
from src.tools.caching import PickleCachingHandler
from src.tools.caching import  PdfCachingHandler
from src.tools.logger import FingreenLogger
logger = FingreenLogger().logger

class DataSustainabilityReport:
    def __init__(self,data_path):
        self.sustainability_report_path = data_path +os.sep  + "corporate" + os.sep +"sustainability"
        self.sustainability_report_extracted = self.sustainability_report_path \
                    + os.sep + "extracted"
