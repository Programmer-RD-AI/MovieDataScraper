from moviedata import *
from moviedata.scraper.imdb.imdb_scraper import *


class IMDBUserReviews(IMDBScraper):
    def __init__(self):
        super().__init__()
