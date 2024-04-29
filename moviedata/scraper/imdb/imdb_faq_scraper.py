from moviedata import *
from moviedata.scraper.imdb.imdb_scraper import *


class IMDBFAQScraper(IMDBScraper):
    def __init__(self):
        super().__init__()
        self.faq_data = {"movieID": [], "faqTitle": [], "faqContent": [], "faqUrl": []}

    def faq_details(self, movie_id, faq_url):
        page_res = get_page(self.BASE_URL + faq_url, self.cookies)
        if not page_res[0]:
            return self.faq_data
        self.page = page_res[1]
        faqs = self.page.find_all("li", class_="ipc-metadata-list__item")
        iterator = tqdm(faqs)
        for faq in iterator:
            title = faq.find("span", class_="ipc-metadata-list-item__label")
            content = faq.find("div", class_="ipc-html-content-inner-div")
            url = (
                (
                    content.find("a", class_="ipc-md-link ipc-md-link--entity").attrs[
                        "href"
                    ]
                    if content.find_all("a") != []
                    else None
                )
                if content
                else None
            )
            self.faq_data["movieID"].append(movie_id)
            self.faq_data["faqTitle"].append(title.text if title else None)
            self.faq_data["faqContent"].append(content.text if content else None)
            self.faq_data["faqUrl"].append(url)

    def save(self):
        save(self.faq_data, "FAQScraper")
