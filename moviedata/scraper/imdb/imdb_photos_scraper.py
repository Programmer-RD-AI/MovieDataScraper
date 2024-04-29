from moviedata import *
from moviedata.scraper.imdb.imdb_scraper import *


class IMDBPhotosScraper(IMDBScraper):
    def __init__(self):
        super().__init__()
        self.photo_data = {
            "movieID": [],
            "photoTitle": [],
            "photoUrl": [],
        }

    def photos_details(self, movie_id, photo_url):
        page_res = get_page(self.BASE_URL + photo_url, self.cookies)
        if not page_res[0]:
            return self.photo_data
        self.page = page_res[1]
        collection_page = self.page.find(
            "a", class_="ipc-icon-link ipc-icon-link--baseAlt ipc-icon-link--onBase"
        ).attrs["href"]
        page_res = get_page(self.BASE_URL + collection_page, self.cookies)
        if not page_res[0]:
            return self.photo_data
        self.page = page_res[1]
        all_images = self.page.find("div", class_="media_index_thumb_list").find_all(
            "a"
        )
        for image in tqdm(all_images, leave=False):
            try:
                photo_url = image.attrs["href"]
                photo_title = image.attrs["title"]
                self.photo_data["movieID"].append(movie_id)
                self.photo_data["photoTitle"].append(photo_title)
                self.photo_data["photoUrl"].append(photo_url)
            except:
                pass
        return self.photo_data

    def save(self):
        save(self.photo_data, "PhotoScraper")
