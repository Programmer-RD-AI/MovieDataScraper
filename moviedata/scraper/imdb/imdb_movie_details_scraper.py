from moviedata import *
from moviedata.scraper.imdb.imdb_scraper import *
from moviedata.scraper.imdb.imdb_faq_scraper import *
from moviedata.scraper.imdb.imdb_photos_scraper import *
from moviedata.scraper.imdb.imdb_similar_movies_scraper import *
from moviedata.scraper.imdb.imdb_technical_specs_scraper import *
from moviedata.scraper.imdb.imdb_video_scraper import *
from moviedata.scraper.imdb.imdb_cast_scraper import *


class IMDBMovieDetailsScraper(IMDBScraper):
    def __init__(self, base_url: str = os.getenv("BASE_URL")):
        super().__init__()
        self.BASE_URL = base_url
        self.faq = IMDBFAQScraper()
        self.cast = IMDBCastScraper()
        self.video = IMDBVideoScraper()
        self.technical_specifications = IMDBTechnicalSpecsScraper()
        self.photos = IMDBPhotosScraper()
        self.similar_movies = IMDBSimilarMoviesScraper()
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
            "technicalSpecs": [],
        }

    def movie_further_details(
        self,
        movie_id: str,
        movie_url: str,
    ):
        page_res = get_page(self.BASE_URL + movie_url, self.cookies)
        if not page_res[0]:
            return self.movie_details
        movie_page = page_res[1]
        movie_description = movie_page.find("span", class_="sc-a31b0662-2 geLkLc").text
        movie_scores = movie_page.find_all(
            "li", class_="ipc-inline-list__item sc-9e83797f-1 cxyOpW"
        )
        reviews = get_reviews_details(movie_scores)
        user_reviews, critic_reviews, metascore = (
            reviews if len(reviews) == 3 else [None] * 3
        )
        nomination_url = movie_page.find(
            "a",
            class_="ipc-metadata-list-item__label ipc-metadata-list-item__label--link",
        ).attrs["href"]
        story_line = movie_page.find("div", class_="ipc-html-content-inner-div")
        story_line = story_line.text if story_line else None
        taglines = movie_page.find(
            "ul",
            class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base",
        ).text
        genres = movie_page.find("li", class_="ipc-metadata-list__item").text
        certificate = movie_page.find(
            "ul",
            class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base",
        ).text
        further_links = movie_page.find_all("a", class_="ipc-title-link-wrapper")
        video_url = further_links[0].attrs["href"]
        photo_url = further_links[1].attrs["href"]
        cast_url = further_links[2].attrs["href"]
        faq_url = further_links[5].attrs["href"]
        technical_specs_url = (
            further_links[6].attrs["href"] if len(further_links) > 6 else None
        )
        self.movie_details = add_to_dict(
            self.movie_details,
            [
                movie_id,
                movie_description,
                movie_scores,
                user_reviews,
                critic_reviews,
                metascore,
                nomination_url,
                story_line,
                taglines,
                genres,
                certificate,
                cast_url,
                faq_url,
                video_url,
                photo_url,
                technical_specs_url,
            ],
        )
        self.faq.faq_details(movie_id, faq_url)
        self.video.videos_details(movie_id, video_url)
        self.photos.photos_details(movie_id, photo_url)
        self.technical_specifications.technical_specs(
            movie_id, technical_specs_url if technical_specs_url else None
        )
        self.cast.cast_details(movie_id, cast_url)
        self.similar_movies.similar_movie_details(movie_id, movie_url)
        return self.movie_details

    def save(self, name: str = "MovieDetailsScraper"):
        self.faq.save()
        self.video.save()
        self.photos.save()
        self.technical_specifications.save()
        self.cast.save()
        save(self.movie_details, name)
