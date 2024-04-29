from tqdm import tqdm
import pandas as pd
import os
from dotenv import load_dotenv
from pprint import pprint
import threading
from typing import *
from bs4 import *
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()
PATH = os.getenv("PATH_OF_DIR")
retry_strategy = Retry(total=10, backoff_factor=5)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)

from moviedata.helper_functions import *
from moviedata.scraper import *
from moviedata.analysis import *
