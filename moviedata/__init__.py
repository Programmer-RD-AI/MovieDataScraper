import os
import threading
from pprint import pprint
from typing import *

import pandas as pd
import requests
from bs4 import *
from dotenv import load_dotenv
from tqdm import tqdm

from moviedata.analysis import *
from moviedata.helper_functions import *
from moviedata.scraper import *

load_dotenv()
PATH = os.getenv("PATH_OF_DIR")
