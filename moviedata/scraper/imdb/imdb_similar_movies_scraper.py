from moviedata import *
from moviedata.scraper.imdb import *


class IMDBSimilarMoviesScraper(IMDBScraper):
    def __init__(self):
        super().__init__()
        self.similar_movie_data = {"movieID": [], "movieTitle": [], "movieUrl": []}

    def similar_movie_details(self, movie_id, movie_url):
        page_res = get_page(self.BASE_URL + movie_url, self.cookies)
        if not page_res[0]:
            return self.similar_movie_data
        self.page = page_res[1]
        movies = self.page.find_all(
            # limitation
            "div",
            class_="ipc-poster-card ipc-poster-card--base ipc-poster-card--dynamic-width ipc-sub-grid-item ipc-sub-grid-item--span-2",
        )[:5]
        for movie in tqdm(movies, leave=False):
            movie_url = movie.find(
                "a",
                class_="ipc-poster-card__title ipc-poster-card__title--clamp-2 ipc-poster-card__title--clickable",
            )
            movie_title = movie_url.text
            movie_url = movie_url.attrs["href"]
            self.similar_movie_data["movieID"].append(movie_id)
            self.similar_movie_data["movieTitle"].append(movie_title)
            self.similar_movie_data["movieUrl"].append(movie_url)
            # movie_details_instance.movie_further_details(
            #     encoded_title, movie_url, movie_details_instance, connected_movies)

    def save(self):
        save(self.similar_movie_data, "SimilarMovieData")
