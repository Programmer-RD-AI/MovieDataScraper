from moviedata import *
from moviedata.scraper.imdb.imdb_scraper import *


class IMDBVideoScraper(IMDBScraper):
    def __init__(self):
        super().__init__()
        self.videos_data = {
            "movieID": [],
            "videoTitle": [],
            "videoSubTitle": [],
            "videoLink": [],
        }

    def videos_details(self, movie_id, video_url):
        page_res = get_page(self.BASE_URL + video_url, self.cookies)
        if not page_res[0]:
            return self.videos_data
        self.page = page_res[1]
        videos = self.page.find_all(
            "div",
            class_="ipc-slate-card ipc-slate-card--base ipc-slate-card--dynamic-width sc-9fe05173-0 jjOZgB videos-slate-card sc-8eaeff14-1 jmPQyC ipc-sub-grid-item ipc-sub-grid-item--span-4 ipc-sub-grid-item ipc-sub-grid-item--span-4",
        )
        for video in tqdm(videos, leave=False):
            video_link = video.find(
                "a",
                class_="ipc-slate-card__title ipc-slate-card__title--clickable VideoSlate__title",
            )
            video_title = video.find(
                "div",
                class_="ipc-slate-card__title-text ipc-slate-card__title-text--clamp-2",
            )
            video_sub_title = video.find("div", class_="ipc-slate-card__subtitle2")
            self.videos_data["movieID"].append(movie_id)
            self.videos_data["videoTitle"].append(video_title.text)
            self.videos_data["videoSubTitle"].append(video_sub_title.text)
            self.videos_data["videoLink"].append(video_link.attrs["href"])
        return self.videos_data

    def save(self):
        save(self.videos_data, "VideoScraper")
