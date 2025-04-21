from tracker.query.base import TVMovieDB, TrendingTimeframe


class MoviesDB(TVMovieDB):
    def get_genres(self) -> dict:
        response = self.request(
            "/genre/movie/list",
            params={"language": "en-US"},
        )
        return response

    def search(self, query: str, include_adult: bool = False) -> dict:
        response = self.request(
            "/search/movie",
            params={
                "query": query,
                "include_adult": include_adult,
                "language": "en-US",
                "page": "1",
            },
        )
        return response

    def get_trending(self, timeframe: TrendingTimeframe) -> dict:
        response = self.request(
            f"/trending/movie/{timeframe}",
            params={"language": "en-US"},
        )
        return response


class MovieShowAdapter:
    pass
