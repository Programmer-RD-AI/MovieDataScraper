from moviedata import *


class DataLoading:
    def __init__(self):
        self.faq_data = pd.read_json(f"{PATH}/data/FAQScraper/FAQScraper.json").sample(
            frac=1
        )
        self.movie_data = pd.read_json(
            f"{PATH}/data/MovieDetailsScraper/MovieDetailsScraper.json"
        ).sample(frac=1)
        self.movie_basic_data = pd.read_json(
            f"{PATH}/data/MoviesBasicDetailsScraper/MoviesBasicDetailsScraper.json"
        ).sample(frac=1)
        self.photo_data = pd.read_json(
            f"{PATH}/data/PhotoScraper/PhotoScraper.json"
        ).sample(frac=1)
        self.technical_specification_data = pd.read_json(
            f"{PATH}/data/TechnicalSpecificationsScraper/TechnicalSpecificationsScraper.json"
        ).sample(frac=1)
        self.video_data = pd.read_json(
            f"{PATH}/data/VideoScraper/VideoScraper.json"
        ).sample(frac=1)
        self.movieIds = np.unique(self.movie_basic_data["movieID"].astype(str))
