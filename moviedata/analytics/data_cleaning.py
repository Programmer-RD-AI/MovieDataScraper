from moviedata import *
from moviedata.analytics.data_loading import *


class DataCleaning(DataLoading):
    def __init__(self):
        super().__init__()
        self.faq_stats = {"movieID": [], "noOfFAQs": []}
        self.price_stats = {
            "movieID": [],
            "movieEarn": [],
            "movieBudget": [],
            "movieOther": [],
        }

    def type_faq_counter(self):
        for movieId in tqdm(self.movieIds):
            faqs_in_movie = self.faq_data[self.faq_data["movieID"] == movieId]
            self.faq_stats["movieID"].append(movieId)
            self.faq_stats["noOfFAQs"].append(len(faqs_in_movie))
            for faq in faqs_in_movie["faqTitle"]:
                if not faq:
                    continue
                name = faq.split(" ")[0].lower() + "Counter"
                if name not in self.faq_stats:
                    self.faq_stats[name] = [0] * len(self.movieIds)
                self.faq_stats[name][np.where(self.movieIds == movieId)[0][0]] += 1
        return pd.DataFrame(self.faq_stats)

    def prices(self):
        for movieId in tqdm(self.movieIds):
            earn = [0, 1]
            budget = [0, 1]
            other = [0, 1]
            faqs_in_movie = self.faq_data[self.faq_data["movieID"] == movieId]
            for content, title in zip(
                faqs_in_movie["faqContent"], faqs_in_movie["faqTitle"]
            ):
                if content and "$" in content:
                    content = content.split(" ")
                    if len(content) <= 1:
                        continue
                    figure = content[-1][0].lower()
                    price = (
                        float(content[0].replace(",", "").replace("$", "")) * 1000
                        if figure == "b"
                        else float(content[0].replace(",", "").replace("$", ""))
                    )
                    if "earn" in title:
                        earn[0] += price
                        earn[1] += 1
                    elif "budget" in title:
                        budget[0] += price
                        budget[1] += 1
                    else:
                        other[0] += price
                        other[1] += 1
            self.price_stats["movieID"].append(movieId)
            self.price_stats["movieEarn"].append(earn[0] / earn[1])
            self.price_stats["movieBudget"].append(budget[0] / budget[1])
            self.price_stats["movieOther"].append(other[0] / other[1])
        return pd.DataFrame(self.price_stats)

    def movie_statistics(self):
        movie_stats = self.movie_basic_data[
            ["movieID", "movieYear", "movieTime", "movieAvgRating", "movieRatingCount"]
        ]
        movie_times = movie_stats["movieTime"]
        movie_times_in_mins = []
        for movie_time in tqdm(movie_times):
            if not movie_time:
                movie_times_in_mins.append(None)
                continue
            split = movie_time.split(" ")
            if len(split) == 1:
                split.append("0m")
            hrs, mins = split
            tot = int(mins.strip().replace("m", ""))
            tot += (
                int(hrs.strip().replace("h", "")) * 60
                if hrs.strip().replace("h", "").isnumeric()
                else 0
            )
            movie_times_in_mins.append(tot)
        movie_stats["movieTime"] = movie_times_in_mins
        ratings = movie_stats["movieRatingCount"]
        new_ratings = []
        for rating in ratings:
            if not rating:
                new_ratings.append(None)
                continue
            sign = rating[-1].lower()
            if sign.isnumeric():
                new_ratings.append(float(rating))
                continue
            rating = rating.replace(rating[-1], "").strip()
            new_ratings.append(float(rating) * 1000 if sign == "k" else 1000000)
        movie_stats["movieRatingCount"] = new_ratings
        return movie_stats

    def technical_specification(self):
        return self.technical_specification_data[["movieID", "specKey", "specValue"]]

    def language(self):
        descriptions = self.movie_data["movieDescription"]
        story_lines = self.movie_data["storyLine"]
        return story_lines, descriptions
