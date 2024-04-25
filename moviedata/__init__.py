
import numpy as np
import json
from tqdm import tqdm
import pandas as pd
import os
from dotenv import load_dotenv

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve
from bs4 import *
import requests

load_dotenv()

from moviedata.helper_functions import *
from moviedata.analysis import *
from moviedata.scraping import *
