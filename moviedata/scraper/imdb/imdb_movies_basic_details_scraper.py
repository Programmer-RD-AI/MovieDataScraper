from moviedata import *
from moviedata.scraper.imdb.imdb_scraper import *
from moviedata.scraper.imdb.imdb_movie_details_scraper import *


class IMDBMoviesBasicDetailsScraper(IMDBScraper):
    def __init__(self, specific_url: str = "/chart/moviemeter/?ref_=nv_mv_mpm"):
        super().__init__()
        self.page = get_page(self.BASE_URL + specific_url, self.cookies)
        self.imdb_movie_details = IMDBMovieDetailsScraper()
        self.movies_basic_details = {
            "movieID": [],
            "movieImg": [],
            "movieMoreUrl": [],
            "movieTitle": [],
            "movieYear": [],
            "movieTime": [],
            "movieAvgRating": [],
            "movieRatingCount": []
        }

    def movies_basic_details(self):
        movies = self.page.find_all(
            "li",
            class_="ipc-metadata-list-summary-item sc-10233bc-0 iherUv cli-parent",
        )
        movie_threads = []
        for movie in tqdm(movies):
            movie_img = movie.find("img", class_="ipc-image").attrs["src"]
            movie_more_url = movie.find("a", class_="ipc-title-link-wrapper").attrs[
                "href"
            ]
            movie_title = movie.find("h3", class_="ipc-title__text").text
            movie_timestamp = movie.find_all(
                "span", class_="sc-b189961a-8 kLaxqf cli-title-metadata-item"
            )
            movie_year = movie_timestamp[0].text
            movie_time = movie_timestamp[1].text
            movie_avg_rating = movie.find(
                "span",
                class_="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating",
            ).contents[1]
            movie_rating_count = (
                movie.find("span", class_="ipc-rating-star--voteCount")
                .text.strip()
                .replace("(", "")
                .replace(")", "")
            )
            self.movies_basic_details = add_to_dict(self.movies_basic_details, [encode(
                movie_title), movie_img, movie_more_url, movie_title, movie_year, movie_time, movie_avg_rating, movie_rating_count])
            movie_thread = threading.Thread(target=self.imdb_movie_details.movie_further_details, args=(
                encode(movie_title), movie_more_url))
            movie_threads.append(movie_thread)
            movie_thread.start()
        wait_for_threads(movie_threads)
        self.imdb_movie_details.save()
        save(self.movies_basic_details, "MoviesBasicDetailsScraper")
        return self.movies_basic_details
