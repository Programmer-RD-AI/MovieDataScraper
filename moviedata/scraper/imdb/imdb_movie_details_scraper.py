from moviedata import *
from moviedata.scraper.imdb.imdb_scraper import *
from moviedata.scraper.imdb.imdb_faq_scraper import *
from moviedata.scraper.imdb.imdb_photos_scraper import *
from moviedata.scraper.imdb.imdb_similar_movies_scraper import *
from moviedata.scraper.imdb.imdb_technical_specs_scraper import *
from moviedata.scraper.imdb.imdb_video_scraper import *
from moviedata.scraper.imdb.imdb_cast_scraper import *


class IMDBMovieDetailsScraper(IMDBScraper):
    def __init__(self, base_url: str = os.getenv('BASE_URL')):
        super().__init__()
        self.BASE_URL = base_url
        self.faq = IMDBFAQScraper()
        self.cast = IMDBCastScraper()
        self.video = IMDBVideoScraper()
        self.technical_specifications = IMDBTechnicalSpecsScraper()
        self.photos = IMDBPhotosScraper()
        self.movie_details = {
            "movieID": [],
            "movieDescription": [],
            "movieScores": [],
            "userReviews": [],
            "criticReviews": [],
            "metascore": [],
            "nominationUrl": [],
            "storyLine": [],
            "taglines": [],
            "genres": [],
            "certificate": [],
            "cast": [],
            "faq": [],
            "videos": [],
            "photos": [],
            "technicalSpecs": []
        }

    def movie_further_details(self, movie_id: str, movie_url: str):
        movie_page = get_page(self.BASE_URL + movie_url, self.cookies)
        movie_description = movie_page.find(
            'span', class_="sc-a31b0662-2 geLkLc").text
        movie_scores = movie_page.find_all(
            'li', class_="ipc-inline-list__item sc-9e83797f-1 cxyOpW")
        user_reviews, critic_reviews, metascore = get_reviews_details(
            movie_scores)
        nomination_url = movie_page.find(
            "a", class_="ipc-metadata-list-item__label ipc-metadata-list-item__label--link").attrs['href']
        story_line = movie_page.find(
            'div', class_="ipc-html-content-inner-div").text
        taglines = movie_page.find(
            'ul', class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base").text
        genres = movie_page.find('li', class_="ipc-metadata-list__item").text
        certificate = movie_page.find(
            'ul', class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base").text
        further_links = movie_page.find_all(
            'a', class_="ipc-title-link-wrapper")
        video_url = further_links[0].attrs['href']
        photo_url = further_links[1].attrs['href']
        cast_url = further_links[2].attrs['href']
        faq_url = further_links[5].attrs['href']
        technical_specs_url = further_links[6].attrs['href']
        self.movie_details = add_to_dict(self.movie_details, [
                                         movie_id, movie_description, movie_scores, user_reviews, critic_reviews, metascore, nomination_url, story_line, taglines, genres, certificate, cast_url, faq_url, video_url, photo_url, technical_specs_url])
        threading.Thread(target=self.faq.faq_details,
                         args=(movie_id, faq_url)).start()
        threading.Thread(target=self.video.videos_details,
                         args=(movie_id, video_url)).start()
        threading.Thread(target=self.photos.photos_details,
                         args=(movie_id, photo_url)).start()
        threading.Thread(target=self.technical_specifications.technical_specs,
                         args=(movie_id, technical_specs_url)).start()
        threading.Thread(target=self.cast.cast_details,
                         args=(movie_id, cast_url)).start()
        return self.movie_details

    def save(self):
        save(self.movie_details, "MovieDetailsScraper")
