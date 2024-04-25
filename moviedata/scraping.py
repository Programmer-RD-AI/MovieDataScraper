from moviedata import *


class MovieDataScraper:
    def __init__(
        self, base_url: str = "https://www.imdb.com", specific_url: str = "/chart/moviemeter/?ref_=nv_mv_mpm"
    ) -> None:
        self.cookies = {
            "UID": os.getenv('Cookie_UID'),
            "aws-ubid-main": os.getenv('Cookie_aws-ubid-main'),
        }
        self.BASE_URL = base_url
        self.page = get_page(self.BASE_URL + specific_url, self.cookies)

    def get_reviews_details(self, reviews: BeautifulSoup) -> [str, str, str]:
        review_details = []
        for review in reviews:
            review_url = review.find('a').attrs['href']
            review_three_elems = review.find(
                'span', class_="three-Elements").find_all('span')
            review_count, review_type = review_three_elems[0].text, review_three_elems[1].text
            review_details.append([review_url, review_count, review_type])
        return review_details

    def movie_further_details(self, movieID: str, movieUrl: str):
        movie_page = get_page(self.BASE_URL + movieUrl, self.cookies)
        movie_description = movie_page.find(
            'span', class_="sc-a31b0662-2 geLkLc").text
        movie_scores = movie_page.find(
            'li', class_="ipc-inline-list__item sc-9e83797f-1 cxyOpW")
        user_reviews, critic_reviews, metascore = self.get_reviews_details(
            movie_scores)
        

    def movies_basic_details(self):
        movies = self.page.find_all(
            "li",
            class_="ipc-metadata-list-summary-item sc-10233bc-0 iherUv cli-parent",
        )
        for movie in movies:
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
            self.movie_further_details(encode(movie_title), movie_more_url)
            break
