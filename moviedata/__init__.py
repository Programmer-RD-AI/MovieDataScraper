import os
import threading
from pprint import pprint
from typing import *

import pandas as pd
import requests
import urllib3
from bs4 import *
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from tqdm import tqdm

from moviedata.analysis import *
from moviedata.helper_functions import *
from moviedata.scraper import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()
PATH = os.getenv("PATH_OF_DIR")
retry_strategy = Retry(total=10, backoff_factor=5)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)
