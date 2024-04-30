from moviedata import *
from moviedata.analytics.data_cleaning import *


class Analytics:
    def __init__(self):
        self.dc = DataCleaning()
        self.faq_counter = self.dc.type_faq_counter()
        self.prices = self.dc.prices()
        self.movie_stats = self.dc.movie_statistics()
        self.technical_specification = self.dc.technical_specification()
        self.stop_words = set(stopwords.words("english"))
        self.story_lines, self.descriptions = self.dc.language()

    def combine(self, columns: str = "movieID"):
        to_be_merged = [
            self.faq_counter,
            self.prices,
            self.movie_stats,
            self.technical_specification,
        ]
        merged = []
        counter = 0
        while counter != len(to_be_merged):
            merged.append(
                pd.merge(to_be_merged[counter], to_be_merged[counter + 1], on=columns)
            )
            counter += 2
        for idx in range(len(merged) - 1):
            merged = pd.merge(merged[idx], merged[idx + 1], on=columns)
        self.df = merged
        return self.df

    def correlation_matrix(self):
        correlation_matrix = self.df.drop(
            ["movieID", "specKey", "specValue"], axis=1
        ).corr()
        correlation_matrix.to_json(f"{PATH}/data/correlation_matrix.json")
        return correlation_matrix

    def heatmap(self, correlation_matrix):
        # Set the style
        sns.set(style="white")
        plt.figure(figsize=(12, 10))
        sns.heatmap(
            correlation_matrix, annot=True, cmap="coolwarm", fmt=".1f", linewidths=0.5
        )
        plt.title("Correlation Heatmap of Features")
        plt.savefig(f"{PATH}/data/heatmap.png")

    def cluster_map(self, correlation_matrix):
        sns.clustermap(
            correlation_matrix.dropna(axis=1, how="all").dropna(axis=0, how="all"),
            annot=True,  # Show the correlation values in each cell
            cmap="coolwarm",  # Color map
            figsize=(12, 10),
        )  # Size of the figure
        plt.title("Cluster Map of Features")
        plt.savefig(f"{PATH}/data/cluster_map.png")

    def count_plot(self, config, name, specific_name, y: str = "Frequency"):
        plt.figure(figsize=(12, 8))
        sns.countplot(**config)
        plt.title(name)
        plt.xlabel(specific_name)
        plt.ylabel(y)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(f"{PATH}/data/count_plot_{name}_{specific_name}.png")

    def violin_plot(
        self,
        title,
        x_name="specKey",
        y_name="movieYear",
    ):
        plt.figure(figsize=(12, 8))
        sns.violinplot(
            data=self.df,
            x=x_name,
            y=y_name,
            palette=f"Pastel{random.randint(1,2)}",
        )
        plt.title(title)
        plt.xlabel(x_name)
        plt.ylabel(y_name)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(f"{PATH}/data/violin_plot_{title}.png")

    def word_cloud(self, sentences, name):
        word_tokens = []
        for sentence in sentences:
            words = word_tokenize(sentence.lower())  # Convert to lowercase
            # Remove punctuation
            words = [word for word in words if word.isalnum()]
            words = [word for word in words if word not in self.stop_words]
            word_tokens.extend(words)
        text = " ".join(word_tokens)
        wordcloud = WordCloud(width=800, height=400, background_color="gray").generate(
            text
        )
        # Plot the word cloud
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig(f"{PATH}/data/violin_plot_{name}.png")

    def pair_plot(self, attributes):
        pp_df = self.df[attributes]
        pp_df.dropna(inplace=True)
        sns.pairplot(pp_df)
        plt.savefig(f"{PATH}/data/pair_plot.png")

    def analyze(self):
        df = self.combine()
        correlation_matrix = self.correlation_matrix()
        self.heatmap(correlation_matrix=correlation_matrix)
        self.cluster_map(correlation_matrix=correlation_matrix)
        self.count_plot(
            {"data": df, "x": "specKey", "palette": "viridis"},
            "Frequency of Technical Specifications",
            "Specification Key",
        )
        self.count_plot(
            {
                "data": df,
                "y": "specValue",
                "palette": "magma",
                "order": self.df["specValue"].value_counts().index[:20],
            },
            "Top 20 Most Common Specification Values",
            "Frequency",
            "Specification Key",
        )
        self.violin_plot(
            "Distribution of specKey by movieYear",
            "specKey",
            "movieYear",
        )
        self.violin_plot(
            "Distribution of specKey by movieEarn",
            "specKey",
            "movieEarn",
        )
        self.violin_plot(
            "Distribution of specKey by movieAvgRating",
            "specKey",
            "movieAvgRating",
        )
        self.violin_plot(
            "Distribution of specKey by movieTime",
            "specKey",
            "movieTime",
        )
        self.word_cloud(self.descriptions.dropna(), "Descriptions")
        self.word_cloud(self.story_lines.dropna(), "StoryLines")
        self.pair_plot(
            [
                "movieYear",
                "movieTime",
                "movieAvgRating",
                "movieRatingCount",
                "movieEarn",
                "movieBudget",
            ]
        )
