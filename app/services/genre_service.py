from app.repositories.genre_repository import GenreRepository
from app.schemas.schemas import GenreResponse


class GenreService:
    def __init__(self, repository: GenreRepository):
        self.repository = repository

    def get_all_genres(self) -> list[GenreResponse]:
        genres = self.repository.get_all()
        return [GenreResponse(id=genre.id, name=genre.name) for genre in genres]
