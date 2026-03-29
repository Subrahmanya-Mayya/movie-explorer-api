from typing import Optional

from fastapi import HTTPException

from app.repositories.movie_repository import MovieRepository
from app.schemas.schemas import (
    MovieDetailResponse,
    MovieListResponse,
    MovieReviewsResponse,
)


class MovieService:
    def __init__(self, repository: MovieRepository):
        self.repository = repository

    def fetch_movies(
        self,
        genre: Optional[str] = None,
        actor: Optional[str] = None,
        director: Optional[str] = None,
        release_year: Optional[int] = None,
    ) -> list[MovieListResponse]:
        movies = self.repository.list_movies(
            genre=genre,
            actor=actor,
            director=director,
            release_year=release_year,
        )
        return [
            MovieListResponse(
                id=movie.id,
                title=movie.title,
                release_year=movie.release_year,
                director=movie.director,
                genres=[genre.name for genre in movie.genres],
            )
            for movie in movies
        ]

    def get_movie_detail(self, movie_id: int) -> MovieDetailResponse:
        movie = self.repository.get_by_id(movie_id)
        if movie is None:
            raise HTTPException(status_code=404, detail="Movie not found")

        avg_score = self.repository.get_average_score(movie_id)
        return MovieDetailResponse(
            id=movie.id,
            title=movie.title,
            release_year=movie.release_year,
            synopsis=movie.synopsis,
            director=movie.director,
            genres=[genre.name for genre in movie.genres],
            actors=list(movie.actors),
            average_score=avg_score,
        )

    def get_movie_reviews(self, movie_id: int) -> MovieReviewsResponse:
        if not self.repository.exists(movie_id):
            raise HTTPException(status_code=404, detail="Movie not found")

        avg_score = self.repository.get_average_score(movie_id)
        reviews = self.repository.get_reviews(movie_id)
        return MovieReviewsResponse(average_score=avg_score, reviews=list(reviews))
