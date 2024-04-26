import json
import os

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

from moviedata.analysis import *
from moviedata.helper_functions import *
from moviedata.scraping import *

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve

import requests
from bs4 import *

load_dotenv()
