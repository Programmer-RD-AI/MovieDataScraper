from moviedata import *
from moviedata.scraper.imdb.imdb_scraper import *

class IMDBScraper:
    def __init__(
        self,
    ) -> None:
        self.cookies = {
            "UID": os.getenv("Cookie_UID"),
            "aws-ubid-main": os.getenv("Cookie_aws-ubid-main"),
        }
        self.BASE_URL = os.getenv("BASE_URL")
