from moviedata import *
from moviedata.scraper.imdb.imdb_scraper import *


class IMDBCastScraper(IMDBScraper):
    def __init__(self):
        super().__init__()
        self.cast_data = {
            "movieID": [],
            "castName": [],
            "castType": [],
            "castRole": [],
            "castUrl": [],
        }

    def cast_details(self, movie_id, cast_url):
        page_res = get_page(self.BASE_URL + cast_url, self.cookies)
        if not page_res[0]:
            return self.cast_data
        self.page = page_res[1]
        tables = self.page.find_all("table")
        for table in tqdm(tables, leave=False):
            cast_type = table.previous_sibling.text
            rows = table.find_all("tr")
            for row in tqdm(rows, leave=False):
                tds = row.find_all("td")
                cast_name = tds[0]
                cast_role = tds[-1] if len(tds) > 1 else None
                cast_url = (
                    cast_name.find("a").attrs["href"]
                    if cast_name.find_all("a") != []
                    else None
                )
                cast_name = cast_name.text
                cast_role = cast_role.text if cast_role else None
                self.cast_data["movieID"] = movie_id
                self.cast_data["castName"] = cast_name
                self.cast_data["castType"] = cast_type
                self.cast_data["castRole"] = cast_role
                self.cast_data["castUrl"] = cast_url
        return self.cast_data

    def save(self):
        save(self.cast_data, "CastScraper")
