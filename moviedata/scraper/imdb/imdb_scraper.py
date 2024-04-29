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
        self.headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
        }
        self.BASE_URL = os.getenv("BASE_URL")
