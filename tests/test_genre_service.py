from app.models.models import Genre
from app.services.genre_service import GenreService


class FakeGenreRepository:
    def __init__(self, genres=None):
        self._genres = genres or []

    def get_all(self):
        return self._genres


def test_get_all_genres_maps_response():
    genres = [Genre(id=1, name="Sci-Fi"), Genre(id=2, name="Drama")]
    service = GenreService(repository=FakeGenreRepository(genres=genres))

    response = service.get_all_genres()

    assert [genre.name for genre in response] == ["Sci-Fi", "Drama"]
