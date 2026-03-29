import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock

from app.models.models import Actor, Movie
from app.services.actor_service import ActorService


class FakeActorRepository:
    def __init__(self, actors=None, actor=None):
        self._actors = actors or []
        self._actor = actor

    def list_actors(self, movies=None, genres=None):
        return self._actors

    def get_by_id(self, actor_id):
        return self._actor


def test_get_actors_maps_domain_to_response():
    actors = [Actor(id=1, name="Cillian Murphy"), Actor(id=2, name="Leonardo DiCaprio")]
    service = ActorService(repository=FakeActorRepository(actors=actors))

    response = service.get_actors(movies=["Inception"])

    assert [actor.name for actor in response] == ["Cillian Murphy", "Leonardo DiCaprio"]


def test_get_actors_passes_filters_to_repository():
    repository = MagicMock()
    repository.list_actors.return_value = []
    service = ActorService(repository=repository)

    service.get_actors(movies=["Inception"], genres=["Drama"])

    repository.list_actors.assert_called_once_with(
        movies=["Inception"], genres=["Drama"]
    )


def test_get_actor_detail_raises_404_when_missing():
    service = ActorService(repository=FakeActorRepository(actor=None))

    with pytest.raises(HTTPException) as error:
        service.get_actor_detail(900)

    assert error.value.status_code == 404
    assert error.value.detail == "Actor not found"


def test_get_actor_detail_returns_movies_projection():
    movies = [
        Movie(id=1, title="Inception", release_year=2010),
        Movie(id=2, title="Oppenheimer", release_year=2023),
    ]
    actor = Actor(id=1, name="Cillian Murphy", movies=movies)
    service = ActorService(repository=FakeActorRepository(actor=actor))

    response = service.get_actor_detail(actor.id)

    assert response.name == "Cillian Murphy"
    assert [movie.title for movie in response.movies] == ["Inception", "Oppenheimer"]
