from moviedata import *
from moviedata.scraper.imdb.imdb_scraper import *


class IMDBTechnicalSpecsScraper(IMDBScraper):
    def __init__(self):
        super().__init__()
        self.technical_specification_data = {
            "movieID": [],
            "specKey": [],
            "specValue": [],
            "specLink": [],
        }

    def technical_specs(self, movie_id, technical_specs_url):
        if not technical_specs_url:
            return self.technical_specification_data
        page_res = get_page(self.BASE_URL + technical_specs_url, self.cookies)
        if not page_res[0]:
            return self.technical_specification_data
        self.page = page_res[1]
        technical_specifications = self.page.find_all(
            "li", class_="ipc-metadata-list__item"
        )
        for technical_specification in tqdm(technical_specifications, leave=False):
            spec_key = technical_specification.find(
                "span", class_="ipc-metadata-list-item__label"
            )
            spec_key = spec_key.text if spec_key else None
            spec_value = technical_specification.find(
                "div", class_="ipc-metadata-list-item__content-container"
            )
            spec_value, spec_link = spec_value.text if spec_value else None, (
                (
                    spec_value.find("a").attrs["href"]
                    if spec_value.find_all("a") != []
                    else None
                )
                if spec_value
                else None
            )
            self.technical_specification_data["movieID"].append(movie_id)
            self.technical_specification_data["specKey"].append(spec_key)
            self.technical_specification_data["specValue"].append(spec_value)
            self.technical_specification_data["specLink"].append(spec_link)
        return self.technical_specification_data

    def save(self):
        save(self.technical_specification_data, "TechnicalSpecificationsScraper")
