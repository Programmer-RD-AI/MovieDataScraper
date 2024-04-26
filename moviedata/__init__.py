
from tqdm import tqdm
import pandas as pd
import os
from dotenv import load_dotenv
from pprint import pprint
import threading
from typing import *
from bs4 import *
import requests

load_dotenv()
PATH = os.getenv('PATH_OF_DIR')

from moviedata.helper_functions import *
from moviedata.scraper import *
from moviedata.analysis import *

