import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock

from app.models.models import Actor, Director, Genre, Movie, Review
from app.services.movie_service import MovieService


class FakeMovieRepository:
    def __init__(self, movies=None, movie=None, exists=True, avg_score=None, reviews=None):
        self._movies = movies or []
        self._movie = movie
        self._exists = exists
        self._avg_score = avg_score
        self._reviews = reviews or []

    def list_movies(self, genre=None, actor=None, director=None, release_year=None):
        return self._movies

    def get_by_id(self, movie_id):
        return self._movie

    def exists(self, movie_id):
        return self._exists

    def get_average_score(self, movie_id):
        return self._avg_score

    def get_reviews(self, movie_id):
        return self._reviews


def test_fetch_movies_maps_domain_to_response():
    director = Director(id=1, name="Christopher Nolan")
    genres = [Genre(id=1, name="Sci-Fi"), Genre(id=2, name="Action")]
    movie = Movie(id=1, title="Inception", release_year=2010, director=director, genres=genres)

    service = MovieService(repository=FakeMovieRepository(movies=[movie]))

    response = service.fetch_movies()

    assert len(response) == 1
    assert response[0].title == "Inception"
    assert response[0].director.name == "Christopher Nolan"
    assert response[0].genres == ["Sci-Fi", "Action"]


def test_fetch_movies_passes_filters_to_repository():
    repository = MagicMock()
    repository.list_movies.return_value = []

    service = MovieService(repository=repository)
    service.fetch_movies(genre="action", actor="cillian", director="nolan", release_year=2010)
    repository.list_movies.assert_called_once_with(
        genre="action", actor="cillian", director="nolan", release_year=2010
    )


def test_get_movie_detail_raises_404_when_not_found():
    service = MovieService(repository=FakeMovieRepository(movie=None))

    with pytest.raises(HTTPException) as error:
        service.get_movie_detail(999)

    assert error.value.status_code == 404
    assert error.value.detail == "Movie not found"


def test_get_movie_detail_builds_response_with_average_score():
    director = Director(id=1, name="Christopher Nolan")
    actors = [Actor(id=1, name="Cillian Murphy")]
    genres = [Genre(id=1, name="Drama")]
    movie = Movie(
        id=2,
        title="Oppenheimer",
        synopsis="A story about science and consequences.",
        release_year=2023,
        director=director,
        actors=actors,
        genres=genres,
    )

    service = MovieService(repository=FakeMovieRepository(movie=movie, avg_score=8.9))

    response = service.get_movie_detail(movie.id)

    assert response.id == movie.id
    assert response.average_score == 8.9
    assert response.actors[0].name == "Cillian Murphy"


def test_get_movie_reviews_raises_404_when_movie_missing():
    service = MovieService(repository=FakeMovieRepository(exists=False))

    with pytest.raises(HTTPException) as error:
        service.get_movie_reviews(100)

    assert error.value.status_code == 404
    assert error.value.detail == "Movie not found"


def test_get_movie_reviews_returns_average_and_reviews():
    reviews = [
        Review(id=1, score=8.5, reviewer_name="Ava", comment="Great", movie_id=1),
        Review(id=2, score=9.0, reviewer_name="Noah", comment="Excellent", movie_id=1),
    ]
    service = MovieService(
        repository=FakeMovieRepository(exists=True, avg_score=8.75, reviews=reviews)
    )

    response = service.get_movie_reviews(1)

    assert response.average_score == 8.75
    assert len(response.reviews) == 2
    assert response.reviews[0].reviewer_name == "Ava"
