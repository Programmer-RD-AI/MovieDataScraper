from moviedata import *
from moviedata.scraper.imdb.imdb_scraper import *


class IMDBCriticReviews(IMDBScraper):
    def __init__(self):
        super().__init__()
