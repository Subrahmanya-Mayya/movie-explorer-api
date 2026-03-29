import pytest
from fastapi import HTTPException

from app.models.models import Director, Movie
from app.services.director_service import DirectorService


class FakeDirectorRepository:
    def __init__(self, directors=None, director=None):
        self._directors = directors or []
        self._director = director

    def get_all(self):
        return self._directors

    def get_by_id(self, director_id):
        return self._director


def test_get_all_directors_maps_response():
    directors = [Director(id=1, name="Christopher Nolan"), Director(id=2, name="Denis Villeneuve")]
    service = DirectorService(repository=FakeDirectorRepository(directors=directors))

    response = service.get_all_directors()

    assert [director.name for director in response] == ["Christopher Nolan", "Denis Villeneuve"]


def test_get_director_detail_raises_404_when_missing():
    service = DirectorService(repository=FakeDirectorRepository(director=None))

    with pytest.raises(HTTPException) as error:
        service.get_director_detail(500)

    assert error.value.status_code == 404
    assert error.value.detail == "Director not found"


def test_get_director_detail_returns_movies_projection():
    movies = [Movie(id=1, title="Inception", release_year=2010)]
    director = Director(id=1, name="Christopher Nolan", movies=movies)
    service = DirectorService(repository=FakeDirectorRepository(director=director))

    response = service.get_director_detail(1)

    assert response.name == "Christopher Nolan"
    assert [movie.title for movie in response.movies] == ["Inception"]
